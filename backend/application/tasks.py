from email import encoders
from email.mime.base import MIMEBase
from main import celery
from celery.schedules import crontab
from jinja2 import Template
from weasyprint import HTML
from application.models import User, Tracker, Log
from main import db,app
from flask import request
import csv
from flask_security import auth_required, current_user
from werkzeug.utils import secure_filename
import datetime
import os

users = db.session.query(User).all()
user_emails = {}
for user in users:
    # user_emails = {
    #  "user1_email":[[Tracker1],[Tracker2]]
    # }
    if user.email not in user_emails:
        user_emails[user.email] = []
    else:
        pass
    user_trackers= db.session.query(Tracker).filter(user.id == Tracker.user_id).all()
    for user_tracker in user_trackers:
        user_emails[user.email].append([user_tracker.name, user_tracker.date_created,user_tracker.description])
 

@celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    # sender.add_periodic_task(crontab(0, 0, day_of_month='1'), monthly_report.s(), name= 'Monthly Report')
    sender.add_periodic_task(10.0, monthly_report.s(), name= 'Monthly Report')
 

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

def send_email(to_address, subject, message,attachement_file=None):
    msg = MIMEMultipart()
    msg['To'] = to_address
    msg['from'] = SENDER_ADDRESS
    msg['subject'] = subject

    msg.attach(MIMEText(message, 'html'))

    # if content == "html":
    #     msg.attach(MIMEText(message, 'html'))
    # else:
    #     msg.attach(MIMEText(message, 'plain'))
    if attachement_file:
        with open(attachement_file, "rb") as attachement:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachement.read())
        encoders.encode_base64(part)   
        part.add_header(
            "Content-Disposition", f"attachement; filename = {attachement_file}",
        )
        msg.attach(part) 
    s = smtplib.SMTP(host = SERVER_SMTP_HOST, port = SERVER_SMTP_PORT)
    s.login(SENDER_ADDRESS, SENDER_PASSWORD)
    s.send_message(msg)
    s.quit()    
    return "Monthly report sent."

ALLOWED_EXTENSIONS = set(["csv"])
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

@celery.task
def hello():
    return "Hello World!!"

SERVER_SMTP_HOST = 'localhost'
SERVER_SMTP_PORT = 1025
SENDER_ADDRESS = 'selfquantifiedapp@gmail.com'
SENDER_PASSWORD = ''

@celery.task
def monthly_report():
    users = db.session.query(User).all()
    user_emails = {}
    for user in users:
    # user_emails = {
    #  "user1_email":[[Tracker1],[Tracker2]]
    # }
        if user.email not in user_emails:
            user_emails[user.email] = []
        else:
            pass
        user_trackers= db.session.query(Tracker).filter(user.id == Tracker.user_id).all()
        user_logs = db.session.query(Log).filter(user.id == Log.user_id).all()
        user_logs_tracker = [user_log.tracker_name for user_log in user_logs]

        for user_tracker in user_trackers:
            user_log_count = user_logs_tracker.count(user_tracker.name)
            user_emails[user.email].append([user_tracker.name, user_tracker.date_created,user_tracker.description,user_log_count])
    
    for user_email in list(user_emails.keys()):
        print(user_email)

        with open('./application/templates/monthly_report.html','r') as f:
            template = Template(f.read())
        temp = template.render(user=user_email, user_tracker = user_emails[user_email])
        html = HTML(string = temp)
        file_name = str(user_email) + ".pdf"
        output = html.write_pdf(target = file_name)
        send_email(user_email, 'Monthly Report', temp, output)
        # send_email(user_email, 'Monthly Report', template.render(user=user_email, user_tracker = user_emails[user_email]))

    return "Monthly Report"

@celery.task
def reminder(current_user):
    with open('./application/templates/reminder.html','r') as f:
            template = Template(f.read())
    send_email(current_user, "Daily Reminder", template.render(user=current_user) )
    return ("Hii!! {} Please Log to the tracker".format(current_user))



@celery.task
def export_mail(current_user):
    send_email(current_user, "Data Exported",  "Hello👋!, {} Your data have been successfully exported to your device".format(current_user))
    return "", 200

@celery.task
def import_tracker():
    return "Data uploaded successfully!"

@app.route('/api/tracker_upload', methods = ['GET','POST'])
@auth_required("token")
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)

            new_filename = f'{filename.split(".")[0]}__.csv'
            file.save(os.path.join(new_filename))
        with open(new_filename, 'r', encoding='utf-8') as csvfile:
            csvreader = csv.reader(csvfile)
        
            rows=[]
            for row in csvreader:
                rows.append(row)
            # print(rows)
            # import_tracker.apply_async(args=[rows], countdown=10)
            import_tracker.apply_async(countdown=1)
            rows.pop(0)
            for row in rows:
                print(row)
                user_=current_user.id
                user_id=user_
                name=row[0]
                description=row[1]
                tracker_type=row[2]
                settings=row[3]
                # with app.app_context():
                new_tracker = Tracker(user_id=user_id, name=name,description=description, tracker_type=tracker_type, settings=settings)
                db.session.add(new_tracker)
                db.session.commit()
                return "Data saved successfully to the backend."
            return "",200

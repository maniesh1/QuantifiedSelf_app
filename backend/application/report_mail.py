from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import sys
import os
SERVER_SMTP_HOST = 'localhost'
SERVER_SMTP_PORT = 1025
SENDER_ADDRESS = 'selfqualifiedapp@gmail.com'
SENDER_PASSWORD = ''

def send_email(to_address, subject, message):
    msg = MIMEMultipart()
    msg['To'] = to_address
    msg['from'] = SENDER_ADDRESS
    msg['subject'] = subject

    msg.attach(MIMEText(message, 'html'))
    s = smtplib.SMTP(host = SERVER_SMTP_HOST, port = SERVER_SMTP_PORT)
    s.login(SENDER_ADDRESS, SENDER_PASSWORD)
    s.send_message(msg)
    s.quit()

    return 

# if __name__ == "__main__":
#     send_email('manishtest@gmail.com', 'your report', 'hello')

from jinja2 import Template
import sys
sys.path.append('QualifiedSelfApp\application')

from application.models import User, Tracker
from main import db


users = db.session.query(User).all()
print(users)
print("gg")
# folder = os.path.dirname(os.path.abspath(__file__))
# url = 'file://' + os.path.join(folder, 'templates')

with open('./application/templates/monthly_report.html','r') as f:
    template = Template(f.read())

send_email('ram@gmail.com', 'some subject', template.render(user='Testing'))
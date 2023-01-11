from http.client import HTTPException
from flask_restful import Resource, Api
from flask_restful import fields, marshal_with, reqparse
from application.database import db
from application.models import Tracker, Log
from application.validation import NotFoundError, BusinessValidationError
import datetime
from flask_security import login_required, auth_required, current_user
from main import api, cache, app
from application import tasks

resource_fields = {
    'id':   fields.Integer,
    'user_id': fields.Integer,
    'timestamp':    fields.String,
    'value':    fields.String,
    'note': fields.String,
    'tracker_name': fields.String,
}

#create log parser for post
create_log_parser  = reqparse.RequestParser()
# create_tlog_parser.add_argument('timestamp')
create_log_parser.add_argument('user_id')
create_log_parser.add_argument('value')
create_log_parser.add_argument('note')
create_log_parser.add_argument('tracker_name')

#create log parser for put
update_log_parser  = reqparse.RequestParser()
# update_log_parser.add_argument('tracker_name')
update_log_parser.add_argument('timestamp')
update_log_parser.add_argument('value')
update_log_parser.add_argument('note')
update_log_parser.add_argument('tracker_name')

#Handling Log API

class LogAPI(Resource):
    #get tracker logs by tracker_name
    @marshal_with(resource_fields)
    @auth_required("token")
    # @login_required
    def get(self, tracker_name):
        user_id = current_user.id
        logs_by_tracker = db.session.query(Log).filter(Log.tracker_name == tracker_name, Log.user_id==user_id).all()
        # print(logs_by_tracker)
        if len(logs_by_tracker) !=0:
            return logs_by_tracker
        else:
            raise NotFoundError(status_code=404, error_code="LE101", error_message="No logs for tracker with name {}".format(tracker_name))
    

    @marshal_with(resource_fields)
    # @login_required
    @auth_required("token")
    def post(self):
        args = create_log_parser.parse_args()
        value=args.get("value",None)
        user_id = current_user.id

        if value is None:
            raise BusinessValidationError(status_code=400, error_code="LE102", error_message="value is required")

        note=args.get('note')
        tracker_name = args.get('tracker_name', None)
        if tracker_name is None:
            raise BusinessValidationError(status_code=400, error_code="LE103", error_message="Tracker name is required")
        
        #tracker_name must exist already
        trackers = db.session.query(Tracker.name).all()
        list_trackers = []
        for v in trackers:
            list_trackers.append(v[0])
        if tracker_name not in list_trackers:
            
            raise BusinessValidationError(status_code=400, error_code="LE104", error_message="No tracker exists with this name")
        

        new_log = Log(user_id=user_id, value=value, note=note, tracker_name=tracker_name)
        db.session.add(new_log)
        db.session.commit()
        tomorrow = datetime.datetime.now() + datetime.timedelta(days=1)
        job=tasks.reminder.apply_async(args=[current_user.email],eta=tomorrow)
        return new_log

    @marshal_with(resource_fields)    
    # @login_required
    @auth_required("token")
    def put(self, id):
        args = update_log_parser.parse_args()
        user_id = current_user.id
        
        value=args.get("value",None)
        if value is None:
            raise  BusinessValidationError(status_code=400, error_code="LE106", error_message="Enter the value for log")
        
        timestamp = args.get("timestamp", None)

        if timestamp is None:
            raise BusinessValidationError(status_code=400, error_code="LE107", error_message="Time logged required")
        note = args.get("note", None)
        if note is None:
            raise BusinessValidationError(status_code=400, error_code="LE105", error_message="Please write a short note")
        

        log=db.session.query(Log).filter(Log.id == id).first()
        if log is None:
            raise NotFoundError(status_code = 404, error_code="LE106", error_message='''No log exists with this id''')
        tracker_name = log.tracker_name
        
        log.value=value
        log.timestamp=timestamp
        log.note=note
        
        db.session.add(log)
        db.session.commit()
        return log

        
    @marshal_with(resource_fields)
    @auth_required("token")
    def delete(self,id):
        
        #check if tracker exists
        log = db.session.query(Log).filter(Log.id == id).first()
        if log is None:
            raise NotFoundError(status_code = 404, error_code="LE107", error_message="No log for id {}".format(id))
        
        db.session.delete(log)
        db.session.commit()
        return "",200

@app.route('/api/export')
@auth_required("token")
def export():
    tasks.export_mail.apply_async(args=[current_user.email], countdown=10)
    return "",200

api.add_resource(LogAPI, "/api/log/<int:id>","/api/log/<string:tracker_name>","/api/log")
from http.client import HTTPException
from xml.dom import NotFoundErr
from flask_restful import Resource, Api
from flask_restful import fields, marshal_with, reqparse
from application.database import db
from application.models import Tracker, Log
from application import tasks
from application.validation import NotFoundError, BusinessValidationError
from flask_security import login_required, auth_required,current_user
import flask_login
from main import cache, api
from main import app
from datetime import timedelta
import datetime

resource_fields = {
    'id':   fields.Integer,
    'user_id': fields.Integer,
    'name':    fields.String,
    'description':    fields.String,
    'tracker_type': fields.String,
    'date_created': fields.String,
    'settings': fields.String

}

create_tracker_parser  = reqparse.RequestParser()
create_tracker_parser.add_argument('user_id')
create_tracker_parser.add_argument('name')
create_tracker_parser.add_argument('description')
create_tracker_parser.add_argument('tracker_type')
create_tracker_parser.add_argument('settings')

create_update_parser  = reqparse.RequestParser()
create_update_parser.add_argument('description')
create_update_parser.add_argument('tracker_type')
create_update_parser.add_argument('settings')
create_update_parser.add_argument('date_created')


#Handling Tracker API
class TrackerAPI(Resource):
    @marshal_with(resource_fields)
    def get(self, name):
        #query the tracker table to get tracker by name
        tracker = db.session.query(Tracker).filter(Tracker.name == name).first()

        #If there is no tracker by that name return not found error
        if tracker is None:
            raise NotFoundError(status_code = 404, error_code="TE105", error_message='''No tracker exists with this name''')

        #If there is a tracker, return tracker json
        return tracker


    @marshal_with(resource_fields)
    @auth_required("token")
    def post(self):
        args = create_tracker_parser.parse_args()
        name=args.get("name",None)
        user_id=current_user.id

        if name is None:
            raise BusinessValidationError(status_code=400, error_code="TE101", error_message="Tracker name is required")
        tracker = db.session.query(Tracker).filter(Tracker.name == name).first()
        if tracker is not None and name == tracker.name and user_id==tracker.user_id:
            raise BusinessValidationError(status_code=400, error_code="TE102", error_message='''Tracker with this name already exists, Please create different tracker''')

        description=args.get('description')
        tracker_type = args.get('tracker_type', None)
        if tracker_type is None:
            raise BusinessValidationError(status_code=400, error_code="TE103", error_message="Tracker type is required")
        if tracker_type not in ['Numerical', 'Boolean', 'Multiple Choice', "Time Duration"]:
            raise BusinessValidationError(status_code=400, error_code="TE104", error_message="Tracker type must be in ['Numerical', 'Boolean', 'Multiple Choice', 'Time Duration']")
        settings=args.get('settings') 

        new_tracker = Tracker(user_id=user_id, name=name,description=description, tracker_type=tracker_type, settings=settings)
        db.session.add(new_tracker)
        db.session.commit()
        cache.clear()

        return "",200

    @marshal_with(resource_fields)
    @auth_required("token")
    def put(self, id):
        # user_id = flask_login.current_user
        args = create_update_parser.parse_args()
        description=args.get('description')
        tracker_type = args.get('tracker_type', None)
        if tracker_type is None:
            raise BusinessValidationError(status_code=400, error_code="TE103", error_message="Tracker type is required")
        if tracker_type not in ['Numerical', 'Boolean', 'Multiple Choice', "Time Duration"]:
            raise BusinessValidationError(status_code=400, error_code="TE104", error_message="Tracker type must be in ['Numerical', 'Boolean', 'Multiple Choice', 'Time Duration']")
        settings=args.get('settings') 
        date_created = args.get('date_created')
        tracker=db.session.query(Tracker).filter(Tracker.id == id).first()
        if tracker is None:
            raise NotFoundError(status_code = 404, error_code="TE109", error_message='''No tracker exists with this id''')
        

        tracker.description = description
        tracker.tracker_type=tracker_type
        tracker.settings= settings

        db.session.add(tracker)
        db.session.commit()
        cache.clear()
        return tracker
        

    @marshal_with(resource_fields)

    @auth_required("token")
    def delete(self,id):
        user_id = current_user.id
        #check if tracker exists
        tracker = db.session.query(Tracker).filter(Tracker.id == id and Tracker.user_id==user_id).first()
        name = tracker.name
        if tracker is None:
            raise NotFoundError(status_code = 404, error_code="TE106", error_message='''No tracker exists with this name''')
        #first delete all the logs for this tracker
        else:
            logs=db.session.query(Log).filter(Log.tracker_name==name and Log.user_id == user_id).all()
            for log in logs:
                db.session.delete(log)
                db.session.commit()
            #then delete the tracker 
            db.session.delete(tracker)
            db.session.commit()
            cache.clear()
        return "",200



api.add_resource(TrackerAPI, "/api/tracker/<string:name>","/api/tracker/<int:id>","/api/tracker")


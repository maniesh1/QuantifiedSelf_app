import json
from application.database import db
from flask import jsonify
from application.models import Tracker, User
from flask_restful import Resource, Api,fields, marshal_with, marshal
from flask_security import login_required, auth_required, auth_token_required, current_user
from main import cache, api
# from flask_caching import cache

# print(dir(flask_caching))
resource_fields = {
    'id':   fields.Integer,
    'name':    fields.String,
    'description':    fields.String,
    'tracker_type': fields.String,
    'date_created': fields.String,
    'settings': fields.String
}



class BaseAPI(Resource):
    @cache.cached(timeout=60, key_prefix="trackers")
    @auth_required("token")
    @marshal_with(resource_fields)
    def get(self):
            # user=User.query.filter_by(id=current_user.id).first()
            trackers = db.session.query(Tracker).filter(Tracker.user_id == current_user.id).all()
            return trackers

# test_api_resource_fields = {
#     'msg':    fields.String,
# }
class TestAPI(Resource):
    @auth_required("token")
    def get(self):
        print("current user: ", current_user.id)
        return jsonify({"msg":"Hello World"})

api.add_resource(BaseAPI, "/api/trackers")
api.add_resource(TestAPI, "/api/test")
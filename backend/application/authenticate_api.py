import json
from msilib.schema import Class
from application.database import db
from application.models import User1
from flask_restful import Resource, Api,fields, marshal_with, marshal
from flask_restful import fields, marshal_with, reqparse

resource_fields = {
    'name':    fields.String,
    'password':    fields.String,
}

create_register_parser  = reqparse.RequestParser()
create_register_parser.add_argument('name')
create_register_parser.add_argument('password')

class RegisterAPI(Resource):
    pass



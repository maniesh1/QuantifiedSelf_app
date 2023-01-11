from flask import Flask, jsonify
from flask_restful import Resource, Api, fields, marshal_with,marshal
import os

# from application.report_mail import *

from application.config import LocalDevelopmentConfig
from application import config
from application.database import db

from flask_security import Security, SQLAlchemySessionUserDatastore, SQLAlchemyUserDatastore
from flask_security import login_required, auth_required, auth_token_required, current_user
from application.models import User, Role

from flask_cors import CORS

from flask_caching import Cache
from application.celery_works import make_celery

from celery import Celery

# cache=Cache()
app = None
api = None
celery = None


def create_app():
    app = Flask(__name__, template_folder='templates')
    if os.getenv('ENV',"development") == "production":
        raise Exception("Currently no production config is set up.")
    else:
        print("Starting Local Development")
        app.config.from_object(LocalDevelopmentConfig)

    db.init_app(app)
    app.app_context().push()
    user_datastore = SQLAlchemySessionUserDatastore(db.session, User, Role)
    security = Security(app, user_datastore)
    api = Api(app)
    
    CORS(app)
    celery = make_celery(app)
    app.app_context().push()

    
    return app, api, celery

app, api, celery = create_app()
cache = Cache(app)


from application.controllers import *
from application.base_api import *
from application.tracker_api import *
from application.tasks import *
from application.log_api import *


@app.errorhandler(403)
def not_allowed(e):
    return '', 403

if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)
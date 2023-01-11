from .database import db
from datetime import datetime
from sqlalchemy.sql import func
from flask_security import Security, UserMixin, RoleMixin, login_required


roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), autoincrement = True, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    fs_uniquifier = db.Column(db.String(255))
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))
class Tracker(db.Model):
    __tablename__ = 'tracker'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer)

    name=db.Column(db.String, nullable=False)
    description=db.Column(db.String)
    tracker_type=db.Column(db.String, nullable=False)
    date_created = db.Column(db.Date, default=datetime.utcnow)
    settings = db.Column(db.String)
    logs = db.relationship('Log', backref='tracker', lazy=True)
    def __repr__(self):
        return '<Tracker %r>' % self.name

class Log(db.Model):
    __tablename__ = 'log'
    id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer)
    timestamp=db.Column(db.String(200), default=datetime.now().strftime("%d/%m/%Y, %H:%M:%S"))
    value=db.Column(db.String, nullable=False)
    note=db.Column(db.String)
    tracker_name=db.Column(db.String, db.ForeignKey('tracker.name'), nullable=False)



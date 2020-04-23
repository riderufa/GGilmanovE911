from flask_login import UserMixin

from app import db, login_manager


user_events = db.Table('user_events', 
                        db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                        db.Column('event_id', db.Integer, db.ForeignKey('event.id'))
                        )


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(20), unique=False, nullable=False)
    date_begin = db.Column(db.Date, unique=False, nullable=False)
    date_end = db.Column(db.Date, unique=False, nullable=False)
    theme = db.Column(db.String(50), unique=False, nullable=False)
    description = db.Column(db.String(200), unique=False, nullable=False)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=False, nullable=True)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    events = db.relationship('Event', secondary=user_events, backref=db.backref('user', lazy='dynamic'))


@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(user_id)
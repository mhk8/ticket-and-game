import datetime
from enum import Enum
from server import db


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    ticket_amount = db.Column(db.Integer)
    activity = db.Column(db.String(255))
    datetime = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    user = db.relationship("User", backref="user_transactions")


class ActivityType(Enum):
    TRANSFER = "transfer"
    COINFILP = "coinfilp"

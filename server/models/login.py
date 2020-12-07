from server import db


class Login(db.Model):
    username = db.Column(db.String(255), primary_key=True)
    password = db.Column(db.String(255))

from server import db


class Store(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    item_group = db.Column(db.Integer)
    price = db.Column(db.Integer)
    limit = db.Column(db.Integer)

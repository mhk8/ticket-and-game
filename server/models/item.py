from server import db


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_type = db.Column(db.Integer)
    item_group = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    count = db.Column(db.Integer, default=1)
    active = db.Column(db.Boolean, default=False)

    user = db.relationship("User", backref="user_items")

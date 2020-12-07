from server import db


class Blackjack(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    deck = db.Column(db.String(2047))
    player_hand = db.Column(db.String(255))
    dealer_hand = db.Column(db.String(255))

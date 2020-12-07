import json

from flask import request, session, Blueprint
from sqlalchemy.sql import func
from server.utils.blackjack_deck import (
    draw_card,
    translate_hand,
    blackjack_total,
    get_deck_set,
)
from server import db
from server.models import Transaction, Blackjack
from server.routes.decorators import login_required


blackjack_bp = Blueprint(
    "blackjack_bp",
    __name__,
)


def new_player(user_id):
    return Blackjack.query.filter_by(user_id=user_id).scalar() is None


def valid_balance(user_id):
    total_tickets = (
        db.session.query(func.sum(Transaction.ticket_amount))
        .filter(Transaction.user_id == user_id)
        .scalar()
    )
    if total_tickets is None:
        return False
    return total_tickets >= 500


def blackjack_transaction(amount):
    transaction = Transaction(
        user_id=session["user_id"],
        ticket_amount=amount,
        activity="blackjack",
    )
    db.session.add(transaction)
    db.session.commit()


def get_starting_cards():
    query = Blackjack.query.filter_by(user_id=session["user_id"]).first()
    deck = json.loads(query.deck)
    card1 = draw_card(deck)
    card2 = draw_card(deck)
    card3 = draw_card(deck)
    card4 = draw_card(deck)
    dealer_hand = [card1, card3]
    player_hand = [card2, card4]
    if len(deck) < 200:
        deck = deck + get_deck_set()
    query.deck = json.dumps(deck)
    query.player_hand = json.dumps(player_hand)
    query.dealer_hand = json.dumps(dealer_hand)
    db.session.commit()
    return {"dealer_hand": dealer_hand, "player_hand": player_hand}


@blackjack_bp.route("/api/blackjack/play", methods=["GET"])
@login_required
def play_blackjack():
    if valid_balance(session["user_id"]) is False:
        return {
            "success": False,
            "message": "Client needs at least 500 tickets to play.",
        }
    return {"success": True, "message": "Welcome to Blackjack!"}


@blackjack_bp.route("/api/blackjack/checkfunds", methods=["POST"])
@login_required
def check_funds_blackjack():
    try:
        data = json.loads(request.data)
        bet_amount = data["amount"]
        total_tickets = (
            db.session.query(func.sum(Transaction.ticket_amount))
            .filter(Transaction.user_id == session["user_id"])
            .scalar()
        )
        if bet_amount > total_tickets:
            return {
                "success": False,
                "message": "You are wagering more tickets than you currently have",
            }
        return {"success": True}
    except json.decoder.JSONDecodeError:
        return {"error": "Malformed request"}, 400


@blackjack_bp.route("/api/blackjack/start", methods=["POST"])
@login_required
def bet_blackjack():
    try:
        data = json.loads(request.data)
        blackjack_transaction(-data["amount"])
        deck = get_deck_set()
        card1 = draw_card(deck)
        card2 = draw_card(deck)
        card3 = draw_card(deck)
        card4 = draw_card(deck)
        dealer_hand = [card1, card3]
        player_hand = [card2, card4]
        if new_player(session["user_id"]):
            player_deck = Blackjack(
                user_id=session["user_id"],
                deck=json.dumps(deck),
                player_hand=json.dumps(player_hand),
                dealer_hand=json.dumps(dealer_hand),
            )
            db.session.add(player_deck)
        else:
            player_row = Blackjack.query.filter_by(user_id=session["user_id"]).first()
            player_row.deck = json.dumps(deck)
            player_row.player_hand = json.dumps(player_hand)
            player_row.dealer_hand = json.dumps(dealer_hand)
        db.session.commit()
        client_dealer = translate_hand(dealer_hand)[0:2]
        client_player = translate_hand(player_hand)
        return {
            "success": True,
            "blackjack": blackjack_total(player_hand) == 21,
            "dealer": client_dealer,
            "player": client_player,
        }
    except json.decoder.JSONDecodeError:
        return {"error": "Malformed request"}, 400


@blackjack_bp.route("/api/blackjack/playagain", methods=["POST"])
@login_required
def play_again_blackjack():
    try:
        data = json.loads(request.data)
        blackjack_transaction(-data["amount"])
        new_cards = get_starting_cards()
        client_dealer = translate_hand(new_cards["dealer_hand"])[0:2]
        client_player = translate_hand(new_cards["player_hand"])
        return {
            "success": True,
            "blackjack": blackjack_total(new_cards["player_hand"]) == 21,
            "dealer": client_dealer,
            "player": client_player,
        }
    except json.decoder.JSONDecodeError:
        return {"error": "Malformed request"}, 400


@blackjack_bp.route("/api/blackjack/hit", methods=["GET"])
@login_required
def hit_blackjack():
    query = Blackjack.query.filter_by(user_id=session["user_id"]).first()
    deck = json.loads(query.deck)
    player_hand = json.loads(query.player_hand)
    next_card = draw_card(deck)
    if len(deck) < 200:
        deck = deck + get_deck_set()
    player_hand.append(next_card)
    query.deck = json.dumps(deck)
    query.player_hand = json.dumps(player_hand)
    db.session.commit()
    total = blackjack_total(player_hand)
    client_player = translate_hand(player_hand)
    if total > 21:
        return {
            "success": True,
            "bust": True,
            "winner": "Dealer",
            "blackjack": False,
            "player": client_player,
        }
    if total == 21:
        return {
            "success": True,
            "bust": False,
            "blackjack": True,
            "player": client_player,
        }
    return {"success": True, "bust": False, "blackjack": False, "player": client_player}


@blackjack_bp.route("/api/blackjack/stand", methods=["GET"])
@login_required
def stand_blackjack():
    query = Blackjack.query.filter_by(user_id=session["user_id"]).first()
    deck = json.loads(query.deck)
    player_hand = json.loads(query.player_hand)
    dealer_hand = json.loads(query.dealer_hand)
    while blackjack_total(dealer_hand) <= 17:
        dealer_hand.append(draw_card(deck))
    if len(deck) < 200:
        deck = deck + get_deck_set()
    query.deck = json.dumps(deck)
    query.player_hand = json.dumps(player_hand)
    query.dealer_hand = json.dumps(dealer_hand)

    client_dealer = translate_hand(dealer_hand)
    client_player = translate_hand(player_hand)
    dealer_total = blackjack_total(dealer_hand)
    player_total = blackjack_total(player_hand)
    if dealer_total > 21 or dealer_total < player_total:
        last_transaction = (
            db.session.query(Transaction)
            .filter_by(user_id=session["user_id"], activity="blackjack")
            .order_by(Transaction.id.desc())
            .first()
        )
        new_amount = last_transaction.ticket_amount * 2
        blackjack_transaction(-new_amount)
        return {
            "success": True,
            "winner": "player",
            "dealer": client_dealer,
            "player": client_player,
        }
    if dealer_total == player_total:
        return {
            "success": True,
            "winner": "none",
            "dealer": client_dealer,
            "player": client_player,
        }
    return {
        "success": True,
        "winner": "dealer",
        "dealer": client_dealer,
        "player": client_player,
    }


@blackjack_bp.route("/api/blackjack/tiebreaker", methods=["GET"])
@login_required
def tiebreaker_blackjack():
    new_cards = get_starting_cards()
    client_dealer = translate_hand(new_cards["dealer_hand"])[0:2]
    client_player = translate_hand(new_cards["player_hand"])
    return {
        "success": True,
        "blackjack": blackjack_total(new_cards["player_hand"]) == 21,
        "dealer": client_dealer,
        "player": client_player,
    }

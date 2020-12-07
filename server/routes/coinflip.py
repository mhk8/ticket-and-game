# pylint: disable=inconsistent-return-statements
import json
from random import randint
from flask import request, session, Blueprint
from sqlalchemy.sql import func

from server import db
from server.models.transaction import Transaction
from server.routes.decorators import login_required

coinflip_bp = Blueprint(
    "coinflip_bp",
    __name__,
)


@coinflip_bp.route("/api/coinflip", methods=["POST", "GET"])
@login_required
def coinflip():
    if "user_id" in session:
        user_id = session["user_id"]

    try:
        data = json.loads(request.data)
        amount = int(data["bet"])
        side = data["side"]
        did_win = side == get_side()

        ticket_balance = (
            db.session.query(func.coalesce(func.sum(Transaction.ticket_amount), 0))
            .filter(Transaction.user_id == user_id)
            .scalar()
        )

        if ticket_balance < amount:
            return {"error": "Insufficient balance"}, 400

        if amount > 0:
            if did_win:
                tickets_won = amount
            else:
                tickets_won = amount * -1

            transaction = Transaction(
                user_id=user_id, ticket_amount=tickets_won, activity="coinflip"
            )
            db.session.add(transaction)
            db.session.commit()

            return {"won": did_win, "amount": amount}

    except json.decoder.JSONDecodeError:
        return {"error": "Malformed request"}, 400


def get_side():
    guess = randint(0, 1)
    if guess == 0:
        comp_side = "Heads"
    else:
        comp_side = "Tails"
    return comp_side

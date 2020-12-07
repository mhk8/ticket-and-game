import random
from flask import session, Blueprint
from sqlalchemy.sql import func

from server import db
from server.routes.decorators import login_required
from server.models.transaction import Transaction

skiball_bp = Blueprint(
    "skiball_bp",
    __name__,
)


@skiball_bp.route("/api/skiball", methods=["POST", "GET"])
@login_required
def coinflip():
    if "user_id" in session:
        user_id = session["user_id"]

    ticket_balance = (
        db.session.query(func.coalesce(func.sum(Transaction.ticket_amount), 0))
        .filter(Transaction.user_id == user_id)
        .scalar()
    )

    if ticket_balance < 30:
        return {"error": "Insufficient balance"}, 400

    amount = return_balance()

    transaction = Transaction(user_id=user_id, ticket_amount=amount, activity="skiball")
    fee = Transaction(user_id=user_id, ticket_amount=-30, activity="skiball")

    db.session.add(fee)
    db.session.add(transaction)
    db.session.commit()

    return {"amount": amount}


def return_balance():
    lst = [10, 20, 30, 40, 50, 100]
    balance = random.choice(lst)
    return balance

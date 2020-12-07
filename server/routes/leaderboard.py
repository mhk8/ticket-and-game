# pylint: disable=consider-using-enumerate
# pylint: disable=invalid-name
from flask import Blueprint
from sqlalchemy.sql import func
from server import db

from server.models import Transaction, User

leaderboard_bp = Blueprint("leaderboard_bp", __name__)


@leaderboard_bp.route("/api/leaderboard")
def get_leader_board():
    rows = (
        db.session.query(
            User.id, User.name, func.coalesce(func.sum(Transaction.ticket_amount), 0)
        )
        .outerjoin(Transaction, User.id == Transaction.user_id)
        .group_by(User.id)
        .order_by(func.coalesce(func.sum(Transaction.ticket_amount), 0).desc())
        .all()
    )

    transactions = []
    for row in rows:
        user_id, name, balance = row
        transaction = {"id": user_id, "name": name, "balance": balance}

        transactions.append(transaction)

    returnMessage = {"transactions": transactions}

    return returnMessage

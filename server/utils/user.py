from typing import Union
from flask import session
from sqlalchemy.sql import func

from server import db
from server.models import User, Transaction


def get_current_user_id() -> Union[int, None]:
    if "user_id" in session:
        user_id = session["user_id"]
        return user_id

    return None


def get_user_by_id(user_id: Union[int, None]) -> Union[User, None]:
    if user_id is None:
        return None

    user = User.query.filter_by(id=user_id).first()

    return user


def get_current_user() -> Union[User, None]:
    user_id = get_current_user_id()

    user = get_user_by_id(user_id)

    return user


def get_user_balance(user_id: int) -> int:
    ticket_balance = (
        db.session.query(func.sum(Transaction.ticket_amount))
        .filter(Transaction.user_id == user_id)
        .scalar()
    )

    if ticket_balance is None:
        return 0

    return ticket_balance

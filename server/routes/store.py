import json

from flask import Blueprint, session, request
from sqlalchemy.sql import func
from server.models import Store, Transaction, Item
from server.routes.decorators import login_required
from server import db

store_bp = Blueprint("store_bp", __name__, url_prefix="/api/store")


def valid_funds(user_id, item_type):
    total_tickets = (
        db.session.query(func.sum(Transaction.ticket_amount))
        .filter(Transaction.user_id == user_id)
        .scalar()
    )
    item_price = Store.query.filter_by(id=item_type).first().price
    if total_tickets is None or item_price is None:
        return False
    return total_tickets >= item_price


def item_available(user_id, item_type, quantity):
    item_info = Store.query.filter_by(id=item_type).first()
    item_query = Item.query.filter_by(user_id=user_id, item_type=item_type).first()
    if item_query is not None and item_query.count + quantity > item_info.limit:
        return False
    return True


def make_purchase(user_id, item_type, quantity):
    item_info = Store.query.filter_by(id=item_type).first()
    transaction = Transaction(
        user_id=user_id,
        ticket_amount=-item_info.price,
        activity="ticketstore",
    )
    db.session.add(transaction)
    item_query = Item.query.filter_by(user_id=user_id, item_type=item_type).first()
    if item_query is None:
        item = Item(
            item_type=item_type,
            item_group=item_info.item_group,
            user_id=user_id,
        )
        db.session.add(item)
    else:
        item_query.count = item_query.count + quantity
    db.session.commit()


@store_bp.route("/list", methods=["GET"])
@login_required
def store_list():
    store_items = []
    for item in Store.query.all():
        item_obj = {
            "id": item.id,
            "name": item.name,
            "group": item.item_group,
            "limit": item.limit,
            "price": item.price,
        }
        store_items.append(item_obj)

    return {"items": store_items}


@store_bp.route("/buy", methods=["POST"])
@login_required
def buy_item():
    try:
        data = json.loads(request.data)
        item_type = data["id"]
        quantity = data["quantity"]
        user_id = session["user_id"]
        if not valid_funds(user_id, item_type):
            return {"success": False, "message": "Insufficient funds"}, 400
        if not item_available(user_id, item_type, quantity):
            return {"success": False, "message": "Reached purchase limit"}, 400
        make_purchase(user_id, item_type, quantity)
        return {"success": True}
    except json.decoder.JSONDecodeError:
        return {"error": "Malformed request"}, 400

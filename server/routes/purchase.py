import os
import json
import stripe
from flask import Blueprint, request

from server import db
from server.models import Transaction, User
from server.utils import get_current_user

from server.routes.decorators import login_required, stripe_required

purchase_bp = Blueprint("purchase_bp", __name__, url_prefix="/api/purchase")

stripe.api_key = os.getenv("STRIPE_SECRET_KEY", "DEFAULT_KEY")
STRIPE_ENDPOINT_SECRET = os.getenv("STRIPE_ENDPOINT_SECRET", "DEFAULT_SECRET")

ITEMS = [
    {
        "tickets": 10000,
        "price": 0.99,
    },
    {
        "tickets": 55000,
        "price": 4.99,
    },
    {
        "tickets": 130000,
        "price": 9.99,
    },
    {
        "tickets": 300000,
        "price": 19.99,
    },
    {
        "tickets": 1000000,
        "price": 49.99,
    },
    {
        "tickets": 2500000,
        "price": 99.99,
    },
]


@purchase_bp.route("/list")
@login_required
def get_purchase_list():
    return {"items": ITEMS}


@purchase_bp.route("/payment-intent", methods=["POST"])
@login_required
@stripe_required
def create_payment_intent():
    data = json.loads(request.data)
    index = data["item_index"]

    item = ITEMS[index]

    user = get_current_user()

    payment_intent = stripe.PaymentIntent.create(
        amount=round(item["price"] * 100),
        currency="usd",
        receipt_email=user.email,
        metadata={"integration_check": "accept_a_payment"},
    )

    return payment_intent


@purchase_bp.route("/complete", methods=["POST"])
@stripe_required
def payment_complete():
    payload = request.get_data()
    event_data = json.loads(request.data)
    sig_header = request.headers.get("STRIPE_SIGNATURE")

    data = event_data["data"]
    event_object = data["object"]
    amount = event_object["amount"]
    email = event_object["receipt_email"]

    item = list(filter(lambda item: round(item["price"] * 100) == amount, ITEMS))[0]
    tickets = item["tickets"]

    try:
        if (
            os.getenv("DEBUG", "").lower() != "true"
        ):  # Skip signiture check on debug mode
            stripe.Webhook.construct_event(payload, sig_header, STRIPE_ENDPOINT_SECRET)
    except ValueError:
        # invalid payload
        return "Invalid payload", 400
    except stripe.error.SignatureVerificationError:
        # invalid signature
        return "Invalid signature", 400

    user = User.query.filter_by(email=email).first()
    if user is not None:
        transaction = Transaction(
            user_id=user.id, ticket_amount=tickets, activity="Ticket purchase"
        )
        db.session.add(transaction)
        db.session.commit()

    return {"success": True}

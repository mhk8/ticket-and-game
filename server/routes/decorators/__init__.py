import os

from functools import wraps
from flask import session


def login_required(function):
    @wraps(function)
    def wrap(*args, **kwargs):
        if "user_id" in session:
            return function(*args, **kwargs)

        return {"error": "User not logged in"}, 401

    return wrap


def stripe_required(function):
    @wraps(function)
    def wrap(*args, **kwargs):
        if os.getenv("STRIPE_SECRET_KEY", "DEFAULT_KEY") != "DEFAULT_KEY":
            return function(*args, **kwargs)

        return {"error": "Stripe key not configured on the server"}, 503

    return wrap

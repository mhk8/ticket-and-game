import json
import requests

from flask import request, session, Blueprint

from sqlalchemy.orm.exc import NoResultFound
from server import db
from server.models import Login, Transaction, User
from server.routes.decorators import login_required
from server.utils.hash import hash_pass, hash_login
from server.utils.user import get_current_user


user_bp = Blueprint(
    "user_bp",
    __name__,
)


def get_token_info(token):
    return requests.get(
        f"https://oauth2.googleapis.com/tokeninfo?id_token={token}"
    ).json()


def query_user(email):
    user = User.query.filter_by(email=email).first()
    return user


@user_bp.route("/api/login/oauth", methods=["POST"])
def oauth_login():
    session.permanent = True

    try:
        data = json.loads(request.data)
        oauth_token = data["token"]
        token_info = get_token_info(oauth_token)

        if "error" in token_info:
            return {"error": token_info["error_description"]}

        sub = token_info["sub"]
        email = token_info["email"]
        name = token_info["name"]

        user = query_user(email)
        if query_user(email) is None:
            # User doesn't exist and we should create a new user
            user = User(oauth_id=sub, name=name, email=email)
            db.session.add(user)
            db.session.commit()
            session["user_id"] = user.id
            return {"success": True, "new_user": True}

        session["user_id"] = user.id

        if user.username is None:
            return {"success": True, "new_user": True}

        return {"success": True, "new_user": False, "user_id": session["user_id"]}

    except json.decoder.JSONDecodeError:
        return {"error": "Malformed request"}, 400


def check_username(username):
    return User.query.filter_by(username=username).scalar() is not None


@user_bp.route("/api/login/newuser", methods=["POST"])
@login_required
def oauth_newuser():
    session.permanent = True

    try:
        data = json.loads(request.data)
        username = data["user"]

        if check_username(username):
            return {
                "success": False,
                "message": "Username already exist. please try another one.",
            }

        user = get_current_user()
        user.username = username
        transaction = Transaction(
            user_id=user.id, ticket_amount=1000, activity="Sign up bonus"
        )
        db.session.add(transaction)
        db.session.commit()

        session["user_id"] = user.id

        return {"success": True, "user_id": session["user_id"]}

    except json.decoder.JSONDecodeError:
        return {"error": "Malformed request"}, 400


def check_email(email):
    return User.query.filter_by(email=email).scalar() is not None


@user_bp.route("/api/signup/password", methods=["POST"])
def password_signup():
    session.permanent = True

    try:
        data = json.loads(request.data)
        name = data["name"]
        username = data["username"]
        email = data["email"]
        password = data["password"]
        if check_email(email):
            return {
                "success": False,
                "message": "Another account seems to be using the same email.",
            }

        if check_username(username):
            return {
                "success": False,
                "message": "Username has already been taken please try another username",
            }
        user = User(oauth_id="password", name=name, username=username, email=email)
        login = Login(username=username, password=hash_pass(password))
        db.session.add(user)
        db.session.add(login)
        db.session.commit()
        transaction = Transaction(
            user_id=user.id, ticket_amount=1000, activity="Sign up bonus"
        )
        db.session.add(transaction)
        db.session.commit()
        session["user_id"] = user.id
        return {"success": True, "user_id": session["user_id"]}

    except json.decoder.JSONDecodeError:
        return {"error": "Malformed request"}, 400


def find_username(username):
    return Login.query.filter_by(username=username).scalar()


def get_pwd(username):
    query = db.session.query(Login).filter(Login.username == username).one()
    return query.password


def get_id(username):
    query = db.session.query(User).filter(User.username == username).one()
    return query.id


@user_bp.route("/api/login/password", methods=["POST"])
def password_login():
    session.permanent = True

    try:
        data = json.loads(request.data)
        username = data["username"]
        password = data["password"]
        if find_username is None or hash_login(get_pwd(username), password) is False:
            return {
                "success": False,
                "message": "Username does not exist or password is invalid.",
            }
        session["user_id"] = get_id(username)

        return {"success": True, "user_id": session["user_id"]}

    except json.decoder.JSONDecodeError:
        return {"error": "Malformed request"}, 400

    except NoResultFound:
        return {
            "success": False,
            "message": "Username does not exist or password is invalid.",
        }


@user_bp.route("/api/user/logout", methods=["GET", "POST"])
@login_required
def logout():
    session.pop("user_id", None)
    return {"success": True}

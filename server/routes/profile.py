from flask import Blueprint

from server.routes.decorators import login_required
from server.utils import get_current_user, get_user_by_id, get_user_balance

profile_bp = Blueprint("profile_bp", __name__)


@profile_bp.route("/api/profile/", defaults={"user_id": None})
@profile_bp.route("/api/profile/<user_id>")
@login_required
def get_profile_view(user_id):
    if user_id is None:
        user = get_current_user()
    else:
        user = get_user_by_id(user_id)

    if user:
        if user.is_public or user_id is None:
            total_tickets = get_user_balance(user.id)
            return {
                "name": user.name,
                "username": user.username,
                "registration_datetime": user.registration_datetime,
                "total_tickets": total_tickets,
                "is_public": user.is_public,
            }

        return {"error": "User profile is private"}, 401

    return {"error": "User not found"}, 404

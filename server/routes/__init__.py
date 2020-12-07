from flask import Blueprint, current_app, send_from_directory

from server.routes.user import user_bp
from server.routes.coinflip import coinflip_bp
from server.routes.dice import dice_bp
from server.routes.leaderboard import leaderboard_bp
from server.routes.profile import profile_bp
from server.routes.ticket import ticket_bp
from server.routes.blackjack import blackjack_bp
from server.routes.skiball import skiball_bp
from server.routes.store import store_bp
from server.routes.purchase import purchase_bp
from server.routes.settings import settings_bp

main_bp = Blueprint(
    "main_bp",
    __name__,
)


@main_bp.route("/", defaults={"filename": "index.html"})
@main_bp.route("/<path:filename>")
def get_client(filename):
    return send_from_directory(current_app.template_folder, filename)


@main_bp.errorhandler(404)
def page_not_found(_e):
    return send_from_directory(current_app.template_folder, "index.html")

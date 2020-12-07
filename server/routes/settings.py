import json

from flask import request, session, Blueprint
from server import db
from server.routes.decorators import login_required
from server.utils import get_current_user
from server.utils.item_helper import (
    item_group_by_user_id,
    handle_text_color,
    handle_username_change,
    get_color_name,
    handle_profile_image
)

settings_bp = Blueprint("settings_bp", __name__, url_prefix="/api/settings")

@settings_bp.route("/get")
@login_required
def get_settings():
    user = get_current_user()
    colors = []
    change_username_bool = False
    change_profile_pic_bool = False
    text_colors = item_group_by_user_id(user.id, 101)
    if text_colors:
        current_color = None
        color_black = {
            "item_type": -1,
            "name": "Black",
        }
        for text_color in text_colors:
            if text_color.active is True:
                current_color = {
                    "item_type": text_color.item_type,
                    "name": get_color_name(text_color.item_type)
                }
            else:
                colors.append({
                    "item_type": text_color.item_type,
                    "name": get_color_name(text_color.item_type)
                })
        if current_color is None:
            colors.insert(0, color_black)
        else:
            colors.insert(0, current_color)
    if item_group_by_user_id(user.id, 102):
        change_username_bool = True
    if item_group_by_user_id(user.id, 107):
        change_profile_pic_bool = True
    return {
        "is_public": user.is_public,
        "text_color": colors,
        "change_username": change_username_bool,
        "change_profile_pic": change_profile_pic_bool
    }

@settings_bp.route("/textcolor", methods=["POST"])
@login_required
def change_text_color():
    try:
        data = json.loads(request.data)
        item_type = data["item_type"]
        user_id = session["user_id"]
        handle_text_color(user_id, item_type)
        return {"success": True}
    except json.decoder.JSONDecodeError:
        return {"error": "Malformed request"}, 400

@settings_bp.route("/username", methods=["POST"])
@login_required
def change_username():
    try:
        data = json.loads(request.data)
        username = data["username"]
        user_id = session["user_id"]
        if handle_username_change(user_id, username):
            return {"success": True, "message": "username changed!"}
        return {"success": False, "message": "username already taken"}
    except json.decoder.JSONDecodeError:
        return {"error": "Malformed request"}, 400

@settings_bp.route("/profilepic", methods=["POST"])
@login_required
def chnage_profile_pic():
    try:
        data = json.loads(request.data)
        image_url = data["image_url"]
        user_id = session["user_id"]
        if handle_profile_image(user_id, image_url):
            return {"success": True, "message": "Image change successful!"}
        return {"success": False, "message": "Given image was invalid."}
    except json.decoder.JSONDecodeError:
        return {"error": "Malformed request"}, 400

@settings_bp.route("/update", methods=["POST"])
@login_required
def update_settings():
    user = get_current_user()
    data = json.loads(request.data)

    is_public = data["is_public"]
    user.is_public = is_public
    db.session.commit()

    return {"success": True}

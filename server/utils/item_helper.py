from rfc3987 import parse
from server.models import Item, User, Login, Store
from server import db

def item_group_by_user_id(user_id, item_group):
    return (
        db.session.query(Item)
        .filter(Item.user_id==user_id, Item.item_group==item_group)
        .all()
    )

def handle_text_color(user_id, item_type):
    query = (
        db.session.query(Item)
        .filter(Item.user_id==user_id, Item.item_type==item_type)
        .all()
    )
    for color in query:
        if color.item_type == item_type:
            color.active = True
        else:
            color.active = False
    db.session.commit()

def get_color_name(item_type):
    query = (
        db.session.query(Store)
        .filter(Store.item_group==101, Store.id==item_type)
        .first()
    )
    if query:
        return query.name.split(" ", 1)[0]
    return "Invalid"

def handle_username_change(user_id, username):
    query = (
        db.session.query(User)
        .filter(User.username==username)
        .all()
    )
    if not query:
        user_profile = (
            db.session.query(User)
            .filter(User.id==user_id)
            .first()
        )
        temp_username = user_profile.username
        user_profile.username = username
        login_profile = (
            db.session.query(Login)
            .filter(Login.username==temp_username)
            .first()
        )
        login_profile.username = username
        db.session.commit()
        return True
    return False

def handle_profile_image(user_id, image_url):
    try:
        parse(image_url, rule="IRI")
    except ValueError:
        return False
    query = (
        db.session.query(User)
        .filter(User.id==user_id)
        .first()
    )
    query.image_url = image_url
    db.session.commit()
    return True

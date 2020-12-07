from server import db
from server.models.store import Store

def populate_store():
    if db.session.query(Store).first() is None:
        items = [
            Store (
                name="Red Text",
                item_group=101,
                price=500,
                limit=1
            ),
            Store (
                name="Green Text",
                item_group=101,
                price=500,
                limit=1
            ),
            Store (
                name="Blue Text",
                item_group=101,
                price=500,
                limit=1
            ),
            Store (
                name="Change Username",
                item_group=102,
                price=10000,
                limit=1
            ),
            Store (
                name="Change Profile Image",
                item_group=107,
                price=10000,
                limit=1
            )
        ]
        for item in items:
            db.session.add(item)
        db.session.commit()

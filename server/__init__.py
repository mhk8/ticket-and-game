import os
from datetime import timedelta

from flask import Flask
from flask_sqlalchemy import SQLAlchemy, sqlalchemy
from flask_socketio import SocketIO
from flask_migrate import Migrate, upgrade

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///database.db")

socketio = SocketIO()
db = SQLAlchemy()
migrate = Migrate(compare_type=True)

def create_app(config):
    app = Flask(
        __name__,
        instance_relative_config=False,
        static_folder=config.STATIC_FOLDER,
        template_folder=config.TEMPLATE_FOLDER,
    )
    app.config.from_object(config)
    app.permanent_session_lifetime = timedelta(days=365)

    db.init_app(app)
    socketio.init_app(app, cors_allowed_origins="*")
    migrate.init_app(app, db, render_as_batch=True)

    with app.app_context():
        import server.routes as routes

        app.register_blueprint(routes.main_bp)
        app.register_blueprint(routes.user_bp)
        app.register_blueprint(routes.coinflip_bp)
        app.register_blueprint(routes.dice_bp)
        app.register_blueprint(routes.leaderboard_bp)
        app.register_blueprint(routes.profile_bp)
        app.register_blueprint(routes.ticket_bp)
        app.register_blueprint(routes.blackjack_bp)
        app.register_blueprint(routes.skiball_bp)
        app.register_blueprint(routes.store_bp)
        app.register_blueprint(routes.purchase_bp)
        app.register_blueprint(routes.settings_bp)

        try:
            from server.utils.store_helper import populate_store
            populate_store()
        except sqlalchemy.exc.OperationalError:
            pass
    return app

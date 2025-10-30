# __init__.py
from flask import Flask
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from .models import db

login_manager = LoginManager()

def create_app():
    app = Flask(__name__)

    app.debug = True
    app.secret_key = 'somesecretkey'

    # --- Core configuration ---
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///localgig.db"
    app.config["SECRET_KEY"] = "dev-change-me" 

    Bootstrap5(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    # Initialise extensions
    db.init_app(app)

    # Register blueprints
    login_manager.login_view = "login" 
    login_manager.login_message_category = "warning"
    # Login manager setup
    from .models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    from .views import main_bp, events_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(events_bp)

    from . import auth
    app.register_blueprint(auth.auth_bp)

    # Error handlers
    from flask import render_template

    @app.errorhandler(404)
    def not_found_error(error):
        return render_template("404.html"), 404

    @app.errorhandler(500)
    def internal_error(error):
        return render_template("500.html"), 500
    return app
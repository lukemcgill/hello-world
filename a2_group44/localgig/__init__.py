from flask import Flask
from flask_bootstrap5 import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()  # MOVED: Initialize outside create_app

def create_app():
    app = Flask(__name__)

    # we use this utility module to display forms quickly
    bootstrap = Bootstrap(app)

    # A secret key for the session object - make this stronger!
    app.secret_key = 'your-very-secret-key-change-this-in-production'

    # Configure and initialise DB
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///localgig.sqlite'
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)  # Initialize login manager with app

    # Set name of login function for user to login
    login_manager.login_view = "auth.login"
    login_manager.login_message_category = 'info'

    # Create a user loader that takes userid and returns User
    from .models import User
    
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    # config upload folder
    UPLOAD_FOLDER = '/static/image'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    
    # add Blueprints
    from . import views
    app.register_blueprint(views.main_bp)
    app.register_blueprint(views.events_bp)
    from . import tickets
    app.register_blueprint(tickets.tickbp)
    from . import auth
    app.register_blueprint(auth.authbp)

    return app
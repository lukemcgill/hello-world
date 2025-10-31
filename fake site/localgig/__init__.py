from flask import Flask
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # we use this utility module to display forms quickly
    Bootstrap5(app)

    #importing models for db.create to work properly
    from .models import User, Event, Comment, Order

    #add login manager supporter
    #initalise the login manager
    login_manager = LoginManager()

    #set name of login function for user to login
    login_manager.login_view="auth.login"
    login_manager.init_app(app)

    #create a user loader takes userid and returns User
    from .models import User  #importing to avoid circular reference
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # A secret key for the session object
    app.secret_key = 'somesecretkey'

    # Configue and initialise DB
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///localgig.sqlite'
    db.init_app(app)

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
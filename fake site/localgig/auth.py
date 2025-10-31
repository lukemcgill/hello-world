from flask import Blueprint, render_template, redirect, url_for, flash
from .forms import LoginForm, RegisterForm
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user

from . import db

# create a blueprint
authbp = Blueprint('auth', __name__ )

@authbp.route('/login', methods=['GET', 'POST'])
def login():
    loginForm = LoginForm()
    if loginForm.validate_on_submit():
        print('Successfully logged in')
        flash('You logged in successfully')
        return redirect(url_for('auth.login'))
    return render_template('user.html', form=loginForm,  heading='Login')

@authbp.route('/register', methods=['GET', 'POST'])
def register():
    register = RegisterForm()
    #the validation of form is fine, HTTP request is POST
    if (register.validate_on_submit()==True):
            #get username, password and email from the form
            uname = register.user_name.data
            pwd = register.password.data
            email = register.email_id.data
            #check if a user exists
            user = db.session.scalar(db.select(User).where(User.username==uname))
            if user:#this returns true when user is not None
                flash('Username already exists, please try another')
                return redirect(url_for('auth.register'))
            # don't store the password in plaintext!
            pwd_hash = generate_password_hash(pwd)
            #create a new User model object
            new_user = User(username=uname, email=email, password_hash=pwd_hash)
            db.session.add(new_user)
            db.session.commit()
            #commit to the database and redirect to HTML page
            return redirect(url_for('main.index'))
    #the else is called when the HTTP request calling this page is a GET
    else:
        return render_template('user.html', form=register, heading='Register')



from flask import Blueprint, render_template, redirect, url_for, flash, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user

# Import from the same package
from localgig.forms import LoginForm, RegisterForm
from localgig.models import User
from localgig import db

# create a blueprint
authbp = Blueprint('auth', __name__)

@authbp.route('/login', methods=['GET', 'POST'])
def login():
    # If user is already logged in, redirect to home
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
        
    loginForm = LoginForm()
    if loginForm.validate_on_submit():
        user_name = loginForm.user_name.data
        password = loginForm.password.data
        
        # Find user by username
        user = db.session.scalar(db.select(User).where(User.username == user_name))
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user, remember=True)  # Added remember=True
            flash('Login successful!', 'success')
            
            # Redirect to next page if it exists, otherwise to home
            next_page = request.args.get('next')
            if next_page and next_page.startswith('/'):
                return redirect(next_page)
            return redirect(url_for('main.index'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('login.html', form=loginForm)

@authbp.route('/register', methods=['GET', 'POST'])
def register():
    # If user is already logged in, redirect to home
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
        
    form = RegisterForm()
    if form.validate_on_submit():
        # Get all fields from the form
        first_name = form.first_name.data
        surname = form.surname.data
        uname = form.user_name.data
        email = form.email_id.data
        contact_number = form.contact_number.data
        street_address = form.street_address.data
        pwd = form.password.data
        
        # Check if username already exists
        existing_user = db.session.scalar(db.select(User).where(User.username == uname))
        if existing_user:
            flash('Username already exists, please try another', 'error')
            return render_template('register.html', form=form)
        
        # Check if email already exists
        existing_email = db.session.scalar(db.select(User).where(User.email == email))
        if existing_email:
            flash('Email already registered, please use a different email', 'error')
            return render_template('register.html', form=form)
        
        # Create new user with hashed password and all fields
        pwd_hash = generate_password_hash(pwd)
        new_user = User(
            first_name=first_name,
            surname=surname,
            username=uname,
            email=email,
            contact_number=contact_number,
            street_address=street_address,
            password_hash=pwd_hash
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('register.html', form=form)

@authbp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('main.index'))
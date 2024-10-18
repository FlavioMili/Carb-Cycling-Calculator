from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/signup',methods=['GET', 'POST'])
def signup():
    if request.method  == 'POST':
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        check_user = User.query.filter_by(email=email).first() 
        if check_user: flash('Email already registered', category='Error')

        if password2 != password1: flash('Passwords need to match', category='Error')
        elif len(password1) < 8: flash('Password must be at least 8 characters long', category='Error')
        else: 
            new_user = User(email=email, password=generate_password_hash(password1, method='pbkdf2:sha1'))
            db.session.add(new_user)
            db.session.commit()
            flash('Account created', category='Success')
            login_user(new_user, remember=True)
            return redirect(url_for('views.home'))

    return render_template("signup.html", user=current_user)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in', category='Success')
                login_user(user, remember=True)
                redirect(url_for('views.home'))
            else: 
                flash('Wrong password', category='Error')
        else: 
            flash('Email not registered', category='Error')
    

    return render_template("login.html", boolean=True)

@auth.route('/logout')
@login_required
def logout():
    flash('Logged out', category="Success")
    logout_user()
    return redirect(url_for('auth.login'))



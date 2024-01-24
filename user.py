from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models import db, User
from flask_login import login_required, current_user, logout_user, login_user
from sqlalchemy.exc import IntegrityError

user_bp = Blueprint("user", __name__)

@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['user-email']
        user = User.query.filter_by(email=email).first()

        if user:
            login_user(user)
            session['user_email'] = email
            return redirect(url_for('home'))
        else:
            flash("Email and password incorrect!!", "error")

    return render_template('login.html')


@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user_email = request.form['user-email']
        password = request.form['user-password']
        user_name = request.form['user-name']
        mobile_number = request.form['user-number']

        print(
            f"Received user_email: {user_email}, password: {password}, user_name: {user_name}, mobile_number: {mobile_number}")

        user = User(email=user_email, username=user_name)
        try:
            db.session.add(user)
            db.session.commit()
            flash('Registration successful!', 'success')
            return redirect(url_for('user.login'))
        except IntegrityError as e:
            db.session.rollback()
            flash('User already exists', 'error')
        except Exception as e:
            db.session.rollback()
            return f'Error: {str(e)}'

    return render_template('register.html', user=current_user)

@user_bp.route('/logout')
@login_required
def logout():
    session.clear()
    logout_user()
    return redirect(url_for('encryption.delete_files'))

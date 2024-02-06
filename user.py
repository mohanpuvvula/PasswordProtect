from flask import Flask, render_template, request, redirect, url_for, flash, Blueprint
from models import db, User
from sqlalchemy.exc import IntegrityError
from time import sleep

app = Flask(__name__)
app.secret_key = 'xyzabc'

user_bp = Blueprint("user", __name__)


@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user_email = request.form['user-email']
        password = request.form['user-password']
        user_name = request.form['user-name']
        mobile_number = request.form['user-number']

        user = User(email=user_email, username=user_name, password=password)

        try:
            db.session.add(user)
            db.session.commit()
            flash('Registration successful!', 'success')
            sleep(2)
            return redirect(url_for('home'))
        except IntegrityError:
            db.session.rollback()
            flash('User with this email already exists', 'error')
            sleep(2)
            return render_template('register.html')

    return render_template('register.html')

app.register_blueprint(user_bp)

if __name__ == '__main__':
    app.run(debug=True)

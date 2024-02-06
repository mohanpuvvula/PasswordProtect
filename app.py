from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_login import LoginManager, login_required, current_user, logout_user, login_user
from models import db, User
from user import user_bp
from encryption import encryption_bp
from sqlalchemy.exc import IntegrityError
import os
import shutil

app = Flask(__name__)
db_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'database.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'xyzabc'
app.config['UPLOAD_FOLDER'] = os.path.join(app.instance_path, 'files')
app.config['ENCRYPT_FOLDER'] = os.path.join(app.instance_path, 'encrypt')
login_manager = LoginManager(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_email):
    return User.query.filter_by(email=user_email).first()


db.init_app(app)

app.register_blueprint(user_bp, url_prefix="/user")
app.register_blueprint(encryption_bp, url_prefix='/encryption')


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        email = request.form['user-email']
        password = request.form['user-password']
        user = User.query.filter_by(email=email).first()

        if user and user.password == password:
            login_user(user)
            session['user_email'] = email
            return redirect(url_for('encryption.upload'))
        elif user:
            flash("Incorrect password. Please try again.", "error")
        else:
            flash("User does not exist. Please register first.", "error")


    user_authenticated = 'user_email' in session
    user_email = session.get('user_email', None)
    user = current_user

    return render_template('home.html', user_authenticated=user_authenticated, user_email=user_email,  user=user)



@app.route('/logout', methods=['GET'])
@login_required
def logout():
    upload_folder = app.config['UPLOAD_FOLDER']
    for filename in os.listdir(upload_folder):
        file_path = os.path.join(upload_folder, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)

    encrypt_folder = app.config['ENCRYPT_FOLDER']
    for filename in os.listdir(encrypt_folder):
        file_path = os.path.join(encrypt_folder, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)

    session.clear()
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run()

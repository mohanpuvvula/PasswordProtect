from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_login import LoginManager, login_required
from models import db, User
from user import user_bp
from encryption import encryption_bp
from flask_login import login_required, current_user, logout_user, login_user
import os

app = Flask(__name__)
db_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'database.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'xyzabc'
login_manager = LoginManager(app)
login_manager.login_view = 'user.login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

db.init_app(app)

app.register_blueprint(user_bp, url_prefix="/user")
app.register_blueprint(encryption_bp, url_prefix='/encryption')


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        entered_email = request.form['user-email']

        if 'user_email' in session:
            stored_email = session['user_email']

            if entered_email == stored_email:

                return redirect(url_for('encryption.upload'))
            else:
                if not current_user.is_authenticated:
                    return redirect(url_for('user.login'))

    user_authenticated = 'user_email' in session
    user_email = session.get('user_email', None)
    user = current_user

    return render_template('home.html', user_authenticated=user_authenticated, user_email=user_email,
                           user=user)

@app.route('/logout')
@login_required
def logout():
    session.clear()
    logout_user()
    return redirect(url_for('encryption.delete_file'))



if __name__ == '__main__':
    app.run()

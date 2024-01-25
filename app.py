from flask import Flask, render_template, request, redirect, url_for, session
from flask_login import LoginManager, login_required
from models import db, User
from user import user_bp
from encryption import encryption_bp
from flask_login import current_user, logout_user
import os

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://vzbvabbwraunrq:f5eb32113a778a27aa5eeda81e4fb2876d79e96d13ca67b001aa1cdfb68419e8@ec2-107-21-67-46.compute-1.amazonaws.com:5432/d4hj3ld5o7fdll'
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

    return app

app = create_app()

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
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

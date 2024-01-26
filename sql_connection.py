from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models import User
from flask_login import UserMixin

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://mohanpuvvula:Manoj@1234@mohanpuvvula.mysql.pythonanywhere-services.com/myconnection'


db = SQLAlchemy(app)

def create_tables():

    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    create_tables()

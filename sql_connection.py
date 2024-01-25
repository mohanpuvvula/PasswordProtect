from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models import User
from flask_login import UserMixin

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://vzbvabbwraunrq:f5eb32113a778a27aa5eeda81e4fb2876d79e96d13ca67b001aa1cdfb68419e8@ec2-107-21-67-46.compute-1.amazonaws.com:5432/d4hj3ld5o7fdll'


db = SQLAlchemy(app)

def create_tables():

    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    create_tables()

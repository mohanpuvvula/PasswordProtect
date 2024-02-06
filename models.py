from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(db.Model, UserMixin):
    email = db.Column(db.String(120), unique=True, primary_key=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    mobilenumber = db.Column(db.String(10), unique=True, nullable=True)

    def get_id(self):
        return str(self.email)

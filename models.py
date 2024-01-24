from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    mobilenumber = db.Column(db.String(10), unique=True, nullable=False)

    def get_id(self):
        return self.id
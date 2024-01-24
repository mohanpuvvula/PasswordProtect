from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure Flask to use PostgreSQL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://vzbvabbwraunrq:f5eb32113a778a27aa5eeda81e4fb2876d79e96d13ca67b001aa1cdfb68419e8@ec2-107-21-67-46.compute-1.amazonaws.com:5432/d4hj3ld5o7fdll'

# Initialize the Flask-SQLAlchemy extension
db = SQLAlchemy(app)

# Define your models and other database-related code here

if __name__ == '__main__':
    app.run()

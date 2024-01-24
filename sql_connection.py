import mysql.connector
from flask import Flask
from models import db

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/myconnection'
app.config['SQLALCHEMY_DATABASE_URI'] = ' postgres://vzbvabbwraunrq:f5eb32113a778a27aa5eeda81e4fb2876d79e96d13ca67b001aa1cdfb68419e8@ec2-107-21-67-46.compute-1.amazonaws.com:5432/d4hj3ld5o7fdll'
app.secret_key = 'your_secure_key_here'

def connect_to_database():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            port=3306,
            password='root',
            database='myconnection',
            autocommit=True
        )
        print("Connected to MySQL database")
        return connection

    except mysql.Error as error:
        print("Error connecting to MySQL database:", error)
        exit(1)

db_connection = connect_to_database()
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/myconnection'
app.config['SQLALCHEMY_DATABASE_URI'] = ' postgres://vzbvabbwraunrq:f5eb32113a778a27aa5eeda81e4fb2876d79e96d13ca67b001aa1cdfb68419e8@ec2-107-21-67-46.compute-1.amazonaws.com:5432/d4hj3ld5o7fdll'

db.init_app(app)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run()

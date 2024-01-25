from flask import Flask
from flask.cli import FlaskGroup
from app import create_app, db

app = create_app()
cli = FlaskGroup(create_app=create_app)

# Create a command to initialize the database
@cli.command("init-db")
def init_db():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    cli()

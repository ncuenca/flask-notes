"""Models for Flask-Notes app."""

from flask_sqlalchemy import SQLAlchemy

DEFAULT_IMAGE = 'https://tinyurl.com/demo-cupcake'

db = SQLAlchemy()

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)

class User(db.Model):
    """User."""

    __tablename__ = "users"

    username = db.Column(db.String(20),
                    primary_key=True)
    password = db.Column(db.Text,
                    nullable=False)
    email = db.Column(db.Integer,
                    nullable=False,
                    unique=True)
    first_name = db.Column(db.String(30),
                    nullable=False)
    last_name = db.Column(db.String(30),
                    nullable=False)                


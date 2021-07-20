"""Models for Flask-Notes app."""

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

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
    email = db.Column(db.Text,
                    nullable=False,
                    unique=True)
    first_name = db.Column(db.String(30),
                    nullable=False)
    last_name = db.Column(db.String(30),
                    nullable=False)                

    @classmethod
    def register(cls, username, password, email, first_name, last_name):
        """Register user w/hashed password & return user."""

        hashed = Bcrypt().generate_password_hash(password).decode('utf8')

        # return instance of user w/username and hashed pwd
        return cls(
            username=username, 
            password=hashed,
            email=email,
            first_name=first_name,
            last_name=last_name
        )

    @classmethod
    def authenticate(cls, username, pwd):
        """Validate that user exists & password is correct.

        Return user if valid; else return False.
        """

        u = cls.query.filter_by(username=username).first()

        if u and Bcrypt().check_password_hash(u.password, pwd):
            # return user instance
            return u
        else:
            return False
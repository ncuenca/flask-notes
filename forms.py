"""Forms for flask-notes app."""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length, Email
from wtforms.widgets import TextArea

class RegisterUserForm(FlaskForm):
    """Form for registering user."""

    username = StringField("username",
                    validators = [InputRequired(), Length(max=20)])
    password = PasswordField("password",
                    validators = [InputRequired()])
    email = StringField("email",
                    validators = [InputRequired(), Email()])
    first_name = StringField("first_name",
                    validators = [InputRequired()])
    last_name = StringField("last_name",
                    validators = [InputRequired()])

class LoginUserForm(FlaskForm):
    """Form for login user."""

    username = StringField("username",
                    validators = [InputRequired(), Length(max=20)])
    password = PasswordField("password",
                    validators = [InputRequired()])

class AddNoteForm(FlaskForm):
    """Form for adding note."""

    title = StringField("title",
                    validators = [InputRequired(), Length(max=100)])
    content = TextArea("content",
                    validators = [InputRequired()])


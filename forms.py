"""Forms for flask-notes app."""

from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField
from wtforms.validators import InputRequired, Length, Email
class RegisterUserForm(FlaskForm):
    """Form for adding pet."""

    username = StringField("username",
                    validators = [InputRequired(), Length(max=20)])
    password = HiddenField("password",
                    validators = [InputRequired()])
    email = StringField("email",
                    validators = [InputRequired(), Email()])
    first_name = StringField("first_name",
                    validators = [InputRequired()])
    last_name = StringField("last_name",
                    validators = [InputRequired()])


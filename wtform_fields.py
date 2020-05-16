from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, EqualTo, ValidationError

from model.user import User

def invalid_credentials(form, field):
    username_entered = form.username.data
    password_entered = field.data
    
    user_object = User.find_by_name(username_entered)
    if user_object is None:
        raise ValidationError("No user found!")
    elif User.find_user_password(username_entered, password_entered) == False:
        raise ValidationError("Wrong password!")


class LoginForm(FlaskForm):

    username = StringField('username_label', validators=[InputRequired(message="Username required")])
    password = PasswordField('password_label', validators=[InputRequired(message="Password required"), invalid_credentials])
    submit_button = SubmitField('login')


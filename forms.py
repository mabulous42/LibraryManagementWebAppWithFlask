import json
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField
from wtforms.validators import ValidationError, InputRequired, Length, DataRequired, EqualTo
from helpers import load_data, save_data
from models import Library

library = Library()


class SignupForm(FlaskForm):
    firstName = StringField(validators=[InputRequired(), Length(min=2, max=20)],
                           render_kw={"placeholder": "First Name"})
    lastName = StringField(validators=[InputRequired(), Length(min=2, max=20)],
                           render_kw={"placeholder": "Last Name"})
    email = EmailField(validators=[InputRequired(), Length(min=8, max=30)],
                           render_kw={"placeholder": "Email"})
    password = PasswordField(validators=[InputRequired(), Length(min=8, max=30)],
                           render_kw={"placeholder": "Password"})
    submit = SubmitField('Sign Up')
    
    def validate_email(self, email):
        try:
            with open('users.json', 'r') as file:
                users = json.load(file)  # users should be a list of user dicts
        except FileNotFoundError:
            return False  # No users yet, so email cannot exist

        for user in users:
            if user.get('email') == email.data:
                raise ValidationError('Email already exist. Please choose a different one')
            
    
    # username = StringField('Username', validators=[DataRequired()])
    # password = PasswordField('Password', validators=[DataRequired()])
    # confirm_password = PasswordField('Confirm Password', validators=[
    #     DataRequired(), EqualTo('password')
    # ])
    # submit = SubmitField('Sign Up')
import json
from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, TextAreaField, IntegerField
from wtforms.validators import ValidationError, InputRequired, Length, DataRequired, EqualTo
from helpers import load_users, save_users
from models import Library, digitalLibrary

library = Library()
dglibrary = digitalLibrary()


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
            users = load_users(library)
            users = [user.to_dict() for user in users.values()]
            # with open('users.json', 'r') as file:
            #     users = json.load(file)  # users should be a list of user dicts
        except FileNotFoundError:
            return False  # No users yet, so email cannot exist

        for user in users:
            if user.get('email') == email.data:
                raise ValidationError('Email already exist. Please choose a different one')
            
class LoginForm(FlaskForm):
    email = EmailField(validators=[InputRequired(), Length(min=8, max=30)],
                           render_kw={"placeholder": "Email"})
    password = PasswordField(validators=[InputRequired(), Length(min=8, max=30)],
                           render_kw={"placeholder": "Password"})
    submit = SubmitField('Login')

class AddBookForm(FlaskForm):
    title = StringField(validators=[InputRequired()],
                           render_kw={"placeholder": "Enter the Book Title"})
    author = StringField(validators=[InputRequired()],
                           render_kw={"placeholder": "Enter the Book Author"})
    isbn = StringField(validators=[InputRequired(), Length(min=13, max=13)],
                           render_kw={"placeholder": "Enter the Book 13-digits ISBN"})
    copies = IntegerField(validators=[InputRequired()],
                           render_kw={"placeholder": "Enter the Book Number of Copies"})
    submit = SubmitField('Add Book')

class AddeBookForm(FlaskForm):
    title = StringField(validators=[InputRequired()],
                           render_kw={"placeholder": "Enter the eBook Title"})
    author = StringField(validators=[InputRequired()],
                           render_kw={"placeholder": "Enter the eBook Author"})
    isbn = StringField(validators=[InputRequired(), Length(min=13, max=13)],
                           render_kw={"placeholder": "Enter the eBook 13-digits ISBN"})
    format = StringField(validators=[InputRequired()],
                           render_kw={"placeholder": "Enter the eBook format"})
    file_path = StringField(validators=[InputRequired()],
                           render_kw={"placeholder": "Enter the eBook file path"})
    submit = SubmitField('Add eBook')

class UpdateUserForm(FlaskForm):
    firstName = StringField(validators=[InputRequired(), Length(min=2, max=20)],
                           render_kw={"placeholder": "First Name"})
    lastName = StringField(validators=[InputRequired(), Length(min=2, max=20)],
                           render_kw={"placeholder": "Last Name"})
    email = EmailField(validators=[InputRequired(), Length(min=8, max=30)],
                           render_kw={"placeholder": "Email"})
    submit = SubmitField('Update User')

class UpdateBookForm(FlaskForm):
    isbn = StringField(validators=[InputRequired(), Length(min=13, max=13)],
                           render_kw={"placeholder": "Enter the Book 13-digits ISBN"})
    title = StringField(validators=[InputRequired()],
                           render_kw={"placeholder": "Enter the Book Title"})
    author = StringField(validators=[InputRequired()],
                           render_kw={"placeholder": "Enter the Book Author"})
    copies = IntegerField(validators=[InputRequired()],
                           render_kw={"placeholder": "Enter the Book Number of Copies"})
    submit = SubmitField('Update Book')

class SearchUserForm(FlaskForm):
    name = StringField(validators=[InputRequired(), Length(min=1, max=30)],
                           render_kw={"placeholder": "Search Users..."})
    submit = SubmitField('Search User')

class SearchBookForm(FlaskForm):
    title = StringField(validators=[InputRequired(), Length(min=1, max=30)],
                           render_kw={"placeholder": "Search Books..."})
    submit = SubmitField('Search Book')
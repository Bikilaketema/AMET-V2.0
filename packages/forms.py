from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, SubmitField, EmailField, IntegerField
from wtforms.validators import Email,EqualTo,Length,DataRequired,ValidationError
from packages.models import User


class SignupForm(FlaskForm):
    def validate_username(self,username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username already exist! Please try a different username.')

    def validate_email(self,email_to_check):
        email = User.query.filter_by(email=email_to_check.data).first()
        if email:
            raise ValidationError('There is already an account with the email address.'
                                  'Please try different email address!')

    username = StringField(label="Username",validators=[Length(min=2,max=20),DataRequired()])
    email = EmailField(label="Email Address",validators=[Email(),DataRequired()])
    phone = IntegerField(label="Phone Number",validators=[DataRequired()])
    dob = DateField(label="Date of birth",validators=[DataRequired()])
    password1 = PasswordField(label="Password",validators=[Length(min=6),DataRequired()])
    password2 = PasswordField(label="Confirm password",validators=[EqualTo('password1'),DataRequired()])
    submit = SubmitField(label="Sign up")


class LoginForm(FlaskForm):
    username = StringField(label="Username")
    password = PasswordField(label="Password")
    login = SubmitField(label="Log in")

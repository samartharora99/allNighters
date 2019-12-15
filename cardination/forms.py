from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from cardination.models import Patient

class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    weight = StringField('Weight')
    height = StringField('Height')
    gender = StringField('Gender',validators=[ Length(min=0,max=1)])
    blood_group = StringField('Blood Group')
    DOB = DateField('Date of Birth')
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        patient = Patient.query.filter_by(username = username.data).first()
        if patient:
            raise ValidationError('That username is taken. Please choose another username')
    def validate_email(self, email):
        patient = Patient.query.filter_by(email = email.data).first()
        if patient:
            raise ValidationError('That email is taken. Please choose another username')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
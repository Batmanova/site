from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class CollectionForm(FlaskForm):
    numb = DateField('Date', validators=[DataRequired()], format='%d.%m.%Y')
    name = StringField('Plan', validators=[DataRequired()])
    submit = SubmitField('Add deal')


class FilterForm(FlaskForm):
    filter = DateField('Date', validators=[], format='%d.%m.%Y')
    submit = SubmitField('Select Date')

class DeleteForm(FlaskForm):
    numb = DateField('Date', validators=[], format='%d.%m.%Y')
    name = StringField('Plan', validators=[DataRequired()])
    submit = SubmitField('Delete')

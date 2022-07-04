
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, DataRequired, Email, ValidationError
from market.models import User


class RegisterForm(FlaskForm):

    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Hafa Guy! One manchi don use this username')

    def validate_email(self, email_to_check):
        user = User.query.filter_by(email=email_to_check.data).first()
        if user:
            raise ValidationError('Eheh! One manchi don use this email address')

            

    username = StringField(label='Username', validators=[Length(min=5, max=30), DataRequired()])
    email = StringField(label='Email', validators=[Email(), DataRequired()])
    password = PasswordField(label='Password', validators=[Length(min=5),DataRequired()])
    password2 = PasswordField(label='Confirm Password',validators=[EqualTo('password'), DataRequired()])    
    submit = SubmitField()
    

class LoginForm(FlaskForm):


    username = StringField(label='Username', validators=[ DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    submit = SubmitField()
    
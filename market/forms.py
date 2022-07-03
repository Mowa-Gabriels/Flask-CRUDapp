
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, DataRequired, Email


class RegisterForm(FlaskForm):

    username = StringField(label='Username', validators=[Length(min=5, max=30), DataRequired()])
    email = StringField(label='Email', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Password', validators=[Length(min=5),DataRequired()])
    password2 = PasswordField(label='Confirm Password',validators=[EqualTo('password1'), DataRequired()])    
    submit = SubmitField()
    
"""
Creates type of input, labels, validation, error messages
validation and error handling is done clientside and before the POST
form.validate_on_submit() detects if a request is both a POST request and a valid request.
after that we can do additional server side checks

note: If you want to see your custom messages for e.g Datarequired, Email validators
the form shoudld have <form novalidate>
else you see the defaults
"""
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField, PasswordField, DateField
from wtforms.validators import DataRequired, Length, Optional, Email, ValidationError
from core.models import Channel, Program


def unique(model, col, message=None):
    """Custom validator: Check if a colum value for a Model has an unique value"""
    if not message:
        message = '{} already exists'.format(col)

    def _unique(form, field):
        existing_name = model.query.filter(col == field.data).first()
        if existing_name:
            raise ValidationError(message)
    return _unique


class LoginForm(FlaskForm):
    """Login form."""
    email = EmailField('Email', [
        DataRequired(message='please fill in an email adres.'),
        Email(message='Not a valid email address.')
    ])
    pasw = PasswordField('Password', [
        DataRequired(message='please fill in a password.'),
        Length(min=5, max=25, message='Password length must be between %(min)d and %(max)dcharacters')
    ])
    submit = SubmitField('Submit')


class ChannelForm(FlaskForm):
    """Channel form."""
    name = StringField('Name', [
        DataRequired(),
        Length(min=3, max=25),
        unique(Channel, Channel.name, message="A channel with this name already exists")
    ])
    title = StringField('Title', [DataRequired(), Length(min=3, max=25)])
    timezone = StringField('Timezone', [DataRequired()])
    submit = SubmitField('Submit')


class ProgramForm(FlaskForm):
    """Program form."""
    name = StringField('Name', [
        DataRequired(),
        Length(min=3, max=25),
        unique(Program, Program.name, message="A Program with this name already exists")
    ])
    title = StringField('Title', [DataRequired(), Length(min=3, max=25)])
    description = StringField('Description', [DataRequired(), Length(min=3, max=250)])
    genre = StringField('Genre', [Optional()])
    rating = StringField('Rating', [Optional()])
    submit = SubmitField('Submit')


class ScheduleForm(FlaskForm):
    """Program form."""
    # TODO combo box with all channels + search
    # TODO combo box with all programs + search
    # or some other method
    start = DateField('Start', [Optional()])
    end = DateField('End', [Optional()])
    submit = SubmitField('Submit')



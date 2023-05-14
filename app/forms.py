"""Forms class declaration"""
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms.fields import (
    BooleanField, DateField, StringField, SubmitField, TextAreaField, TimeField
    )
from wtforms.validators import DataRequired, ValidationError

class AppointmentForm(FlaskForm):
    '''Form in Calendar'''
    name = StringField('Name', validators=[DataRequired()])
    start_date = DateField('Start Date', validators=[DataRequired()])
    start_time = TimeField('Start Time', validators=[DataRequired()])
    end_date = DateField('End Date', validators=[DataRequired()])
    end_time = TimeField('End Time', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    private = BooleanField('Private')
    submit = SubmitField('Save')

    def validate_end_date(form, field): # pylint: disable=no-self-argument
        '''Validating start < end'''
        start = datetime.combine(form.start_date.data, form.start_time.data)
        end = datetime.combine(field.data, form.end_time.data)
        if start >= end:
            raise ValidationError('End date/time must come after start date/time')

        if form.start_date.data != form.end_date.data:
            raise ValidationError('Currently Calendar supports only'
                'in-Day shedule (startDay = endDay)')

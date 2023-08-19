from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, IntegerField, TextAreaField
from wtforms.validators import InputRequired, URL, NumberRange, Length, Optional


class AddPetForm(FlaskForm):
    name = StringField('Pet name', validators=[InputRequired()])
    species = SelectField('Species', choices=[('cat', 'Cat'), ('dog', 'Dog'), ('porcupine', 'Porcupine')],
                          validators=[InputRequired()])
    photo_url = StringField('Photo URL', validators=[URL(), Optional()])
    age = IntegerField('Age', validators=[NumberRange(min=0, max=30), Optional()])
    notes = TextAreaField('Notes', validators=[Length(max=500), Optional()])


class EditPetForm(FlaskForm):
    name = StringField('Pet name', validators=[InputRequired()])
    species = SelectField('Species', choices=[('cat', 'Cat'), ('dog', 'Dog'), ('porcupine', 'Porcupine')],
                          validators=[InputRequired()])
    photo_url = StringField('Photo URL', validators=[URL(), Optional()])
    age = IntegerField('Age', validators=[NumberRange(min=0, max=30), Optional()])
    notes = TextAreaField('Notes', validators=[Length(max=500), Optional()])

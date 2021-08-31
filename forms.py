from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, TextAreaField, BooleanField
from wtforms.validators import InputRequired, Length, NumberRange, URL, Optional

class AddPetForm(FlaskForm):

    name = StringField("Pet Name", validators=[InputRequired()])

    species = SelectField("Species", choices=[("cat", "Cat"), ("dog", "Dog"), ("porcupine", "Porcupine")])

    photo_url = StringField("Photo url", validators=[Optional(), URL()])

    age = IntegerField("Age", validators=[Optional(), NumberRange(0,30)])

    notes = TextAreaField("Extra Notes", validators=[Optional()])

class EditPetForm(FlaskForm):

    photo_url = StringField("Photo URL", validators=[Optional(), URL()])

    notes = TextAreaField("Comments", validators=[Optional(), Length(min=10)])

    available = BooleanField("Availble?")
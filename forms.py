from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, FloatField, validators, SubmitField
from wtforms.validators import InputRequired, NumberRange, Optional, URL

class CupcakeForm(FlaskForm):
    flavor = StringField('Flavor',
                         validators=[InputRequired()])
    size = SelectField('Size',
                       choices=[('Small', 'Small'), ('Medium', 'Medium'), ('Large', 'Large')])
    rating = FloatField('Rating', 
                        validators=[InputRequired(), NumberRange(min=1, max=10, message="Number must be between 1 and 5")])
    image = StringField('Image',
                        validators=[Optional(), URL()])
    submit = SubmitField('Submit')
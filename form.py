from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SelectField
from wtforms.validators import InputRequired, NumberRange, Optional, URL

class AddCupcakeForm(FlaskForm):
    
    flavor = StringField("Flavor:", 
                         validators=[InputRequired()])
    size = SelectField("Size:", 
                       choices=[('small', 'Small'), ('medium', 'Medium'), ('large', 'Large')], 
                       validators=[InputRequired()])
    rating = FloatField("Rating:",
                        validators=[InputRequired(), NumberRange(max=10.0)])
    image = StringField("Image:", 
                        validators=[Optional(), URL()],
                        filters=[lambda x: x.strip() if x else None])
            
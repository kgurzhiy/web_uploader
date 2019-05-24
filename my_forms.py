from flask_wtf import FlaskForm
from wtforms import IntegerField, FileField
from wtforms.validators import NumberRange


class FormFile(FlaskForm):
    file = FileField('file')
    expiration_time = IntegerField(
        'expiration_time', validators=[NumberRange(min=1, max=60)]
    )

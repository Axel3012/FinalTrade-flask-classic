from flask_wtf import FlaskForm
from wtforms import FloatField, HiddenField,SelectField,SubmitField
from wtforms.validators import DataRequired, Length
from . import MONEDAS

class ComprasForm(FlaskForm):
    id = HiddenField()
    moneda_from = SelectField(
        u'Moneda From:', choices = MONEDAS, validators=[DataRequired(
            message='Moneda de origen obligatoria')] )

    cantidad_from = FloatField(
        'Q:', validators=[DataRequired(
            message='Cantidad para intercambio obligatoria')])

    moneda_to = SelectField(
        u'Moneda To:', choices = MONEDAS, validators=[DataRequired(
            message='Moneda de destino obligatoria')])    

    consulta_api = SubmitField(
        'Consulta', render_kw={'class':'blue-button'})

    cancelar = SubmitField('✖')
    guardar = SubmitField('✓')


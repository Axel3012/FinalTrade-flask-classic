from datetime import date, datetime, time
from flask import render_template, request, url_for, redirect

from . import app
from . import RUTA
from .forms import ComprasForm
from .models import DBManager, CriptoModel

@app.route('/')
def movimientos():
    db = DBManager(RUTA)
    movimientos = db.consultaSQL('SELECT * FROM movimientos')
    return render_template('inicio.html', movs=movimientos)

@app.route('/comprar', methods=['GET','POST'])
def comprar():
    '''
    Este metodo permite consultar el valor de una moneda y
    de realizar una transaccion guardandola en la base de datos
    '''
    
    if request.method == 'GET':
        formulario = ComprasForm() 
        return(render_template(
            'form_compra.html', form=formulario))

    elif request.method == 'POST':
        form = ComprasForm(data=request.form)
        cripto_cambio = CriptoModel()
        if form.validate():
            db = DBManager(RUTA)
            cripto_cambio.moneda_from = form.moneda_from.data
            cripto_cambio.moneda_to = form.moneda_to.data
            cantidad_from = form.cantidad_from.data
            cambio = cripto_cambio.consultar_cambio()
            cantidad_to = cantidad_from * cambio

            if form.consulta_api.data:
                return render_template(
                    'form_compra.html', form = form,
                        cantidad_to = cantidad_to,
                        precio_unitario = cambio)

            elif form.guardar.data:

                fecha = date.today().isoformat()
                hora = time(
                    datetime.now().hour,
                    datetime.now().minute,
                    datetime.now().second)
                consulta = 'INSERT INTO movimientos(fecha, hora, moneda_from, cantidad_from, moneda_to, cantidad_to) VALUES (fecha=?, hora=?, moneda_from=?, cantidad_from=?, moneda_to=?, cantidad_to=?)'
                params = (
                    fecha,
                    hora,
                    form.moneda_from.data,
                    form.cantidad_from.data,
                    form.moneda_to.data,
                    cantidad_to
                )

                resultado = db.consultaConParametros(consulta, params)
                if resultado:
                    return redirect(url_for('inicio'))
                return render_template("form_compra.html", form=form, id=id, errores=["Ha fallado la operación de guardar en la base de datos"])
            else:
                return render_template("form_compra.html", form=form, id=id, errores=["Ha fallado la validación de los datos"])






@app.route('/status')
def status():
    return 'Estado del movimiento en euros'

@app.route('/deposito',methods=['GET','POST'])
def deposito():
    '''
    Este metodo agrega euros a el wallet del cliente
    lo hace con el formato de un formulario de tarjeta de credito
    '''
    return 'Deposito a la cuenta en euros'

@app.route('/wallet')
def wallet():
    return 'Cadidad de Euros o criptomonedas disponibles'



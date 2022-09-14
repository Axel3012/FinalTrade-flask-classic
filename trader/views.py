from datetime import date, datetime, time
from flask import flash ,redirect, render_template, request, url_for 

from . import MONEDAS, MONEDAS1, app
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
        if not form.validate():
            return render_template(
                "form_compra.html", form=form, id=id, errores=[
                    "Ha fallado la validación de los datos"])

        db = DBManager(RUTA)
        cripto_cambio.moneda_from = form.moneda_from.data
        cripto_cambio.moneda_to = form.moneda_to.data
        cantidad_from = form.cantidad_from.data
        cambio = cripto_cambio.consultar_cambio()
        cantidad_to = cantidad_from * cambio

        if form.moneda_from.data == form.moneda_to.data:

            flash("Moneda From y Moneda To deben ser diferentes", category="exito")
            return redirect(url_for('comprar'))

        if form.consulta_api.data:
            return render_template(
                'form_compra.html', form = form,
                    cantidad_to = cantidad_to,
                    precio_unitario = cambio)

        elif form.cancelar.data:
            return redirect(url_for('comprar'))

        elif form.guardar.data:
            fecha = date.today().isoformat()
            hora = time(
                datetime.now().hour,
                datetime.now().minute,
                datetime.now().second)
            consulta = 'INSERT INTO movimientos(fecha, hora, moneda_from, cantidad_from, moneda_to, cantidad_to) VALUES (?, ?, ?, ?, ?, ?)'
            params = (
                fecha,
                str(hora),
                form.moneda_from.data,
                cantidad_from,
                form.moneda_to.data,
                cantidad_to)   
            resultado = db.consultaConParametros(consulta, params)
            
            if not resultado:
                return render_template("form_compra.html", form=form, id=id, errores=["Ha fallado la operación de guardar en la base de datos"])

            flash("Movimiento agregado correctamente ;)", category="exito")
            return redirect(url_for('movimientos'))
            
@app.route('/status')
def status():
    cripto_cambio = CriptoModel()
    db = DBManager(RUTA)
    valor_criptos_euros = []
    for moneda in MONEDAS1:
        consulta_from = 'SELECT SUM(cantidad_from) FROM movimientos WHERE moneda_from=? AND cantidad_from IS NOT NULL'
        consulta_to = 'SELECT SUM(cantidad_to) FROM movimientos WHERE moneda_to=? AND cantidad_to IS NOT NULL'
        parametros = (moneda,)
        cantidad_from = db.solicitudConParametros(consulta_from,params=parametros)
        if moneda == 'EUR':
            total_euros = cantidad_from
        cantidad_to = db.solicitudConParametros(consulta_to, params=parametros)
        print(moneda)
        print(cantidad_to, cantidad_from)
        saldo_cripto = cantidad_to - cantidad_from
        cripto_cambio.moneda_from = moneda
        cripto_cambio.moneda_to = 'EUR'
        cambio_status = cripto_cambio.consultar_cambio()
        cripto_a_euros = cambio_status * saldo_cripto
        valor_criptos_euros.append(cripto_a_euros)

    valor_criptos_euros = sum(valor_criptos_euros) + total_euros

    return render_template(
        'status.html', invertido = total_euros,
            valor_actual = valor_criptos_euros )

@app.route('/wallet')
def wallet():
    return 'Cadidad de Euros o criptomonedas disponibles'
    
@app.route('/deposito',methods=['GET','POST'])
def deposito():
    '''
    Este metodo agrega euros a el wallet del cliente
    lo hace con el formato de un formulario de tarjeta de credito
    '''
    return 'Deposito a la cuenta en euros'



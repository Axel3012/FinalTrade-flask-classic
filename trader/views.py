from datetime import date, datetime, time
from flask import flash ,redirect, render_template, request, url_for 

from . import MONEDAS, app
from . import RUTA
from .forms import ComprasForm
from .models import CriptoModel, DBManager
from .functions import consulta_saldo

@app.route('/')
def movimientos():
    db = DBManager(RUTA)
    movimientos = db.consultaSQL('SELECT * FROM movimientos ORDER BY fecha DESC, hora DESC LIMIT 15')
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
        moneda_from = form.moneda_from.data
        moneda_to = form.moneda_to.data
        cripto_cambio = CriptoModel()

        if not form.validate():
            return render_template(
                "form_compra.html", form=form, id=id, errores=[
                    "Ha fallado la validación de los datos"])

        if moneda_from == moneda_to:
            flash('Moneda From y Moneda To deben ser diferentes', category='warning')
            return redirect(url_for('comprar'))

        db = DBManager(RUTA)
        cripto_cambio.moneda_from = moneda_from
        cripto_cambio.moneda_to = moneda_to
        cantidad_from = form.cantidad_from.data
        cambio = cripto_cambio.consultar_cambio()
        cantidad_to = cantidad_from * cambio

        saldo, gastado = consulta_saldo(moneda_from)
        
        if moneda_from == 'EUR':
            saldo = float('inf')

        if saldo < cantidad_from:
            flash('Saldo insuficiente', category='warning')
            return redirect(url_for('comprar'))

        if form.consulta_api.data:
            form.cantidad_from.render_kw = {'readonly':True}
            return render_template(
                'form_compra.html', form = form,
                    cantidad_to = round(cantidad_to,5),
                    precio_unitario = round(cambio,5))

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
                moneda_from,
                cantidad_from,
                moneda_to,
                cantidad_to)   
            resultado = db.consultaConParametros(consulta, params)
            
            if not resultado:
                return render_template(
                    'form_compra.html', form=form, id=id, errores=[
                        'Ha fallado la operación de guardar en la base de datos'])

            flash('Movimiento agregado correctamente ;)', category='exito')
            return redirect(url_for('movimientos'))
            
@app.route('/status')
def status():
    cripto_cambio = CriptoModel()
    db = DBManager(RUTA)
    valor_criptos_euros = []
    for moneda in MONEDAS:
        moneda = moneda[0]
        saldo_cripto, cantidad_from = consulta_saldo(moneda)

        if moneda == 'EUR':
            total_euros = cantidad_from
        
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
    

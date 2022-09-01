
from flask import render_template, request, url_for, redirect
from . import app
from .forms import ComprasForm
from .models import DBManager

RUTA = 'data/trade.db'

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
        return(render_template('form_compra.html', form=formulario))

    elif request.method == 'POST':
        pass
    #return render_template('comprar.html', compra=False)

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



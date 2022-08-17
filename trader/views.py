from . import app

@app.route('/')
def movimientos():
    return 'Pagina de inicio'

@app.route('/compra', methods=['GET','POST'])
def compra():
    return 'Compra/venta de criptos'

@app.route('/status')
def status():
    return 'Estado del movimiento en euros'

@app.route('/deposito',methods=['GET','POST'])
def deposito():
    return 'Deposito a la cuenta en euros'
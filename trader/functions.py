from .models import DBManager
from trader import RUTA


def consulta_saldo(moneda):
    db = DBManager(RUTA)
    consulta_from = 'SELECT SUM(cantidad_from) FROM movimientos WHERE moneda_from=? AND cantidad_from IS NOT NULL'
    consulta_to = 'SELECT SUM(cantidad_to) FROM movimientos WHERE moneda_to=? AND cantidad_to IS NOT NULL'
    parametros = (moneda,)
    gastado = db.solicitudConParametros(consulta_from, parametros)
    comprado = db.solicitudConParametros(consulta_to, parametros)
    saldo = comprado - gastado
    return saldo
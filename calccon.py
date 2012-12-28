#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Calculo de consolidado"""
import cgi
import cgitb ; cgitb.enable()
import htm
import datos
import sys
import pagina
def calcular(frm):
    """Calcula el consolidado y lo va mostrando en una página"""
    if not frm.has_key("ano"):
        pagina.error_parametros("consolidado.py")
    else:
        ano = frm["ano"].value
        pag = pagina.Pagina("Procesando consolidado", 4)
        print(htm.h2("Por favor espere a que finalice el proceso..."))
        print("Puede tomar varios minutos")
        print(htm.h3("Reseteando consolidado..."))
        sys.stdout.flush()
        resetear_consolidado()
        print(htm.h3("Calculando consolidado..."))
        sys.stdout.flush()
        calcular_consolidado(ano)
        print(htm.h3("Rellenando consolidado..."))
        sys.stdout.flush()
        rellenar_consolidado()
        print "OK"
        print(htm.h2("Proceso finalizado"))
        print(htm.button("Volver","consolidado.py"))
        pag.fin()
def resetear_consolidado():
    """Limpia la tabla consolidado y genera nueva vacía"""
    meses = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "setiembre", "octubre", "noviembre", "diciembre"]
    print(htm.h3("Vaciando tabla  de Consolidado..."))
    sql = "TRUNCATE TABLE consolidado"
    dat = datos.Datos()
    dat.cursor.execute(sql)
    cuentas = datos.Tabla("cuentas")
    cuentas.orden = " rubro "
    cuentas.filtrar()
    consolidado = datos.Tabla("consolidado")
    print(htm.h3("Llenando con datos del Plan de Cuentas..."))
    for fila in cuentas.resultado:
        consolidado.registro["rubro"] = fila["rubro"]
        if len(fila["nombre"]) < 39:
            consolidado.registro["nombre"] = fila["nombre"]
        else:
            nombre = fila["nombre"]
            # OJO, hay una diferencia entre el largo de nombre en CUENTAS y en CONSOLIDADO
            nombre = nombre[0:38]
            consolidado.registro["nombre"] = nombre
        consolidado.registro["nivel"] = fila["nivel"]
        for item in meses:
            consolidado.registro[item] = 0
        consolidado.insertar()
def calcular_consolidado(ano):
    """Calcula el consolidado"""
    # ajustar para que calcule PARA ESTE AÑO
    meses = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "setiembre", "octubre", "noviembre", "diciembre"]
    # transacciones = datos.Tabla("transacciones")
    # Cargar primero las transacciones consume MUCHOS recursos
    transacciones = datos.Datos()
    cuentas = datos.Tabla("cuentas")
    cuentas.orden = "rubro"
    cuentas.filtrar()
    consolidado = datos.Tabla("consolidado", clave="rubro")
    for cuenta in cuentas.resultado:
        consolidado.ir_a(cuenta["rubro"])
        saldo = 0
        for mes in range(12):
            sql = "SELECT sum(debe) as d, sum(haber) as h FROM transacciones WHERE YEAR(fecha)=" + \
                ano + " AND MONTH(fecha)=" + str(mes + 1) + " AND cuenta_id = " + \
                str(cuenta["id"])
            transacciones.cursor.execute(sql)
            resultado = transacciones.cursor.fetchone()
            haber = resultado["h"]
            debe = resultado["d"]
            if type(haber) == type(None):
                haber = 0
            if type(debe) == type(None):
                debe = 0
            saldo = haber - debe
            consolidado.registro[meses[mes]] = saldo
        consolidado.actualizar()

def rellenar_consolidado():
    """Rellena de datos el consolidado"""
    meses = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "setiembre", "octubre", "noviembre", "diciembre"]
    consolidado = datos.Tabla("consolidado")
    consolidado.filtro = " nivel <> 0 "
    consolidado.filtrar()
    dat = datos.Datos()
    for fila in consolidado.resultado:
        nivel = fila["nivel"]
        rubro = str(fila["rubro"])
        for m in range(0, 11):
            # subrub = substr(rubro, 0, -nivel)
            subrub = rubro[0:-nivel]
            sql_sub = "SELECT SUM(" + meses[m] + ") as suma FROM consolidado WHERE (rubro LIKE '"
            sql_sub = sql_sub + subrub + "%') AND (nivel=0)"
            dat.cursor.execute(sql_sub)
            resultado = dat.cursor.fetchone()
            suma = resultado["suma"]
            sql_upd = "UPDATE consolidado SET "
            sql_upd = sql_upd + meses[m] + "= '" + str(suma) + "' WHERE rubro = '" + rubro + "'"
            dat.cursor.execute(sql_upd)
def main():
    """Rutina principal"""
    form = cgi.FieldStorage()
    accion = form.getvalue("accion", "calcular")
    if accion == 'calcular':
        calcular(form)
    else:
        pagina.error_parametros("geined.py?accion=principal")
if __name__ == "__main__":
    main()

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Programa para mostrar evolución financiera"""
import cgitb; cgitb.enable()
import htm
import cgi
import datos
import funciones
import pagina
def listado():
    """Listado de evolución financiera"""
    pag = pagina.Pagina("Evolución financiera", 2)
    htm.button("Volver", "geined.py?accion=financiero")
    global i
    i = 0
    htm.encabezado_tabla(["Item", "2008", "2009", "2010"])
    hilera("Bienes de uso", "122")
    hilera("Ingresos por cursos", "411")
    hilera("Otros ingresos", "412")
    hilera("Ingresos por textos", "413")
    hilera("Ingresos no operativos", "42")
    i = 1
    hilera("TOTAL DE INGRESOS", "4")
    i = 0
    hilera("Gastos operativos", "51")
    hilera("Gastos no operativos", "52")
    i = 1
    hilera("TOTAL DE GASTOS", "5")
    htm.fila_alterna(i)
    print(htm.td("RESULTADOS FINANCIEROS"))
    ingresos_2008 = consulta("2008", "4")
    egresos_2008 = consulta("2008", "5")
    saldo_2008 = ingresos_2008 + egresos_2008
    print(htm.td(funciones.moneda(saldo_2008), "d"))

    ingresos_2009 = consulta("2009", "4")
    egresos_2009 = consulta("2009", "5")
    saldo_2009 = ingresos_2009 + egresos_2009
    print(htm.td(funciones.moneda(saldo_2009), "d"))

    ingresos_2010 = consulta("2010", "4")
    egresos_2010 = consulta("2010", "5")
    saldo_2010 = ingresos_2010 + egresos_2010
    print(htm.td(funciones.moneda(saldo_2010), "d"))
    print("</tr>")

    htm.fin_tabla()
    htm.button("Volver", "geined.py?accion=financiero")
    pag.fin()
def hilera(texto, rubro):
    """Devuelve una hilera de la tabla de evolución"""
    global i
    htm.fila_alterna(i)
    print(htm.td(texto))
    print(htm.td(funciones.moneda(consulta("2008", rubro)), "d"))
    print(htm.td(funciones.moneda(consulta("2009", rubro)), "d"))
    print(htm.td(funciones.moneda(consulta("2010", rubro)), "d"))
    print("</tr>")

def consulta(ano, rubro):
    """Devuelve el saldo para un año y encabezado de rubro"""
    db = datos.Datos()
    sql = "select sum(transacciones.debe) as debe, sum(transacciones.haber) as haber from transacciones join cuentas on transacciones.cuenta_id = cuentas.id WHERE (YEAR(transacciones.fecha)=" \
        + ano + ") and (cuentas.rubro like '" + rubro + "%')"
    db.cursor.execute(sql)
    resultado = db.cursor.fetchone()
    if type(resultado["haber"]) == type(None):
        haber = 0
    else:
        haber = resultado["haber"]
    if type(resultado["debe"]) == type(None):
        debe = 0
    else:
        debe = resultado["debe"]
    saldo = haber - debe
    return saldo

if __name__ == "__main__":
    form = cgi.FieldStorage()
    accion = form.getvalue("accion", "listado")
    if accion == "listado":
        listado()
    else:
        listado()

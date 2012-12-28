#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Cuenta de los empleados"""
#import cgitb; cgitb.enable()
import cgi
import htm
import datos
import funciones
import pagina
def listado(frm):
    """Listado de la cuenta de un empleado en particular"""
    id_no = frm["id"].value
    cta_emp = datos.Tabla("cta_empleados")
    cta_emp.buscar("empleado_id", id_no)
    pag = pagina.Pagina("Estado de cuenta de empleado", 5)
    htm.encabezado_tabla(["Nº", "Fecha", "Detalle", "Debe", "Haber", "Saldo", "Movimiento"])
    i = 0
    saldo = 0
    for linea in cta_emp.resultado:
        saldo = saldo + linea["debe"] - linea["haber"]
        htm.fila_alterna(i)
        print(htm.td(linea["id"]))
        print(htm.td(funciones.mysql_a_fecha(linea["fecha"])))
        print(htm.td(linea["detalle"]))
        print(htm.td(funciones.moneda(linea["debe"])))
        print(htm.td(funciones.moneda(linea["haber"])))
        print(htm.td(funciones.moneda(saldo)))
        if linea["extra_id"] == 1:
            movimiento = "Prestamo material"
        else:
            movimiento = str(linea["extra_id"])
        print(htm.td(movimiento))
        i = i + 1
    htm.fin_tabla()
    htm.button("Volver a préstamo de material", "presmat.py")
    pag.fin()
def main():
    """Principal"""
    form = cgi.FieldStorage()
    accion = form.getvalue("accion", "listado")
    if accion == "listado":
        listado(form)

if __name__ == "__main__":
    main()
    
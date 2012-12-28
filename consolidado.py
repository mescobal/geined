#!/usr/bin/env python
#! -*- coding: utf-8 -*-
"""Listado y creación del consolidado anual"""
import cgi
import cgitb; cgitb.enable()
import funciones
import datos
import pagina
import htm
import csv
import StringIO
def listado():
    """Listado de consolidado"""
    pag = pagina.Pagina("Consolidado anual", 4)
    print(htm.encabezado("Consolidado anual", "Administración financiera", 
                         "geined.py?accion=financiero"))
    print("<table class='tabla_barra'><tr><td>")
    print(htm.button("Exportar a Planilla", "consolidado.py?accion=exportar"))
    print("</td><td>")
    htm.formulario("calccon.py")
    print("Seleccione año:")
    print(htm.hidden("accion", "calcular"))
    htm.seleccionar_ano()
    print('<input type="submit" value="Recalcular" />')
    htm.fin_formulario()
    print("</td>")
    print("</tr></table>")
    htm.encabezado_tabla(["Rubro", "Nombre", "Enero", "Febrero", "Marzo", 
        "Abril", "Mayo", "Junio", "Julio", "Agosto", "Setiembre", "Octubre",
        "Noviembre", "Diciembre", "Total"])
    consolidado = datos.Tabla("consolidado")
    cuentas = datos.Tabla("cuentas")
    consolidado.orden = "rubro"
    consolidado.filtrar()
    meses = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio",
             "agosto", "setiembre", "octubre", "noviembre", "diciembre"]
    for fila in consolidado.resultado:
        print("<tr class='fila_datos'>")
        print(htm.td(fila['rubro']))
        cuentas.buscar("rubro", fila["rubro"])
        print(htm.td(cuentas.registro["nombre"]))
        total = 0
        for item in meses:
            print(htm.td(funciones.moneda(fila[item]), "right"))
            total = total + fila[item]
        print(htm.td(funciones.moneda(total), "right"))
        print('</tr>')
    htm.fin_tabla()
    pag.fin()
def exportar():
    """Exportar consolidado en formato CSV"""
    salida = StringIO.StringIO()            
    expcsv = csv.DictWriter(salida, ["Rubro", "Nombre", "Enero", "Febrero", 
                                     "Marzo", "Abril", "Mayo", "Junio", 
                                     "Julio", 
                                     "Agosto", "Setiembre", "Octubre", 
                                     "Noviembre", "Diciembre", "Total"])
    consolidado = datos.Tabla("consolidado")
    consolidado.orden = "rubro"
    consolidado.filtrar()
    filename = "consolidado.csv"
    meses = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio",
             "agosto", "setiembre", "octubre", "noviembre", "diciembre"]
    expcsv.writeheader()         
    for fila in consolidado.resultado:
        # Recuperar variables */
        total = 0
        for item in meses:
            total = total + fila[item]
        expcsv.writerow({"Rubro":str(fila["rubro"]), "Nombre":fila["nombre"],
            "Enero":fila["enero"], "Febrero":fila["febrero"], 
            "Marzo":fila["marzo"], "Abril":fila["abril"], "Mayo":fila["mayo"],
            "Junio":fila["junio"], "Julio":fila["julio"], 
            "Agosto":fila["agosto"],
            "Setiembre":fila["setiembre"], "Octubre":fila["octubre"],
            "Noviembre":fila["noviembre"], "Diciembre":fila["diciembre"],
            "Total":total})
    headers = '\r\n'.join([
        "Content-type: %s;",
        "Content-Disposition: attachment; filename=%s",
        "Content-Title: %s",
        "Content-Length: %i",
        "\r\n", # empty line to end headers
        ])
    length = len(salida.getvalue())
    print(headers % ('text/csv', filename, filename, length))
    print(salida.getvalue())
    salida.close()
    listado()
def main():
    """Principal"""
    form = cgi.FieldStorage()
    accion = form.getvalue("accion", "listado")
    if accion == "listado":
        listado()
    elif accion == "exportar":
        exportar()

if __name__ == "__main__":
    main()

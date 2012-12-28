#!/usr/bin/env python
# -*- coding: utf-8 -*-
import cgi
import cgitb; cgitb.enable()
import funciones
import htm
import datos
import pagina
import csv
import StringIO
def listado(frm):
    pag = pagina.Pagina("Cobranzas a depositar", 4)
    print(htm.encabezado("Cobranzas a depositar", "Administración financiera", 
                         "geined.py?accion=financiero"))
    print(htm.div(htm.boton("Exportar", "111018_bancos.py?accion=exportar"), 
                  clase="barra"))
    filas_por_pagina = 20
    pagina_actual = 1
    if frm.has_key('pagina'):
        pagina_actual = frm.getvalue('pagina')
    cuentas = datos.Tabla('cuentas')
    cuentas.buscar('rubro', '111018')
    cuenta_id = cuentas.registro['id']
    dat = datos.Datos()
    sql_debe = 'SELECT SUM(debe) AS debe, SUM(haber) AS haber FROM transacciones WHERE cuenta_id=' + str(cuenta_id)
    dat.ejecutar(sql_debe)
    res = dat.cursor.fetchone()
    tot_debe = res['debe']
    tot_haber = res['haber']
    off_set = (int(pagina_actual) - 1) * filas_por_pagina
    tot_saldo = tot_haber - tot_debe
    print("<table class='barra'>")
    print(htm.tr(
            htm.td("Debe:" + funciones.moneda(tot_debe)) +
            htm.td("Haber:" + funciones.moneda(tot_haber)) +
            htm.td("Saldo:" + funciones.moneda(tot_saldo))))
    print("</table>")
    sql_tot = 'SELECT * FROM transacciones WHERE cuenta_id=' + str(cuenta_id)
    dat.ejecutar(sql_tot)
    transacciones = datos.Tabla('transacciones')
    transacciones.filtro = "cuenta_id=" + str(cuenta_id)
    transacciones.filtrar()
    total_filas = transacciones.num_filas
    total_paginas = total_filas / filas_por_pagina
    transacciones.limite = str(filas_por_pagina) + " OFFSET " + str(off_set)
    transacciones.orden = 'id'
    transacciones.filtrar()
    saldo = 0
    htm.encabezado_tabla(["Nº", "Fecha", "Detalle", "Debe", "Haber", "Saldo"])
    for fila in transacciones.resultado:
        print("<tr class='fila_datos'>")
        print(htm.td(fila['id']))
        print(htm.td(funciones.mysql_a_fecha(fila['fecha'])))
        print(htm.td(fila['detalle']))
        print(htm.td(funciones.moneda(fila['debe']), 'right'))
        print(htm.td(funciones.moneda(fila['haber']), 'right'))
        saldo = saldo + fila['haber'] - fila['debe']
        print(htm.td(funciones.moneda(saldo)))
    htm.fin_tabla()
    htm.navegador('111018_bancos.py?accion=listado', 
                  pagina_actual, total_paginas)
    htm.button('Volver', 'geined.py?accion=direccion')
    pag.fin()
def exportar():
    """Exportacion a CSV"""
    cuentas = datos.Tabla('cuentas')
    cuentas.buscar('rubro', '111018')
    cuenta_id = cuentas.registro['id']
    transacciones = datos.Tabla('transacciones')
    transacciones.filtro = 'cuenta_id=' + str(cuenta_id)
    transacciones.orden = 'fecha'
    transacciones.filtrar()
    salida = StringIO.StringIO()
    saldo = 0
    sum_debe = 0
    sum_haber = 0
    tracsv = csv.DictWriter(salida, ["No", "Fecha", "Detalle", "Debe", 
                                     "Haber", "Saldo"])
    for fila in transacciones.resultado:
        haber = 0
        if fila["haber"]:
            haber = fila["haber"]
        debe = 0
        if fila["debe"]:
            debe = fila["debe"]
        saldo = saldo +  haber - debe
        sum_debe = sum_debe + debe
        sum_haber = sum_haber + haber
        tracsv.writerow({"No":str(fila['id']), 
                         'Fecha':funciones.mysql_a_fecha(fila['fecha']),
            "Detalle":fila['detalle'], "Debe":funciones.moneda(debe),
            'Haber':funciones.moneda(haber),
            'Saldo':funciones.moneda(saldo)})
    tracsv.writerow({"No":"", 'Fecha':"",
        "Detalle":"Total", "Debe":funciones.moneda(sum_debe),
        'Haber':funciones.moneda(sum_haber),
        'Saldo':funciones.moneda(saldo)})
    filename = "bancos.csv"
    HEADERS = '\r\n'.join([
        "Content-type: %s;",
        "Content-Disposition: attachment; filename=%s",
        "Content-Title: %s",
        "Content-Length: %i",
        "\r\n", # empty line to end headers
        ])
    length = len(salida.getvalue())
    print(HEADERS % ('text/csv', filename, filename, length))
    print(salida.getvalue())
    salida.close()
def main():
    """Principal"""
    form = cgi.FieldStorage()
    accion = form.getvalue('accion', 'listado')
    if accion == 'listado':
        listado(form)
    elif accion == 'exportar':
        exportar()
if __name__ == "__main__":
    main()
    
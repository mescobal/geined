#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Programa para conciliaciones de transacciones
import cgitb; cgitb.enable()
import cgi
import datos
import htm
import funciones
import csv
import StringIO
import pagina
def nueva():
    """ Crear la tabla borrando la previa si existe"""
    # BDD
    dat = datos.Datos()
    sql = 'SELECT id,CONCAT(rubro,"-",nombre) as selec FROM cuentas'
    dat.cursor.execute(sql)
    resultado = dat.cursor.fetchall()   
    # Pagina
    pag = pagina.Pagina("Llenar tabla de conciliacion", 4)
    htm.encabezado("Llenar tabla de conciliación", "Contabilidad", "geined.py?accion=contabilidad")
    print("<div class='barra'>")
    print("Llenar una nueva tabla de conciliación implica perder la anterior.")
    print("</div>")
    htm.form_edicion("Crear tabla", "conciliacion.py")
    print(htm.hidden('accion', 'llenar'))
    htm.input_combo('Cuenta:', 'cuenta_id', resultado, ['id', 'selec'], 'Seleccionar...')
    htm.botones("conciliacion.py?accion=listado")
    htm.form_edicion_fin()
    pag.fin()
def llenar(frm):
    """ Llenar con datos de un rubro en particular"""
    cuenta_id = frm.getvalue("cuenta_id")
    # BDD
    conciliacion = datos.Tabla("conciliacion")
    transacciones = datos.Tabla("transacciones")
    conciliacion.borrar_tabla()
    transacciones.filtro = "cuenta_id = " + str(cuenta_id)
    transacciones.filtrar()
    for fila in transacciones.resultado:
        conciliacion.nuevo()
        conciliacion.registro["id_id"] = fila["id"]
        conciliacion.registro["fecha"] = fila["fecha"]
        conciliacion.registro["detalle"] = fila["detalle"]
        conciliacion.registro["cuenta_id"] = fila["cuenta_id"]
        conciliacion.registro["debe"] = fila["debe"]
        conciliacion.registro["haber"] = fila["haber"]
        conciliacion.insertar()
def listado(frm):
    """ Desplegar listado"""
    # Recuperar variables
    cuenta_id = frm.getvalue('cuenta_id')
    # BDD
    cuentas = datos.Tabla("cuentas")
    conciliacion = datos.Tabla("conciliacion")
    sql = "SELECT sum(debe) as debe, sum(haber) as haber from conciliacion"
    dat = datos.Datos()
    dat.cursor.execute(sql)
    resultado = dat.cursor.fetchone()
    # Buscar
    cuentas.ir_a(cuenta_id)
    # Pagina
    pag = pagina.Pagina("Conciliación de cuentas", 4)
    print(htm.encabezado("Conciliación de cuentas", "Contabilidad", "geined.py?accion=contabilidad"))
    print("<div class='barra'>")
    print("Conciliación de: " + str(cuentas.registro["rubro"]) + " - " + cuentas.registro["nombre"])
    filas_por_pagina = 20
    pagina_actual = frm.getvalue("pagina", 1)
    off_set = (int(pagina_actual) - 1) * filas_por_pagina
    tot_debe = resultado["debe"]
    tot_haber = resultado["haber"]
    tot_saldo = tot_haber - tot_debe
    print("<table class='barra'>" + 
        htm.tr(htm.th("Debe") + htm.th("Haber") + htm.th("Saldo")) +
        htm.tr(
            htm.td(funciones.moneda(tot_debe), "right") +
            htm.td(funciones.moneda(tot_haber), "right") +
            htm.td(funciones.moneda(tot_saldo), "right")) + 
        "</table>")
    total_filas = conciliacion.num_filas
    #total_paginas = total_filas / filas_por_pagina
    if frm.has_key('mostrar'):
        if frm['mostrar'] == 'no':
            mostrar='no'
            print(htm.button('Mostrar', "conciliacion.py?accion=listado&cuenta_id=" + str(cuenta_id) + "&mostrar=si"))
            conciliacion.filtro = "conciliacion.check IS NULL"
            conciliacion.filtrar()
            total_filas = conciliacion.num_filas
            conciliacion.limite = str(off_set) + "," +str(filas_por_pagina)
            conciliacion.orden = "fecha"
            conciliacion.filtrar()
        else:
            mostrar='si'
            print(htm.button('Ocultar', "conciliacion.py?accion=listado&cuenta_id=" + str(cuenta_id) + "&mostrar=no"))
            conciliacion.filtro = ""
            conciliacion.filtrar()
            total_filas = conciliacion.num_filas
            conciliacion.limite = str(off_set) + "," + str(filas_por_pagina)
            conciliacion.orden = "fecha"
            conciliacion.filtrar()
    else:
        mostrar='no'
        print(htm.button('Mostrar', "conciliacion.py?accion=listado&cuenta_id=" + str(cuenta_id) + "&mostrar=no"))
        conciliacion.filtro = " conciliacion.check is null"
        conciliacion.filtrar()
        conciliacion.limite = str(off_set) + "," + str(filas_por_pagina)
        conciliacion.orden = "fecha"
        conciliacion.filtrar()
    print(htm.button('Nueva tabla', "conciliacion.py?accion=nueva&cuenta_id=" + str(cuenta_id)))
    print(htm.button('Exportar a planilla',
        "conciliacion.py?accion=exportar&cuenta_id=" + str(cuenta_id) + "&mostrar=" + mostrar))
    htm.formulario('conciliacion.py?accion=actualizar')
    print(htm.hidden('mostrar', mostrar))
    print(htm.hidden('pagina', str(pagina_actual)))
    print(htm.hidden('cuenta_id', cuenta_id))
    total_paginas = total_filas / filas_por_pagina
    off_set = (int(pagina_actual) - 1) * filas_por_pagina
    i = 0
    saldo = 0
    htm.encabezado_tabla(['Nº', 'Fecha', 'Detalle', 'Debe', 'Haber', 'Marca', 'Saldo'])
    for fila in conciliacion.resultado:
        print("<tr class='fila_datos'>")
        saldo = saldo + fila["debe"] - fila["haber"]
        adicional = ""
        if fila["check"]:
            adicional = "checked"
        print(htm.td(fila["id_id"]) +
            htm.td(funciones.mysql_a_fecha(fila["fecha"])) +
            htm.td(fila["detalle"]) +
            htm.td(funciones.moneda(fila["debe"])) +
            htm.td(funciones.moneda(fila["haber"])) +
            htm.td("<input type='checkbox' name='check_" + str(i) + "' value='1' " + adicional + ">") +
            htm.hidden("campo_" + str(i), str(fila["id"])) +
            htm.td(funciones.moneda(saldo), "right"))
        print('</tr>')
        i = i + 1
    htm.fin_tabla()
    print(htm.submit('Actualizar'))
    htm.fin_formulario()
    htm.navegador("conciliacion.py?accion=listado&cuenta_id=" + str(cuenta_id) + "&mostrar=" + mostrar, pagina_actual, total_paginas)
    print(htm.button('Volver', 'geined.py?accion=contabilidad'))
    pag.fin()
def actualizar(frm):
    conciliacion = datos.Tabla("conciliacion")
    for i in range(0, 19):
        ident = frm.getvalue("campo_" + str(i))
        check_valor = frm.getvalue("check_" + str(i))
        if int(ident) > 0:
            conciliacion.ir_a(ident)
            conciliacion.registro["check"] = check_valor
            conciliacion.actualizar()
def exportar(frm):
    """Exportar datos de conciliación"""
    # Recuperar variables
    cuenta_id = frm.gevalue('cuenta_id')
    # Bases de datos
    cuentas = datos.Tabla("cuentas")
    conciliacion = datos.Tabla("conciliacion")
    # Variables
    archivo = StringIO.StringIO()
    # Buscar
    cuentas.ir_a(cuenta_id)
    nom_archivo = "Conciliacion_" + cuentas.registro["rubro"] + ".csv"
    if frm.has_key('mostrar'):
        if frm['mostrar'] == 'no':
            #mostrar='no'
            conciliacion.filtro = "conciliacion.check IS NULL"
            conciliacion.orden = "fecha"
            conciliacion.filtrar()
        else:
            #mostrar='si'
            conciliacion.orden = "fecha"
    else:
        #mostrar='no'
        conciliacion.filtro = "conciliacion.check IS NULL"
        conciliacion.orden = "fecha"
    saldo = 0
    sum_debe =0
    sum_haber = 0
    conccsv = csv.DictWriter(archivo, ["No", "Fecha", "Detalle", "Debe", "Haber", "Saldo"])
    for fila in conciliacion.resultado:
        saldo = saldo +  fila["haber"] - fila["debe"]
        sum_debe = sum_debe + fila["debe"]
        sum_haber = sum_haber + fila["haber"]
        conccsv.writerow({"No":str(fila['id']), 'Fecha':funciones.mysql_a_fecha(fila['fecha']),
            "Detalle":fila['detalle'], "Debe":funciones.moneda(fila["debe"]),
            'Haber':funciones.moneda(fila["haber"]),
            'Saldo':funciones.moneda(saldo)})
    conccsv.writerow({"No":"", 'Fecha':"",
        "Detalle":"Total", "Debe":funciones.moneda(sum_debe),
        'Haber':funciones.moneda(sum_haber),
        'Saldo':funciones.moneda(saldo)})
    filename = nom_archivo
    HEADERS = '\r\n'.join([
        "Content-type: %s;",
        "Content-Disposition: attachment; filename=%s",
        "Content-Title: %s",
        "Content-Length: %i",
        "\r\n", # empty line to end headers
        ])
    length = len(archivo.getvalue())
    print(HEADERS % ('text/csv', filename, filename, length))
    print(archivo.getvalue())
    archivo.close()
def main():
    """PRincipal"""
    form = cgi.FieldStorage()
    accion = form.getvalue("accion", "listado")
    conciliacion = datos.Tabla("conciliacion")
    conciliacion.filtrar()
    if accion == "listado":
        # Si no hay filas en conciliacion
        if conciliacion.num_filas == 0:
            nueva()
        else:
            if form.has_key('cuenta_id'):
                # Si hay una cuenta
                listado(form)
            else:
                # Si no hay una cuenta, toma la primera cuenta del registro
                cta = conciliacion.registro["cuenta_id"]
                htm.inicio()
                print(htm.redirigir("conciliacion.py?accion=listado&cuenta_id=" + str(cta)))
    elif accion == 'actualizar':
        actualizar(form)
        listado(form)
    elif accion == 'llenar':
        llenar(form)
        listado(form)
    elif accion == 'nueva':
        nueva()
    elif accion == 'exportar':
        exportar(form)
    else:
        listado(form)

if __name__ == "__main__":
    main()
    
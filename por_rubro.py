#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Manejo de transacciones por rubro"""
import cgi
import cgitb; cgitb.enable()
import funciones
import datos
import pagina
import htm
import StringIO
import csv
import xlwt


def listado(frm):
    """Listado por rubro"""
    # Parámetros:
    # busqueda: id de la transacción, 0 por defecto
    # orden: fecha o id (cadena)
    # recuperar variables:
    busqueda = frm.getvalue("busqueda", "0")
    orden = frm.getvalue("orden", "")
    # Bases de datos
    sql = 'SELECT id,CONCAT(rubro," ", nombre) AS referencia '
    sql = sql + 'FROM cuentas ORDER BY rubro'
    dat = datos.Datos()
    dat.cursor.execute(sql)
    cuentas = dat.cursor.fetchall()
    plancta = datos.Tabla("cuentas")
    transacciones = datos.Tabla("transacciones")
    # Pagina
    pag = pagina.Pagina('Listado por rubro', 4)
    print(htm.encabezado("Listado por rubro", "Contabilidad", 
                         "geined.py?accion=contabilidad"))
    htm.formulario('por_rubro.py')
    print("<table class='tabla_barra'><tr>")
    print(htm.td(htm.boton("Exportar CSV",
        "por_rubro.py?accion=exportar&busqueda=" +\
        busqueda + "&orden=" + orden)))
    print(htm.td(htm.boton("Exportar Planilla",
        "por_rubro.py?accion=exportar_excel&busqueda=" +\
        busqueda + "&orden=" + orden)))
    print(htm.td('Busqueda:'))    
    print("<td><select name='busqueda' id='busqueda'>")
    for fila in cuentas:
        if busqueda == str(fila['id']):
            print("<option value='" + str(fila["id"]) + \
                "' selected='selected'>" + fila["referencia"] + "</option>")
        print("<option value='" + str(fila["id"]) + "'>" + fila["referencia"] +\
            "</option>")
    print('</select></td>')
    print(htm.td(' Orden: ') +
      htm.td('<input type="radio" name="orden" value="fecha" checked />Fechas') +
      htm.td('<input type="radio" name="orden" value="ingreso" />Ingreso ') +
      htm.td(htm.submit('Buscar')))
    print('</tr></table>')
    htm.fin_formulario()
    if busqueda == "0":
        cuenta_id = 0
        cartel_rubro = '0'
        cartel_nombre = 'Rubro sin asignar'
    else:
        cuenta_id = busqueda
        plancta.ir_a(cuenta_id)
        cartel_rubro = plancta.registro["rubro"]
        cartel_nombre = plancta.registro["nombre"]
    transacciones.filtro = "cuenta_id=" + str(cuenta_id)
    if orden != "":
        if orden == 'ingreso':
            transacciones.orden = "id"
        else:
            transacciones.orden = "fecha"
    transacciones.filtrar()
    saldo = 0
    print(htm.h2("Rubro: " + str(cartel_rubro) + " - " + cartel_nombre))
    htm.encabezado_tabla(['Nº', 'Fecha', 'Detalle', 'Debe', 'Haber', 'Saldo', 
                          'Acciones'])
    for fila in transacciones.resultado:
        htm.fila_resaltada()
        saldo = saldo + fila["haber"] - fila["debe"]
        print(htm.td(str(fila["id"])) +
            htm.td(funciones.mysql_a_fecha(fila["fecha"])) +
            htm.td(fila["detalle"]) +
            htm.td(funciones.moneda(fila["debe"]), "right") +
            htm.td(funciones.moneda(fila["haber"]), "right") +
            htm.td(funciones.moneda(saldo), "right"))
        print("<td align='center'>")
        htm.boton_editar("por_rubro.py?accion=editar&id=" + str(fila["id"]) + \
            "&busqueda=" + busqueda + "&orden=" + orden)
        print('</td>')
    htm.fin_tabla()
    pag.fin()
def editar(frm):
    """Edición de transacciones"""
    # recuperar variables
    busqueda = frm.getvalue("busqueda", "0")
    orden = frm.getvalue("orden", "fecha")
    # pagina
    pag = pagina.Pagina("Editar transaccion", 4,  fecha=1)
    ident = frm.getvalue('id')
    transacciones = datos.Tabla('transacciones')
    transacciones.ir_a(ident)
    sql = 'SELECT id,CONCAT(rubro," ", nombre) AS referencia FROM cuentas WHERE nivel=0 ORDER BY rubro'
    dat = datos.Datos()
    dat.cursor.execute(sql)
    cuentas = dat.cursor.fetchall()
    # cuentas.ir_a(transacciones.registro["cuenta_id"])
    htm.form_edicion("Edición de transacción", "por_rubro.py?accion=actualizar")
    # htm.campo_oculto('accion', 'actualizar')
    htm.campo_oculto("id", ident)
    htm.campo_oculto("busqueda", busqueda)
    htm.campo_oculto('orden', orden)
    htm.input_fecha('Fecha:', 'fecha', transacciones.registro['fecha'])
    htm.input_texto('Detalle:', 'detalle', transacciones.registro['detalle'])
    htm.input_combo('Rubro:', 'cuenta_id', cuentas, ["id", "referencia"], 
                    transacciones.registro['cuenta_id'])
    htm.input_numero('Debe:', 'debe', transacciones.registro['debe'])
    htm.input_numero('Haber:', 'haber', transacciones.registro['haber'])
    htm.botones("por_rubro.py?accion=listado&busqueda=" + busqueda +\
        "&orden=" + orden)
    htm.form_edicion_fin()
    pag.fin()
def actualizar(frm):
    """Actualizar datos de transacciones"""
    # recuperar variables: no es necesario, vienen en FRM
    # base de datos
    transaccion = datos.Tabla('transacciones')
    transaccion.ir_a(frm.getvalue('id'))
    transaccion.registro['fecha'] = funciones.fecha_a_mysql(frm.getvalue('fecha'))
    transaccion.registro['detalle'] = frm.getvalue('detalle')
    transaccion.registro['cuenta_id'] = frm.getvalue('cuenta_id')
    transaccion.registro['debe'] = float(frm.getvalue('debe'))
    transaccion.registro['haber'] = frm.getvalue('haber')
    transaccion.actualizar()
    listado(frm)
def exportar(frm):
    """Exportación a CSV"""
    # Recuperar variables
    busqueda = frm.getvalue("busqueda", "0")
    orden = frm.getvalue("orden", "fecha")
    # Seteo de variables
    salida = StringIO.StringIO()            
    expcsv = csv.DictWriter(salida, ["Fecha", "Detalle", "Debe", 
                                     "Haber", "Saldo"])
    # Datos
    transacciones = datos.Tabla("transacciones")
    transacciones.orden = orden
    transacciones.filtro = 'cuenta_id=' + busqueda
    transacciones.filtrar()
    cuentas = datos.Tabla("cuentas")
    cuentas.ir_a(busqueda)
    rubro = str(cuentas.registro["rubro"])
    filename = "rubro_" + rubro + ".csv"
    expcsv.writeheader()         
    saldo = 0
    for fila in transacciones.resultado:
        saldo = saldo + fila['haber'] - fila ['debe']
        expcsv.writerow({"Fecha":funciones.mysql_a_fecha(fila["fecha"]), 
                         "Detalle":fila['detalle'], "Debe": fila['debe'], 
                        "Haber":fila['haber'], "Saldo":saldo})
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
    listado(frm)


def exportar_excel(frm):
    """Exportar planilla electrónica formateada"""
    # Recuperar variables
    busqueda = frm.getvalue("busqueda", "0")
    orden = frm.getvalue("orden", "fecha")
    # Datos
    transacciones = datos.Tabla("transacciones")
    transacciones.orden = orden
    transacciones.filtro = 'cuenta_id=' + busqueda
    transacciones.filtrar()
    cuentas = datos.Tabla("cuentas")
    cuentas.ir_a(busqueda)
    rubro = str(cuentas.registro["rubro"])
    filename = "rubro_" + rubro + ".xls"
    salida = StringIO.StringIO()    
    
    workbook = xlwt.Workbook()
    worksheet = workbook.add_sheet("Por rubro")
    # Add headings with styling and froszen first row
    heading_xf = xlwt.easyxf('font: bold on; align: wrap on, vert centre, horiz center')
    headings = ['Fecha', 'Detalle', 'Debe', 'Haber', "Saldo"]
    rowx = 0
    worksheet.set_panes_frozen(True) # frozen headings instead of split panes
    worksheet.set_horz_split_pos(rowx+1) # in general, freeze after last heading row
    worksheet.set_remove_splits(True) # if user does unfreeze, don't leave a split there
    for colx, value in enumerate(headings):
        worksheet.write(rowx, colx, value, heading_xf)
    # for i, row in enumerate(DATA):
    saldo = 0
    for i, row in enumerate(transacciones.resultado):
        worksheet.write(i+1, 0, row["fecha"])
        worksheet.write(i+1, 1, row["detalle"])
        worksheet.write(i+1, 2, row["debe"])
        worksheet.write(i+1, 3, row["haber"])
        saldo = saldo + row["debe"] - row["haber"]
        worksheet.write(i+1, 4, saldo)
    workbook.save(salida)
    tamano = len(salida.getvalue())
    headers = '\r\n'.join([
        "Content-type: %s;",
        "Content-Disposition: attachment; filename=%s",
        "Content-Title: %s",
        "Content-Length: %i",
        "\r\n", # empty line to end headers
        ])
    print(headers % ('application/msexcel', filename, filename, tamano)),
    print(salida.getvalue())
    salida.close()
    listado(frm)
    
def main():
    """Principal"""
    form = cgi.FieldStorage()
    accion = form.getvalue("accion", "listado")
    if accion == "listado":
        listado(form)
    elif accion == "exportar":
        exportar(form)
    elif accion == 'editar':
        editar(form)
    elif accion == 'actualizar':
        actualizar(form)
    elif accion == "exportar_excel":
        exportar_excel(form)
    else:
        listado(form)

if __name__ == "__main__":
    main()

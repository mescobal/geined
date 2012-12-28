#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Menu principal"""
import cgi
import cgitb; cgitb.enable()
import funciones
import datos
import htm
import pagina
def listado(frm):
    """Listado de transacciones"""
    pag = pagina.Pagina("Listado de transacciones", 4)
    print(htm.encabezado("Listado de transacciones", "Contabilidad", 
        "geined.py?accion=contabilidad"))
    print("<table class='barra'>")
    htm.formulario("transacciones.py")
    print("<tr><td>")
    print("Buscar:")
    htm.input_input("text", "busqueda")
    print("</td><td>")
    print("Desde:")
    htm.input_input("text", "desde")
    print("</td><td>")
    print("Limite:")
    htm.input_input("text", "limite", "20")
    print("</td><td>")
    print(htm.submit("Buscar"))
    htm.fin_formulario()
    print '</td>'
    print(htm.td(htm.button("Nuevo", "transacciones.py?accion=nuevo")))
    print(htm.td(htm.button("Doble entrada","den.php?accion=nuevo")))
    print('</tr>')
    print('</table>')
    # sql_sum = "SELECT SUM(debe) AS d, SUM(haber) AS h FROM transacciones"
    # sumas = Transaccion.find_by_sql(sql_sum)
    dat = datos.Datos()
    sql = "SELECT sum(haber) as haber FROM transacciones"
    dat.cursor.execute(sql)
    registro = dat.cursor.fetchone()
    haber = registro['haber']
    if haber == None:
        haber = 0
    sql = "SELECT sum(debe) as debe FROM transacciones"
    dat.cursor.execute(sql)
    registro = dat.cursor.fetchone()
    debe = registro['debe']
    if debe == None:
        debe = 0
    print("<table class='barra'><tr><td>Total debe:  " + funciones.moneda(debe) + "</td><td>")
    print("Total haber: " + funciones.moneda(haber) + "</td><td>")
    print("Saldo      : " + funciones.moneda(haber - debe) + "</td></tr></table>")
    #cargar datos
    busqueda = frm.getvalue('busqueda')
    desde = frm.getvalue('desde')
    limite = " LIMIT " + frm.getvalue("limite", "20")
    condicion = ""
    orden = " ORDER BY id"
    sql = 'SELECT * FROM transacciones ' + orden + limite
    if frm.has_key('busqueda'):
        cond1 = '(detalle LIKE "%' + busqueda + '%")'
        cond2 = '(debe LIKE "%' + busqueda + '%")'
        cond3 = '(haber LIKE "%' + busqueda + '%")'
        condicion = cond1 + ' OR ' + cond2 + ' OR ' + cond3 + ' '
        htm.h3("Filtrando por : " + busqueda)
        sql = 'SELECT * FROM transacciones WHERE ' + condicion + orden + limite
    if frm.has_key('desde'):
        if frm.getvalue('desde') > 0:
            desde = frm.getvalue('desde')
        else:
            desde = 1
        a_partir_de = ' id >=' + str(desde)
        htm.h3("Listando desde asiento Nº: " + str(desde))
        sql = 'SELECT * FROM transacciones WHERE ' + a_partir_de + orden + limite
    if (frm.has_key('busqueda') and frm.has_key('desde')):
        condicion = '(' + condicion + ") AND (" + a_partir_de + ')'
        sql = 'SELECT * FROM transacciones WHERE ' + condicion + orden + limite
    dat = datos.Datos()
    dat.cursor.execute(sql)
    transacciones = dat.cursor.fetchall()
    htm.encabezado_tabla(["Nº", "Fecha", 
        "Detalle", "Cuenta", "Debe", "Haber", "Saldo", "Acciones"])
    saldo = 0
    cuentas = datos.Tabla('cuentas')
    for fila in transacciones:
        print("<tr class='fila_datos'>")
        print(htm.td(fila["id"]))
        print(htm.td(funciones.mysql_a_fecha(fila["fecha"])))
        print(htm.td(fila["detalle"]))
        # Cuenta
        cuentas.ir_a(fila['cuenta_id'])
        print(htm.td(cuentas.registro['rubro']))
        print(htm.td(funciones.moneda(fila['debe']), "rigth"))
        print(htm.td(funciones.moneda(fila['haber']), "right"))
        saldo = saldo + fila['debe'] - fila['haber']
        print(htm.td(funciones.moneda(saldo), "right"))
        print('<TD>')
        #if fila.documento_id == nil
        #    boton_editar("transacciones.py?accion=editar&id=#{fila.id}")
        #end
        # Modificación transitoria para permitir que Adriana arregle cosas!!!!!
        htm.boton_editar("transacciones.py?accion=editar&id=" + str(fila["id"]))
        htm.boton_eliminar("transacciones.py?accion=eliminar&id=" + str(fila["id"]))
        print('</td></tr>')
    htm.fin_tabla()
    pag.fin()
def editar(frm):
    """Edición de transacciones"""
    pag = pagina.Pagina("Editar transaccion", 4,  fecha=1)
    ident = frm.getvalue('id')
    transacciones = datos.Tabla('transacciones')
    transacciones.ir_a(ident)
    sql = 'SELECT id,CONCAT(rubro," ", nombre) AS referencia FROM cuentas ORDER BY rubro'
    dat = datos.Datos()
    dat.cursor.execute(sql)
    cuentas = dat.cursor.fetchall()
    # cuentas.ir_a(transacciones.registro["cuenta_id"])
    htm.form_edicion("Edición de transacción", "transacciones.py?accion=actualizar")
    # htm.campo_oculto('accion', 'actualizar')
    htm.campo_oculto("id", ident)
    htm.input_fecha('Fecha:', 'fecha', transacciones.registro['fecha'])
    htm.input_texto('Detalle:', 'detalle', transacciones.registro['detalle'])
    htm.input_combo('Rubro:', 'cuenta_id', cuentas, ["id", "referencia"], 
                    transacciones.registro['cuenta_id'])
    htm.input_numero('Debe:', 'debe', transacciones.registro['debe'])
    htm.input_numero('Haber:', 'haber', transacciones.registro['haber'])
    htm.botones('transacciones.py?accion=listado')
    htm.form_edicion_fin()
    pag.fin()
def actualizar(frm):
    """Actualizar datos de transacciones"""
    transaccion = datos.Tabla('transacciones')
    transaccion.ir_a(frm.getvalue('id'))
    transaccion.registro['fecha'] = funciones.fecha_a_mysql(frm.getvalue('fecha'))
    transaccion.registro['detalle'] = frm.getvalue('detalle')
    transaccion.registro['cuenta_id'] = frm.getvalue('cuenta_id')
    transaccion.registro['debe'] = float(frm.getvalue('debe'))
    transaccion.registro['haber'] = frm.getvalue('haber')
    transaccion.actualizar()
    listado(frm)
def nuevo():
    """Nuevo registro de transacciones"""
    pag = pagina.Pagina("Nueva transaccion", 4, fecha=1)
    sql = 'SELECT id,CONCAT(rubro," ", nombre) as referencia FROM cuentas ORDER BY rubro'
    dat = datos.Datos()
    dat.cursor.execute(sql)
    cuentas = dat.cursor.fetchall()
    htm.form_edicion("Nueva transacción", "transacciones.py?accion=agregar")
    htm.input_fecha('Fecha:', 'fecha', funciones.fecha_a_mysql(funciones.hoy()))
    htm.input_texto('Detalle:', 'detalle', '')
    htm.input_combo('Rubro:', 'cuenta_id', cuentas, ["id", "referencia"], '')
    htm.input_numero('Debe:', "debe", 0)
    htm.input_numero('Haber:', "haber", 0)
    htm.botones('transacciones.py?accion=listado')
    htm.form_edicion_fin()
    pag.fin()
def agregar(frm):
    """ Rutina para agregar datos nuevos a transacciones"""
    transaccion = datos.Tabla('transacciones')
    transaccion.nuevo()
    transaccion.registro['fecha'] = funciones.fecha_a_mysql(frm.getvalue('fecha'))
    transaccion.registro['detalle'] = frm.getvalue('detalle')
    transaccion.registro['cuenta_id'] = frm.getvalue('cuenta_id')
    transaccion.registro['debe'] = frm.getvalue('debe')
    transaccion.registro['haber'] = frm.getvalue('haber')
    transaccion.registro['documento_id'] = 0
    transaccion.insertar()
    listado(frm)
def eliminar(frm):
    """Eliminar transaccion"""
    transaccion = datos.Tabla('transacciones')
    transaccion.borrar(frm.getvalue('id'))
    listado(frm)
    
if __name__ == "__main__":
    form = cgi.FieldStorage()
    accion = form.getvalue("accion", "listado")
    if accion == 'listado':
        listado(form)
    elif accion == 'editar':
        editar(form)
    elif accion == 'actualizar':
        actualizar(form)
    elif accion == 'nuevo':
        nuevo()
    elif accion == 'agregar':
        agregar(form)
    elif accion == 'eliminar':
        eliminar(form)
    else:
        listado(form)

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Liquidaciones de sueldos"""
import cgi
import cgitb; cgitb.enable()
import funciones
import datos
import pagina
import htm
def listado():
    """Listado de liquidaciones de sueldos"""
    # Recuperar variables
    # Bases de datos
    liquidacion = datos.Tabla("liquidacion")
    variables = datos.Tabla("variables")
    salario = datos.Tabla("salario")
    # Busquedas
    liquidacion.orden = "fecha DESC"
    liquidacion.filtrar()
    # Pagina
    pag = pagina.Pagina("Listado de liquidaciones de sueldos", 4)
    print(htm.encabezado("Listado de liquidaciones de sueldos", "Sueldos", "geined.py?accion=sueldos"))
    print("<div class='barra'>" + htm.boton("Nuevo", "liq.py?accion=nuevo") + "</div>")
    htm.encabezado_tabla(["Nº", "Fecha", "Variables", "Salarios",
                          "Corresponde a:", "Líquido", "BPS", "DGI", "Acciones"])
    for fila in liquidacion.resultado:
        print("<tr class='fila_datos'>")
        ident = fila["id"]
        print(htm.td(ident))
        print(htm.td(funciones.mysql_a_fecha(fila["fecha"])))
        variables_id = fila["variables_id"]
        salario_id = fila["salario_id"]
        variables.ir_a(variables_id)
        print(htm.td(funciones.fecha_a_mysql(variables.registro["fecha"])))
        salario.ir_a(salario_id)
        print(htm.td(funciones.fecha_a_mysql(salario.registro["fecha"])))
        print(htm.td(fila["corresponde"]))
        print(htm.td(funciones.moneda(fila["liquido"]), "right"))
        print(htm.td(funciones.moneda(fila["BPS"]), "right"))
        print(htm.td(funciones.moneda(fila["DGI"]), "right"))
        print("<td>")
        htm.boton_detalles("liq_ver.py?accion=listado&liquidacion_id=" + str(ident))
        htm.boton_editar("liq.py?accion=editar&id=" + str(ident))
        htm.boton_eliminar("liq.py?accion=eliminar&id=" + str(ident))
        print('</td></tr>')
    htm.fin_tabla()
    print(htm.button('Volver', 'geined.py?accion=sueldos'))
    pag.fin()
def nuevo():
    """Nueva liquidación de sueldos"""
    pag = pagina.Pagina("Nueva liquidación de sueldos", 4, fecha=1)
    htm.form_edicion("Nueva liquidacion", "liq.py?accion=agregar")
    htm.input_fecha('Fecha:', 'fecha', funciones.fecha_a_mysql(funciones.hoy()))
    htm.input_texto('Corresponde a:', 'corresponde','')
    htm.botones("liq.py?accion=listado")
    print("<div class='barra'>")
    htm.nota('Los valores de salario y aportes se calculan automáticamente en base a la fecha de la liquidación')
    htm.nota('Debe estar al día el archivo de variables y salarios.')
    print("</div>")
    htm.form_edicion_fin()
    pag.fin()
def agregar(frm):
    """Agregar una liquidación de sueldos"""
    # Bases de datos
    variables = datos.Tabla("variables")
    salario = datos.Tabla("salario")
    liquidacion = datos.Tabla("liquidacion")
    # Seleccionar segun fecha
    variables.filtro = "fecha <='" + funciones.fecha_a_mysql(frm.getvalue("fecha")) + "'"
    variables.orden = "fecha DESC"
    variables.filtrar()
    variables_id = variables.registro["id"]
    # buscar salarios
    salario.filtro = "fecha <='" + funciones.fecha_a_mysql(frm.getvalue("fecha")) + "'"
    salario.orden = "fecha DESC"
    salario.filtrar()
    salario_id = salario.registro["id"]    
    # insertar
    liquidacion.nuevo()
    liquidacion.registro["fecha"] = funciones.fecha_a_mysql(frm.getvalue("fecha"))
    liquidacion.registro["salario_id"] = salario_id
    liquidacion.registro["variables_id"] = variables_id
    liquidacion.registro["corresponde"] = frm.getvalue("corresponde")
    liquidacion.insertar()
    listado()
def editar(frm):
    """Editar una liquidacion"""
    pag = pagina.Pagina("Editar liquidación de sueldos", 4, fecha=1)
    htm.form_edicion("Edicion de sueldos", "liq.py?accion=actualizar")
    liq_id = frm.getvalue("id")
    liquidacion = datos.Tabla("liquidacion")
    liquidacion.ir_a(liq_id)
    htm.hidden("id", liq_id)
    htm.input_fecha('Fecha:', 'fecha', liquidacion.registro['fecha'])
    htm.input_texto('Corresponde a:', 'corresponde', liquidacion.registro['corresponde'])
    htm.botones("liq.py?accion=listado")
    htm.form_edicion_fin()
    htm.nota('Los valores de salario y aportes se calculan automáticamente en base a la fecha de la liquidación')
    htm.nota('Debe estar al día el archivo de variables y salarios.')
    print(htm.button('Volver', 'liq.py?accion=listado'))
    pag.fin()
def actualizar(frm):
    """Actualizar liquidación de sueldos"""
    # Seleccionar segun fecha
    variables = datos.Tabla("variables")
    variables.filtro = "fecha <='" + funciones.fecha_a_mysql(frm["fecha"]) + "'"
    variables.orden = "fecha DESC"
    variables.filtrar()
    variables_id = variables.registro["id"]
    salario = datos.Tabla("salario")
    salario.filtro = "fecha <= '" + funciones.fecha_a_mysql(frm["fecha"]) + "'"
    salario.orden = "fecha DESC"
    salario_id = salario.registro["id"]
    liquidacion = datos.Tabla("liquidacion")
    liquidacion.ir_a(frm["id"])
    liquidacion.registro["variables_id"] = variables_id
    liquidacion.registro["fecha"] = funciones.fecha_a_mysql(frm["fecha"])
    liquidacion.registro["variables_id"] = variables_id
    liquidacion.registro["salario_id"] = salario_id
    liquidacion.registro["corresponde"] = frm["corresponde"]
    liquidacion.actualizar()
    listado()    
def eliminar(frm):
    """Eliminar liquidacion"""
    detalle = datos.Tabla("det_liquidacion")
    detalle.filtro = "liquidacion_id=" + frm["id"]
    detalle.filtrar()
    for item in detalle.resultado:
        detalle.borrar(item["id"])
    liquidacion = datos.Tabla("liquidacion")
    liquidacion.borrar(frm["id"])
    listado()

if __name__ == "__main__":
    form = cgi.FieldStorage()
    accion = form.getvalue("accion", "listado")
    if accion == "listado":
        listado()
    elif accion == "nuevo":
        nuevo()
    elif accion == "agregar":
        agregar(form)
    elif accion == "editar":
        editar(form)
    elif accion == "actualizar":
        actualizar(form)
    elif accion == "eliminar":
        eliminar(form)

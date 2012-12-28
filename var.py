#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Menu principal"""
import cgi
import cgitb ; cgitb.enable()
import funciones
import datos
import htm
import datetime
import pagina
def listado():
    """listado de registro de Variables"""
    pag = pagina.Pagina("Listado de variables", 4)
    print(htm.encabezado("Listado de variables de sueldos", "Sueldos", "geined.py?accion=sueldos"))
    print(htm.div(
        htm.boton("Nuevo",'var.py?accion=nuevo'), clase="barra"))
    variables = datos.Tabla("variables")
    variables.orden = "fecha DESC"
    variables.filtrar()
    htm.encabezado_tabla(["Fecha", "Sal.Min", "BCP", "BPS", "DISSE", "FRL", "Acciones"])
    i = 0
    for fila in variables.resultado:
        print("<tr class='fila_datos'>")
        ident = str(fila["id"])
        print(htm.td(funciones.mysql_a_fecha(fila["fecha"])))
        print(htm.td(funciones.moneda(fila["sm"]), "right"))
        print(htm.td(funciones.moneda(fila["bcp"]), "right"))
        print(htm.td(str(funciones.numero(fila["bps"])) + " %", "right"))
        print(htm.td(str(funciones.numero(fila["disse"], 2)) + " %", "right"))
        print(htm.td(str(funciones.numero(fila["frl"], 3)) + " %", "right"))
        print("<td align=center>")
        htm.boton_editar("var.py?accion=editar&id=" + ident)
        htm.boton_eliminar("var.py?accion=eliminar&id="+ ident)
        print("</td></tr>")
        i = i + 1
    htm.fin_tabla()
    htm.button('Volver','geined.py?accion=sueldos')
    pag.fin()
def nuevo():
    """Formulario para nuevo registro de variables"""
    pag = pagina.Pagina("Nuevo conjunto de variables", 4, fecha=1)
    htm.form_edicion("Nuevas variables salariales",
        "var.py?accion=agregar")
    htm.input_fecha("Fecha:", "fecha",
        funciones.fecha_a_mysql(datetime.date.today().strftime("%d/%m/%y")))
    htm.input_numero("Salario mínimo:", "sm", "")
    htm.input_numero("BCP:", "bcp", "")
    htm.input_numero("BPS:", "bps", "")
    htm.input_numero("DISSE:", "disse", "")
    htm.input_numero("Fdo.Rec.Laboral:", "frl", "")
    htm.botones('var.py?accion=listado')
    htm.form_edicion_fin()
    pag.fin()
def agregar(frm):
    """Rutina para agregar un registro a Variables"""
    variables = datos.Tabla("variables")
    variables.registro["fecha"] = funciones.fecha_a_mysql(frm["fecha"].value)
    variables.registro["sm"] = frm["sm"].value
    variables.registro["bcp"] = frm["bcp"].value
    variables.registro["disse"] = frm["disse"].value
    variables.registro["frl"] = frm["frl"].value
    variables.insertar()
    listado()
def editar(frm):
    """Formulario para editar un registro de Variables"""
    variables = datos.Tabla("variables")
    variables.ir_a(frm["id"].value)
    pag = pagina.Pagina("Editar variables", 4, fecha=1)
    htm.form_edicion("Editando conjunto variables salariales",
        "var.py?accion=actualizar")
    htm.campo_oculto("id", frm["id"].value)
    htm.input_fecha("Fecha:", "fecha", variables.registro['fecha'])
    htm.input_numero("Salario mínimo:", "sm", variables.registro['sm'])
    htm.input_numero("BCP:", "bcp", variables.registro['bcp'])
    htm.input_numero("BPS:", "bps", variables.registro['bps'])
    htm.input_numero("DISSE", "disse", variables.registro['disse'])
    htm.input_numero("Fdo Rec Laboral:", "frl", variables.registro["frl"], 3)
    htm.botones('var.py?accion=listado')
    htm.form_edicion_fin()
    pag.fin()
def actualizar(frm):
    """Rutina para actualizar registro de Variables"""
    variables = datos.Tabla("variables")
    variables.ir_a(frm["id"].value)
    variables.registro["fecha"] = funciones.fecha_a_mysql(frm["fecha"].value)
    variables.registro["sm"] = frm["sm"].value
    variables.registro["bcp"] = frm["bcp"].value
    variables.registro["bps"] = frm["bps"].value
    variables.registro["disse"] = frm["disse"].value
    variables.registro["frl"] = frm["frl"].value
    variables.actualizar()
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
        pag_eli = pagina.Pagina("Eliminando datos", 4)
        variabs = datos.Tabla("variables")
        variabs.borrar(form["id"].value)
        htm.redirigir("var.py?accion=listado")
        pag_eli.fin()
    else:
        pagina.error_parametros("geined.py")
        print "Accion:" + form.getvalue("accion", "sin especificar")

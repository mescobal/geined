#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Manejo de valores salariales"""
import cgitb ; cgitb.enable()
import cgi
import funciones
import htm
import datos
import pagina
def listado():
    """Lista variables de salarios"""
    pag = pagina.Pagina("Listado de variales de salarios",  10)
    print(htm.encabezado("Listado de variables de salarios", "Sueldos",
                         "geined.py?accion=sueldos"))
    print(htm.div(htm.boton("Nuevo",  "sal.py?accion=nuevo") +
        'Nota: Ingresar solamente cuando hayan modificaciones salariales.' +
        'Consignar la fecha a partir de la cual es EFECTIVO el aumento', 
        clase="barra"))
    salario = datos.Tabla("salario")
    salario.orden = "fecha DESC"
    salario.filtrar()
    cat_empleados = datos.Tabla("cat_empleados")
    salario.orden = "fecha DESC"
    htm.encabezado_tabla(["Categoria", "Fecha", "Hora semanal", 
                          "Ficto semanal", "Accion"])
    for fila in salario.resultado:
        print("<tr class='fila_datos'>")
        cat_empleados.buscar("id", fila["cat_empleado_id"])
        print(htm.td(cat_empleados.registro["categoria"]) +
            htm.td(funciones.mysql_a_fecha(fila["fecha"])) +
            htm.td(funciones.moneda(fila["hora_semanal"]), "right") +
            htm.td(funciones.moneda(fila["ficto_semanal"]), "right"))
        print("<td align='center'>")
        htm.boton_editar("sal.py?accion=editar&id=" + str(fila["id"]))
        htm.boton_eliminar("sal.py?accion=eliminar&id=" + str(fila["id"]))
        print("</td></tr>")
    htm.fin_tabla()
    print(htm.button('Volver', 'geined.py?accion=administracion'))
    pag.fin()
def nuevo():
    """Nuevo grupo de valores salariales"""
    pag = pagina.Pagina("Nuevo grupo de valores salariales",  4, fecha = 1)
    cat_empleados = datos.Tabla("cat_empleados")
    cat_empleados.orden = "id ASC"
    cat_empleados.filtrar()
    htm.form_edicion("Nuevos valores salariales", "sal.py?accion=agregar")
    htm.input_combo("Categoría:", "cat_empleado_id", 
                    cat_empleados.resultado, ['id', 'categoria'], '')
    htm.input_fecha("Fecha:", "fecha", 
                    funciones.fecha_a_mysql(funciones.hoy()))
    htm.input_numero('Hora Semanal:', 'hora_semanal', 0)
    htm.input_numero('Ficto semanal:', 'ficto_semanal', 0)
    # htm.input_numero('Salario mensual:', 'mensual', 0)
    htm.botones('sal.py?accion=listado')
    htm.form_edicion_fin()
    pag.fin()
def agregar(frm):
    """Agregar datos de salario"""
    salario = datos.Tabla("salario")
    salario.nuevo()
    salario.registro["cat_empleado_id"] = frm["cat_empleado_id"].value
    salario.registro['fecha'] = funciones.fecha_a_mysql(frm['fecha'].value)
    salario.registro['hora_semanal'] = frm.getvalue('hora_semanal')
    salario.registro['ficto_semanal'] = frm.getvalue('ficto_semanal')
    # salario.registro['mensual'] = frm['mensual'].value
    salario.insertar()
    listado()
def editar(frm):
    """Editar valor salarial"""
    pag = pagina.Pagina("Edicion de valor salarial", 4, fecha = 1)
    # Bases de datos
    salario = datos.Tabla('salario')
    catemp = datos.Tabla('cat_empleados')
    salario.buscar('id', frm['id'].value)
    catemp.orden = "id ASC"
    catemp.filtrar()
    # Formulario
    htm.form_edicion("Edición de valores salariales", 
                     "sal.py?accion=actualizar")
    htm.campo_oculto("id", frm['id'].value)
    htm.input_combo("Categoría:", "cat_empleado_id", catemp.resultado, 
                    ['id', 'categoria'], salario.registro['cat_empleado_id'])
    htm.input_fecha("Fecha:", "fecha", salario.registro["fecha"])
    htm.input_numero("Hora semanal:", "hora_semanal", 
                     salario.registro["hora_semanal"])
    htm.input_numero("Ficto semanal:", "ficto_semanal", 
                     salario.registro["ficto_semanal"])
    # htm.input_numero("Salario mensual:", 
    # "mensual", salario.registro["mensual"])
    htm.botones('sal.py?accion=listado')
    htm.form_edicion_fin()
    pag.fin()
def actualizar(frm):
    """Actualizar valores salariales"""
    salarios = datos.Tabla("salario")
    salarios.buscar("id", frm['id'].value)
    salarios.registro["cat_empleado_id"] = frm["cat_empleado_id"].value
    salarios.registro["fecha"] = funciones.fecha_a_mysql(frm["fecha"].value)
    salarios.registro["hora_semanal"] = frm.getvalue("hora_semanal")
    salarios.registro["ficto_semanal"] = frm.getvalue("ficto_semanal")
    # salarios.registro["mensual"] = frm["mensual"].value
    salarios.actualizar()
    listado()
def eliminar(frm):
    """Eliminar un registro de salario"""
    salario = datos.Tabla("salario")
    salario.borrar(frm["id"].value)
    listado()
def main():
    """Principal"""
    form = cgi.FieldStorage()
    accion = "listado"
    if form.has_key("accion"):
        accion = form["accion"].value
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
if __name__ == "__main__":
    main()
    
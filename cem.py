#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Categoría de empleado"""
import cgi
import cgitb; cgitb.enable()
import datos
import pagina
import htm
def listado():
    """Listado de categorías de empleados"""
    pag = pagina.Pagina("Listado de categorías de empleados", 4)
    print(htm.encabezado("Listado de categorías de empleados", "Sistema", "geined.py?accion=sistema"))
    print("<div class='barra'>")
    print(htm.boton("Nuevo","cem.py?accion=nuevo"))
    print("</div>")
    cat_empleados = datos.Tabla("cat_empleados")
    cat_empleados.filtrar()
    htm.encabezado_tabla(["Nº", "Categoria", "Acciones"])
    for row in cat_empleados.resultado:
        print("<tr class='fila_datos'>")
        ident = row['id']
        print(htm.td(ident))
        print(htm.td(row['categoria']))
        print('<td>')
        htm.boton_detalles("cem.py?accion=ver&id=" + str(ident))
        htm.boton_editar("cem.py?accion=editar&id=" + str(ident))
        htm.boton_eliminar("cem.py?accion=eliminar&id=" + str(ident))
        print('</td>')
        print("</tr>")
    htm.fin_tabla()
    pag.fin()
    
def nuevo():
    """Nueva categoría de empleados"""
    pag = pagina.Pagina("Nueva categoría de empleado", 2)
    htm.form_edicion("Nueva categoría de empleado", "cem.py?accion=agregar")
    htm.input_texto("Categoria:", "categoria", "")
    htm.botones("cem.py?accion=listado")
    htm.form_edicion_fin()
    pag.fin()

def agregar(frm):
    """Agregar categoría de empleado"""
    cat_empleados = datos.Tabla("cat_empleados")
    cat_empleados.buscar("categoria", frm.getvalue("categoria"))
    if cat_empleados.encontrado:
        htm.duplicado("cem.py?accion=listado")
    else:
        cat_empleados.nuevo()
        cat_empleados.registro["categoria"] = frm.getvalue("categoria")
        cat_empleados.insertar()
        listado()
def editar(frm):
    """Editar categoría de empleado"""
    pag = pagina.Pagina("Edición de categoría de empleado", 2)
    htm.encabezado_tabla(["Campo", "Valor"])
    htm.formulario("cem.py?accion=actualizar")
    cat_empleados = datos.Tabla("cat_empleados")
    cat_empleados.ir_a(frm.getvalue("id"))
    print(htm.hidden("id", frm.getvalue("id")))
    htm.input_texto("Categoría:", "categoria", cat_empleados.registro['categoria'])
    htm.botones("cem.py?accion=listado")
    htm.fin_formulario()
    htm.fin_tabla()
    print(htm.button('Volver', 'cem.py?accion=listado'))
    pag.fin()
def actualizar(frm):
    """Actualizar datos de categoría de empleados"""
    ident = frm.getvalue("id")
    cat_empleados = datos.Tabla("cat_empleados")
    cat_empleados.ir_a(ident)
    cat_empleados.registro["categoria"] = frm.getvalue("categoria")
    cat_empleados.actualizar()
    listado()
def detalle(frm):
    """Detalle de categoría de empleados"""
    pag = pagina.Pagina("Detalles de categoría de empleado", 5)
    cat_empleados = datos.Tabla("cat_empelados")
    cat_empleados.ir_a(frm.getvalue("id"))
    print(htm.h2(cat_empleados.registro['categoria']))
    htm.encabezado_tabla(["Nombre", "CI", "Direccion", "Telefono", "eMail", "Ingreso", "Notas", "Acciones"])
    empleados = datos.Tabla("empleados")
    empleados.filtro = "categoria_id=" + str(frm.getvalue("id"))
    empleados.filtrar()
    i = 0
    for fila in empleados.resultado:
        htm.fila_alterna(i)
        print(htm.td(fila["nombre"]))
        print(htm.td(fila['ci']))
        print(htm.td(fila["direccion"]))
        print(htm.td(fila["telefono"]))
        print(htm.td(fila["email"]))
        print(htm.td(fila["ingreso"]))
        print(htm.td(fila["notas"]))
        print("<td>")
        htm.boton_detalles("emp_ver.php?id=" + str(fila['id']))
        print('</tr>')
    htm.fin_tabla()
    htm.button('Volver','cem.py?accion=listado')
    pag.fin()
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
        cat_empleados = datos.Tabla("cat_empleados")
        cat_empleados.borrar(form.getvalue("id"))
        listado()
    elif accion == 'ver':
        detalle(form)

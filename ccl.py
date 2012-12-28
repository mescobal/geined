#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Gestión de categorías de clientes"""
import cgitb; cgitb.enable()
import cgi
import datos
import htm
import pagina
def listado():
    """Listado de categorías de clientes"""
    pag = pagina.Pagina("Listado de categorías de clientes", 4)
    print(htm.button("Nuevo", "ccl.py?accion=nuevo"))
    cat_clientes = datos.Tabla("cat_clientes")
    cat_clientes.orden = "categoria"
    cat_clientes.filtrar()
    htm.encabezado_tabla(["Nº", "Categoria", "Acciones"])
    for fila in cat_clientes.resultado:
        print("<tr class='fila_datos'>")
        print(htm.td(fila["id"]))
        print(htm.td(fila["categoria"]))
        print("<td>")
        htm.boton_detalles("ccl_ver.php?accion=categoria&id=" +
            str(fila["id"]))
        htm.boton_editar("ccl.py?accion=editar&id=" + str(fila["id"]))
        htm.boton_eliminar("ccl.py?accion=eliminar&id=" + str(fila["id"]))
        print('</td></tr>')
    htm.fin_tabla()
    print(htm.button('Volver', 'geined.py?accion=sistema'))
    pag.fin()
def editar(frm):
    """Editar categoria de cliente"""
    ident = str(frm.getvalue("id"))
    cat_clientes = datos.Tabla("cat_clientes")
    cat_clientes.buscar("id", ident)
    pag = pagina.Pagina("Edición de categoría de clientes", 2)
    htm.form_edicion("Edición de categorías de clientes",
        "ccl.py?accion=actualizar")
    htm.campo_oculto('id', ident)
    htm.input_texto("Categoría:", "categoria",
        cat_clientes.registro['categoria'])
    htm.botones('ccl.py?accion=listado')
    htm.form_edicion_fin()
    pag.fin()
def nuevo():
    """Nueva categoria de clientes"""
    pag = pagina.Pagina("Categoría de clientes")
    htm.form_edicion("Nueva categoría de clientes", "ccl.py?accion=agregar")
    htm.input_texto("Categoría:", "categoria", '')
    htm.botones('ccl.py?accion=listado')
    htm.form_edicion_fin()
    pag.fin()
def actualizar(frm):
    """Actualizad datos en la BDD"""
    pag = pagina.Pagina("Actualizando", 20)
    ident = frm.getvalue("id")
    cat_clientes = datos.Tabla("cat_clientes")
    cat_clientes.buscar("id", ident)
    cat_clientes.registro["categoria"] = frm.getvalue("categoria")
    cat_clientes.actualizar()
    listado()
    listado()
    pag.fin()

def agregar(frm):
    """Agregar categoría de cliente"""
    pag = pagina.Pagina("Agregando datos", 20)
    cat_clientes = datos.Tabla("cat_clientes")
    cat_clientes.buscar("categoria", frm.getvalue("categoria"))
    if cat_clientes.encontrado:
        print(htm.h2("Ya existe una categoría con ese nombre"))
        print(htm.button("Volver", "ccl.py?accion=listado"))
    else:
        cat_clientes.registro["categoria"] = frm.getvalue("categoria")
        cat_clientes.insertar()
        print(htm.h2("Dato insertado"))
        listado()
    pag.fin()
def eliminar(frm):
    """Eliminar categoría de cliente"""
    # Modificar categorías de clientes a Null
    # OJO, tengo dificultades para asignar el valor NULL (None en python)
    # al campo categoria_id dentro de CLIENTES
    # queda como bug en launchpad
    clientes = datos.Tabla("clientes")
    clientes.filtro = "categoria_id=" + str(frm["id"].value)
    clientes.filtrar()
    cliente = datos.Tabla("clientes")
    #cliente.filtrar()
    # Esto es necesario porque sinó queda un registro sin cambiar!
    clientes.registro["categoria_id"] = None
    clientes.actualizar()
    for fila in clientes.resultado:       
        cliente.ir_a(fila["id"])
        cliente.registro["categoria_id"] = None
        cliente.actualizar()
    # Eliminar la categoría de clientes
    cat_clientes = datos.Tabla("cat_clientes")
    cat_clientes.borrar(frm.getvalue("id"))
    listado()
def main():
    """Rutina principal"""
    form = cgi.FieldStorage()
    accion = form.getvalue("accion", "listado")
    if accion == "listado":
        listado()
    elif accion == "editar":
        editar(form)
    elif accion == "actualizar":
        actualizar(form)
    elif accion == "nuevo":
        nuevo()
    elif accion == "agregar":
        agregar(form)
    elif accion == "eliminar":
        eliminar(form)
    else:
        listado()
if __name__ == "__main__":
    main()

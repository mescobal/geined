#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Gestión de balance comparativo"""
import cgi
import htm
import funciones
import datos
import pagina
def listado():
    """Listado de balance comparativo"""
    pag = pagina.Pagina('Balance comparativo', 3)
    print(htm.button('Nuevo', 'balcom.py?accion=nuevo'))
    print(htm.button('Volver', 'geined.py?accion=administracion'))
    htm.formulario('balcom.py')
    print(htm.hidden('accion', 'listado'))
    balcom = datos.Tabla("balcom")
    balcom.filtrar()
    htm.encabezado_tabla(["Item", "Ene", "Feb", "Mar", "Abr", "May",
        "Jun", "Jul", "Ago", "Set", "Oct", "Nov", "Dic", "Acciones"])
    i = 0
    for fila in balcom.resultado:
        htm.fila_alterna(i)
        ident = fila["id"]
        print(htm.td(fila["item"]))
        for mes  in funciones.meses:
            print(htm.td(funciones.moneda(fila[mes]), "right"))
        print('<td>')
        htm.boton_editar("balcom.py?accion=editar&id=" + str(ident))
        htm.boton_eliminar("balcom.py?accion=eliminar&id=" + str(ident))
        print('</td></tr>')
        i = i + 1
    htm.fin_tabla()
    print(htm.button('Volver', 'geined.py?accion=administracion'))
    pag.fin()
def nuevo():
    """Nuevo item en balance comparativo"""
    pag = pagina.Pagina('Balance comparativo', 5)
    htm.form_edicion('Nuevo item', 'balcom.py')
    print(htm.hidden('accion', 'agregar'))
    htm.input_texto("Item:", "item", "")
    for mes in funciones.meses:
        htm.input_texto(mes.capitalize() + ":", mes,"")
    htm.botones('balcom.py?accion=listado')
    htm.form_edicion_fin()
    print(htm.button("Volver", "balcom.py?accion=listado"))
    pag.fin()
def agregar(frm):
    """Agregar registro a balance comparativo"""
    balcom = datos.Tabla("balcom")
    balcom.nuevo()
    balcom.registro["item"] = frm.getvalue("item")
    for mes in funciones.meses:
        balcom.registro[mes] = frm.getvalue(mes)
    balcom.insertar()
    listado()
def editar(frm):
    """Editar item en balance comparativo"""
    pag = pagina.Pagina('Balance comparativo', 10)
    ident = frm.getvalue('id')
    balcom = datos.Tabla("balcom")
    balcom.ir_a(ident)
    htm.form_edicion('Edicion de item', 'balcom.py')
    print(htm.hidden('accion', 'actualizar'))
    print(htm.hidden('id', ident))
    htm.input_texto("Item:", "item", balcom.registro["item"])
    for mes in funciones.meses:
        htm.input_numero(mes.capitalize() + ":", mes, balcom.registro[mes])
    htm.botones('balcom.py?accion=listado')
    htm.form_edicion_fin()
    pag.fin()
def actualizar(frm):
    """Actualizar datos de balance comparativo"""
    balcom = datos.Tabla("balcom")
    balcom.ir_a(frm.getvalue("id"))
    balcom.registro["item"] = frm.getvalue('item')
    for mes in funciones.meses:
        balcom.registro[mes] = frm.getvalue(mes)
    balcom.actualizar()
    listado()
def eliminar(frm):
    """Eliminar item de balance comparativo"""
    balcom = datos.Tabla("balcom")
    balcom.borrar(frm.getvalue("id"))
    listado()    
if __name__ == "__main__":
    form = cgi.FieldStorage()
    accion = form.getvalue("accion", 'listado')
    if accion == 'listado':
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


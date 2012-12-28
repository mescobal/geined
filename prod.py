#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Manejo de Productos"""
import cgitb; cgitb.enable()
import cgi
import funciones
import datos
import pagina
import htm
def listado():
    """Listado de productos"""
    pag = pagina.Pagina("Listado de producotos", 4)
    print(htm.button("Nuevo","prod.py?accion=nuevo"))
    print(htm.button('Volver','geined.py?accion=administracion'))
    # cargar datos
    productos = datos.Tabla("productos")
    productos.orden = "producto"
    productos.filtrar()
    htm.encabezado_tabla(["Nº", "Producto", "Rubro", "Precio", "Acciones"])
    i = 0
    for row in productos.resultado:
        htm.fila_alterna(i)
        print(htm.td(row['id']))
        print(htm.td(row['producto']))
        print(htm.td(row['rubro']))
        print(htm.td(funciones.moneda(row['precio'])))
        print('<td>')
        htm.boton_detalles('prod_ver.php?cuenta_id=' + str(row['id']))
        htm.boton_editar('prod.py?id=' + str(row['id']) + '&accion=editar')
        htm.boton_eliminar('prod.py?accion=confirmar&id=' + str(row['id']))
        print('</td></tr>')
    htm.fin_tabla()
    print(htm.button("Volver", 'geined.py?accion=administracion'))
    pag.fin()
def nuevo():
    """Nuevo producto"""
    pag = pagina.Pagina("Nuevo producto", 4)
    cuentas = datos.Tabla("cuentas")
    cuentas.orden = "rubro"
    cuentas.filtro = "rubro like 4%"
    cuentas.filtrar()
    # voy por aca
    htm.encabezado_tabla(["Campo","Valor"])
    print('<form action="prod.php?accion=agregar" name="f" method="post">')
    htm.input_texto('Producto:','producto','')
    print(htm.tr(htm.td("Rubro:") + htm.td('<input type="text" name="rubro" value="" onChange="codifica()" /> - <input disabled size="80" value="desconocido" name="lblrubro" />')))
    htm.input_numero("Precio:","precio","")
    htm.botones("prod.py?accion=listado")
    htm.fin_formulario()
    htm.fin_tabla()
    print(htm.button('Volver','prod.php?accion=listado'))
    pag.fin()
def agregar(frm):
    productos = datos.Tabla("productos")
    productos.buscar("producto", frm.getvalue("producto"))
    if not productos.encontrado:
        productos.nuevo()
        productos.registro["producto"] = frm.getvalue("producto")
        productos.registro["rubro"] = frm.getvalue("rubro")
        productos.registro["precio"] = frm.getvalue("precio")
        productos.insertar()
        listado()
    else:
        htm.duplicado('prod.py?accion=listado')
def editar(frm):
    """Editar producto"""
    pag = pagina.Pagina("Edición de producto", 4)
    cuentas = datos.Tabla("cuentas")
    cuentas.orden = "rubro"
    cuentas.filtrar()
    productos = datos.Tabla("productos")
    productos.ir_a(frm.getvalue("id"))
    htm.encabezado_tabla(["Campo","Valor"])
    print('<form action="prod.php?accion=actualizar" name="f" method="post">')
    print(htm.hidden("id", frm.getvalue("id")))
    htm.input_texto('Producto:','producto', productos.registro['producto'])
    print(htm.tr(htm.td('Rubro:') + htm.td('<td><input type="text" name="rubro" value="' + productos.registro['rubro'] +  '" onChange="codifica()" /> - <input disabled size="80" value="desconocido" name="lblrubro" />')))
    htm.input_numero("Precio:","precio", productos.registro['precio'])
    htm.botones("prod.py?accion=listado")
    htm.fin_formulario()
    htm.fin_tabla()
    print('<script language="javascript">codifica();</script>')
    print(htm.button('Volver','prod.php?accion=listado'))
    pag.fin()
def actualizar(frm):
    """Actualizar el producto"""
    productos = datos.Tabla("productos")
    productos.ir_a(frm.getvalue("id"))
    productos.registro["rubro"] = frm.getvalue("rubro")
    productos.registro["producto"] = frm.getvalue("producto")
    productos.registro["precio"] = frm.getvalue("precio")
    productos.actualizar()
    listado()
if __name__ == "__main__":
    form = cgi.FieldStorage()
    accion = form.getvalue("accion", "listado")
    if accion == "listado":
        listado()
    elif accion == "editar":
        editar(form)
    elif accion == "nuevo":
        nuevo()
    elif accion == "agregar":
        agregar(form)
    elif accion == "eliminar":
        productos = datos.Tabla("productos")
        productos.borrar(form.getvalue("id"))
        listado()

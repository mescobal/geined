#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Manejo del plan de cuentas"""
import cgi
import cgitb; cgitb.enable()
import pagina
import datos
import htm
import funciones
def listado(frm):
    """Listado de plan de cuentas"""
    pag = pagina.Pagina("Listado de plan de cuentas")
    print(htm.encabezado("Listado de plan de cuentas", "Contabilidad", "geined.py?accion=contabilidad"))
    print(htm.div(htm.boton("Nuevo", "cuentas.py?accion=nuevo"), clase="barra"))
    cuentas = datos.Tabla("cuentas")
    tipo_cuenta = datos.Tabla("tipo_cuenta")
    if frm.getvalue("busqueda", "") != "":
        cuentas.filtro = "nombre LIKE '" + frm.getvalue("busqueda") + "%' "
    cuentas.orden = "rubro"
    cuentas.filtrar()
    htm.encabezado_tabla(["No.", "Rubro", "Nombre", "Tipo", "Nivel", "Fee", "Impuestos", "Auxiliar", "Acciones"])
    for fila in cuentas.resultado:
        print("<tr class='fila_datos'>")
        print(htm.td(fila['id']))
        print(htm.td(fila['rubro']))
        print(htm.td(fila['nombre']))
        tipo_cuenta.ir_a(fila['tipo_id'])
        print(htm.td(tipo_cuenta.registro['tipo']))
        print(htm.td(fila["nivel"]))
        if fila["nivel"] == 0:
            print(htm.td(funciones.numero(fila["fee"], 2), "right"))
            print(htm.td(funciones.numero(fila["impuestos"], 2), "right"))
            print(htm.td(fila["auxiliar"]))
        else:
            print(htm.td() + htm.td() + htm.td())
        print('<td>')
        htm.boton_detalles('pct_ver.php?cuenta_id=' + str(fila['id']))
        htm.boton_editar('cuentas.py?id=' + str(fila['id']) + '&accion=editar')
        htm.boton_eliminar('cuentas.py?accion=confirmar&id=' + str(fila['id']))
        print('</td></tr>')
    htm.fin_tabla()
    print(htm.button('Volver', 'geined.py?accion=contabilidad'))
    pag.fin()
def nuevo():
    """Nuevo item en plan de cuentas"""
    pag = pagina.Pagina("Nuevo rubro en plan de cuentas")
    htm.form_edicion("Nuevo rubro", "cuentas.py?accion=agregar")
    tipo_cuenta = datos.Tabla("tipo_cuenta")
    tipo_cuenta.filtrar()
    htm.input_texto('Rubro:', 'rubro', '')
    htm.input_texto('Nombre:', 'nombre', '')
    htm.input_combo("Tipo:", "tipo_id", tipo_cuenta.resultado, ["id", "tipo"], "")
    htm.input_numero("Nivel:",  "nivel",  0)
    htm.input_numero("Fee:",  "fee",  0)
    htm.input_numero("Impuestos:",  "impuestos",  0)
    htm.input_texto("Auxiliar:",  "auxiliar", "")
    htm.botones("cuentas.py?accion=listado")
    htm.form_edicion_fin()
    pag.fin()
def agregar(frm):
    """Agregar item plan de cuentas"""
    cuentas = datos.Tabla("cuentas")
    cuentas.buscar("rubro", frm.getvalue("rubro"))
    if cuentas.encontrado:
        htm.duplicado("cuentas.py?accion=listado")
    else:
        cuentas.nuevo()
        cuentas.registro["rubro"] = frm.getvalue("rubro")
        cuentas.registro["nombre"] = frm.getvalue("nombre")
        cuentas.registro["tipo_id"] = frm.getvalue("tipo_id")
        cuentas.registro["nivel"] = frm.getvalue("nivel")
        cuentas.registro["fee"] = frm.getvalue("fee")
        cuentas.registro["impuestos"] = frm.getvalue("impuestos")
        cuentas.registro["auxiliar"] = frm.getvalue("auxiliar")
        cuentas.insertar()
        listado(frm)
def editar(frm):
    """Editar item plan de cuentas"""
    pag = pagina.Pagina("Edición de plan de cuentas")
    htm.form_edicion("Edicion", "cuentas.py?accion=actualizar")
    cuentas = datos.Tabla("cuentas")
    cuentas.ir_a(frm.getvalue("id"))
    tipo_cuenta = datos.Tabla("tipo_cuenta")
    tipo_cuenta.filtrar()
    print(htm.hidden("id", frm.getvalue("id")))
    htm.input_texto('Rubro:', 'rubro', cuentas.registro['rubro'])
    htm.input_texto('Nombre:', 'nombre', cuentas.registro['nombre'])
    htm.input_combo('Tipo:', 'tipo_id', tipo_cuenta.resultado, ["id", "tipo"],
                    cuentas.registro["tipo_id"])
    htm.input_numero("Nivel:",  "nivel",  cuentas.registro["nivel"])
    htm.input_numero("Fee:",  "fee",  cuentas.registro["fee"])
    htm.input_numero("Impuestos:",  "impuestos",  cuentas.registro["impuestos"])
    htm.input_texto("Auxiliar:",  "auxiliar", cuentas.registro["auxiliar"])
    htm.botones("cuentas.py?accion=listado")
    htm.form_edicion_fin()
    pag.fin()
def actualizar(frm):
    """Actualizar item de plan de cuentas"""
    cuentas = datos.Tabla("cuentas")
    cuentas.ir_a(frm.getvalue("id"))
    cuentas.registro["rubro"] = frm.getvalue("rubro")
    cuentas.registro["nombre"] = frm.getvalue("nombre")
    cuentas.registro["tipo_id"] = frm.getvalue("tipo_id")
    cuentas.registro["nivel"] = frm.getvalue("nivel")
    cuentas.registro["fee"] = frm.getvalue("fee")
    cuentas.registro["impuestos"] = frm.getvalue("impuestos")
    cuentas.registro["auxiliar"] = frm.getvalue("auxiliar")
    cuentas.actualizar()
    listado(frm)
def eliminar(frm):
    """Eliminar item de plan de cuentas"""
    cuentas = datos.Tabla("cuentas")
    cuentas.borrar(frm.getvalue("id"))
    listado(frm)
if __name__ == "__main__":
    form = cgi.FieldStorage()
    accion = form.getvalue("accion", "listado")
    if accion == "listado":
        listado(form)
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

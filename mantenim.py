#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Mantenimiento de area contable"""
import cgi
import cgitb ; cgitb.enable()
import funciones
import htm
import datos
import pagina
def borrar(frm):
    """Borrar un item de las transacciones en base a la ID proporcionada por el LINK"""
    pag = pagina.Pagina("Borrando transaccion", 5)
    llave = frm["id"].value
    transacciones = datos.Tabla("transacciones")
    transacciones.borrar(llave)
    # Dudo si poner acá además la rutina de borrar registros nulos
    htm.redirigir("mantenim.py?accion=ver_nulos")
    pag.fin()
def eliminar_ceros():
    """Elimina registros de transacciones con debe y haber nulos"""
    transacciones = datos.Tabla("transacciones")
    transacciones.filtro = " (debe=0) AND (haber=0) "
    transacciones.borrar_filtro()
    ver_nulos()
def mantenimiento():
    """Listado de registros inválidos"""
    pag = pagina.Pagina("Listado de registros inválidos", 4)
    print(htm.encabezado("Mantenimiento", "Contabilidad", "geined.py?accion=contabilidad"))
    print(htm.button("Eliminar registros CERO", "mantenim.py?accion=eliminar_ceros"))
    print(htm.button("Volver","mantenim.py?accion=menu"))
    print(htm.h2("Registros con 0 en debe y en haber"))
    transacciones = datos.Tabla("transacciones")
    cuentas = datos.Tabla("cuentas")
    transacciones.filtro = " (debe=0) AND (haber=0) "
    transacciones.orden = "id DESC"
    transacciones.filtrar()
    htm.encabezado_tabla(["Nº", "Fecha", "Detalle", "Rubro", "Debe", "Haber", "Acciones"])
    for fila in transacciones.resultado:
        htm.fila_resaltada()
        ident = str(fila['id'])
        print(htm.td(ident) +
            htm.td(funciones.mysql_a_fecha(fila['fecha'])) +
            htm.td(fila['detalle']))
        cuentas.buscar("id", fila["cuenta_id"])
        rubro = "No encontrado"
        if cuentas.num_filas != 0:
            rubro = cuentas.registro["rubro"]
        print(htm.td(rubro) +
            htm.td(funciones.moneda(fila["debe"]), "right") +
            htm.td(funciones.moneda(fila["haber"]), "right") +
            htm.td(htm.button("Borrar", "mantenim.py?accion=borrar&id=" + ident)))
        print('</tr>')
    htm.fin_tabla()
    print "<br />"
    print(htm.hr())
    print "<br />"
    print(htm.h2("Registros con Rubro 0"))
    transacciones.filtro = " (cuenta_id=NULL) OR (cuenta_id=0) "
    transacciones.orden = " id DESC "
    transacciones.filtrar()
    tot_debe = 0
    tot_haber = 0
    htm.encabezado_tabla(["Nº", "Fecha", "Detalle", "Rubro", "Debe", "Haber", "Acciones"])
    for fila in transacciones.resultado:
        htm.fila_resaltada()
        ident = str(fila['id'])
        print(htm.td(ident) +
            htm.td(funciones.mysql_a_fecha(fila['fecha'])) +
            htm.td(fila['detalle']))
        cuentas.buscar("id", fila["cuenta_id"])
        if not cuentas.encontrado:
            rubro = "No encontrado"
        else:
            rubro = cuentas.registro["rubro"]
        tot_debe = tot_debe + fila['debe']
        tot_haber = tot_haber + fila['haber']
        print(htm.td(rubro) +
            htm.td(funciones.moneda(fila['debe']), "right") +
            htm.td(funciones.moneda(fila['haber']), "right") +
            htm.td(htm.button("Ver asientos","mantenim.py?accion=ver_asientos&id=" + ident)))
        print '</tr>'
    print(htm.tr(
        htm.td("---") +
        htm.td("---") +
        htm.td("Total") +
        htm.td("---") +
        htm.td(funciones.moneda(tot_debe), "right") +
        htm.td(funciones.moneda(tot_haber), "right") +
        htm.td("---")))
    htm.fin_tabla()
    print(htm.h2("Registros imputados a rubro incorrecto"))
    cuentas.filtro = " nivel <> 0 "
    cuentas.orden = " rubro "
    cuentas.filtrar()
    tot_debe = 0
    tot_haber = 0
    htm.encabezado_tabla(["Nº", "Fecha", "Detalle", "Rubro", "Nombre", "Debe", "Haber", "Acciones"])
    for fila in cuentas.resultado:
        cuenta_id = fila["id"]
        transacciones.filtro = " cuenta_id = " + str(cuenta_id)
        transacciones.filtrar()
        for item in transacciones.resultado:
            htm.fila_resaltada()
            rubro = str(fila["rubro"])
            nombre = str(fila["nombre"])
            if type(item["debe"]) == type(None):
                debe = 0
            else:
                debe = item["debe"]
            if type(item["haber"]) == type(None):
                haber = 0 
            else:
                haber = item["haber"]
            tot_debe = tot_debe + debe
            tot_haber = tot_haber + haber
            print(htm.td(item["id"]) +
                htm.td(funciones.mysql_a_fecha(item["fecha"])) +
                htm.td(item["detalle"]) +
                htm.td(rubro) +
                htm.td(nombre) +
                htm.td(funciones.moneda(debe), "rigth") +
                htm.td(funciones.moneda(haber), "right") +
                htm.td(
                    htm.button("Ver asientos","mantenim.py?accion=ver_asientos&id=" + str(item["id"]))))
            print("</tr>")
    print(htm.tr(
        htm.td("---") +
        htm.td("---") +
        htm.td("Total") +
        htm.td("---") +
        htm.td("---") +
        htm.td(funciones.moneda(tot_debe), "right") +
        htm.td(funciones.moneda(tot_haber), "right") +
        htm.td("---")))
    htm.fin_tabla()
    print(htm.button("Volver","mantenim.py?accion=menu"))
    pag.fin()
def ver_asientos(frm):
    """Muestra un asiento doble en base a una ID de TRANSACCIONES"""
    if not frm.has_key("id"):
        pagina.error_parametros("mantenim.py")
    else:
        ident = str(frm["id"].value)
        pag = pagina.Pagina("Par de asientos inválidos", 4)
        transacciones = datos.Tabla("transacciones")
        cuentas = datos.Tabla("cuentas")
        transacciones.ir_a(ident)
        detalle = transacciones.registro["detalle"]
        #detalle = detalle[0:10]
        transacciones.filtro = " detalle LIKE '" + detalle + "%' "
        transacciones.filtrar()
        if not transacciones.encontrado:
            print(htm.h3("Registro/s no encontrado/s") +
                htm.button("Volver", "mantenim.py?accion=ver_nulos"))
        else:
            htm.encabezado_tabla(["Nº", "Fecha", "Detalle", "Rubro", "Debe", "Haber", "Acciones"])
            for fila in transacciones.resultado:
                htm.fila_resaltada()
                cuentas.buscar("id", fila["cuenta_id"])
                rubro = "No encontrado"
                if cuentas.encontrado:
                    rubro = cuentas.registro["rubro"]
                print(htm.td(fila["id"]) +
                    htm.td(funciones.mysql_a_fecha(fila["fecha"])) +
                    htm.td(fila["detalle"]) +
                    htm.td(rubro) +
                    htm.td(funciones.moneda(fila["debe"]), "right") +
                    htm.td(funciones.moneda(fila["haber"]), "right") +
                    htm.td(
                        htm.button("Editar","transacciones.py?accion=editar&id=" + ident) +
                        htm.button("Borrar ambos","mantenim.py?accion=borrar_ambos&id=" + ident)))
                print("</tr>")
            htm.fin_tabla()
        print(htm.button("Volver", "mantenim.py?accion=ver_nulos"))
        pag.fin()
if __name__ == '__main__':
    form = cgi.FieldStorage()
    accion = "mantenimiento"
    if form.has_key("accion"):
        accion = form.getvalue("accion")
    if accion == 'mantenimiento':
        mantenimiento()
    elif accion == "borrar":
        borrar(form)
    elif accion == "eliminar_ceros":
        eliminar_ceros()
    elif accion == "ver_asientos":
        ver_asientos(form)
    else:
        pagina.error_parametros("geined.py?accion=principal")

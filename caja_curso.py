#!/usr/bin/env python
# -*- coding: utf-8 -*-
import cgitb; cgitb.enable()
import pagina
import htm
import datos
import cgi
import funciones
def nuevo(frm):
    """Nuevo ingreso a caja por cursos"""
    # Recuperar variables
    deposito_id = frm.getvalue("deposito_id")
    caja_id = frm.getvalue("caja_id")
    cola = "deposito_id=" + str(deposito_id) + "&caja_id=" + str(caja_id)
    # Base de datos
    cuentas = datos.Tabla("cuentas")
    cuentas.filtro = "rubro like '411%' and nivel=0"
    cuentas.orden = "rubro"
    cuentas.filtrar()
    pag = pagina.Pagina("Entrada a caja por cursos",  5)
    htm.form_edicion("Entrada a caja por cursos",  "caja_curso.py?accion=agregar&" + cola)
    print(htm.hidden("tipo",  "entrada"))
    htm.input_combo("Rubro:",  "cuenta_id", cuentas.resultado,  ["id",  "nombre"], "Elegir...")
    htm.input_numero("Efectivo:",  "efectivo",  "")
    htm.input_numero("Cheques:",  "cheques",  "")
    htm.input_numero("Vouchers:",  "vouchers",  "")
    htm.input_numero("Otros:",  "otros",  "")
    htm.botones("caja_ver.php?accion=listado&caja_id=" + str(caja_id) + "&deposito_id=" + str(deposito_id))
    print("</td></tr>")
    htm.form_edicion_fin()
    pag.fin()
def devolucion(frm):
    """Devolución de ingreso a caja por cursos"""
    # Recuperar variables
    deposito_id = frm.getvalue("deposito_id")
    caja_id = frm.getvalue("caja_id")
    cola = "deposito_id=" + str(deposito_id) + "&caja_id=" + str(caja_id)
    # Base de datos
    cuentas = datos.Tabla("cuentas")
    cuentas.filtro = "rubro like '411%' and nivel=0"
    cuentas.orden = "rubro"
    cuentas.filtrar()
    pag = pagina.Pagina("Devolución de entrada a caja por cursos",  5)
    htm.form_edicion("Devolución de entrada a caja por cursos",  "caja_curso.py?accion=agregar&" + cola)
    print(htm.hidden("tipo",  "salida"))
    htm.input_combo("Rubro:",  "cuenta_id", cuentas.resultado,  ["id",  "nombre"], "Elegir...")
    htm.input_numero("Efectivo:",  "efectivo",  "")
    htm.input_numero("Cheques:",  "cheques",  "")
    htm.input_numero("Vouchers:",  "vouchers",  "")
    htm.input_numero("Otros:",  "otros",  "")
    htm.botones("caja_ver.php?accion=listado&caja_id=" + str(caja_id) + "&deposito_id=" + str(deposito_id))
    print("</td></tr>")
    htm.form_edicion_fin()
    pag.fin()
def agregar(frm):
    """Agregar una nueva linea a caja con datos de ingresos por cursos"""
    # recuperar variables
    deposito_id = int(frm.getvalue("deposito_id"))
    efectivo = float(frm.getvalue('efectivo'))
    cheques = float(frm.getvalue("cheques"))
    vouchers = float(frm.getvalue("vouchers"))
    otros = float(frm.getvalue("otros"))
    cuenta_id = frm.getvalue("cuenta_id")
    caja_id = frm.getvalue('caja_id')
    cola = "deposito_id=" + str(deposito_id) + "&caja_id=" + str(caja_id)
    # base de datos
    mov_caja = datos.Tabla("mov_caja")
    cuentas = datos.Tabla("cuentas")
    cajas = datos.Tabla("cajas")
    # Buscar en bases de datos
    cajas.ir_a(caja_id)
    cuentas.ir_a(frm.getvalue("cuenta_id"))
    # Ajustes
    detalle = "Ingreso por cursos: " + cuentas.registro["nombre"]
    if frm.getvalue("tipo") == "salida":
        efectivo = -efectivo
        cheques = -cheques
        vouchers = -vouchers
        otros = -otros
        detalle = "Devolución por cursos: " + cuentas.registro["nombre"]
    # Movimientos de caja
    mov_caja.nuevo()
    mov_caja.registro["caja_id"] = caja_id
    mov_caja.registro["detalle"] = detalle
    mov_caja.registro["efectivo"] = efectivo
    mov_caja.registro["cheques"] = cheques
    mov_caja.registro["vouchers"] = vouchers
    mov_caja.registro["otros"] = otros
    mov_caja.insertar()
    # Transacciones
    fecha = cajas.registro["fecha"]
    cuenta_efectivo = 111010
    cuenta_cheques = 111020
    cuenta_vouchers = 113001
    cuenta_otros = 111024
    if deposito_id == 2:
        cuenta_efectivo = 111011
        cuenta_cheques = 111021
        cuenta_vouchers = 113002
        cuenta_otros = 111025
    elif deposito_id == 3:
        cuenta_efectivo = 111012
        cuenta_cheques = 111022
        cuenta_vouchers = 113003
        cuenta_otros = 111026
    else:
        cuenta_efectivo = 111010
        cuenta_cheques = 111020
        cuenta_vouchers = 113001
        cuenta_otros = 111024
    # Debe: caja en cuestión
    if frm.getvalue("tipo") == "entrada":
        if efectivo != 0:
            cuentas.buscar("rubro", cuenta_efectivo)
            efectivo_id = cuentas.registro["id"]
            transaccion(fecha, detalle, efectivo_id, efectivo, 0, caja_id)
            transaccion(fecha, detalle, cuenta_id, 0, efectivo, caja_id)
        if cheques != 0:
            cuentas.buscar("rubro", cuenta_cheques)
            cheques_id = cuentas.registro["id"]
            transaccion(fecha, detalle, cheques_id, cheques, 0, caja_id)
            transaccion(fecha, detalle, cuenta_id, 0, cheques, caja_id)
        if vouchers != 0:
            cuentas.buscar("rubro", cuenta_vouchers)
            vouchers_id = cuentas.registro["id"]
            transaccion(fecha, detalle, vouchers_id, vouchers, 0, caja_id) 
            transaccion(fecha, detalle, cuenta_id, 0, vouchers, caja_id)
        if otros != 0:
            cuentas.buscar("rubro", cuenta_otros)
            otros_id = cuentas.registro["id"]
            transaccion(fecha, detalle, otros_id, otros, 0, caja_id)
            transaccion(fecha, detalle, cuenta_id, 0, otros, caja_id)
    else:
        if efectivo != 0:
            cuentas.buscar("rubro", cuenta_efectivo)
            efectivo_id = cuentas.registro["id"]
            transaccion(fecha, detalle, cuenta_id, -efectivo, 0, caja_id)
            transaccion(fecha, detalle, efectivo_id, 0, -efectivo, caja_id)
        if cheques != 0:
            cuentas.buscar("rubro", cuenta_cheques)
            cheques_id = cuentas.registro["id"]
            transaccion(fecha, detalle, cuenta_id, -cheques, 0, caja_id)
            transaccion(fecha, detalle, cheques_id, 0, -cheques, caja_id)
        if vouchers != 0:
            cuentas.buscar("rubro", cuenta_vouchers)
            vouchers_id = cuentas.registro["id"]
            transaccion(fecha, detalle, cuenta_id, -vouchers, 0, caja_id) 
            transaccion(fecha, detalle, vouchers_id, 0, -vouchers, caja_id)
        if otros != 0:
            cuentas.buscar("rubro", cuenta_otros)
            otros_id = cuentas.registro["id"]
            transaccion(fecha, detalle, cuenta_id, -otros, 0, caja_id)
            transaccion(fecha, detalle, otros_id, 0, -otros, caja_id)
    # Haber: rubro del cursos    
    htm.inicio()
    print('<META HTTP-EQUIV="Refresh" CONTENT="0;URL=caja_ver.php?accion=listado&' + str(cola) + '">')
def transaccion(fecha, detalle, cuenta_id, debe, haber, documento):
    """Agregar una transacción"""
    transacciones = datos.Tabla("transacciones")
    transacciones.nuevo()
    transacciones.registro['fecha'] = funciones.fecha_a_mysql(fecha)
    transacciones.registro['detalle'] = detalle
    transacciones.registro['cuenta_id'] = cuenta_id
    transacciones.registro['debe'] = debe
    transacciones.registro['haber'] = haber
    transacciones.registro['documento_id'] = documento
    transacciones.insertar()
if __name__ == "__main__":
    form = cgi.FieldStorage()
    accion = form.getvalue("accion",  "nuevo")
    if accion == "agregar":
        agregar(form)
    elif accion == "devolucion":
        devolucion(form)
    else:
        nuevo(form)

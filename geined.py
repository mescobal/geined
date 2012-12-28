#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Menu principal del sistema GEINED"""
import cgitb ; cgitb.enable()
import cgi
import htm
import subprocess
import pagina
def principal():
    """Menu principal"""
    pag = pagina.Pagina("Menu principal", 10)
    print(htm.h1("Menú principal"))
    print(htm.table(
        htm.tr(
            htm.celda_menu("Recepción", "geined.py?accion=recepcion", 
                           "recepcion.png") +
            htm.celda_menu("Académico", "geined.py?accion=academico", 
                           "academico.png") +
            htm.celda_menu("Administración", "geined.py?accion=administracion",
                           "administracion.png")) +
        htm.tr(
            htm.celda_menu("Dirección", "geined.py?accion=direccion", 
                           "direccion.png") +
            htm.celda_menu("Usuario", "datos_usuario.py", "usuario.png") +
            htm.celda_menu("Sistema", "geined.py?accion=sistema", 
                           "sistema.png")) +
        htm.tr(
            htm.celda_menu("Desarrollo", "des.py?accion=listado", "bug.png") +
            htm.celda_menu("Ayuda", "ayuda.html", "ayuda.png") +
            htm.celda_menu("Salir", "logout.php", "salir.png")),
        clase="tabla_menu"))
    version = "Desconocida"    
    try:
        p = subprocess.Popen(["bzr", "revno"], shell=False, 
                             stdout=subprocess.PIPE)
        v = p.communicate()
        version = str(v[0])
    except OSError, e:
        version = "Desconocida. Error: " + str(e)
    print('<div class="pie_pagina">')
    print("Revisión Nº " + \
          version + \
          " - " + \
          "Software Libre, hecho con Software Libre " + \
          "<img src='./img/pingu.png'  border='0' width='48' height='48'>")
    print("</div>")
    pag.fin()
def recepcion():
    """Menu recepcion"""
    pag = pagina.Pagina("Recepcion", 10)
    print(htm.encabezado("Recepción", "Principal", 
                         "geined.py?accion=principal"))
    print('<table class="tabla_menu">')
    print(htm.tr(
            htm.celda_menu("Clientes", "cli.py", "clientes.png") +
            htm.celda_menu("Inscripción", "alu_inscripcion1.py", 
                           "inscripcion.png") +
            htm.celda_menu("Caja", "caja.php", "caja.png")) +
        htm.tr(
            htm.celda_menu("Comprobantes", "geined.py?accion=comprobantes", 
                           "comprobantes.png") +
            htm.celda_menu("Mensaje al pie", "menpie.php", "pie.png") +
            htm.celda_menu("Deudores", "deudores.php", "clientes.png")) +
        htm.tr(
            htm.celda_menu("Llamadas", "lla.php", "llamadas.png") +
            htm.td("") +
            htm.td("")))
    print("</table>")
    pag.fin()
def academico():
    """Menu academico"""
    pag = pagina.Pagina("Coordinación académica", 10)
    print(htm.encabezado("Académico", "Principal", 
                         "geined.py?accion=principal"))
    print("<table class='tabla_menu'")
    print(htm.tr(
            htm.celda_menu("Docentes", "doc.py?accion=listado", 
                           "docentes.png") +
            htm.celda_menu("Cursos", "cur.php?accion=listado", "cursos.png") +
            htm.celda_menu("Alumnos", "alu.py?accion=listado", "alumnos.png")) +
        htm.tr(
            htm.celda_menu("Drop-outs", "dro.py", "dropout.png") +
            htm.celda_menu("Interesados", "int.py", "emblem-people.png") +
            htm.td("")))
    print('</table>')
    pag.fin()
def administracion():
    """Menu administracion"""
    pag = pagina.Pagina("Tareas administrativas", 10)
    print(htm.encabezado("Administración", "Principal", 
                         "geined.py?accion=principal"))
    print("<table class='tabla_menu'")
    print(htm.tr(
            htm.celda_menu("Sueldos", "geined.py?accion=sueldos", 
                           "calendario.png") +
            htm.celda_menu("Contabilidad", "geined.py?accion=contabilidad", 
                           "contabilidad.png") +
            htm.celda_menu("Stock", "geined.py?accion=stock", "stock.png")) +
        htm.tr(
            htm.celda_menu("Fee", "fee.py", "fee.png") +
            htm.celda_menu("Inventario", "inventario.py", "inventario.png") +
            htm.td("")))
    print('</table>')
    pag.fin()
def sueldos():
    """Menu sueldos"""
    pag = pagina.Pagina("Sistema de sueldos", 10)
    print(htm.encabezado("Sueldos", "Administración", 
                         "geined.py?accion=administracion"))
    print(htm.ul(
        htm.li(htm.a("var.py?accion=listado", 
                     "Variables del sistema de sueldos")) +
        htm.li(htm.a("sal.py?accion=listado", "Valores salariales")) +
        htm.li(htm.a("liq.py?accion=listado", "Liquidación de sueldos")) +
        htm.li(htm.a("calc_ant_ret.py?accion=seleccionar", 
                     "Cálculo retroactivo de antigüedad"))))
    pag.fin()
def contabilidad():
    """Menu contabilidad"""
    pag = pagina.Pagina("Sistema de contabilidad", 10)
    print(htm.encabezado("Contabilidad", "Administración", 
                         "geined.py?accion=administracion"))
    print(htm.ul(
        htm.li(htm.a("cuentas.py?accion=listado", "Plan de cuentas")) +
        htm.li(htm.a("transacciones.py?accion=listado&inicio=0", 
                     "Transacciones")) +
        htm.li(htm.a("por_rubro.py?accion=listado", "Listado por rubro")) +
        htm.li(htm.a("mantenim.py?accion=mantenimiento", "Mantenimiento")) +
        htm.li(htm.a("conciliacion.py?accion=listado", "Conciliaciones"))))
    pag.fin()
def stock():
    """Menu Stock"""
    pag = pagina.Pagina("Sistema de stock", 10)
    print(htm.encabezado("Stock", "Administración", 
                         "geined.py?accion=administracion"))
    print(htm.ul(htm.li(htm.a("biecam.py?accion=listado", 
                              "Bienes de cambio"))))
    pag.fin()
def financiero():
    """Menu financiero"""
    pag = pagina.Pagina("Administración Financiera", 10)
    print(htm.encabezado("Administración financiera", "Administración", 
                         "geined.py?accion=direccion"))
    print(htm.ul(
        htm.li(htm.a("consolidado.py?accion=listado", "Consolidado anual")) +
        htm.li(htm.a("balcom.py?accion=listado", "Balance comparativo")) +
        htm.li(htm.a("inf_fin.py?accion=menu", "Informe financiero")) +
        htm.li(htm.a("cur_rent.py", "Rentabilidad de cursos")) +
        htm.li(htm.a("bc_suc.php", "Balance comparativo por sucursal")) +
        htm.li(htm.a("111018_bancos.py", "Cobranzas a depositar")) +
        htm.li(htm.a("evolucion.py", "Evolución financiera"))))
    pag.fin()
def direccion():
    """Menu direccion"""
    pag = pagina.Pagina("Dirección", 10)
    print(htm.encabezado("Dirección", "Principal", 
                         "geined.py?accion=principal"))
    print(htm.ul(
        htm.li(htm.a("empleados.py?accion=listado", "Empleados")) +
        htm.li(htm.a("tcu.py?accion=listado", "Tipos de cursos")) +
        htm.li(htm.a("bancos.php?accion=listado", "Bancos")) +
        htm.li(htm.a("geined.py?accion=financiero", 
                     "Administración financiera")) +
        htm.li(htm.a("dir_111018.php", "Depósitos MN"))))
    pag.fin()
def sistema():
    """Menu del sistema"""
    pag = pagina.Pagina("Administración del sistema", 10)
    print(htm.encabezado("Sistema", "Principal", "geined.py?accion=principal"))
    print(htm.ul(
        htm.li(htm.a("usu.py?accion=listado", "Usuarios")) +
        htm.li(htm.a("ccl.py?accion=listado", "Categorías de clientes")) +
        htm.li(htm.a("cem.php?accion=listado", "Categorías de empleados")) +
        htm.li(htm.a("dep.php?accion=listado", "Depósitos")) +
        htm.li(htm.a("pro.php?accion=listado", "Proveedores")) +
        htm.li(htm.a("upload.php", "Subir archivos")) +
        htm.li(htm.a("download.php", "Bajar archivos")) +
        htm.li(htm.a("prod.php?accion=listado", "Productos")) +
        htm.li(htm.a("codss.php?accion=listado", 
                     "Códigos de Seguridad Social"))))
    pag.fin()
def comprobantes():
    """Menu de comprobantes"""
    pag = pagina.Pagina("Manejo de comprobantes", 10)
    print(htm.encabezado("Comprobantes", "Recepción", 
                         "geined.py?accion=recepcion"))
    print(htm.h2("Ventas"))
    print(htm.ul(
        htm.li(htm.a("bol.py?accion=listado", "Boletas contado"))))
    #boton('Nota de débito (emisión)','comp.py?accion=com_pro');
    #boton('Nota de crédito (emisión)','comp.py?accion=com_pro');
    print(htm.h2("Compras"))
    #boton('Factura (recepción)','comp.py?accion=com_pro');
    #boton('Nota de débito (recepción)','comp.py?accion=com_pro');
    #boton('Nota de crédito (recepción)','comp.py?accion=com_pro');
    print(htm.h2("Ingresos"))
    #boton('Boleta de venta','comp.py?accion=com_pro');
    #boton('Recibo de cobranza','comp.py?accion=com_pro');
    #boton('Comprobante por cobro de conforme','comp.py?accion=com_pro');
    #boton('Diferido a cobrar','comp.py?accion=com_pro');
    #boton('Otos comprobantes de ingreso','comp.py?accion=com_pro');
    #boton('Retiro bancario','comp.py?accion=com_pro');
    #boton('Comprobante de retiro de caja','comp.py?accion=com_pro');
    #boton('Boleta de devolución contado EMITIDA','comp.py?accion=com_pro');
    print(htm.h2("Egresos"))
    #boton('Boleta de compra','comp.py?accion=com_pro');
    #boton('Recibo de pago','comp.py?accion=com_pro');
    #boton('Comprobante por pago de conforme','comp.py?accion=com_pro');
    #boton('Emisión de cheque diferido','comp.py?accion=com_pro');
    #boton('Otros comprobantes de egreso','comp.py?accion=com_pro');
    #boton('Depósito bancario','comp.py?accion=com_pro');
    #boton('Boleta de devolución contado RECIBIDA','comp.py?accion=com_pro');
    print(htm.h2('Proveedores'))
    #boton('Compra a proveedor','comp.py?accion=com_pro');
    #boton('Pago a proveedor','comp.py?accion=pag_pro');
    #boton('Devolución a proveedor','comp.py?accion=dev_pro');
    print(htm.h2("Clientes"))
    #boton('Venta a cliente','comp.py?accion=com_cli');
    #boton('Cobranza cliente','comp.py?accion=com_cli');
    #boton('Entrega a cliente','comp.py?accion=com_cli');
    #boton('Entrega de cliente','comp.py?accion=com_cli');
    #boton('Devolución de cliente','comp.py?accion=com_cli');
    print(htm.h2('Transferencias'))
    #boton('Desde Central','comp.py?accion=com_cli');
    #boton('Desde Costa','comp.py?accion=com_cli');
    #boton('Desde Carrasco','comp.py?accion=com_cli');
    #boton('Desde Banco','comp.py?accion=com_cli');
    print(htm.h2('Empleados'))
    #boton('Vale','comp.py?accion=com_cli');
    #boton('Reposición de vale','comp.py?accion=com_cli');
    print(htm.ul(
        htm.li(htm.a("presmat.php?accion=listado", 'Préstamo de material'))))
    #boton('Devolución de material','comp.py?accion=com_cli');
    pag.fin()
if __name__ == "__main__":
    form = cgi.FieldStorage()
    accion = form.getvalue("accion", "principal")
    if accion == 'principal':
        principal()
    elif accion == 'recepcion':
        recepcion()
    elif accion == 'academico':
        academico()
    elif accion == 'administracion':
        administracion()
    elif accion == 'sueldos':
        sueldos()
    elif accion == 'contabilidad':
        contabilidad()
    elif accion == 'stock':
        stock()
    elif accion == 'financiero':
        financiero()
    elif accion == 'direccion':
        direccion()
    elif accion == 'sistema':
        sistema()
    elif accion == 'comprobantes':
        comprobantes()
    else:
        principal()

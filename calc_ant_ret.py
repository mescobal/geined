#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Rutina de cálculo de antigüedad retroactiva"""
import cgi
import cgitb; cgitb.enable()
import funciones
import datos
import pagina
import htm
import calc_sueldos
import csv
import StringIO
def sel_empleado():
    """ Seleccionar empleado """
    pag = pagina.Pagina("Cálculo retroactivo de antigüedad", 2)
    print(htm.h2("Selección de empleado")) 
    print(htm.button("Exportar todo","calc_ant_ret.py?accion=exportar"))
    print(htm.button("Volver","geined.py?accion=sueldos"))
    empleados = datos.Tabla("empleados")
    cat_empleados = datos.Tabla("cat_empleados")
    empleados.orden = 'nombre'
    empleados.filtrar()
    htm.encabezado_tabla(["Nombre", "Categoría", "Notas", "Acciones"])
    for fila in empleados.resultado:
        ident = fila['id']
        print("<tr class='fila_datos'>")
        print(htm.td(fila['nombre']))
        cat_empleados.ir_a(fila["categoria_id"])
        categoria = cat_empleados.registro['categoria']
        print(htm.td(categoria))
        print(htm.td(fila['notas']))
        print(htm.td(
            htm.button("Seleccionar", "calc_ant_ret.py?empleado_id=" + 
                str(ident))))
        print('</tr>')
    htm.fin_tabla()
    print(htm.button('Volver', 'geined.py?accion=salarios'))
    pag.fin()
def listado(frm):
    """Listado de reliquidación"""
    # Buscar al empleado
    empleado_id = frm.getvalue("empleado_id")
    # Buscar categoría de empleado
    empleados = datos.Tabla("empleados")
    empleados.ir_a(empleado_id)
    cat_empleado_id = empleados.registro["categoria_id"]
    # carga parámetros actuales de valor hora
    salario = datos.Tabla("salario")
    salario.filtro = "cat_empleado_id=" + str(cat_empleado_id)
    salario.orden = "fecha desc"
    salario.filtrar()
    ficto_semanal = salario.registro["ficto_semanal"]
    # ficto_hora_reloj = ficto_semanal / 4.29
    # Recorre la base de datos de liquidaciones
    liquidaciones = datos.Tabla("liquidacion")
    liquidaciones.orden = "fecha"
    liquidaciones.filtrar()
    det_liquidacion = datos.Tabla("det_liquidacion")
    # Va liquidación x liquidación
    pag = pagina.Pagina("Lista de antigüedades retroactivas", 4)
    print(htm.h2(empleados.registro["nombre"]))
    print(htm.div(htm.boton("Volver", "geined.py?accion=sueldos"), 
                  clase="barra"))
    htm.encabezado_tabla(["Fecha", "Liquidacion", "Liquidado", "A liquidar"])
    # presenta la tabla de antigëdades no liquidadas
    total_antig = 0
    for liquidacion in liquidaciones.resultado:
        liq_id = liquidacion["id"]
        det_liquidacion.filtro = "liquidacion_id=" + str(liq_id) + " AND " \
            + "empleado_id=" + str(empleado_id)
        det_liquidacion.filtrar()
        for detalle in det_liquidacion.resultado:
            if detalle["antiguedad"] == 0:
                print("<tr class='fila_datos'>")
                print(htm.td(liquidacion['fecha']))
                print(htm.td(liquidacion["corresponde"]))
                print(htm.td(detalle["antiguedad"]))
                # reliquida las horas de ese mes según el valor hora ACTUAL
                detalle["ficto_semanal"] = ficto_semanal
                sueldo = calc_sueldos.Sueldo(detalle)
                # calcula la antigüedad para ese mes
                print(htm.td(funciones.moneda(sueldo.antiguedad),  "right"))
                total_antig = total_antig + sueldo.antiguedad
                # lo agrega a una tabla ad-hoc
                print("</tr>")
    htm.fin_tabla()
    print(htm.h2("Total: " + funciones.moneda(total_antig)))
    # da la opción de guardar, exportar a openoffice o salir
    pag.fin()
def exp_csv():
    """Rutina para exportar a archivo CSV"""
    # Bases de datos
    empleados = datos.Tabla("empleados")
    salario = datos.Tabla("salario")
    liquidaciones = datos.Tabla("liquidacion")
    det_liquidacion = datos.Tabla("det_liquidacion")
    # Armar datos
    empleados.orden = "nombre"
    liquidaciones.orden = "fecha"
    empleados.filtrar()
    liquidaciones.filtrar()
    # Salida
    salida = StringIO.StringIO()
    filename = "antig.csv"
    ant_csv = csv.DictWriter(salida, ["Empleado", "Fecha", "Liquidacion", 
                                      "Monto"])
    total_ant = 0
    for empleado in empleados.resultado:
        total_emp = 0
        # carga parámetros actuales de valor hora
        salario.filtro = "cat_empleado_id=" + str(empleado["categoria_id"])
        salario.orden = "fecha desc"
        salario.filtrar()
        ficto_semanal = salario.registro["ficto_semanal"]
        # Va liquidación x liquidación
        for liquidacion in liquidaciones.resultado:
            det_liquidacion.filtro = "liquidacion_id=" + \
                str(liquidacion["id"]) + " AND " \
                + "empleado_id=" + str(empleado["id"])
            det_liquidacion.filtrar()
            for detalle in det_liquidacion.resultado:
                if detalle["antiguedad"] == 0:
                    # reliquida las horas de ese mes según el valor hora ACTUAL
                    detalle["ficto_semanal"] = ficto_semanal
                    sueldo = calc_sueldos.Sueldo(detalle)
                    # calcula la antigüedad para ese mes
                    ant_csv.writerow({"Empleado":empleado["nombre"], \
                        "Fecha":funciones.mysql_a_fecha(liquidacion["fecha"]), \
                        "Liquidacion":liquidacion["corresponde"],\
                        "Monto":funciones.to_decimal(sueldo.antiguedad)})
                    total_emp = total_emp + sueldo.antiguedad
        ant_csv.writerow({"Empleado":"SubTotal", 
                          "Monto":funciones.to_decimal(total_emp)})
        total_ant = total_ant + total_emp
        total_emp = 0
    ant_csv.writerow({"Empleado":"TOTAL", 
                      "Monto":funciones.to_decimal(total_ant)})
    HEADERS = '\r\n'.join([
        "Content-type: %s;",
        "Content-Disposition: attachment; filename=%s",
        "Content-Title: %s",
        "Content-Length: %i",
        "\r\n", # empty line to end headers
        ])
    print(HEADERS % ('text/csv', filename, filename, len(salida.getvalue())))
    print(salida.getvalue())
    salida.close()
if __name__ == "__main__":
    form = cgi.FieldStorage()
    accion = form.getvalue("accion", "listado")
    if accion == "listado":
        if "empleado_id" not in form:
            sel_empleado()
        else:
            listado(form)
    elif accion == "seleccionar":
        sel_empleado()
    elif accion == "exportar":
        exp_csv()
    else:
        sel_empleado()

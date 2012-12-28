#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Listado de alumnos por sucursal"""
import cgitb; cgitb.enable()
import funciones
import datos
import htm
import cgi
import pagina
def seleccionar():
    """Selección de sucursal para listado de alumnos"""
    pag = pagina.Pagina("Listado de alumnos", 10)
    print(htm.encabezado("Seleccionar sucursal", "Alumnos", "alu.py?accion=listado"))
    depositos = datos.Tabla("depositos")
    depositos.orden = "deposito"
    depositos.filtrar()
    htm.encabezado_tabla(["Nº", "Nombre", "Acciones"])
    for fila in depositos.resultado:
        print("<tr class='fila_datos'>")
        print(htm.td(str(fila["id"])))
        print(htm.td(fila["deposito"]))
        print("<td>")
        print(htm.button("Seleccionar", "alu_suc.py?accion=listado&deposito_id=" + str(fila["id"])))
        print("</td></tr>")
    htm.fin_tabla()
    pag.fin()

def listado(frm):
    """Listado de alumnos para una sucursal"""
    # Recuperar variables
    tipo_pagina = frm.getvalue("tipo", "comun")
    deposito_id = frm.getvalue("deposito_id", "")
    # Bases de datos
    depositos = datos.Tabla("depositos")
    alumnos = datos.Tabla("alumnos")
    clientes = datos.Tabla("clientes")
    tipo_pago = datos.Tabla("tipo_pago")
    # Buscar registros
    depositos.buscar("id", deposito_id)
    sucursal = depositos.registro["deposito"]
    cod_suc = depositos.registro["codigo"]
    cursos = datos.Tabla("cursos")
    cursos.filtro = "(finalizado IS NULL) AND (curso LIKE '" + cod_suc + "%')"
    cursos.orden = "curso"
    cursos.filtrar()
    total_alumnos = 0
    pag = pagina.Pagina("Listado de alumnos de " + sucursal, fecha=0, tipo=tipo_pagina)
    print(htm.encabezado("Alumnos por sucursal", "Alumnos", "alu.py?accion=listado"))
    print("<div class='barra'>")
    print(htm.button("Reporte", "alu_suc.py?accion=listado&deposito_id=" + str(deposito_id) + "&tipo=informe") +
        htm.h2(str(cursos.num_filas) + " cursos abiertos en " + sucursal + ":"))
    for curso in cursos.resultado:
        print(htm.a("#" + curso["curso"], curso["curso"]))
        print("|"),
    print("</div>")
    for curso in cursos.resultado:
        print("<div class='barra'><a name='" + curso["curso"] + "'></a></div>")
        # alumnos.buscar("curso_id", curso["id"])
        alumnos.filtro = "curso_id=" + str(curso["id"])
        alumnos.filtrar()
        total_alumnos = total_alumnos + alumnos.num_filas
        print(htm.h3(str(alumnos.num_filas) + " alumnos en " + curso["curso"]))
        htm.encabezado_tabla(["Nº", "Nombre", "Tipo de pago", "Cuota"])
        for alumno in alumnos.resultado:
            print("<tr class='fila_datos'>")
            print(htm.td(str(alumno["id"])))
            clientes.buscar("id", alumno["cliente_id"])
            print(htm.td(clientes.registro["nombre"]))
            tipo_pago.buscar("id", alumno["tipo_pago_id"])
            print(htm.td(tipo_pago.registro["tipo"]))
            print(htm.td(funciones.moneda(alumno["cuota"])))
            print("</tr>")
        htm.fin_tabla()
    print(htm.h2("Total: " + str(total_alumnos) + " en " + sucursal))
    pag.fin()

def main():
    """Rutina principal"""
    form = cgi.FieldStorage()
    accion = form.getvalue("accion", "seleccionar")
    deposito_id = form.getvalue("deposito_id", "")
    if deposito_id == "":
        accion = "seleccionar"
    if accion == "seleccionar":
        seleccionar()
    elif accion == "listado":
        listado(form)
if __name__ == "__main__":
    main()

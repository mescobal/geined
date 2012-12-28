#!/usr/bin/env python
# -*- coding: utf-8 -*-
import cgitb; cgitb.enable()
import cgi
import funciones
import htm
import datos
import pagina
def listado():
    """Listado de docentes"""
    pag = pagina.Pagina("Listado de docentes", 5)
    empleados = datos.Tabla("empleados")
    cat_empleados = datos.Tabla("cat_empleados")
    empleados.filtro = " (categoria_id <=7) AND (categoria_id >=2) "
    empleados.orden = "nombre"
    empleados.filtrar()
    print(htm.button("Volver",'geined.py?accion=academico'))
    htm.encabezado_tabla(["Nombre", "Categoria", "CI", "Direccion", "Teléfonos",
        "eMail", "Ingreso", "Acciones"])
    i = 0
    for fila in empleados.resultado:
        htm.fila_alterna(i)
        cat_empleados.buscar("id", fila["categoria_id"])
        print(htm.td(fila["nombre"]))
        cat_empleados.buscar("id", fila["categoria_id"])
        print(htm.td(cat_empleados.registro["categoria"]))
        print(htm.td(fila["ci"]))
        print(htm.td(fila["direccion"]))
        print(htm.td(fila["telefono"]))
        print(htm.td(fila["email"]))
        print(htm.td(funciones.mysql_a_fecha(fila["ingreso"])))
        print("<td>")
        print(htm.button("Ver grupos",'doc_ver.py?accion=grupos&id=' + str(fila["id"])))
        print("</td></tr>")
        i = i + 1
    htm.fin_tabla()
    print(htm.button('Volver','geined.py?accion=academico'))
    pag.fin()
if __name__ == "__main__":
    form = cgi.FieldStorage()
    accion = form.getvalue("accion", "listado")
    if accion == "listado":
        listado()
    else:
        listado()

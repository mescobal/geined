#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Ver detalles de un documento"""
import cgi
import cgitb; cgitb.enable()
import htm
import datos
import pagina
def grupos(frm):
    """Grupos por docente"""
    pag = pagina.Pagina("Grupos por docente", 4)
    # Datos del docente
    ident = frm.getvalue("id")
    empleados = datos.Tabla("empleados")
    empleados.ir_a(ident)
    print(htm.button('Volver', 'doc.py?accion=listado'))
    print(htm.h2(empleados.registro["nombre"] + "<br />"))
    lista_cursos(ident)
    lista_cursos(ident, 1)
    print(htm.button('Volver', 'doc.py?accion=listado'))
    pag.fin()
def lista_cursos(ident, tipo=0):
    """Listado de cursos abierto o cerrados segun parámetro"""
    cursos = datos.Tabla("cursos")
    if tipo == 1:
        cursos.filtro = "empleado_id=" + str(ident) + " AND finalizado=1"
        print(htm.h3("Cursos finalizados"))
    else:
        cursos.filtro = "empleado_id=" + str(ident) + " AND finalizado<>1"
        print(htm.h3("Cursos abiertos"))
    htm.encabezado_tabla(["Nº", "Curso", "Sucursal", "Tipo", "Dias", "Horario", "Acciones"])
    i = 0
    cursos.filtrar()
    depositos = datos.Tabla("depositos")
    tipo_curso = datos.Tabla("tipo_curso")
    for fila in cursos.resultado:
        htm.fila_alterna(i)
        print(htm.td(fila['id']))
        print(htm.td(fila['curso']))
        depositos.ir_a(fila["deposito_id"])
        print(htm.td(depositos.registro['deposito']))
        tipo_curso.ir_a(fila["tipo_id"])
        print(htm.td(tipo_curso.registro['tipo']))
        print(htm.td(fila['dias']))
        print(htm.td(fila['horas']))
        # Acomodar la opcion de borrar un curso para que de de baja a todos los alumnos
        print('<td>')
        print(htm.button("Ver alumnos", 'cur_ver.py?id=' + str(fila['id'])))
        print(htm.button("Editar", 'cur.py?accion=editar&id='+ str(fila['id'])))
        print('</td></tr>')
        i = i + 1
    htm.fin_tabla()
if __name__ == "__main__":
    form = cgi.FieldStorage()
    accion = form.getvalue("accion", "grupos")
    if accion == "grupos":
        grupos(form)

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Usuarios"""
import cgitb ; cgitb.enable()
import datos
import htm
import cgi
import pagina
def listado(frm):
    """Listado de variables"""
    pag = pagina.Pagina("Detalles del tipo de curso", 5)
    tipo_curso = datos.Tabla('tipo_curso')
    tipo_curso.buscar("id", frm['id'].value)
    htm.h2("Tipo: " + tipo_curso.registro['tipo'])
    print("Código: " + tipo_curso.registro['codigo'])
    cursos = datos.Tabla('cursos')
    cursos.buscar("tipo_id", frm['id'].value)
    htm.encabezado_tabla(["Nº", "Curso", "Docente", "Sucursal", "Días", "Horario", "Acciones"])
    i = 0
    docentes = datos.Tabla("empleados")
    depositos = datos.Tabla("depositos")
    for fila in cursos.resultado:
        htm.fila_alterna(i)
        print(htm.td(fila['id']))
        print(htm.td(fila['curso']))
        # Docente
        docentes.buscar('id', fila['empleado_id'])
        if docentes.num_filas == 0:
            print(htm.td("Sin datos"))
        else:
            print(htm.td(docentes.registro['nombre']))
        # S U C U R S A L
        depositos.buscar('id', fila['deposito_id'])
        if depositos.num_filas == 0:
            print(htm.td('Sin datos'))
        else:
            print(htm.td(depositos.registro['deposito']))
        print(htm.td(fila['dias']))
        print(htm.td(fila['horas']))
        # Acomodar la opcion de borrar un curso para que de de baja a todos los alumnos
        print('<td>')
        print(htm.button("Detalles", 'cur_ver.py?id=' + str(fila['id'])))
        if fila["finalizado"] != 1:
            print(htm.button("Editar", 'cur.php?accion=editar&id=' + str(fila['id'])))
            print(htm.button("Cerrar", 'cur.php?accion=cerrar&id=' + str(fila['id']) + '&bdd=cursos'))
        else:
            print("Cerrado")
        print('</td></tr>')
    htm.fin_tabla()
    print(htm.button('Volver', 'tcu.py?accion=listado'))
    pag.fin()
def error():
    """Imprime pagina de error"""
    pag = pagina.Pagina("Error", 10)
    print(htm.h2("Error: faltan variables"))
    pag.fin()
def main():
    """Principal"""
    form = cgi.FieldStorage()
    if form.has_key("id"):
        listado(form)
    else:
        error()

if __name__ == "__main__":
    main()
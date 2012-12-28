#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Segundo paso de inscripcion: agrega curso"""
import cgi
import cgitb; cgitb.enable()
import pagina
import htm
import datos
def paso_2(frm):
    """Segundo paso de inscripción: agrega curso"""
    clientes = datos.Tabla("clientes")
    cliente_id = frm.getvalue("cliente_id", "")
    clientes.ir_a(cliente_id)
    pag = pagina.Pagina("Inscripción: paso 2", 4)
    print(htm.h2("Elegir curso para: " + clientes.registro['nombre']))
    # elegir curso
    print('<table><tr><td>')
    print(htm.button('Volver', 'geined.py?accion=recepcion'))
    print("""</td><td>
        <form action = "alu_inscipcion2.py?cliente_id='.$cliente_id.'" method="post">
            <input type="text" name="busqueda">
            <input type="submit" value="Buscar">
        </form>
        </td></tr></table>""")
    # cargar datos
    # OJO! Solo cursos abiertos
    busqueda = frm.getvalue("busqueda", "")
    cursos = datos.Tabla("cursos")
    empleados = datos.Tabla("empleados")
    depositos = datos.Tabla("depositos")
    tipo_curso = datos.Tabla("tipo_curso")
    cursos.orden = "curso"
    if busqueda != "":
        cursos.filtro = 'curso LIKE LIKE "%' + str(busqueda) + '%" AND finalizado IS NULL '
    else:
        cursos.filtro = "finalizado IS NULL"
    cursos.filtrar()
    htm.encabezado_tabla(["Nº", "Curso", "Docentes", "Sucursal", "Tipo",
        "Dias", "Horario", "Notas", "Acciones"])
    i = 0
    for fila in cursos.resultado:
        htm.fila_alterna(i)
        ident = fila['id']
        print(htm.td(str(ident)))
        print(htm.td(fila['curso']))
        # D O C E N T E
        empleados.ir_a(fila["empleado_id"])
        print(htm.td(empleados.registro["nombre"]))
        # SUCURSAL
        depositos.ir_a(fila["deposito_id"])
        print(htm.td(depositos.registro["deposito"]))
        # T I P O
        tipo_curso.ir_a(fila["tipo_id"])
        print(htm.td(tipo_curso.registro["tipo"]))
        print(htm.td(fila['dias']))
        print(htm.td(fila['horas']))
        print(htm.td(fila['notas']))
        print('<td>')
        print(htm.button("Continuar", "alu_inscripcion3.py?cliente_id=" + 
            str(cliente_id) + "&curso_id=" + str(ident)))
        i = i + 1
    htm.fin_tabla()
    print(htm.button('Volver', 'geined.py?accion=recepcion'))
    pag.fin()
if __name__ == "__main__":
    form = cgi.FieldStorage()
    paso_2(form)

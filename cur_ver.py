#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Ver detalles de un curso"""
import cgi
import cgitb ; cgitb.enable()
import htm
import datos
import funciones
import pagina
def listado(frm):
    """Listado de detalle del curso"""
    ident = frm.getvalue("id", 0)
    if ident == 0:
        pagina.error_variable("cur.php?accion=listado")
    else:
        cursos = datos.Tabla("cursos")
        empleados = datos.Tabla("empleados")
        alumnos = datos.Tabla("alumnos")
        clientes = datos.Tabla("clientes")
        tipo_pago = datos.Tabla("tipo_pago")
        # Contemplar alterantiva de que el dato no esté.
        pag = pagina.Pagina("Listado por curso", 5)
        curso = "Desconocido"
        docente = "Desconocido"
        cursos.buscar("id", ident)
        if cursos.encontrado:
            curso = cursos.registro["curso"]
        htm.h1("Curso: " + curso)
        empleados.buscar("id", cursos.registro["empleado_id"])
        if empleados.encontrado:
            docente = empleados.registro["nombre"]
        htm.h2("Docente: " + docente)
        htm.button("Volver", "cur.php?accion=listado")
        alumnos.filtro = "curso_id=" + str(ident)
        alumnos.filtrar()
        htm.encabezado_tabla(["Alumno", "Tipo de pago", "Cuota", "Estado", "Acciones"])
        for fila in alumnos.resultado:
            alumno_id = fila['id']
            htm.fila_resaltada()
            clientes.buscar("id", fila["cliente_id"])
            print(htm.td(clientes.registro["nombre"]))
            tipo_pago.buscar("id", fila["tipo_pago_id"])
            print(htm.td(tipo_pago.registro["tipo"]))
            htm.linea_moneda(fila['cuota'])
            if fila["finalizado"] == 1:
                print(htm.td("No cursando"))
            else:
                print(htm.td("Cursando"))
            print("<td align='center'>")
            htm.boton_detalles('cli_ver.php?id=' + str(fila['cliente_id']))
            htm.boton_editar("alu.py?accion=editar&id=" + str(alumno_id))
            # htm.boton_eliminar("cur_ver.py?id=" + str(ident) + "&accion=drop_out&alumno_id=" + str(alumno_id))
            htm.boton_confirmar("Drop-out", "¿Desea marcar este cliente como Drop-out?", "cur_ver.py?id=" + str(ident) + "&accion=drop_out&alumno_id=" + str(alumno_id))
            print('<td></tr>')
            htm.fin_tabla()
        htm.button('Volver', 'cur.php?accion=listado')
        pag.fin()
def drop_out(frm):
    """Rutina para confirmar drop-out"""
    pag = pagina.Pagina("Efectuando procedimiento de Drop-out", nivel=5, fecha=1)
    htm.form_edicion("Datos de Drop-out", "cur_ver.py?accion=eliminar")
    alumno_id = frm.getvalue("alumno_id")
    alumnos = datos.Tabla("alumnos")
    clientes = datos.Tabla("clientes")
    cursos = datos.Tabla("cursos")
    alumnos.buscar("id", alumno_id)
    curso_id = alumnos.registro["curso_id"]
    cursos.buscar("id", alumnos.registro["curso_id"])
    cliente_id = alumnos.registro["cliente_id"]
    clientes.buscar("id", cliente_id)
    print("<tr><td>Nombre:</td><td>" + clientes.registro["nombre"] + "</td></tr>")
    print("<tr><td>Curso:</td><td>" + cursos.registro["curso"] + "</td></tr>")
    htm.input_fecha("Fecha de Drop-out", "fecha", funciones.fecha_a_mysql(funciones.hoy()))
    htm.input_memo("Notas", "notas", clientes.registro["notas"])
    htm.campo_oculto("alumno_id", alumno_id)
    htm.campo_oculto("curso_id", curso_id)
    # TODO, pendiente
    htm.botones("cur_ver.py?accion=listado&id=" + str(curso_id))
    htm.form_edicion_fin()
    pag.fin()
def eliminar(frm):
    """Eliminar datos y modificad en la base de datos""" 
    alumno_id = frm.getvalue("alumno_id", 0)
    if alumno_id == 0:
        pagina.error_variable("cur.php?accion=listado")
    else:
        pag = pagina.Pagina("Modificando datos", 5)
        # Verificar si es alumno en mas de un curso ABIERTO!
        alumnos = datos.Tabla("alumnos")
        clientes = datos.Tabla("clientes")
        cursos = datos.Tabla("cursos")
        alumnos.buscar("id", alumno_id)
        curso_id = alumnos.registro["curso_id"]
        cliente_id = alumnos.registro["cliente_id"]
        clientes.buscar("id", cliente_id)
        alumnos.filtro = "cliente_id=" + str(cliente_id)
        alumnos.filtrar()
        cursos_abiertos = 0
        for fila in alumnos.resultado:
            cursos.buscar("id", fila["curso_id"])
            if cursos.registro["finalizado"] != 1:
                cursos_abiertos = cursos_abiertos + 1
        if cursos_abiertos > 1:
            htm.h1("El cliente no figura como DROP-OUT porque se encuentra " +\
                "actualmente inscripto en más de un curso AUN abierto")
            htm.h2("Aún así será dado de baja como alumno de ESTE curso")
            htm.h3("La fecha de último contacto del cliente se actualiza a la fecha de este drop-out")
            clientes.registro["ultimo_contacto"] = funciones.fecha_a_mysql(frm.getvalue("fecha"))
            clientes.actualizar()
            htm.button("Volver", "cur_ver.py?accion=listado&id=" + str(curso_id))
        else:
            clientes.registro["ultimo_contacto"] = funciones.fecha_a_mysql(frm.getvalue("fecha"))
            clientes.registro["categoria_id"] = 3
            clientes.actualizar() 
            htm.redirigir("cur_ver.py?id=" + frm.getvalue("curso_id"))
        alumnos.buscar("id", alumno_id)
        alumnos.registro["finalizado"] = 1
        alumnos.actualizar()
        pag.fin()
def main():
    """Principal"""
    form = cgi.FieldStorage()
    accion = form.getvalue("accion", "listado")
    if accion == 'listado':
        listado(form)
    elif accion == "drop_out":
        drop_out(form)
    elif accion == "eliminar":
        eliminar(form)

if __name__ == "__main__":
    main()
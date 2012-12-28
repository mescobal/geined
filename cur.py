#!/usr/bin/env python
# -*- coding: utf8 -*-
"""Manejo de cursos"""
import cgitb; cgitb.enable()
import cgi
import datos
import htm
import pagina

def listado(frm):
    """Listado de cursos abiertos"""
    pag = pagina.Pagina("Listado de cursos abiertos", 10)
    print("<table><tr><td>")
    htm.button("Nuevo", 'cur.py?accion=nuevo')
    htm.button("Cursos finalizados", "cur.py?accion=cerrados")
    htm.button("Volver", "geined.py?accion=academico")
    print('</td><td>')
    htm.formulario('cur.py')
    print('<input type="text" name="busqueda"><input type="submit" \
        value="Buscar">')
    htm.fin_formulario()
    print('</td></tr></table>')
    htm.nota('Notas: ELIMINAR CURSO: se elimina el curso, todos los alumnos de \
        ese curso se eliminan y los clientes pasan a categoria "en espera"')
    htm.nota("Notas: FINALIZAR CURSO: TODOS los alumnos de ese curso pasan a \
        ser 'Ex-Alumnos'. Implica finalización normal de un curso")
    # cargar datos: no se cargan los cursos finalizados
    cursos = datos.Tabla("cursos")
    empleados = datos.Tabla("empleados")
    depositos = datos.Tabla("depositos")
    tipo_curso = datos.Tabla("tipo_curso")
    cursos.orden = "curso"
    cursos.filtro = "finalizado IS NULL"
    if frm.getvalue("busqueda", "") != "":
        cursos.filtro = " curso LIKE '%" + str(frm.getvalue("busqueda")) + \
            "%' AND finalizado IS NULL "
    cursos.filtrar()
    htm.encabezado_tabla(["Nº", "Curso", "Docente", "Sucursal", "Tipo",
        "Acciones"])
    for fila in cursos.resultado:
        htm.fila_resaltada()
        print(htm.td(str(fila['id'])))
        print(htm.td(fila['curso']))
        empleados.buscar("id", fila["empleado_id"])
        print(htm.td(empleados.registro["nombre"]))
        depositos.buscar("id", fila["deposito_id"])
        print(htm.td(depositos.registro["deposito"]))
        tipo_curso.buscar("id", fila["tipo_id"])
        print(htm.td(tipo_curso.registro["tipo"]))
        # Acomodar la opcion de borrar un curso para que de de baja a todos los
        # alumnos
        print('<td>')
        htm.boton_detalles('cur_ver.py?id=' + str(fila["id"]))
        htm.boton_editar('cur.py?accion=editar&id=' + str(fila['id']))
        htm.boton_eliminar("cur.py?accion=eliminar&id=" + str(fila["id"]))
        # htm.button("Cerrar", 'cur.py?accion=confirmar&id=' + str(fila["id"]))
        htm.button("Finalizar", 'cur.py?accion=finalizar&id=' + str(fila['id']))
        print('</td></tr>')
    htm.fin_tabla()
    htm.button("Volver", "geined.py?accion=academico")
    pag.fin()

def nuevo():
    """Formulario de ingreso de nuevo curso"""
    pag = pagina.Pagina("Apertura de curso", 5)
    htm.nota('La apertura de un curso genera un número único para cada curso. \
        El nombre del curso puede escribirse manualmente o puede generarse \
        automáticamente en un formato estándar: AA-BBBB-CCC-DD:DD donde AA es \
        la sucursal, BBBB es el tipo de curso, CCC los días y DD:DD la hora de \
        inicio.')
    # datos
    tipo_curso = datos.Tabla("tipo_curso")
    docentes = datos.Tabla("empleados")
    depositos = datos.Tabla("depositos")
    # filtros
    tipo_curso.orden = "tipo"
    tipo_curso.filtrar()
    docentes.filtro = "(categoria_id>=2) AND (categoria_id<=7)"
    docentes.orden = "nombre"
    docentes.filtrar()
    depositos.orden = "deposito"
    depositos.filtrar()
    # formulario
    htm.form_edicion("Nuevo curso", "cur.py?accion=agregar")
    htm.input_texto('Nombre:', 'curso', '')
    htm.input_check("Generar nombre al guardar:", "generar", "1")
    htm.input_combo("Docente:", "empleado_id", docentes.resultado, ["id",
        "nombre"], "")
    htm.input_combo("Sucursal:", "deposito_id", depositos.resultado, ["id",
        "deposito"], "")
    htm.input_combo("Tipo:", "tipo_id", tipo_curso.resultado, ["id", "tipo"],
        "")
    htm.input_texto('Dias:', 'dias', '')
    htm.input_texto('Horas:', 'horas', '')
    htm.input_memo("Notas", "notas", "")
    htm.fin_tabla()
    htm.botones("cur.py?accion=listado")
    htm.form_edicion_fin()
    pag.fin()
def agregar(frm):
    """Agrega un nuevo curso"""
    pag = pagina.Pagina("Nuevo curso", 5)
    nombre = frm.getvalue("curso", "---")
    if frm.gevalue("generar", '0') == 1:
        # Generar nombre
        # Sucursal + Tipo + Dias + Horas
        depositos = datos.Tabla("deposito")
        depositos.buscar("id", frm.getvalue("deposito_id"))
        tipo_curso = datos.Tabla("tipo_curso")
        tipo_curso.buscar("id", "tipo_id")
        nombre = depositos.registro["codigo"] + "-" + \
            tipo_curso.registro["codigo"] + "-" + frm.getvalue("dias") + "-" +\
            frm.getvalue("horas")
    cursos = datos.Tabla("cursos")
    cursos.filtro = "curso='" + nombre + "' AND finalizado<>'1')"
    cursos.filtrar()
    if cursos.num_filas == 0:
        cursos.registro["curso"] = nombre
        cursos.registro["empleado_id"] = frm.gevalue("empleado_id")
        cursos.registro["deposito_id"] = frm.getvalue("deposito_id")
        cursos.registro["tipo_id"] = frm.getvalue("tipo_id")
        cursos.registro["dias"] = frm.getvalue("dias")
        cursos.registro["horas"] = frm.getvalue("horas")
        cursos.registro["notas"] = frm.getvalue("notas")
        cursos.insertar()
        htm.redirigir("cur.py?accion=listado")
    else:
        htm.duplicado("cur.py?accion=listado")
    pag.fin()

def editar(frm):
    """Edicion de curso"""
    pag = pagina.Pagina("Edición de curso Nº " + str(frm.getvalue("id")), 5)
    htm.nota('El nombre del curso puede escribirse manualmente o puede \
        generarse automáticamente en un formato estándar: AA-BBBB-CCC-DD:DD \
        donde AA es la sucursal, BBBB es el tipo de curso, CCC los días y \
        DD:DD la hora de inicio.')
    htm.nota("Los cambios no se grabarán hasta que presione ACEPTAR")
    # datos
    tipo_curso = datos.Tabla("tipo_curso")
    docentes = datos.Tabla("empleados")
    depositos = datos.Tabla("depositos")
    cursos = datos.Tabla("cursos")
    cursos.buscar("id", frm.getvalue("id"))
    # filtros
    tipo_curso.orden = "tipo"
    tipo_curso.filtrar()
    docentes.filtro = "(categoria_id>=2) AND (categoria_id<=7)"
    docentes.orden = "nombre"
    docentes.filtrar()
    depositos.orden = "deposito"
    depositos.filtrar()
    # formulario
    htm.form_edicion("Edición de curso Nº " + str(frm.getvalue("id")),
        "cur.py?accion=actualizar")
    htm.campo_oculto("id", frm.getvalue("id"))
    htm.input_texto('Nombre:', 'curso', cursos.registro["curso"])
    htm.input_check("Generar nombre al guardar:", "generar", "1")
    htm.input_combo("Docente:", "empleado_id", docentes.resultado, ["id",
        "nombre"], cursos.registro["empleado_id"])
    htm.input_combo("Sucursal:", "deposito_id", depositos.resultado, ["id",
        "deposito"], cursos.registro["deposito_id"])
    htm.input_combo("Tipo:", "tipo_id", tipo_curso.resultado, ["id", "tipo"],
        cursos.registro["tipo_id"])
    htm.input_texto('Dias:', 'dias', cursos.registro["dias"])
    htm.input_texto('Horas:', 'horas', cursos.registro["horas"])
    htm.input_memo("Notas", "notas", cursos.registro["notas"])
    htm.fin_tabla()
    htm.botones("cur.py?accion=listado")
    htm.form_edicion_fin()
    pag.fin()
def actualizar(frm):
    """Actualizar datos de un curso"""
    pag = pagina.Pagina("Nuevo curso", 5)
    nombre = frm.getvalue("curso", "---")
    if frm.gevalue("generar", '0') == 1:
        # Generar nombre
        # Sucursal + Tipo + Dias + Horas
        depositos = datos.Tabla("deposito")
        depositos.buscar("id", frm.getvalue("deposito_id"))
        tipo_curso = datos.Tabla("tipo_curso")
        tipo_curso.buscar("id", "tipo_id")
        nombre = depositos.registro["codigo"] + "-" + \
            tipo_curso.registro["codigo"] + "-" + frm.getvalue("dias") + "-" +\
            frm.getvalue("horas")
    cursos = datos.Tabla("cursos")
    cursos.buscar("id", frm.getvalue("id"))
    cursos.registro["curso"] = nombre
    cursos.registro["empleado_id"] = frm.gevalue("empleado_id")
    cursos.registro["deposito_id"] = frm.getvalue("deposito_id")
    cursos.registro["tipo_id"] = frm.getvalue("tipo_id")
    cursos.registro["dias"] = frm.getvalue("dias")
    cursos.registro["horas"] = frm.getvalue("horas")
    cursos.registro["notas"] = frm.getvalue("notas")
    cursos.actualizar()
    htm.redirigir("cur.py?accion=listado")
    pag.fin()

def cerrados():
    """Listado de cursos cerrados"""
    pag = pagina.Pagina("Listado de cursos cerrados", 5)
    htm.button("Volver", "cur.py?accion=listado")
    # Datos
    cursos = datos.Tabla("cursos")
    empleados = datos.Tabla("empleados")
    tipo_curso = datos.Tabla("tipo_curso")
    # Filtros
    cursos.filtro = "finalizado=1"
    cursos.orden = "id desc"
    cursos.filtrar()
    htm.encabezado_tabla(["Nº", "Curso", "Docente", "Tipo", "Dias", "Horario"])
    for fila in cursos.resultado:
        htm.fila_resaltada()
        ident = str(fila['id'])
        print(htm.td(ident))
        print(htm.td(fila['curso']))
        empleados.buscar("id", fila["empleado_id"])
        print(htm.td(empleados.registro["nombre"]))
        tipo_curso.buscar("id", fila["tipo_id"])
        print(htm.td(tipo_curso.registro["tipo"]))
        print(htm.td(fila["dias"]))
        print(htm.td(fila["horas"]))
        print('</td></tr>')
    htm.fin_tabla()
    htm.button("Volver", "cur.py?accion=listado")
    pag.fin()
def eliminar(frm):
    """Eliminar un curso: no es lo mismo que CERRAR ni FINALIZAR"""
    pag = pagina.Pagina("Eliminando curso", 2)
    # datos
    cursos = datos.Tabla("cursos")
    clientes = datos.Tabla("clientes")
    alumnos = datos.Tabla("alumnos")
    # Poner clientes que son alumnos de ese curo a "EN ESPERA"
    alumnos.filtro = "curso_id=" + str(frm.getvalue("id"))
    alumnos.filtrar()
    for alumno in alumnos.resultado:
        clientes.buscar("id", alumno["cliente_id"])
        clientes.registro["categoria_id"] = 5
        clientes.actualizar()
    # se eliminan los alumnos
    sql = 'DELETE FROM alumnos WHERE curso_id="' + frm.getvalue("id") + '"'
    dat = datos.Datos()
    dat.cursor.execute(sql)
    # Eliminar el curso
    cursos.borrar(frm.getvalue("id"))
    htm.redirigir("cur.py?accion=listado")
    pag.fin()

def finalizar(frm):
    """Finalizar un curso normalmente"""
    pag = pagina.Pagina("Finalización de curso", 4)
    htm.nota('Este curso finaliza normalmente. Todos los alumnos de este curso \
        pasan a categoría Ex-Alumno')
    # datos
    clientes = datos.Tabla("clientes")
    cursos = datos.Tabla("cursos")
    alumnos = datos.Tabla("alumnos")
    cursos.buscar("id", frm.getvalue("id"))
    htm.h2("Curso: " + cursos.registro["curso"])
    alumnos.filtro = "curso_id=" + frm.getvalue("id")
    alumnos.filtrar()
    htm.h3("Alumnos:")
    for alumno in alumnos.resultado:
        clientes.buscar("id", alumno["cliente_id"])
        print(clientes.registro["nombre"])
        print("</br>")
    htm.formulario("cur.py?accion=finalizar2&id=" + str(frm.getvalue("id")))
    htm.botones("cur.py?accion=listado")
    pag.fin()
def finalizar2(frm):
    """Rutina que efectivamente finaliza un curso"""
    pag = pagina.Pagina("Finalizando curso", 5)
    # Tablas
    alumnos = datos.Tabla("alumnos")
    clientes = datos.Tabla("clientes")
    cursos = datos.Tabla("cursos")
    cursos.buscar("id", frm.getvalue("id"))
    # Se pone el flag FINALIZADO de cada alumno a 1
    ident = str(frm.getvalue("id"))
    dat = datos.Datos()
    sql = 'UPDATE alumnos SET finalizado="1" WHERE curso_id="' + ident + '"'
    dat.cursor.execute(sql)
    # Se ponen los clientes como ex-alumnos
    alumnos.filtro = "curso_id=" + ident
    alumnos.filtrar()
    for alumno in alumnos.resultado:
        clientes.buscar("id", alumno["cliente_id"])
        clientes.registro["categoria_id"] = 4
        clientes.actualizar()
    # Se pone el curso como finalizado
    cursos.registro["finalizado"] = 1
    cursos.actualizar()
    # sql = 'UPDATE cursos SET finalizado="1" WHERE id="' + ident + '"'
    # dat.cursor.execute(sql)
    htm.redirigir("cur.py?accion=listado")
    pag.fin()
def main():
    """Principal"""
    form = cgi.FieldStorage()
    accion = form.getvalue("accion", "listado")
    if accion == "listado":
        listado(form)
    elif accion == "nuevo":
        nuevo()
    elif accion == "agregar":
        agregar(form)
    elif accion == "editar":
        editar(form)
    elif accion == "actualizar":
        actualizar(form)
    elif accion == "cerrados":
        cerrados()
    elif accion == "eliminar":
        eliminar(form)
    elif accion == "finalizar":
        finalizar(form)
    elif accion == "finalizar2":
        finalizar2(form)

if __name__ == "__main__":
    main()
    
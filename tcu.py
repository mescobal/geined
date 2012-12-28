#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Manejo de tipos de cursos"""
import cgitb; cgitb.enable()
import cgi
import datos
import htm
import pagina
def listado():
    """Listado de tipos de cursos"""
    pag = pagina.Pagina("Listado de tipos de cursos", 2)
    htm.button("Nuevo", 'tcu.py?accion=nuevo')
    htm.button("Volver", "geined.py?accion=direccion")
    tipo_curso = datos.Tabla("tipo_curso")
    cuentas = datos.Tabla("cuentas")
    tipo_curso.orden = "tipo"
    tipo_curso.filtrar()
    htm.encabezado_tabla(["Tipo", "Código", "Duracion", "Rubro", "Acciones"])
    i = 0
    for fila in tipo_curso.resultado:
        htm.fila_alterna(i)
        print(htm.td(fila["tipo"]))
        print(htm.td(fila["codigo"]))
        print(htm.td(fila["duracion"]))
        cuentas.buscar("rubro", fila["rubro"])
        if cuentas.encontrado:
            print(htm.td(cuentas.registro["nombre"]))
            # htm.celda(fila['rubro'])
        else:
            print(htm.td("Desconocido"))
        print("<td>")
        htm.boton_detalles('tcu_ver.py?id=' + str(fila["id"]))
        htm.boton_editar("tcu.py?accion=editar&id=" + str(fila["id"]))
        htm.boton_eliminar('tcu.py?accion=eliminar&id='+ str(fila["id"]))
        print('</td></tr>')
        i = i + 1
    htm.fin_tabla()
    print(htm.button("Volver",'geined.py?accion=direccion'))
    pag.fin()
def nuevo():
    """Nuevo tipo de curso"""
    pag = pagina.Pagina("Nuevo tipo de curso", 2)
    cuentas = datos.Tabla("cuentas")
    cuentas.orden = "rubro"
    cuentas.filtro = "rubro like '4%'"
    cuentas.filtrar()
    htm.form_edicion("Nuevo tipo de curso", "tcu.py?accion=agregar")
    htm.input_texto("Tipo:", "tipo", "")
    htm.input_texto("Código:", "codigo", "")
    htm.input_numero("Duracion:", "duracion", "")
    htm.input_combo('Rubro:', 'rubro', cuentas.resultado, ["rubro", "nombre"], "Asignar un rubro")
    htm.botones("tcu.py?accion=listado")
    htm.form_edicion_fin()
    pag.fin()
def editar(frm):
    """Edición de un tipo de curso"""
    pag = pagina.Pagina("Edición de tipo de curso", 2)
    cuentas = datos.Tabla("cuentas")
    tipo_curso = datos.Tabla("tipo_curso")
    cuentas.orden = "rubro"
    cuentas.filtro = "rubro like '4%'"
    cuentas.filtrar()
    tipo_curso.buscar("id", frm.getvalue("id"))
    htm.form_edicion("Editar tipo de curso", "tcu.py?accion=actualizar")
    htm.campo_oculto("id", frm.getvalue("id"))
    htm.input_texto("Tipo:", "tipo", tipo_curso.registro["tipo"])
    htm.input_texto("Código:", "codigo", tipo_curso.registro["codigo"])
    htm.input_numero("Duracion:", "duracion", tipo_curso.registro["duracion"])
    htm.input_combo('Rubro:', 'rubro', cuentas.resultado, ["rubro", "nombre"], tipo_curso.registro["rubro"])
    htm.botones("tcu.py?accion=listado")
    htm.form_edicion_fin()
    pag.fin()
def agregar(frm):
    """Agregar tipo de curso"""
    tipo_curso = datos.Tabla("tipo_curso")
    tipo_curso.buscar("tipo", frm.getvalue("tipo"))
    pag = pagina.Pagina("Agregando tipo de curso", 2)
    if tipo_curso.encontrado:
        print(htm.h2("Ya existe ese tipo de curso"))
        print(htm.button("Volver", "tcu.py?accion=listado"))
    else:
        tipo_curso.registro["tipo"] = frm.getvalue("tipo")
        tipo_curso.registro["codigo"] = frm.getvalue("codigo")
        tipo_curso.registro["duracion"] = frm.getvalue("duracion")
        tipo_curso.registro["rubro"] = frm.getvalue("rubro")
        tipo_curso.insertar()
        htm.redirigir("tcu.py?accion=listado")
    pag.fin()
def actualizar(frm):
    """Actualizar un tipo de curso"""
    pag = pagina.Pagina("Actualizar", 20)
    ident = frm.getvalue("id")
    tipo_curso = datos.Tabla("tipo_curso")
    tipo_curso.buscar("id", ident)
    tipo_curso.registro["tipo"] = frm.getvalue("tipo")
    tipo_curso.registro["codigo"] = frm.getvalue("codigo")
    tipo_curso.registro["duracion"] = frm.getvalue("duracion")
    tipo_curso.registro["rubro"] = frm.getvalue("rubro")
    tipo_curso.actualizar()
    htm.redirigir("tcu.py?accion=listado")
    pag.fin()
if __name__ == "__main__":
    form = cgi.FieldStorage()
    accion = form.getvalue("accion", "listado")
    if accion == "listado":
        listado()
    elif accion == "editar":
        editar(form)
    elif accion == "actualizar":
        actualizar(form)
    elif accion == "nuevo":
        nuevo()
    elif accion == "agregar":
        agregar(form)
    elif accion == "eliminar":
        pagi = pagina.Pagina("Eliminar tipo de curso", 20)
        print(htm.h2("No es posible completar la acción"))
        htm.nota("No es posible eliminar un tipo de curso por el momento")
        htm.nota("""Si se eliminara un tipo de curso,
            se deberían eliminar todos los cursos correspondientes, lo cual
            de tratarse de un error, tendría graves consecuencias para todo
            el sistema. De ser necesario, se puede hacer "a mano" y considero
            que es más seguro, por ahora, de esa manera (hasta que pueda
            implementar una forma segura de hacerlo, como por ejemplo listando
            todos los cursos involucrados antes de proceder a la eliminación""")
        print(htm.button("Volver", "tcu.py?accion=listado"))
        pagi.fin()

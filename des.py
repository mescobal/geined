#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Seguimiento de bugs"""
import cgitb; cgitb.enable()
import cgi
import funciones
import datos
import htm
import pagina
def filtro_por_tarea(tarea):
    """Devuelve un filtro para la BDD segun tarea en desarrollo"""
    filtro = ''
    if tarea == '0':
        filtro = 'estado=0'
    elif tarea == '50':
        filtro = 'estado>0 AND estado<100'
    elif tarea == '100':
        filtro = 'estado=100'
    elif tarea == 'todo':
        filtro = ''
    return filtro

def referencia(cero, enc, cien, total):
    """Tabla de referencia de tareas"""
    htm.encabezado_tabla(['Icono', 'Lectura', 'Número'])
    print(htm.tr(
            htm.td(htm.img("./img/0.png", 12, 12)) +
            htm.td(htm.a("des.py?accion=listado&tarea=0", "Tarea sin comenzar")) +
            htm.td(cero)) +
        htm.tr(
            htm.td('<img src="./img/50.png" width="12" height="12" />') +
            htm.td('<A HREF="des.py?accion=listado&tarea=50">Tarea en curso</A>') +
            htm.td(enc)) +
        htm.tr(
            htm.td('<img src="./img/100.png" width="12" height="12" />') +
            htm.td('<A HREF="des.py?accion=listado&tarea=100">Tarea completa</A>') +
            htm.td(cien)) +
        htm.tr(
            htm.td("") +
            htm.td('<A HREF="des.py?accion=listado&tarea=total">Total</A>') +
            htm.td(total)))
    htm.fin_tabla()

def listado(frm):
    """Listado de tareas"""
    desarrollo = datos.Tabla("desarrollo")
    tarea = frm.getvalue("tarea", "0")
    total = desarrollo.num_filas
    desarrollo.filtro = "estado=0"
    desarrollo.filtrar()
    cero = desarrollo.num_filas
    desarrollo.filtro = "estado=100"
    desarrollo.filtrar()
    cien = desarrollo.num_filas
    enc = total - cien - cero
    desarrollo.orden = 'fecha DESC'
    desarrollo.filtro = filtro_por_tarea(tarea)
    desarrollo.filtrar()
    pag = pagina.Pagina("Desarrollo: estado actual")
    print(htm.table(
        htm.tr(
            htm.td("""Los pedidos, preguntas y reguistros de errores serán gestionados \
        fuera del sistema, por Launchpad.</br> Para usar Launchpad deben registrarse previamente con una \
        dirección de correo electrónico.</br>""") +
            htm.td("""<a href='https://bugs.launchpad.net/geined/+filebug'
                target='_blank'>Informar de un error</a></br>
                <a href='https://blueprints.launchpad.net/geined'
                target='_blank'>Pedir nueva caracteristica</a></br>
                <a href='https://answers.launchpad.net/geined'
                target='_blank'>Realizar una pregunta</a></br>""")
            )
        )
    )
    referencia(cero, enc, cien, total)
    htm.nota('Los campos son de hasta 50 caracteres y no se permiten comillas')
    print(htm.button('Nuevo', 'des.py?accion=nuevo'))
    print(htm.button("Volver", "geined.py?accion=principal"))
    htm.encabezado_tabla(["Nº", "Fecha", "Cambios", "Usuario", "Detalle",
        "Notas", "Estado", "Acciones"])
    i = 0
    for fila in desarrollo.resultado:
        htm.fila_alterna(i)
        print(htm.td(fila["id"]))
        print(htm.td(funciones.mysql_a_fecha(fila['fecha'])))
        print(htm.td(funciones.mysql_a_fecha(fila["cambios"])))
        print(htm.td(fila["usuario"]))
        print(htm.td(fila['detalle']))
        print(htm.td(str(fila['notas'])[0:80] + "..."))
        print('<td>')
        if fila['estado'] == 0:
            print(htm.img("./img/0.png", 12, 12))
        elif fila['estado'] >= 100:
            print('<img src="./img/100.png" width="12" height="12" />')
        else:
            print('<img src="./img/50.png" width="12" height="12" />')
        print('</TD>')
        print('<td>')
        htm.boton_editar("des.py?accion=editar&id=" + str(fila["id"]))
        htm.boton_eliminar("des.py?accion=eliminar&id=" + str(fila["id"]))
        print('</td></tr>')
        i = i + 1
    htm.fin_tabla()
    print(htm.button("Volver", "geined.py?accion=principal"))
    pag.fin()

def nuevo():
    """Nuevo item de desarrollo"""
    pag = pagina.Pagina("Desarrollo",  10)
    htm.form_edicion("Nuevo bug o pedido", "des.py?accion=agregar")
    htm.input_texto("Detalle:",  "detalle", "")
    htm.input_texto("Estado:",  "estado",  "")
    htm.input_memo("Notas:",  "notas",  "")
    htm.botones("des.py?accion=listado")
    htm.form_edicion_fin()
    pag.fin()

def agregar(frm):
    """Agregar un registro a la tabla desarrollo"""
    pag = pagina.Pagina("Agregar informe de error o pedido", 20)
    if frm.has_key('detalle'):
        desarrollo = datos.Tabla("desarrollo")
        desarrollo.registro["fecha"] = funciones.fecha_a_mysql(funciones.hoy())
        desarrollo.registro["cambios"] = funciones.fecha_a_mysql(funciones.hoy())
        desarrollo.registro["usuario"] = pag.sesion["usuario"].value
        desarrollo.registro['detalle'] = frm.getvalue('detalle', "")
        desarrollo.registro['notas'] = frm.getvalue("notas", "")
        desarrollo.registro['estado'] = frm.getvalue("estado","0")
        desarrollo.insertar()
        htm.redirigir('des.py?accion=listado')
    else:
        print('Error: faltan variables')
        print(htm.button('Volver', 'des.py?accion=listado'))
    pag.fin()

def editar(frm):
    """Edición de ítem de seguimiento de desarrollo"""
    pag = pagina.Pagina('Desarrollo', 5)
    htm.form_edicion("Editar pendiente", 'des.py?accion=actualizar')
    desarrollo = datos.Tabla("desarrollo")
    desarrollo.buscar('id', frm['id'].value)
    htm.campo_oculto("id", frm['id'].value)
    htm.input_texto('Detalle:', 'detalle', desarrollo.registro['detalle'])
    htm.input_texto('Estado:', 'estado', desarrollo.registro['estado'])
    htm.input_memo("Notas:", 'notas', desarrollo.registro['notas'])
    htm.botones("des.py?accion=listado")
    htm.form_edicion_fin()
    pag.fin()

def actualizar(frm):
    """Actualizar datos de desarrollo"""
    pag = pagina.Pagina('Actualizando datos', 20)
    if frm.has_key("id"):
        ident = frm['id'].value
        desarrollo = datos.Tabla('desarrollo')
        desarrollo.buscar('id', ident)
        desarrollo.registro["cambios"] = funciones.fecha_a_mysql(funciones.hoy())
        desarrollo.registro['detalle'] = frm.getvalue("detalle", "")
        desarrollo.registro['notas'] = frm.getvalue("notas", "")
        desarrollo.registro['estado'] = frm.getvalue("estado", "0")
        desarrollo.actualizar()
        htm.redirigir('des.py?accion=listado')
    else:
        print('Error: faltan variables')
        print(htm.button('Volver', 'des.py?accion=listado'))
    pag.fin()

def main():
    """Funcion principal: evitar ejecucion al importar"""
    form = cgi.FieldStorage()
    accion = form.getvalue("accion", "listado")
    if form.has_key('accion'):
        accion = form['accion'].value
    if accion == 'listado':
        listado(form)
    elif accion == "nuevo":
        nuevo()
    elif accion == "agregar":
        agregar(form)
    elif accion == "actualizar":
        actualizar(form)
    elif accion == "editar":
        editar(form)
    elif accion == "eliminar":
        pag = pagina.Pagina("Eliminando datos", 1)
        desarrollo = datos.Tabla("desarrollo")
        if form.getvalue("id", "0") != 0:
            desarrollo.borrar(form["id"].value)
        else:
            print("No se especificó qué dato borrar")
        htm.redirigir("des.py?accion=listado")
        pag.fin()

if __name__ == "__main__":
    main()

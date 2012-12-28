#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Usuarios"""
import cgi
import cgitb; cgitb.enable()
import funciones
import datos
import htm
import pagina
def listado():
    """Listado de usuarios"""
    pag = pagina.Pagina("Listado de usuarios", 1)
    usuarios = datos.Tabla("usuarios")
    htm.button("Nuevo","usu.py?accion=nuevo")
    htm.button("Volver",'geined.py?accion=sistema')
    htm.encabezado_tabla(["Usuario", "Creación", "Clave", "Nombre", "Nivel", "eMail", "Acciones"])
    for linea in usuarios.resultado:
        htm.fila_resaltada()
        print(htm.td(linea["usuario"]))
        print(htm.td(linea["creacion"]))
        print(htm.td(linea["clave"]))
        print(htm.td(linea["nombre"]))
        print(htm.td(linea["nivel"]))
        print(htm.td(linea["email"]))
        print('<td>')
        htm.boton_detalles('usu.py?accion=detalles&usuario=' + linea["usuario"])
        htm.boton_editar('usu.py?accion=editar&usuario=' + linea["usuario"])
        htm.boton_eliminar('usu.py?accion=eliminar&usuario=' + linea["usuario"])
        print('</td></tr>')
    htm.fin_tabla()
    htm.button('Volver', 'geined.py?accion=sistema')
    pag.fin()
def nuevo():
    """Formulario para nuevo usuario"""
    pag = pagina.Pagina("Usuarios", nivel=1, fecha = 1)
    htm.form_edicion("Nuevo usuario", "usu.py?accion=agregar")
    htm.input_texto("Usuario:", "usuario", "")
    htm.input_fecha("Creación:", "creacion", funciones.fecha_a_mysql(funciones.hoy()))
    htm.input_texto("Clave:", "clave", "")
    htm.input_texto("Nombre:", "nombre", "")
    htm.input_texto("Nivel", "nivel", "")
    htm.input_texto("eMail:", "email", "")
    htm.botones('usu.py?accion=listado')
    htm.form_edicion_fin()
    pag.fin()
def agregar(frm):
    """Agregar nuevo usuario"""
    usuarios = datos.Tabla("usuarios")
    usuarios.buscar("usuario", frm["usuario"].value)
    # ver si existe usuario
    if usuarios.num_filas == 0:
        pag = pagina.Pagina("Agregando datos de usuario")
        usuarios.registro["usuario"] =  frm['usuario'].value
        usuarios.registro['creacion'] = funciones.fecha_a_mysql(frm['creacion'].value)
        usuarios.registro['clave'] = frm['clave'].value
        usuarios.registro['nombre'] = frm['nombre'].value
        usuarios.registro['nivel'] = frm['nivel'].value
        usuarios.registro['email'] = frm['email'].value
        usuarios.insertar()
        htm.redirigir("usu.py?accion=listado")
    else:
        pag = pagina.Pagina("Error", 10)
        htm.duplicado("usu.py")
        pag.fin()
def editar(frm):
    """Editar usuario"""
    usuario = frm["usuario"].value
    usuarios = datos.Tabla("usuarios")
    usuarios.buscar("usuario", usuario)
    pag = pagina.Pagina("Editar datos del usuario", 1)
    htm.form_edicion("Editar datos de usuario", "usu.py?accion=actualizar")
    htm.campo_oculto("usuario", usuario)
    htm.input_texto("Clave:", "clave", usuarios.registro['clave'])
    htm.input_texto("Nombre:", "nombre", usuarios.registro['nombre'])
    htm.input_texto("Nivel:", "nivel", usuarios.registro['nivel'])
    mail = "-"
    if len(usuarios.registro["email"]) > 0:
        mail = usuarios.registro["email"]
    htm.input_texto("eMail:", "email", mail)
    htm.botones('usu.py?accion=listado')
    htm.form_edicion_fin()
    pag.fin()
def actualizar(frm):
    """Rutina de actualizacion de datos de usuario"""
    # Ver si existe el campo usuarios en el URL
    pag = pagina.Pagina("Actualizacion de datos de usuario", 1)
    usuarios = datos.Tabla("usuarios", clave="usuario")
    usuarios.buscar("usuario", frm["usuario"].value)
    # Ver si existe el usuarios que se va a actualizar
    usuarios.registro["clave"] = frm["clave"].value
    usuarios.registro["nombre"] = frm["nombre"].value
    usuarios.registro["nivel"] = frm["nivel"].value
    usuarios.registro["email"] = frm["email"].value
    usuarios.actualizar()
    htm.redirigir("usu.py?accion=listado")
    pag.fin()
def detalles(frm):
    """Detalles de usuarios"""
    pag = pagina.Pagina("Detalles del usuario", 1)
    usuarios = datos.Tabla('usuarios')
    usuarios.buscar("usuario", frm['usuario'].value)
    print("Usuario: " + usuarios.registro['usuario'])
    print("Nombre: " + usuarios.registro['nombre'])
    print("Nivel: " + str(usuarios.registro['nivel']))
    htm.button("Volver","usu.py?accion=listado")
    registro = datos.Tabla('registro')
    registro.orden = "entrada DESC"
    registro.buscar("usuario", frm['usuario'].value)
    htm.encabezado_tabla(["Nº", 'Fecha de sesión'])
    for linea in registro.resultado:
        htm.fila_resaltada()
        print(htm.td(linea["id"]))
        print(htm.td(str(linea['entrada'])))
        print('</tr>')
    htm.fin_tabla()
    htm.button('Volver', 'usu.py?accion=listado')
    pag.fin()
def main():
    form = cgi.FieldStorage()
    accion = form.getvalue("accion", "listado")
    if accion == "listado":
        listado()
    elif accion == "nuevo":
        nuevo()
    elif accion == "agregar":
        agregar(form)
    elif accion == "editar":
        editar(form)
    elif accion == "actualizar":
        actualizar(form)
    elif accion == 'eliminar':
        pagi = pagina.Pagina("Borrando registro de entrada", 1)
        usuarios = datos.Tabla("usuarios", clave="usuario")
        usuarios.borrar(form.getvalue("usuario"))
        htm.redirigir('usu.py?accion=listado')
        pagi.fin()
    elif accion == 'detalles':
        detalles(form)
if __name__ == "__main__":
    main()

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Datos del usuario"""
import cgi
import cgitb ; cgitb.enable()
import htm
import datos
import os
import Cookie
import pagina
def editar():
    """Recuperar variables"""
    sesion = Cookie.SimpleCookie(os.environ.get("HTTP_COOKIE",""))
    logname = sesion['usuario'].value
    usuarios = datos.Tabla("usuarios","usuario")
    depositos = datos.Tabla("depositos")
    usuarios.buscar("usuario", logname)
    pag = pagina.Pagina("Datos del usuario", 20)
    print '<h2>Datos de: ' + logname + '</h2>'
    htm.nota('Si modifica su clave, asegúrese de recordarla ya que de lo contrario no podrá acceder al sistema')
    htm.form_edicion("Editar datos de usuario", 'datos_usuario.py?accion=actualizar')
    htm.campo_oculto("usuario", usuarios.registro['usuario'])
    htm.input_texto("Nombre:", "nombre", usuarios.registro['nombre'])
    htm.input_texto("Clave:", "clave", usuarios.registro['clave'])
    htm.input_texto("e-Mail:", "email", usuarios.registro['email'])
    htm.input_combo("Sucursal habitual:","deposito_id", depositos.resultado, ["id", "deposito"], sesion["deposito_id"]);
    htm.botones('geined.py?accion=principal')
    htm.form_edicion_fin()
    pag.fin()
def actualizar(frm):
    """Actualiza datos del usuario"""
    usuario = frm["usuario"].value
    usuarios = datos.Tabla("usuarios", "usuario")
    usuarios.buscar("usuario", usuario)
    usuarios.registro["clave"] = frm["clave"].value
    usuarios.registro["nombre"] = frm["nombre"].value
    usuarios.registro["email"] = frm["email"].value
    usuarios.registro["deposito_id"] = frm["deposito_id"].value
    usuarios.actualizar()
    execfile("geined.py")
if __name__ == "__main__":
    form = cgi.FieldStorage()
    accion = form.getvalue("accion", "editar")
    if accion == 'editar':
        editar()
    elif accion == 'actualizar':
        actualizar(form)
    else:
        pagina.error_parametros("geined.py?accion=principal")

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Modulo con datos para realizacion de login al sitio Geined"""
import cgi
import cgitb ; cgitb.enable()
import htm
import datos
import Cookie
def pantalla(mensaje):
    """Pantalla generica de login"""
    htm.inicio()
    print '<head>'
    print(htm.title("Entrada al sistema"))
    print '<link type="text/css" href="./css/geinedpy.css" rel="stylesheet" />'
    print '<script type="text/javascript" src="geined.js" charset="utf-8">'
    print '</script></head>'
    print '<body><div id="env_fina">'
    print "<table width='100%'><tr><td><img src='./conf/logo.png' /></td>"
    print(htm.td(htm.h1("Entrada al sistema")))
    print("</tr></table>")
    print(htm.h2(mensaje))
    htm.form_edicion("Ingrese sus datos:", "login.py")
    htm.input_texto("Usuario:", "fusuario", "")
    print(htm.tr(htm.td('Clave:') +
        htm.td('<input type="password" name="fclave">')))
    htm.botones("Salida.html")
    htm.form_edicion_fin()
    print "</body></html>"
def inicio():
    """Rutina que procesa datos de realizacion de login"""
    form = cgi.FieldStorage()
    if form.has_key("fusuario"):
        usuario = form.getvalue("fusuario", "")
        dbase = datos.Tabla("usuarios", "usuario", ins_clave="si")
        dbase.ir_a(usuario)
        #sql = "SELECT * FROM usuarios WHERE usuario='" + usuario + "'"
        #dbase.cursor.execute(sql)
        if dbase.num_filas > 0:
            #El usuario existe, procesar la clave
            clave = form.getvalue('fclave')
            #TODO: Si la clave es  'inhabilitado' salir
            sql_usu = "SELECT * FROM usuarios WHERE usuario ='"+usuario
            sql_usu = sql_usu +"' AND clave ='"+clave +"'"
            dbase.cursor.execute(sql_usu)
            if dbase.cursor.rowcount > 0:
                # La clave es correcta, entrar
                # las mismas cookies se usan en Ruby
                sesion = Cookie.SimpleCookie()
                sesion['autorizado'] = 'si'
                sesion['usuario'] = usuario
                fil_usu = dbase.cursor.fetchone()
                sesion['deposito_id'] = str(fil_usu['deposito_id'])
                sesion['nivel'] = str(fil_usu['nivel'])
                if form.getvalue("parametro")!="no_registrar":
                    #Si ya está registrado, no hacerlo de nuevo
                    registro = datos.Tabla("registro")
                    registro.registro["usuario"] = usuario
                    registro.insertar()
                # Parche para bypasear transitoriamente entrada x Ruby
                # Comentar o descomentar lo que corresponda
                print 'Content-Type: text/html; charset=utf-8'
                print sesion, "\n\n"
                print '<head>'
                htm.title("Entrada al sistema")
                print '<script type="text/javascript" src="geined.js" '
                print 'charset="utf-8"></script>'
                print '</head><body><div id="env_fina">'
                print "Procesando entrada (Python)..."
                #print('<script type="text/javascript">window.location = "geined.py";</script>')
                print "Ingresó al sistema."
                print "Permanecerá conectado hasta que cierre el navegador "
                print "o elija la opción Salir del Menú Principal."
                # TODO: es una desproljidad hacerlo como un forma autoenviado
                print "<form id='autolog' action='geined.py?accion=principal' method='post'>"
                # se envía datos de login a programa que autentica en RUBY
                # NOTA: No voy a usar programas en Ruby en el sitio x un tiempo
                #htm.campo_oculto("fusername",usuario)
                #htm.campo_oculto("fpassword", clave)
                # aclarar que viene de script hecho en Python
                #htm.campo_oculto("vienede","python")
                #print "<input type='submit' value='Continuar' >"
                print "</form>"
                print "<script language='JavaScript' type='text/javascript'>\n"
                print "<!--\n"
                print "document.getElementById('autolog').submit();\n"
                print "//-->\n"
                print "</script>"
                print "</div></body>"
            else:
                mens = "El usuario %s existe, " %  form.getvalue("fusername")
                mens = mens + "pero la clave de acceso es incorrecta. "
                mens = mens + "Por favor intentelo nuevamente. <br>"
                pantalla(mens)
        else:
            mens = 'El nombre de usuario ingresado no existe. Por favor intentelo de nuevo.<br>'
            pantalla(mens )
    else:
        pantalla('Tiene que ingresar al sistema para poder usarlo.<br>')
if __name__ == "__main__":
    inicio()

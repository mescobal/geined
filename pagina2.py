#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Conjunto de rutinas para generar paginas htm"""
import htm
import Cookie
import os
class Pagina:
    """Clase para generar una pagina web"""
    def __init__(self, titulo, nivel=20, fecha=0, tipo="comun"):
        #tipos: comun, boleta, informe, recibo
        self.tipo = tipo
        self.sesion = Cookie.SimpleCookie(os.environ.get("HTTP_COOKIE",""))
        self.fecha = fecha
        accion = self.autorizacion(nivel)
        if accion == "login":
            htm.inicio()
            print('<META HTTP-EQUIV="Refresh" CONTENT="0;URL=Login.php">')
        elif accion == "noautorizado":
            htm.inicio()
            print('<META HTTP-EQUIV="Refresh" CONTENT="0;URL=no_autorizado.html">')
        else:
            self.titulo = titulo
            self.filas_por_pagina = 20
            self.encabezado(self.titulo)
    def estilo(self):
        """Agrega cadena que hace referencia a archivo css"""
        if self.tipo == "boleta":
            print('<link type="text/css" href="./css/boleta.css" rel="stylesheet" />')
        elif self.tipo == "informe":
            print('<link type="text/css" href="./css/greyscale.css" rel="stylesheet" />')
        elif self.tipo == "recibo":
            print('<link type="text/css" href="./css/recibo.css" rel="stylesheet" />')
        else:
            print('<link type="text/css" href="./css/geined3.css" rel="stylesheet" />')
    def encabezado(self, titulo):
        """Encabezado de pagina web"""
        htm.inicio()
        print '<head>'
        if self.fecha >= 1:
            print '<style type="text/css">@import url(./js/calendar-win2k-1.css);</style>'
            print '<script type="text/javascript" src="./js/calendar.js"></script>'
            print '<script type="text/javascript" src="./js/lang/calendar-es.js"></script>'
            print '<script type="text/javascript" src="./js/calendar-setup.js"></script>'
        print '<script type="text/javascript" src="geined.js" charset="utf-8"></script>'
        if self.tipo == "boleta":
            print(htm.title("Boleta"))
        else:
            print(htm.title(self.titulo))
        self.estilo()
        #print '</head><body><div id="envoltura">'
        print '</head><body>'
        if self.tipo == "comun":
            print('<div class="topbar" align="center">')
            print('<img src="./img/minilogo.png" STYLE="position:absolute; TOP:17px; LEFT:15px">')
            print('<div align="center">Usuario: ' + self.sesion["usuario"].value + " - Sucursal: " + self.sucursal() + "</div>")
            print("<a title='Inicio' href='geined.py'>")
            print('<img src="./img/Home.png" STYLE="position:absolute; TOP:15px; RIGHT:15px" height="24" width="24"></a>')
            print("</div>")
            print('<div class="cuerpo" align="center">')
    def fin(self):
        """Tags de finalizacion de una pagina"""
        if self.fecha >= 1:
            print(htm.script_fecha())
        if self.fecha >= 2:
            print(htm.script_fecha2())
        print('</div></body>')
    def autorizacion(self, niv):
        """Rutina para autorizar ingreso a una pagina"""
        # 20: cualquiera 10: docente 5: recepcion 4: Adriana
        # 3: Hassan / Leo 2: Mariana 1: Marcelo
        # if not self.sesion.has_key("nivel"):
        if not "nivel" in self.sesion:
            # Imprime encabezado de pagina web
            return "login"
        else:
            nivel_sesion = int(self.sesion["nivel"].value)
            if nivel_sesion > niv:
                return "noautorizado"
    def sucursal(self):
        """Devuelve nombre de la sucursal"""
        sucursal = "Sin asignar"
        deposito_id = 0
        if "deposito_id" in self.sesion:
            if self.sesion["deposito_id"].value == "None":
                deposito_id = 1
            else:
                deposito_id = int(self.sesion['deposito_id'].value)
        #TODO: debería recuperar la sucursal de la base de datos
        if deposito_id == 1:
            sucursal = "Central"
        elif deposito_id == 2:
            sucursal = "Costa de Oro"
        elif deposito_id == 3:
            sucursal = "Carrasco"
        return sucursal
def error_parametros(retorno):
    """Devuelve página con error en parámetros"""
    pag = Pagina("Error de parámetros", 20)
    print("Hay un error en los parámetros pasados<br />")
    print htm.button("Volver", retorno)
    pag.fin()
def error_variable(retorno):
    """Devuelve una página con el error"""
    pag = Pagina("Error de variables", 20)
    print "Faltan variables para realizar la operacion<br />"
    print htm.button("Volver", retorno)
    pag.fin()
def duplicado(retorno):
    """Devuelve una página con error de duplicado"""
    pag = Pagina("Registro duplicado", 20)
    print("El registro que intenta agregar ya existe<br />")
    print(htm.button("Volver", retorno))
    pag.fin()
def no_autorizado(retorno):
    """Pone pagina de acceso no autorizado"""
    pag = Pagina("Acceso no autorizado", 20)
    htm.nota('Usted no se encuentra autorizado para ver esta página')
    print htm.button('Volver', retorno)
    pag.fin()

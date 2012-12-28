#!/usr/bin/env ruby
# Conjunto de rutinas para generar paginas htm
require 'cgi'
require 'htm'
class Pagina
    # Clase para generar una pagina web
    def initialize(titulo, nivel=20, fecha=0, tipo="comun")
        #tipos: comun, boleta, informe
        @cgi = CGI.new("html4")
        @tipo = tipo
        @sesion = {}
        @fecha = fecha
        self.leer_sesion
        accion = autorizacion(nivel)
        if accion == "login":
            htm.inicio()
            print('<META HTTP-EQUIV="Refresh" CONTENT="0;URL=Login.php">')
        elsif accion == "noautorizado":
            htm.inicio()
            print('<META HTTP-EQUIV="Refresh" CONTENT="0;URL=no_autorizado.html">')
        else
            @titulo = titulo
            @filas_por_pagina = 20
            self.encabezado(titulo)
        end
    end
    def estilo
        """Agrega cadena que hace referencia a archivo css"""
        if @tipo == "boleta"
            print('<link type="text/css" href="./css/boleta.css" rel="stylesheet" />')
        elsif @tipo == "informe"
            print('<link type="text/css" href="./css/greyscale.css" rel="stylesheet" />')
        else
            print('<link type="text/css" href="./css/geinedpy.css" rel="stylesheet" />')
        end
    end
    def encabezado(titulo)
        """Encabezado de pagina web"""
        htm.inicio
        print '<head>'
        if @fecha >= 1
            print '<style type="text/css">@import url(./js/calendar-win2k-1.css);</style>'
            print '<script type="text/javascript" src="./js/calendar.js"></script>'
            print '<script type="text/javascript" src="./js/lang/calendar-es.js"></script>'
            print '<script type="text/javascript" src="./js/calendar-setup.js"></script>'
        end
        print '<script type="text/javascript" src="geined.js" charset="utf-8"></script>'
        if @tipo == "boleta"
            print(htm.title("Boleta"))
        else
            print(htm.title(self.titulo))
        end
        self.estilo
        #print '</head><body><div id="envoltura">'
        print '</head><body><div align="center">'
        if @tipo == "comun"
            print "<table class='tmenu'><tr>"
            print(htm.td(htm.img('./conf/logo.png')))
            #celda("<h1>" + titulo + "</h1>")
            #print "</tr>"
        end
        #if not self.sesion.has_key("deposito_id"):
        if not @sesion.include?("deposito_id")
            sucursal = "Sin asignar"
            deposito_id = 0
        else
            if @sesion["deposito_id"].value == "None"
                deposito_id = 1
            else
                deposito_id = int(@sesion['deposito_id'].value)
            end
        end
        if deposito_id == 1
            sucursal = "Central"
        elsif deposito_id == 2
            sucursal = "Costa de Oro"
        elsif deposito_id == 3
            sucursal = "Carrasco"
        else
            sucursal = "xxxx"
        end
        if @tipo == "comun"
            #celda(self.sesion["usuario"].value + " en " + sucursal, "d")
            #print "<tr><td>" + self.sesion["usuario"].value + "  en " + sucursal  +"</td>"
            print('<td align="right">')
            print("<a title='Inicio' href='geined.py'>")
            # print ("<img src='./img/inicio.png' width='32' height='32'></a>")
            print ("<img src='./img/inicio.png'></a>")
            print("<a title='Reportar un error o idea' href='des.py'> \
            <img src='./img/reportar.png'></a>")
            # TODO: ver si además hay que cambar suc en Python / Ruby
            print("<a title='Cambiar de sucursal' href='suc.php'> \
            <img src='./img/cambiar.png'></a>")
            print "</td></tr></table>"
            print("<table class='tmenu2'><tr><td align='left'>" + titulo + "</td>")
            print("<td align='right'>"+ self.sesion["usuario"].value + 
                " en " + sucursal +"</td></tr></table>")
        end
    end
    def fin
        """Tags de finalizacion de una pagina"""
        if @fecha >= 1
            print(htm.script_fecha())
        end
        if @fecha >= 2
            print(htm.script_fecha2())
        end
        print('</div></body>')
    end
    def autorizacion(niv)
        """Rutina para autorizar ingreso a una pagina"""
        # 20: cualquiera 10: docente 5: recepcion 4: Adriana
        # 3: Hassan / Leo 2: Mariana 1: Marcelo
        # if not self.sesion.has_key("nivel"):
        if not @sesion.has_key?("nivel")
            # Imprime encabezado de pagina web
            return "login"
        else
            nivel_sesion = int(@sesion["nivel"].value)
            if nivel_sesion > niv
                return "noautorizado"
            end
        end
    end
    def leer_sesion
        for item in @cgi.cookies["rubyweb"]
            par = item.split("=")
            @sesion[par[0]] = par[1]
        end
        @deposito_id = @sesion['deposito_id'].to_i
        case @deposito_id
            when 1 then @sucursal = "Central"
            when 2 then @sucursal = "Costa de Oro"
            when 3 then @sucursal = "Carrasco"
        end
    end
end
def error_parametros(retorno)
    """Devuelve página con error en parámetros"""
    pag = Pagina.new("Error de parámetros", 20)
    print("Hay un error en los parámetros pasados<br />")
    print htm.button("Volver", retorno)
    pag.fin()
end
def error_variable(retorno)
    """Devuelve una página con el error"""
    pag = Pagina("Error de variables", 20)
    print "Faltan variables para realizar la operacion<br />"
    print htm.button("Volver", retorno)
    pag.fin()
end
def duplicado(retorno)
    """Devuelve una página con error de duplicado"""
    pag = Pagina("Registro duplicado", 20)
    print("El registro que intenta agregar ya existe<br />")
    print(htm.button("Volver", retorno))
    pag.fin()
end
def no_autorizado(retorno)
    """Pone pagina de acceso no autorizado"""
    pag = Pagina("Acceso no autorizado", 20)
    htm.nota('Usted no se encuentra autorizado para ver esta página')
    print htm.button('Volver', retorno)
    pag.fin()
end
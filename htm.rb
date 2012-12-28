#!/usr/bin/env ruby
# Conjunto de rutinas para generar paginas htm
require 'cgi'
require 'funciones'
# Clase para generar una página web
class Pagina
  attr_accessor :titulo, :nivel, :cgi, :fecha
  def initialize
    @cgi = CGI.new("html4")
    @tipo = "comun"
    @fecha = 0
    @titulo = "Sin titulo"
    @sesion = {}
    @filas_por_pagina = 20
    @cascada = "./css/geinedrb.css"
    @sucursal = "Sin asignar"
    @deposito_id = 0
    @nivel = 20
    leer_sesion
  end
  # Lee una sesión y almacena datos en variable
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
  #Rutina para autorizar ingreso a una pagina
    # 20: cualquiera 10: docente 5: recepcion 4: Adriana
    # 3: Hassan / Leo 2: Mariana 1: Marcelo
  def autorizacion
    if @sesion["nivel"] == nil
      redirigir("Login.php")
    else
      nivel_sesion = @sesion["nivel"].to_i
      redirigir("no_autorizado.html") if nivel_sesion > @nivel
    end
  end
  # Imprime encabezado de pagina web
  def inicio
    puts 'Content-Type: text/html; charset=utf-8'
    puts ""
  end
  # Encabezado de pagina web
  def encabezado
    autorizacion
    case @tipo
      when "boleta" then @cascada = "./css/boleta.css"
      when "informe" then @cascada = "./css/greyscale.css"
      when "recibo" then @cascada = "./css/recibo.css"
    end
    contenido_fecha = ''
    if @fecha >= 1
      contenido_fecha << '<style type="text/css">@import url(./js/calendar-win2k-1.css);</style>'
      contenido_fecha << '<script type="text/javascript" src="./js/calendar.js"></script>'
      contenido_fecha << '<script type="text/javascript" src="./js/lang/calendar-es.js"></script>'
      contenido_fecha << '<script type="text/javascript" src="./js/calendar-setup.js"></script>'
    end
    inicio
    puts @cgi.head{
      '<script type="text/javascript" src="./js/alianza.js" charset="utf-8"></script>' +
      @cgi.title{@titulo} +
      @cgi.link("type"=>"text/css", "href"=>@cascada, "rel"=>"stylesheet") +
      contenido_fecha
    }
    puts '<body>'
    if @tipo != "boleta"
        puts "<div class='nota'>"
      puts @cgi.table{
        @cgi.tr{
          @cgi.td{@cgi.img('./img/logo2009a.jpeg')} +
          @cgi.td{@cgi.h1{@titulo}} +
          @cgi.td{"Usted se encuentra en: #{@sucursal}"} +
          @cgi.td("align"=>"right"){
            @cgi.a("geined.py"){"Inicio"} + " | " +
            @cgi.a("des.py"){"Reportar error"} + " | " +
            @cgi.a("suc.php"){"Cambiar de sucursal"}
          }
        }
      }
        puts "</div>"
    end
  end
  def duplicado(pag)
    # Genera html de error por existencia de duplicado
    @titulo = "Error: duplicado"
    encabezado
    texto = 'Ya existe un dato igual al que usted intenta agregar.'
    texto = texto + ' Verifique el dato e inténtelo nuevamente'
    nota(texto)
    boton('Volver', pag)
  end
  def redirigir(url)
    # Redirige usando javascript a otra pagina
    puts @cgi.script("type"=>"text/javascript"){"window.location = '#{url}';"}
  end
  def fin
    # Tags de finalizacion de una pagina
    script_fecha if @fecha >= 1
    script_fecha2 if @fecha >= 2
    puts '</body></html>'
  end
  def script_fecha
    # Imprime en una pagina web un javascript para manejo de fechas
    puts @cgi.script("type"=>"text/javascript"){"
      Calendar.setup({
      inputField     :    'f_date_b',     //*
      ifFormat       :    '%d/%m/%Y',
      showsTime      :    false,
      button         :    'f_trigger_b',  //*
      step           :    1
      });"}
  end
  # Script alternativo para manejar dos fechas en una pagina
  def script_fecha2
    puts @cgi.script("type"=>"text/javascript"){"
      Calendar.setup({
      inputField     :    'f_date_b2',
      ifFormat       :    '%d/%m/%Y',
      showsTime      :    false,
      button         :    'f_trigger_b2',
      step           :    1
      });"}
  end
  def nota(texto)
    # Imprime una tabla con texto pequeno
    puts "<div class='nota'>" + @cgi.table{@cgi.tr{@cgi.td{texto}}} + "</div>"
  end

  # Imprime boton de enviar formulario con texto = Aceptar
  def botones
    puts @cgi.tr{@cgi.td{@cgi.submit("Aceptar")}}
  end
  # Genera pagina de confirmacion de accion de borrar. Da posibilidad de volver
  def confirmar_borrar(ident, pag)
    @pag.titulo = "Confirmar eliminación de registro"
    @pag.nivel = 20
    encabezado
    nota('¿Esta seguro que desea eliminar este registro?')
    puts @cgi.form("post", "#{pag}?accion=eliminar"){
      @cgi.hidden("id", ident) +
      @cgi.submit("Confirmar")
    }
    boton('Volver', pag)
    fin
  end
  def celda(texto, alineado="left")
    # Imprime una celda con el TEXTO especificado
    puts @cgi.td("align"=>alineado){texto.to_s}
  end
  def fila_datos(texto, datos)
    # Imprime una hilera con 2 celdas: una de texto y otra de datos
    puts @cgi.tr{@cgi.td{texto} + @cgi.td{datos}}
  end
  def linea_moneda(texto)
    # Imprime una celda con un valor monetario adentro
    print '<td align="right">' + moneda(texto)  + '</td>'
  end
  def linea_numero(texto, decimales=2)
    # Imprime una celda con un número formateado con 2 decimales"""
    print("<td align='right'>" + numero(texto, decimales, '.', '') + "</td>")
  end
  def no_autorizado(retorno)
    # Pone pagina de acceso no autorizado
    @titulo = "Acceso no autorizado"
    @nivel = 20
    encabezado
    nota('Usted no se encuentra autorizado para ver esta página')
    boton('Volver', retorno)
    fin
  end
  def script_noenter
    # Impide que funcione la tecla enter en una pagina
    puts '<script type="text/javascript">
      function stopRKey(evt) {
      var evt = (evt) ? evt : ((event) ? event : null);
      var node = (evt.target) ? evt.target : ((evt.srcElement) ? evt.srcElement : null);
      if ((evt.keyCode == 13) && (node.type=="text"))  {return false;}
      }
      document.onkeypress = stopRKey;
      </script>;'
  end
  def input_fecha(texto, campo, valor)
    # Crea celdas contiguas con texto y campo de texto
    puts @cgi.tr{
      @cgi.td{texto} +
      @cgi.td{
        "<input type='text' name='#{campo}' id='f_date_b' value='#{valor}'>" +
        "<BUTTON TYPE='reset' ID='f_trigger_b'>...</button>"
      }
    }
  end
  def input_fecha2(texto, campo, valor)
    # Crea celdas contiguas con texto y campo de texto
    puts @cgi.tr{
      @cgi.td{texto} +
      @cgi.td{
        '<input type="text" name="' + campo + '" id="f_date_b2" value="' + valor + '">' +
        '<BUTTON TYPE="reset" ID="f_trigger_b2">...</button>'
      }
    }
  end
  def input_texto(texto, campo, valor, ancho=20)
    # Imprime celda con un texto y campo para llenarlo, el ancho se puede determinar
    puts @cgi.tr{
      @cgi.td{texto} +
      @cgi.td{"<input type='text' name='#{campo}' value='#{valor}' size='#{ancho}'/>"}
    }
  end
  # Imprime un campo de ingreso de valor numerico
  def input_numero(texto, campo, valor, decimales=2)
    texto = texto.to_s
    valor = valor.to_f if valor.class == String
    puts @cgi.tr{
      @cgi.td{texto} +
      @cgi.td{"<input type='text' style='text-align:right' name='#{campo}'
value='#{numero(valor, decimales)}'>"}
    }
  end
  def input_memo(texto, campo, valor)
    # Imprime una linea con una celda con texto y otra con un campo memo
    print @cgi.tr{
      @cgi.td{texto} +
      @cgi.td{textarea(campo,10,50){valor}}
    }
  end
  def formulario(accion)
    # Imprime el encabezado de un formulario
    puts "<form action='#{accion}' method='POST'>"
  end
  def fin_tabla
    # Imprime tags de finalizacion de una tabla
    puts '</tbody></table>'
  end
    # Linea con celda con texto y otra con combobox
    # @TODO Problema con COMBOBOX, convertir resultados (hash) en array
    def input_combo(texto, campo, resultado, valor)
        puts '<TR>'
        puts @cgi.td{texto}
        print "<td><SELECT NAME='#{campo}'>"
        puts resultado
        while fil = resultado.fetch_row do
            print "<option value='#{fil[0].to_s}'"
            if fil[0].to_s == valor
                print 'selected="selected"'
            end
            puts ">#{fil[1]}</option>"
        end
        puts '</select></td></tr>'
    end
    def boton(texto, accion)
        # Pone un boton
        puts "<input type='button' value='#{texto}' onClick='parent.location=\"#{accion}\"'/>"
    end
    def imagen(img)
        # Pone imagen con caracteristicas predeterminadas"""
        puts "<img src='./img/#{img}%s' width='64' height='64' border='0'>"
    end
    def encabezado_tabla(arr)
        # A partir de un array arma el encabezado de una tabla"""
        #print '<table width="100%"><thead><tr>'
        print('<table><thead><tr>')
        for lin in arr
            puts @cgi.th{lin}
        end
        print '</tr></thead><tbody>'
    end
    def campo_oculto(variable, dato)
        # Imprime un campo oculto
        puts @cgi.hidden(variable, dato)
    end
    def fin_formulario
        # Termina el formulario
        puts '</form>'
    end
    def input_input(tipo, nombre, valor='')
        # Imprime un campo tipo INPUT
        puts "<input type='#{tipo}'name='#{nombre}' value='#{valor}'></input>"
    end
    def input_check(texto, variable, valor)
        # Imprime 2 celdas, una con texto y otra con un checkbox"""
        print '<TR><TD>'
        print texto
        adicional = "checked" if valor == "1"
        print "</TD><TD><INPUT TYPE='checkbox' "
        print "NAME='#{variable}' VALUE='1' #{adicional}></TD></TR>"
    end
    def linea
        # Linea horizontal"""
        print '<hr />'
    end
    def btn_confirmar_borrar(url)
        # Pone un boton de borrar, de donde sale un dialogo, de donde se redirige a una url
        print '<input type=button value="Borrar" onClick="if(confirm('
        print "'¿Desea borrar este registro?'"+')) window.location='+"'"+url+"';"+'">'
    end
    # Pone un boton para confirmar, saca un cuadro con el TEXTO y redirige a url
    def btn_confirmar(btn, texto, url)
        print '<input type=button value="'+btn
        print '" onClick="if(confirm('+"'"+texto+"'"+')) window.location='+"'"+url+"';"+'">'
    end
    def fila_alterna(i)
        # Genera colores alternos para filas de una tabla
        if (i % 2) == 0
            puts "<tr>"
        else
            puts "<tr class='odd'>"
        end
    end
    def imagen_menu(img, enlace, texto)
        # Imprime una celda con una imagen, enlace y texto"""
        print "<td align='center'><a href='#{enlace}'><img src='./img/#{img}' width='64' height='64' align='top' border='0'></a>#{texto}</td>"
    end
    #  Devuelve una página con el error
    def error_variable(retorno)
        @titulo = "Error de variables"
        @nivel = 20
        encabezado
        print "Faltan variables para realizar la operacion<br />"
        boton("Volver", retorno)
        fin
    end
    def error_parametros(retorno)
        # Devuelve página con error en parámetros
        pag = Pagina.new("Error de parámetros", 20)
        print("Hay un error en los parámetros pasados<br />")
        boton("Volver", retorno)
        pag.fin()
    end
    def navegador(este_archivo, pagina_actual, total_paginas, union="?")
        # Imprime un navegador al pie de una tabla
        nav = ""
        pagina_actual = pagina_actual.to_i
        total_paginas = total_paginas.to_i
        for n in (1..total_paginas + 1)
            if n == pagina_actual
                nav << " #{pagina_actual.to_s} "
            else
                nav << " <a href='#{este_archivo}#{union}pagina=#{n.to_s}'>#{n.to_s}</a> "
            end
        end
        # enlaces a primero - anterior - posterior - ultimo
        if pagina_actual > 1
            pag = pagina_actual -1
            prev = " <a href='#{este_archivo}#{union}pagina=#{pag.to_s}'>[<-]</a> "
            prim = " <a href='#{este_archivo}#{union}pagina=1'>[<<]</a> "
        else
            prev = " "
            prim = " "
        end
        if pagina_actual < total_paginas
            pag = pagina_actual + 1
            sig = " <a href='#{este_archivo}#{union}pagina=#{pag.to_s}'>[->]</a> "
            ult = " <a href='#{este_archivo}#{union}pagina=#{total_paginas + 1}'>[>>]</a> "
        else
            sig = " "
            ult = " "
        end
        print("<hr />")
        print("<center>" + prim + prev + nav + sig + ult + "</center>")
        print("<hr />")
    end
end


#!/usr/bin/env ruby
# Funciones generales
require "date"
class Fecha
    attr_accessor :dia, :mes, :ano
    attr_reader :fecha
    EPOCA = 40
    def initialize(cadena,  formato='eu')
        if cadena.class == Date
            @fecha = cadena
        elsif cadena.class == String
            sep = separador(cadena)
            casilleros = cadena.split(sep)
            if casilleros.size != 3
                @fecha = Date.today
            else
                if (formato=='eu') or (formato=='us')
                    if casilleros[2].size !=4
                        if casilleros[2].to_i > EPOCA
                            casilleros[2] = "19#{casilleros[2]}"
                        else
                            casilleros[2] = "20#{casilleros[2]}"
                        end
                    end
                    if casilleros[0].size == 1
                        casilleros[0] = '0' + casilleros[0]
                    end
                    if casilleros[1].size == 1
                        casilleros[1] = '0' + casilleros[1]
                    end
                    cadena = "#{casilleros[0]}#{sep}#{casilleros[1]}#{sep}#{casilleros[2]}"
                end
                
                case formato
                when 'eu'
                    @fecha = Date.strptime(cadena, "%d#{sep}%m#{sep}%Y")
                when 'mysql'
                    if not cadena.include?('-')
                        @fecha = Date.today
                    else
                        casilleros = cadena.split('-')
                        if casilleros[0].size != 4
                            @fecha = Date.today
                        else
                            @fecha = Date.strptime(cadena, '%Y-%m-%d')
                        end
                    end
                when 'us'
                    @fecha = Date.strptime(cadena, "%m#{sep}%d#{sep}%Y")
                else
                    @fecha = Date.today
                end
            end
        else
            @fecha = Date.today
        end
        @ano = @fecha.year
        @mes = @fecha.month
        @dia = @fecha.day
    end
    def eu
        if @dia < 10
            dia = "0#{@dia.to_s}"
        else
            dia = @dia.to_s
        end
        if @mes < 10
            mes = "0#{@mes.to_s}"
        else
            mes = @mes.to_s
        end
        return "#{dia}/#{mes}/#{@ano}"
    end
    def us
        if @dia < 10
            dia = "0#{@dia.to_s}"
        else
            dia = @dia.to_s
        end
        if @mes < 10
            mes = "0#{@mes.to_s}"
        else
            mes = @mes.to_s
        end
        return "#{mes}/#{dia}/#{@ano}"
    end
    def iso
        return @fecha.to_s
    end
    def mysql
        return @fecha.to_s
    end
end
def hoy
  return Date.today.strftime("%d/%m/%Y")
end
# Determina el separador de una fecha
def separador(cadena)
    sep = ''
    #separar componentes
    if cadena.include?('/')
        sep = '/'
    elsif cadena.include?('-')
        sep = '-'
    end
    return sep
end
# Transforma una cadena de números en una cadena con formato moneda"""
def moneda(num)
    mon = numero(num,2)
    mon = "$ " + mon
    return mon
end
# Convierte fecha en formato mysql a legible
def mysql_a_fecha(fecha)
    if fecha.class == Time or fecha.class == Date
        fecha2 = fecha.strftime("%d/%m/%y")
    elsif fecha.class == NilClass
        fecha2 = ""
    else
        ano = fecha[0..3]
        mes = fecha[5..6]
        dia = fecha[8..9]
        fecha2 = dia + "/" + mes + "/" + ano
    end
    return fecha2
end
# Numero con separadores de miles y decimales según lo determinado
def numero(num, lugares=0)
    if num == nil
        num = 0
    end
    tmp = format("%.#{lugares}f", num)
    partes = tmp.split(".")
    entero = partes[0].to_s
    decimal = partes[1].to_s
    ent = ts(entero)
    if decimal != ''
        ent = ent + "."
    end
    return ent + decimal
end
# Numero con separadores de miles
def ts( st )
  st = st.reverse
  r = ""
  max = if st[-1].chr == '-'
    st.size - 1
  else
    st.size
  end
  if st.to_i == st.to_f
    1.upto(st.size) {|i| r << st[i-1].chr ; r << ',' if i%3 == 0 and i < max}
  else
    start = nil
    1.upto(st.size) {|i|
      r << st[i-1].chr
      start = 0 if r[-1].chr == '.' and not start
      if start
        r << ',' if start % 3 == 0 and start != 0  and i < max
        start += 1
      end
    }
  end
  r.reverse
end

# Convierte de fecha formato Ruby a fecha comun
def rubyfecha_a_fecha(t)
    fecha = t.strftime("%d/%m/%y")
    return fecha
end
# Convierte de fecha común a formato MySQL
def fecha_a_mysql(fecha)
  return Date.strptime(fecha,"%d/%m/%Y").to_s
end
def fecha_a_date(fecha)
    return Date.strptime(fecha, "%m/%d/%y").to_s
end
def date_a_fecha(fecha)
    return Date.strptime(fecha, "%d/%m/%y").to_s
end
# Reemplaza CADENA con REEMPLAZO en POSICION, sin alterar la longitud de la cadena
def substr_replace(cadena, reemplazo, posicion)
    s = cadena[0..posicion] + reemplazo + cadena[posicion + reemplazo.size..cadena.size]
    return s
end

if __FILE__ == $0
    print "Es un módulo no ejecutable"
end

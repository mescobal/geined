#!/usr/bin/env ruby
require 'cgi_exception'
require 'htm'
pag = Pagina.new('Multas y recargos', 5)
puts pag.cgi.table{
    pag.cgi.caption{'Multas y recargos'} +
    pag.cgi.tr{
        pag.cgi.td{'Cuota'} +
        pag.cgi.td{pag.cgi.text_field('cuota')}
    } +
    pag.cgi.tr{
        pag.cgi.td{'Dias de atraso'} +
        pag.cgi.td{pag.cgi.text_field('dias')}
    } +
    pag.cgi.tr{
        pag.cgi.td{'Multa:'} +
        pag.cgi.td{pag.cgi.text_field('multa')}
    }

}
pag.fin

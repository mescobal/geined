#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Inscripcion, tercer paso: confirmar datos"""
import cgi
import cgitb; cgitb.enable()
import datos
import pagina
import htm
def paso_3(frm):
    """Inscripcion, tercer paso: confirmar datos"""
    pag = pagina.Pagina("Inscripción: confirmar datos", 4)
    # Recuperar variables
    cliente_id = frm.getvalue("cliente_id", 0)
    curso_id = frm.getvalue("curso_id", 0)
    clientes = datos.Tabla("clientes")
    tipo_pago = datos.Tabla("tipo_pago")
    tipo_pago.filtrar()
    cursos = datos.Tabla("cursos")
    clientes.ir_a(cliente_id)
    cursos.ir_a(curso_id)  
    htm.formulario("alu_inscribir.py")
    htm.encabezado_tabla(["Campo", "Valor"])
    # CLiente
    print(htm.hidden("cliente_id", cliente_id))
    print('<tr><td>Nombre:</td><td>' + clientes.registro['nombre'] + '</td></tr>')
    # Curso
    print(htm.hidden("curso_id", curso_id))
    print('<tr><td>Curso:</td><td>' + cursos.registro['curso'] + '</td></tr>')
    htm.input_combo("Tipo de pago:", "tipo_pago_id", tipo_pago.resultado, ["id", "tipo"], "")
    htm.input_numero("Cuota:", "cuota", "")
    # Definir el asunto PAGO
    htm.botones("geined.py?accion=recepcion")
    htm.fin_formulario()
    htm.fin_tabla()
    pag.fin()
def main():
    """Principal"""
    form = cgi.FieldStorage()
    paso_3(form)

if __name__ == "__main__":
    main()
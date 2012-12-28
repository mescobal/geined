#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Hace efectiva la inscripción del alumno"""
import cgi
import cgitb ; cgitb.enable()
import htm
import datos
import pagina
def main():
    """Rutina principal para inscribir alumno"""
    # @TODO: Falta considerar que pasa si no se ingresan variables POST
    form = cgi.FieldStorage()
    if not form.has_key("cliente_id"):
        pagina.error_variable("geined.py?accion=recepcion")
    else:
        if not form.has_key("curso_id"):
            pagina.error_variable("geined.py?accion=recepcion")
        else:
            cliente_id = form["cliente_id"].value
            curso_id = form["curso_id"].value
            alumnos = datos.Tabla("alumnos")
            alumnos.filtro = " (cliente_id = '%s') AND (curso_id = '%s')" % (cliente_id, curso_id)
            alumnos.filtrar()
            if alumnos.num_filas == 0:
                alumnos.registro["cliente_id"] = cliente_id
                alumnos.registro["curso_id"] = curso_id
                alumnos.registro["tipo_pago_id"] = form["tipo_pago_id"].value
                alumnos.registro["cuota"] = form["cuota"].value
                alumnos.insertar()
                # se cambia la categoría del cliente
                clientes = datos.Tabla("clientes")
                clientes.ir_a(cliente_id)
                clientes.resultado["categoria_id"] = 2
                clientes.actualizar()
                pag = pagina.Pagina("Inscripciones", 10)
                print htm.h2("Alumno inscripto")
                print htm.button("Ir a caja","caja.php?accion=listado")
                print htm.button("Volver","geined.py?accion=recepcion")
                pag.fin()
            else:
                htm.duplicado("geined.py?accion=recepcion")
if __name__ == "__main__":
    main()

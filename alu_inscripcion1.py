#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Inscripcion paso 1: agregar cliente"""
import cgi
import cgitb; cgitb.enable()
import datos
import htm
import pagina
def paso_1(frm):
    """Inscripcion paso 1: agregar cliente"""
    cliente_id = frm.getvalue("cliente_id", 0)
    if cliente_id != 0:
        htm.redirigir("alu_inscipcion2.py?cliente_id=" + str(cliente_id))
    else:
        pag = pagina.Pagina("Inscripción - Paso 1", 4)
        print(htm.h2("Elegir cliente")) 
        print(htm.table(
            htm.tr(
                htm.td('Buscar' +
                    '<form action = "alu_inscripcion1.py" method="post">' +
                    '<input type="text" name="busqueda">' +
                    '<input type="submit" value="Buscar"></form>') +
                htm.td(htm.button("Volver", "geined.py?accion=recepcion"))
                )
            )
        )
        busqueda = frm.getvalue("busqueda", "")
        clientes = datos.Tabla("clientes")
        cat_clientes = datos.Tabla("cat_clientes")
        clientes.orden = 'nombre'
        if busqueda != "":
            clientes.filtro = 'nombre LIKE "%' + busqueda + '%" '
        clientes.filtrar()
        i = 0
        htm.encabezado_tabla(["Nombre", "Categoría", "Notas", "Acciones"])
        for fila in clientes.resultado:
            ident = fila['id']
            htm.fila_alterna(i)
            print(htm.td(fila['nombre']))
            cat_clientes.ir_a(fila["categoria_id"])
            categoria = cat_clientes.registro['categoria']
            print(htm.td(categoria))
            print(htm.td(fila['notas']))
            print(htm.td(
                htm.button("Inscribir", "alu_inscripcion2.py?cliente_id=" + 
                str(ident))))
            print('</tr>')
            i = i +1
        htm.fin_tabla()
        print(htm.button('Volver', 'geined.py?accion=recepcion'))
        pag.fin()
def main():
    """Principal"""
    form = cgi.FieldStorage()
    paso_1(form)

if __name__ == "__main__":
    main()
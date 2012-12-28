#!/usr/bin/env python
# -*- coding: utf-8 -*-
import cgi 
import cgitb; cgitb.enable()
import datos
import htm
import pagina
def listado(frm):
    """Listado de detalles del cliente"""
    # Recuperar variables
    cliente_id = frm.getvalue("id")
    # Bases de datos
    clientes = datos.Tabla("clientes")
    cat_clientes = datos.Tabla("cat_clientes")
    alumnos = datos.Tabla("alumnos")
    cursos = datos.Tabla("cursos")
    # Busquedas
    clientes.ir_a(cliente_id)
    cat_clientes.ir_a(clientes.registro["categoria_id"])
    alumnos.filtro = "cliente_id=" + str(cliente_id)
    alumnos.filtrar()
    # Pagina
    pag = pagina.Pagina('Detalles del cliente', 5)   
    htm.encabezado_tabla(['Cliente:', clientes.registro["nombre"]])
    print(htm.tr(htm.td('Dirección:') + htm.td(clientes.registro["direccion"])) +
        htm.tr(htm.td("Teléfono:") + htm.td(clientes.registro["telefono"])) +
        htm.tr(htm.td("eMail:") + htm.td(clientes.registro["email"])) +
        htm.tr(htm.td("Categoría:") + htm.td(cat_clientes.registro["categoria"])) +
        htm.tr(htm.td("CI:") + htm.td(clientes.registro["ci"])) +
        htm.tr(htm.td("Notas:") + htm.td(clientes.registro["notas"])))
    htm.fin_tabla()
    htm.encabezado_tabla(["Estado", "Curso"])
    i = 0
    for fila in alumnos.resultado:
        cursos.ir_a(fila["curso_id"])
        htm.fila_alterna(i)
        if cursos.registro["finalizado"] == 1:
            print(htm.td("Cursó:"))
        else:
            print(htm.td("Inscripto en:"))
        print(htm.td(cursos.registro["curso"]))
        print('</tr>')
        i = i + 1
    htm.fin_tabla()
    print(htm.button('Estado de cuenta', "ctacli.php?id=" + str(cliente_id) + "&accion=listado"))
    print(htm.button('Llamadas', "lla.php?accion=listado&cliente_id=" + str(cliente_id)))
    # print(htm.button('Notas', "cli_ver.py?id=" + str(cliente_id) + "&accion=notas"))
    # print(htm.button('Escolaridad', "cli_ver.py?id=" + str(cliente_id) + "&accion=escolaridad"))
    # print(htm.button('Documentos', "cli_ver.py?id=" + str(cliente_id) + "&accion=documentos"))
    print(htm.button('Volver', 'cli.py?accion=listado'))
    pag.fin()
if __name__ == "__main__":
    form = cgi.FieldStorage()
    accion = form.getvalue("accion", "listado")
    if accion == "listado":
        listado(form)
    else:
        listado(form)
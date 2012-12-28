#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Pograma LAMB para códigos de salud de BPS"""
import datos
import htm
import pagina
import cgi
def listado():
    """ Listado de códigos de seguro de salud """
    pag = pagina.Pagina("Listado de códigos del Seguro de Salud", 4)
    htm.button("Nuevo","codss.py?accion=nuevo")
    htm.button('Volver','geined.py?accion=sistema')
    # cargar datos
    codigoss = datos.Tabla("codigoss")
    i = 0
    htm.encabezado_tabla(["Nº", "Categoria", "Acciones"])
    for fila in codigoss.resultado:
        htm.fila_alterna(i)
        ident = fila["id"]
        print(htm.td(ident))
        print(htm.td(fila["codigo"]))
        print("<td>")
        htm.boton_detalles("codss.py?accion=ver&id=" + str(ident))
        htm.boton_editar("codss.py?accion=editar&id=" + str(ident))
        htm.boton_eliminar("codss.py?accion=eliminar&id=" + str(ident))
        print("</td>")
        i = i + 1
    htm.fin_tabla()
    htm.button('Volver','geined.py?accion=sistema')
    pag.fin()
def nuevo():
    """ Formulario para nuevo código de Seguro de Salud """
    pag = pagina.Pagina('Nuevo código de Seguro de Salud')
    htm.form_edicion("Nuevo código de Seguro de Salud", "codss.py?accion=agregar")
    htm.input_texto("Código:", "codigo", "")
    htm.botones('codss.py?accion=listado')
    htm.form_edicion_fin()
    pag.fin
def agregar(frm):
    """Agrega registro a la base de datos codigoss"""
    # Voy por acá
    codigoss = datos.Tabla("codigoss")
    codigoss.buscar("codigo", frm["codigo"])
    if codigoss.num_filas > 0:
        pagina.duplicado("codss.py")
    else:
        codigoss.registro["codigo"] = frm["codigo"]
        codigoss.agregar()
        htm.redirigir("cem.php?accion=listado")
def editar(frm):
    """ Edición de código de Seguro de Salud"""
    pag = pagina.Pagina("Edición de código de seguro de salud", 2)
    htm.encabezado_tabla(["Campo","Valor"])
    htm.formulario("codss.php?accion=actualizar")
    codigoss = datos.Tabla("codigoss")
    codigoss.ir_a(frm["id"])
    print(htm.hidden("id", frm['id']))
    htm.input_texto("Código:", "codigo", codigoss.registro['codigo'])
    htm.botones()
    htm.fin_formulario()
    htm.fin_tabla()
    print(htm.boton('Volver','codss.php?accion=listado'))
    pag.fin()
def actualizar(frm):
    """ Actualiza registro de Código de Seguro de Salud """
    ident = frm['id']
    codigoss = datos.Tabla("codigoss")
    codigoss.ir_a(ident)
    codigoss.registro["codigo"] = frm["codigo"]
    codigoss.actualizar()
    htm.redirigir('codss.php?accion=listado')
def detalle(frm):
    """ Listado de empleados por código de Seguro de Salud"""
    pag = pagina.Pagina("Detalles de CSS de un empleado", 5)
    codigoss = datos.Tabla("codigoss")
    codigoss.ir_a(frm["id"])
    # cli_ver
    print(htm.h2(codigoss.registro['codigo']))
    htm.encabezado_tabla(["Nombre","CI","Direccion","Telefono","eMail","Ingreso","Notas","Acciones"])
    empleados = datos.Tabla("empleados")
    empleados.buscar("codigoss", frm["id"])
    i = 0
    for fil2 in empleados.resultado:
        htm.fila_alterna(i)
        print(htm.td(fil2['nombre']))
        print(htm.td(fil2['ci']))
        print(htm.td(fil2['direccion']))
        print(htm.td(fil2['telefono']))
        print(htm.td(fil2['email']))
        print(htm.td(fil2['ingreso']))
        print(htm.td(fil2['notas']))
        print('<td>')
        print(htm.boton("Detalles", 'emp_ver.php?id=' + str(fil2['id'])))
        print('</tr>')
        i = i + 1
    htm.fin_tabla()
    htm.boton('Volver','codss.php?accion=listado')
    pag.fin()
def main():
    """Principal"""
    form = cgi.FieldStorage()
    accion = form.getvalue("accion","listado")
    if accion == 'listado':
        listado()
    elif accion == "nuevo":
        nuevo()
    elif accion == "agregar":
        agregar(form)
    elif accion == "editar":
        editar(form)
    elif accion == "actulizar":
        actualizar(form)
    elif accion == 'eliminar':
        # TODO borrar('codigoss',$_POST['id'],'codss.php');
        pass
    elif accion == 'ver':
        detalle(form)

if __name__ == "__main__":
    main()
    
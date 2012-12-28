#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Listado de boletas contado"""
import cgi
import cgitb ; cgitb.enable()
import funciones
import htm
import datos
import pagina
def listado(frm):
    """Listado de boletas contado"""
    pag = pagina.Pagina("Listado de boletas contado", 5)
    filas_por_pagina = 20
    pagina_actual = 1
    if frm.has_key("pagina"):
        pagina_actual = int(frm["pagina"].value)
    offset = (pagina_actual -1) * filas_por_pagina
    print('<table><tr>')
    print(htm.td(htm.button("Eliminar boletas vacías","bol.py?accion=limpiar") +
        htm.button("Volver",'geined.py?accion=recepcion')))
    print('<td>')
    htm.formulario("bol.py")
    print('Buscar por No. de boleta:')
    htm.input_input("text", "buscar")
    htm.input_input("submit", "enviar", "Enviar")
    htm.fin_formulario()
    print('</td></tr></table>')
    boletas = datos.Tabla("bol_cont")
    boletas.filtrar()
    total_paginas = boletas.num_filas / filas_por_pagina
    clientes = datos.Tabla("clientes")
    boletas.limite = " " + str(offset) + "," + str(filas_por_pagina)
    boletas.orden = " id DESC "
    if frm.has_key("buscar"):
        boletas.filtro = "id = " + str(frm['buscar'].value)
        print(htm.h3("Datos filtrados, boleta No.:" + str(frm['buscar'].value)))
    boletas.filtrar()
    print(htm.h3("Pagina actual:" + str(pagina_actual)))
    htm.encabezado_tabla(["Nº", "Caja Nº", "Fecha", "Cliente", "Total", "Acciones"])
    i = 0
    for fila in boletas.resultado:
        htm.fila_alterna(i)
        id_no = fila['id']
        print(htm.td(id_no))
        print(htm.td(fila['caja_id']))
        print(htm.td(funciones.mysql_a_fecha(fila['fecha'])))
        clientes.buscar("id", fila["cliente_id"])
        print(htm.td(clientes.registro['nombre']))
        htm.linea_moneda(fila['total'])
        print('<td>')
        htm.boton_detalles("bol.py?accion=detalles&id=" + str(id_no))
        htm.boton_imprimir("bol.py?accion=imprimir&id=" + str(id_no))
        # NO esta contemplada la opción de borrar boletas
        # Habría que implementar una opción de anulación
        print('</td></tr>')
        i = i +1
    htm.fin_tabla()
    htm.navegador("bol.py", pagina_actual, total_paginas)
    print(htm.button("Volver",'geined.py?accion=recepcion'))
    pag.fin()
def imprimir(frm):
    """Rutina para imprimir boletas"""
    boleta_id = frm['id'].value
    boletas = datos.Tabla("bol_cont")
    cajas = datos.Tabla("cajas")
    clientes = datos.Tabla("clientes")
    boletas.buscar("id", boleta_id)
    caja_id = boletas.registro["caja_id"]
    cajas.buscar("id", caja_id)
    cliente_id = boletas.registro['cliente_id']
    # -----------------------------------------
    hoja = {}
    fecha = funciones.mysql_a_fecha(boletas.registro['fecha'])
    clientes.buscar("id", cliente_id)
    nombre = clientes.registro['nombre']
    direccion = clientes.registro['direccion']
    pag = pagina.Pagina("Boleta contado", 5, tipo="boleta")
    lin = ' ' * 90
    for i in range(0, 70):
        hoja[i] = lin
    desp = 34
    hoja[0] = funciones.substr_replace(hoja[0], fecha, 80)
    hoja[0 + desp] = funciones.substr_replace(hoja[0 + desp], fecha, 80)
    hoja[3] = funciones.substr_replace(hoja[3], nombre, 20)
    hoja[3 + desp] = funciones.substr_replace(hoja[3 + desp], nombre, 20)
    hoja[5] = funciones.substr_replace(hoja[5], direccion, 20)
    hoja[5 + desp] = funciones.substr_replace(hoja[5 + desp], direccion, 20)
    detalle = datos.Tabla("bol_det")
    detalle.filtro = "bol_cont_id = '" + str(boleta_id) + "'"
    detalle.filtrar()
    hoja[7] = funciones.substr_replace(hoja[7], "Cantidad", 4)
    hoja[7] = funciones.substr_replace(hoja[7], "Detalle", 13)
    hoja[7] = funciones.substr_replace(hoja[7], "Precio", 79-6)
    hoja[7] = funciones.substr_replace(hoja[7], "Total", 95-5)
    hoja[7 + desp] = funciones.substr_replace(hoja[7 + desp], "Cantidad", 4)
    hoja[7 + desp] = funciones.substr_replace(hoja[7 + desp], "Detalle", 13)
    hoja[7 + desp] = funciones.substr_replace(hoja[7 + desp], "Precio", 79-6)
    hoja[7 + desp] = funciones.substr_replace(hoja[7 + desp], "Total", 95-5)
    conta = 8
    totbol = 0
    for fila in detalle.resultado:
        cantidad = str(fila["cantidad"])
        detalle = fila['detalle'].strip()
        unitario = funciones.moneda(fila['unitario'])
        total = funciones.moneda(fila['total'])
        if (len(detalle) > 57):
            detalle = detalle[0:57]
        hoja[conta] = funciones.substr_replace(hoja[conta], cantidad, 6)
        hoja[conta] = funciones.substr_replace(hoja[conta], detalle, 13)
        hoja[conta] = funciones.substr_replace(hoja[conta], unitario, 80 - len(unitario))
        hoja[conta] = funciones.substr_replace(hoja[conta], total, 96 - len(total))
        # Segunda hoja
        hoja[conta + desp] = funciones.substr_replace(hoja[conta + desp], cantidad, 6)
        hoja[conta + desp] = funciones.substr_replace(hoja[conta + desp], detalle, 13)
        hoja[conta + desp] = funciones.substr_replace(hoja[conta + desp], unitario, 80 - len(unitario))
        hoja[conta + desp] = funciones.substr_replace(hoja[conta + desp], total, 96 - len(total))
        # Total
        totbol = totbol + fila['total']
        conta = conta + 1
    total_boleta = funciones.moneda(totbol)
    hoja[17] = funciones.substr_replace(hoja[17], total_boleta, 96 - len(total_boleta))
    hoja[17 + desp] = funciones.substr_replace(hoja[17 + desp], total_boleta, 96 - len(total_boleta))
    print("<pre>")
    offset_y = 5
    for i in range(0, offset_y):
        print('')
    for i in range(0, 60):
        print(hoja[i] + "</br>")
    print("</pre>")
    print(htm.button("...","bol.py?accion=listado"))
    pag.fin()
def limpiar():
    """Limpiar boletas contado sin detalles"""
    pag = pagina.Pagina("Limpiando boletas contado sin detalles", 5)
    boletas = datos.Tabla("bol_cont")
    detalle = datos.Tabla("bol_det")
    for fila in boletas.resultado:
        id_no = fila['id']
        detalle.buscar("bol_cont_id", id_no)
        #if($num_fil == 0){
            #$sql_del = "DELETE FROM bol_cont WHERE id='$id'";
            #$res = mysql_query($sql_del);
    htm.redirigir("bol.py?accion=listado")
    pag.fin()
def detalles(frm):
    """Detalles de la boleta"""
    bol_id = frm['id'].value
    pag = pagina.Pagina("Detalles de boleta Nº " + str(bol_id), 5)
    print(htm.button("Volver","bol.py?accion=listado"))
    boletas = datos.Tabla("bol_cont")
    boletas.buscar("id", bol_id)
    clientes = datos.Tabla("clientes")
    clientes.buscar("id", boletas.registro["cliente_id"])
    print('<table><tr><td>')
    print('Nombre: ' + clientes.registro['nombre'])
    print('</td></tr><tr><td>')
    print('Direccion: ' + clientes.registro['direccion'])
    print('</td></tr></table>')
    dets = datos.Tabla("bol_det")
    dets.filtro = "bol_cont_id=" + str(bol_id)
    dets.filtrar()
    i = 0
    htm.encabezado_tabla(["Nº", "Cantidad", "Detalle", "Unitario", "Total", "Rubro"])
    for fila in dets.resultado:
        htm.fila_alterna(i)
        print(htm.td(fila['id']))
        print(htm.td(fila['cantidad']))
        print(htm.td(fila['detalle']))
        print(htm.td(fila['unitario']))
        print(htm.td(fila['total']))
        print(htm.td(fila['rubro']))
        i = i +1
    htm.fin_tabla()
    print(htm.button("Volver","bol.py?accion=listado"))
    pag.fin()
if __name__ == "__main__":
    form = cgi.FieldStorage()
    accion = 'listado'
    if not (form.has_key("accion")):
        accion = 'listado'
    else:
        accion = form.getvalue("accion")
    if accion == 'listado':
        listado(form)
    elif accion == 'detalles':
        detalles(form)
    elif accion == "imprimir":
        imprimir(form)
    elif accion == "limpiar":
        limpiar()

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Manejo de BIENES DE CAMBIO"""
import cgitb; cgitb.enable()
import cgi
import htm
import datos
import pagina
import funciones
def listado():
    """Listado de bienes de cambio"""
    pag = pagina.Pagina("Listado de Bienes de Cambio", 5)
    print(htm.button("Nuevo", "biecam.py?accion=nuevo"))
    print(htm.button('Volver', 'geined.py?accion=direccion'))
    # cargar datos
    bie_cam = datos.Tabla("bie_cam")
    bie_cam.filtrar()
    existencias = datos.Tabla("existencias")
    htm.encabezado_tabla(["Nº", "Descripción", "Precio", "Cantidad", 
                          "Acciones"])
    for fila in bie_cam.resultado:
        htm.fila_lista()
        bie_cam_id = str(fila['id'])
        print(htm.td(bie_cam_id))
        print(htm.td(fila['descripcion']))
        print(htm.td(funciones.moneda(fila['precio']), "right"))
        existencias.filtro = "bie_cam_id = " + bie_cam_id
        existencias.filtrar()
        if not existencias.encontrado:
            cantidad = 0
        cantidad = existencias.num_filas
        print(htm.td(cantidad))
        print('<td>')
        htm.boton_detalles('biecam.py?accion=ver&id=' + bie_cam_id)
        htm.boton_editar('biecam.py?accion=editar&id=' + bie_cam_id)
        htm.boton_eliminar('biecam.py?accion=eliminar&id=' + bie_cam_id)
        print('</td>')
    htm.fin_tabla()
    print(htm.button('Volver', 'geined.py?accion=direccion'))
    pag.fin()
def nuevo():
    """Formulario nuevo ítem BC"""
    pag = pagina.Pagina("Nuevo ítem en Bienes de Cambio")
    htm.form_edicion("Nuevo ítem", "biecam.py?accion=agregar")
    htm.input_texto("Descripción:", "descripcion", "")
    htm.input_numero("Precio:", "precio", "")
    htm.botones("biecam.py?accion=listado")
    htm.form_edicion_fin()
    pag.fin()
def agregar(frm):
    """Inserta un item de BC en la BDD"""
    pag = pagina.Pagina("Insertando datos")
    bie_cam = datos.Tabla("bie_cam")
    bie_cam.buscar("descripcion", frm.getvalue("descripcion"))
    if bie_cam.encontrado:
        htm.duplicado("biecam.py?accion=listado")
    else:
        bie_cam.registro["descripcion"] = frm.getvalue("descripcion")
        bie_cam.registro["precio"] = frm.getvalue("precio")
        bie_cam.insertar()
    htm.redirigir("biecam.py?accion=listado")
    pag.fin()
def editar(frm):
    """Edición de ítem de Bienes de cambio"""
    pag = pagina.Pagina("Edición de ítem en Bienes de Cambio", 5)
    bie_cam = datos.Tabla("bie_cam")
    bie_cam.buscar("id", frm.getvalue("id"))
    htm.form_edicion("Editar:" + bie_cam.registro['descripcion'], 
                     "biecam.py?accion=actualizar")
    htm.campo_oculto("id", bie_cam.registro["id"])
    htm.input_texto("Descripción:", "descripcion", 
                    bie_cam.registro["descripcion"])
    htm.input_numero("Precio:", "precio", bie_cam.registro["precio"])
    htm.botones("biecam.py?accion=listado")
    htm.form_edicion_fin()
    pag.fin()

def actualizar(frm):
    """Actualizar ítem de Bienes de Cambio"""
    bie_cam = datos.Tabla("bie_cam")
    bie_cam.buscar("id", frm.getvalue("id"))
    bie_cam.registro["descripcion"] = frm.getvalue("descripcion")
    bie_cam.registro["precio"] = frm.getvalue("precio")
    bie_cam.actualizar()
    listado()

def detalle(frm):
    """Detalles de un item de Bienes de cambio"""
    # Recuperar variables
    ident = frm.getvalue("id")
    # datos
    existencias = datos.Tabla("existencias")
    bie_cam = datos.Tabla("bie_cam")
    depositos = datos.Tabla("depositos")
    # Pagina
    pag = pagina.Pagina("Existencias de Bienes de Cambio", 5)
    print(htm.button("Ingresar a stock", 
                     "biecam.py?accion=ingstock&id=" + str(id)))
    print(htm.button('Volver', 'biecam.py?accion=listado'))
    bie_cam.ir_a(ident)
    print(htm.h2(bie_cam.registro["descripcion"]))
    htm.encabezado_tabla(["Sucursal", "Cantidad", "Acciones"])
    existencias.buscar("bie_cam_id", ident)
    i = 0
    for fila in existencias.resultado:
        htm.fila_alterna(i)
        depositos.buscar("id", fila["deposito_id"])
        print(htm.td(depositos.registro["deposito"]))
        print(htm.td(fila["cantidad"]))
        print("<td>")
        print(htm.button("Ajustar", 
                         "biecam.py?accion=ajustar&id=" + str(fila['id'])))
        print(htm.button("Transferir", 
                         'biecam.py?accion=transferir&id=' + str(fila['id'])))
        print('</td></tr>')
    htm.fin_tabla()
    print(htm.button('Volver', 'biecam.py?accion=listado'))
    pag.fin()
def ing_stock(frm):
    """Ingresar Stock"""
    # Recuperar variables
    ident = frm.getvalue("id")
    bie_cam = datos.Tabla("bie_cam")
    bie_cam.ir_a(ident)
    bien = bie_cam.registro['descripcion']
    depositos = datos.Tabla('depositos')
    depositos.filtrar()
    pag = pagina.Pagina('Ingresar bienes al stock')
    print(htm.h3(bien))
    htm.form_edicion("Ingreso de bien a stock",
                     "biecam.py?accion=ingresar&bie_cam_id=" + str(ident))
    htm.input_combo("Sucursal:", "deposito_id", 
                    depositos.resultado, ['id', 'deposito'], "")
    htm.input_numero("Cantidad:", "cantidad", "")
    htm.fin_tabla()
    htm.botones("biecam.py?accion=listado")
    htm.form_edicion_fin()
    pag.fin()
def ingresar(frm):
    """Ingresar a stock"""
    # Recuperación de variables
    bie_cam_id = frm.getvalue('bie_cam_id')
    deposito_id = frm.getvalue('deposito_id')
    cantidad = frm.getvalue('cantidad')
    # Detección de duplicados
    existencias = datos.Tabla("existencias")
    # existencias.buscar("deposito_id", deposito_id)
    existencias.filtro = "deposito_id=" + str(deposito_id) + \
        " AND bie_cam_id=" + str(bie_cam_id)
    existencias.filtrar()
    if existencias.resultado == 0:
        # Armar SQL
        existencias.registro["deposito_id"] = deposito_id
        existencias.registro["cantidad"] = cantidad
        existencias.registro["bie_cam_id"] = bie_cam_id
        existencias.insertar()
        # Redirigir
        htm.redirigir("biecam.py?accion=ver&id=" + str(bie_cam_id))
    else:
        htm.duplicado("biceam.php?accion=ver&id=" + str(bie_cam_id))
def ajustar(frm):
    """Actualizar existencias"""
    pag = pagina.Pagina("Actualizar existencias", 5)
    htm.formulario("biecam.py?accion=act_exi")
    htm.encabezado_tabla(["Campo", "Valor"])
    ident = frm.getvalue('id')
    existencias = datos.Tabla('existecias')
    depositos = datos.Tabla('depositos')
    existencias.ir_a(ident)
    #fil_exi = buscar_registro("existencias", "id", id)
    deposito_id = existencias.registro['deposito_id']
    depositos.ir_a(deposito_id)
    sucursal = depositos.registro['deposito']
    #fil_suc = buscar_registro("depositos", "id", deposito_id)
    #sucursal = fil_suc['deposito']
    print(htm.hidden("id", ident))
    print(htm.hidden("bie_cam_id", existencias.registro['bie_cam_id']))
    print(htm.tr(htm.td("Sucursal:") + htm.td(sucursal)))
    htm.input_numero("Cantidad:", "cantidad", existencias.registro['cantidad'])
    htm.fin_tabla()
    htm.botones('biecam.py?accion=listado')
    htm.fin_formulario()
    pag.fin()
def act_exi(frm):
    """Actualizar existencias"""
    ident = frm.getvalue('id')
    cantidad = frm.getvalue('cantidad')
    # bie_cam_id = frm.getvalue('bie_cam_id')
    # No me queda clar porqué estaba la línea anterior
    existencias = datos.Tabla("existencias")
    existencias.ir_a(ident)
    existencias.registro["cantidad"] = cantidad
    existencias.actualizar()
    htm.redirigir("biecam.py?accion=ver&id=" + str(ident))
def transferir(frm):
    """Transferencia de bienes entre depositos"""
    ident = frm.getvalue('id')
    depositos = datos.Tabla("depositos")
    depositos.filtrar()
    pag = pagina.Pagina("Transferir bienes de cambio")
    htm.form_edicion("Transferencia",  "biecam.py?accion=acttra")
    print(htm.hidden("id", ident))
    htm.input_combo("Tansferir hasta:", "hasta", depositos.resultado, 
                    ["id", "deposito"], "")
    htm.input_numero("Cantidad a transferir:", "cantidad", "")
    htm.botones("biecam.py?accion=listado")
    htm.form_edicion_fin()
    pag.fin()
def acttra(frm):
    """Actualizar transferencia"""
    existencias = datos.Tabla("existencias")
    # Parametros
    ident = frm.getvalue('id')
    destino = frm.getvalue('hasta')
    # Origen
    cantidad_a_transferir = frm.getvalue('cantidad')
    existencias.ir_a(ident)
    # deposito de origen = existencias.registro['deposito_id']
    bie_cam_id = existencias.registro['bie_cam_id']
    pre_origen = existencias.registro['cantidad']
    # Destino
    existencias.filtro = "deposito_id=" + str(destino) + " AND bie_cam_id=" +\
        str(bie_cam_id)
    existencias.filtrar()
    if existencias.resultado == 0:
        # Si no existe registro destino, crear uno
        existencias.registro["deposito_id"] = destino
        existencias.registro["cantidad"] = cantidad_a_transferir
        existencias.registro["bie_cam_id"] = bie_cam_id
        existencias.insertar()
    else:
        #  Si el destino existe, actualizarlo
        pre_destino = existencias.registro['cantidad']
        id_destino = existencias.registro['id']
        saldo_destino = pre_destino + cantidad_a_transferir
        existencias.ir_a(id_destino)
        existencias.registro["cantidad"] = saldo_destino
        existencias.actualizar()
    # Actualizar origen
    saldo_origen = pre_origen - cantidad_a_transferir
    existencias.ir_a(ident)
    existencias.registro["cantidad"] = saldo_origen
    existencias.actualizar()
    htm.redirigir("biecam.py?accion=ver&id=" + str(bie_cam_id))
def eliminar(frm):
    """Eliminar item de bienes de cambio"""
    #TODO: ver si no hay un problema de privilegios con esto
    bie_cam = datos.Tabla('bie_cam')
    bie_cam.borrar(frm.getvalue('id'))
    listado()
def main():
    """Programa principal"""
    form = cgi.FieldStorage()
    accion = 'listado'
    if form.has_key('accion'):
        accion = form.getvalue('accion')
    if accion == 'listado':
        listado()
    elif accion == 'nuevo':
        nuevo()
    elif accion == 'agregar':
        agregar(form)
    elif accion == 'editar':
        editar(form)
    elif accion == 'actualizar':
        actualizar(form)
    elif accion == 'eliminar':
        eliminar(form)
    elif accion == 'ver':
        detalle(form)
    elif accion == 'ajustar':
        ajustar(form)
    elif accion == 'act_exi':
        act_exi(form)
    elif accion == 'transferir':
        transferir(form)
    elif accion == 'acttra':
        acttra(form)
    elif accion == 'ingstock':
        ing_stock(form)
    elif accion == 'ingresar':
        ingresar(form)
if __name__ == "__main__":
    main()

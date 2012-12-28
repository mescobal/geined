#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Manejo de elmentos de inventario"""
import cgitb; cgitb.enable()
import cgi
import htm
import pagina
import datos
import funciones
def listado():
    """Listado de inventario"""
    # Bases de datos
    inventario = datos.Tabla("inventario")
    depositos = datos.Tabla("depositos")
    inventario.filtrar()
    # Pagina
    pag = pagina.Pagina("Listado de inventario", 5)
    print(htm.encabezado("Listado de inventario", "Administración", 
                   "geined.py?accion=administracion"))
    print(htm.button("Nuevo", "inventario.py?accion=nuevo"))
    htm.encabezado_tabla(['No.', 'Nombre', 'Deposito', 'Compra', 'Costo', 
                          'Vida', 'Residual', 'Metodo', 'Valor', 'Fecha', 
                          'Acciones'])
    for fila in inventario.resultado:
        depositos.ir_a(fila["deposito_id"])
        print("<tabla class='fila_datos'>")
        print(htm.td(fila["id"]) +
            htm.td(fila["nombre"]) +
            htm.td(depositos.registro["deposito"]) +
            htm.td(funciones.mysql_a_fecha(fila["compra"])) +
            htm.td(funciones.moneda(fila["costo"])) +
            htm.td(fila["vida"]) +
            htm.td(funciones.moneda(fila["residual"])) +
            htm.td(fila["metodo"]) +
            htm.td(funciones.moneda(fila["revaluacion"])) +
            htm.td(funciones.mysql_a_fecha(fila["fecha_rev"])))
        print '<td>'
        htm.boton_editar("inventario.py?accion=editar&id=" + 
            str(fila["id"]))
        htm.boton_eliminar("inventario.py?accion=eliminar&id=" + 
            str(fila["id"]))
        print(htm.button("Recalcular", "inventario.py?accion=recalcular&id=" + 
            str(fila["id"])))
        print('</td></tr>')
    pag.fin()
def nuevo():
    """Nuevo item en inventario"""
    # Bases de datos
    depositos = datos.Tabla("depositos")
    depositos.filtrar()
    # Pagina
    pag = pagina.Pagina("Nuevo item de inventario", nivel=4, fecha=2)   
    htm.form_edicion("Nuevo item", 'inventario.py?accion=agregar')
    htm.input_texto("Nombre:", 'nombre', "")
    htm.input_combo("Deposito:", "deposito_id", depositos.resultado, 
                    ['id', 'deposito'], '')
    htm.input_fecha("Fecha de compra:", 'compra', 
                    funciones.fecha_a_mysql(funciones.hoy()))
    htm.input_numero("Costo:", 'costo', "")
    htm.input_numero('Vida útil:', 'vida', "")
    htm.input_numero('Valor residual', 'residual', "")
    htm.input_texto('Método de cálculo:', 'metodo', "")
    htm.input_numero('Revaluación:', 'revaluacion', "")
    htm.input_fecha2('Fecha de revaluación:', 'fecha_rev', 
                     funciones.fecha_a_mysql(funciones.hoy()))
    htm.botones('inventario.py?accion=listado')
    htm.form_edicion_fin()
    pag.fin()
def agregar(frm):
    """ Agregar item a inventario, con fecha corregida"""
    inventario = datos.Tabla("inventario")
    inventario.nuevo()
    inventario.registro["nombre"] = frm.getvalue("nombre")
    inventario.registro["deposito_id"] = frm.getvalue("deposito_id")
    inventario.registro["compra"] =  frm.getvalue("compra")
    inventario.registro["costo"] = frm.getvalue("costo")
    inventario.registro["vida"] = frm.getvalue("vida")
    inventario.registro["residual"] = frm.getvalue("residual")
    inventario.registro["metodo"] = frm.getvalue("metodo")
    inventario.registro["revaluacion"] = frm.getvalue("revaluacion")
    inventario.registro["fecha_rev"] = frm.getvalue("fecha_rev")
    inventario.insertar()
    listado()
def editar(frm):
    """Editar un ítem del inventario"""
    inventario = datos.Tabla("inventario")
    inventario.ir_a(frm["id"].value)
    depositos = datos.Tabla("depositos")
    depositos.filtrar()
    pag = pagina.Pagina("Edición de inventario", nivel=4, fecha=2)
    htm.form_edicion("Modificar ítem", "inventario.py?accion=actualizar")
    htm.campo_oculto("id", frm["id"].value)
    htm.input_texto("Nombre:", 'nombre',  inventario.registro["nombre"])
    htm.input_combo("Deposito:", "deposito_id", depositos.resultado, ["id", "deposito"], inventario.registro["deposito_id"])
    htm.input_fecha("Fecha de compra:", 'compra', 
                    inventario.registro["compra"])
    htm.input_numero("Costo:", 'costo',  inventario.registro["costo"])
    htm.input_numero('Vida útil:', 'vida',  inventario.registro["vida"])
    htm.input_numero('Valor residual', 'residual',  
                     inventario.registro["residual"])
    htm.input_texto('Método de cálculo:', 'metodo',  
                    inventario.registro["metodo"])
    htm.input_numero('Revaluación:', 'revaluacion',  
                     inventario.registro["revaluacion"])
    htm.input_fecha2('Fecha de revaluación:', 'fecha_rev', 
                     inventario.registro["fecha_rev"])
    htm.botones('inventario.py?accion=listado')
    htm.form_edicion_fin()
    pag.fin()
def actualizar(frm):
    """Actualizar datos de inventario"""
    inventario = datos.Tabla("inventario")
    inventario.ir_a(frm["id"].value)
    inventario.registro["nombre"] = frm.getvalue("nombre")
    inventario.registro["deposito_id"] = frm.getvalue("deposito_id")
    inventario.registro["compra"] =  funciones.fecha_a_mysql(frm.getvalue("compra"))
    inventario.registro["costo"] = frm.getvalue("costo")
    inventario.registro["vida"] = frm.getvalue("vida")
    inventario.registro["residual"] = frm.getvalue("residual")
    inventario.registro["metodo"] = frm.getvalue("metodo")
    inventario.registro["revaluacion"] = frm.getvalue("revaluacion")
    inventario.registro["fecha_rev"] = funciones.fecha_a_mysql(frm.getvalue("fecha_rev"))
    inventario.actualizar()
    listado()
def recalcular(frm):
    """Recalcular inventario"""
    inventario = datos.Tabla("inventario")
    inventario.ir_a(frm["id"].value)
    ahora = funciones.hoy()
    if inventario.registro["metodo"] == '':
        valor = 100
        inventario.registro["revaluacion"] = valor
        inventario.registro["fecha_rev"] = funciones.fecha_a_mysql(ahora)
    listado()
def eliminar(frm):
    """Eliminar un item del inventario"""
    # NOTA: solo se puede eliminar un ítem del inventario si hay CERO unidades
    # O si se tira algo del inventario: deducir de la contabilidad el valor 
    # correspondiente
    inventario = datos.Tabla("inventario")
    inventario.borrar(frm["id"].value)
    listado()
if __name__ == "__main__":
    form = cgi.FieldStorage()
    accion = form.getvalue("accion", "listado")
    if accion == "listado":
        listado()
    elif accion == "editar":
        editar(form)
    elif accion == 'actualizar':
        actualizar(form)
    elif accion == 'nuevo':
        nuevo()
    elif accion == 'agregar':
        agregar(form)
    elif accion == 'recalcular':
        recalcular(form)
    elif accion == 'eliminar':
        eliminar(form)
    else:
        listado()

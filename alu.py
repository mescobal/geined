#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Listado de alumnos"""
import cgi
import cgitb ; cgitb.enable()
import htm
import datos
import pagina
def listado(frm):
    """Listado de alumnos"""
    # datos
    tipo_pago = datos.Tabla("tipo_pago")
    pag = pagina.Pagina("Listado de alumnos", 10)
    print(htm.encabezado("Listado de alumnos", "Académico", "geined.py?accion=academico"))
    print("<table class='barra'><tr><td>")
    htm.formulario("alu.py?accion=listado")
    print('Nombre:')
    print('<input type="text" name="nombre"></input>')
    print('CI:')
    print('<input type="text" name="ci"></input>')
    print(' y Sucursal: <select name="sucursal"> \
        <option selected value="">Cualquiera</option> \
        <option value="CA">Carrasco</option> \
        <option value="CO">Costa</option> \
    </select>')
    print('<input type="submit" value="Buscar" />')
    htm.fin_formulario()
    print(htm.boton("Alumnos x Sucursal", "alu_suc.py"))
    print("</td></tr></table>")
    nombre = frm.getvalue("nombre", "")
    ci = frm.getvalue("ci", "")
    sucursal = frm.getvalue("sucursal", "")
    #Limité el número de alumnos a 50 para que no se eternice el listado inicial
    sql = "SELECT alumnos.*, clientes.nombre, clientes.ci, cursos.curso FROM alumnos,clientes,cursos WHERE (clientes.nombre LIKE '%" + \
        nombre + "%') AND (clientes.ci LIKE '%" + ci + \
        "%') AND (cursos.curso LIKE '" + sucursal + \
        "%') AND (clientes.id = alumnos.cliente_id) AND (cursos.id = alumnos.curso_id) ORDER BY alumnos.id DESC LIMIT 50"
    dat = datos.Datos()
    dat.ejecutar(sql)
    resultado = dat.cursor.fetchall()
    htm.encabezado_tabla(["Nº", "Alumno", "CI", "Curso", "Tipo de pago", "Cuota", "Acciones"])
    for fila in resultado:
        print("<tr class='fila_datos'>")
        ident = fila['id']
        print(htm.td(ident))
        print(htm.td(fila['nombre']))
        print(htm.td(fila['ci']))
        print(htm.td(fila['curso']))
        tipo_pago.buscar("id", fila["tipo_pago_id"])
        print(htm.td(tipo_pago.registro["tipo"]))
        htm.linea_moneda(fila['cuota'])
        print('<td>')
        htm.boton_editar("alu.py?accion=editar&id=" + str(ident))
        print(htm.button("Cliente", 'cli_ver.php?id=' + str(fila['cliente_id'])))
        print(htm.button("Curso", 'cur_ver.py?id=' + str(fila['curso_id'])))
        htm.boton_confirmar("Drop-out", "¿Desea pasar este alumno a Drop-Out?", 
            "alu.py?accion=drop-out&id=" + str(ident))
        htm.boton_confirmar("Eliminar", "¿Desea eliminar este alumno y todos los datos relacionados?",      "alu.py?accion=eliminar&id=" + str(ident))
        print('</td></tr>')
    htm.fin_tabla()
    print(htm.button("Volver",'geined.py?accion=academico'))
    pag.fin()
def nuevo():
    """Pasar a categoría Alumno"""
    pag = pagina.Pagina("Inscripción", 5)
    htm.nota("Una vez guardados los datos, el cliente pasa a la categoría Alumno")
    htm.form_edicion("Nuevo alumno", "alu.py?accion=agregar")
    # Clientes
    clientes = datos.Tabla("clientes")
    clientes.orden = "nombre"
    # Cursos
    cursos = datos.Tabla("cursos")
    cursos.orden = "curso"
    # Tipo de pago
    tipo_pago = datos.Tabla("tipo_pago")
    htm.input_combo("Cliente:", "cliente_id", clientes.resultado, ["id", "nombre"], "")
    htm.input_combo("Curso:", "curso_id", cursos.resultado, ["id", "curso"], "")
    htm.input_combo("Tipo de pago:", "tipo_pago_id", tipo_pago.resultado, ["id", "tipo"], "")
    htm.input_texto("Cuota:", "cuota", "")
    htm.input_numero("Cuotas pagas:", "pago", "")
    htm.botones("alu.py?accion=listado")
    htm.form_edicion_fin()
    pag.fin()
def agregar(frm):
    """Agregar un alumno"""
    pag = pagina.Pagina("Agregando alumno", 10)
    alumnos = datos.Tabla("alumnos")
    alumnos.registro["cliente_id"] = frm.getvalue("cliente_id")
    alumnos.registro["curso_id"] = frm.getvalue("curso_id")
    alumnos.registro["tipo_pago_id"] = frm.getvalue("tipo_pago_id")
    alumnos.registro["cuota"] = frm.getvalue("cuota")
    alumnos.registro["pago"] = frm.getvalue("pago")
    alumnos.insertar()
    # pasar el cliente a categoría alumnos
    clientes = datos.Tabla("clientes")
    clientes.buscar("id", frm.getvalue("cliente_id"))
    clientes.registro["categoria_id"] = 2
    clientes.actualizar()
    htm.redirigir("alu.py?accion=listado")
    pag.fin()
def editar(frm):
    """Editar alumno"""
    pag = pagina.Pagina("Edición de alumno", 10)
    htm.form_edicion("Modificación de alumno", "alu.py?accion=actualizar")
    alumnos = datos.Tabla("alumnos")
    alumnos.buscar("id", frm.getvalue("id"))
    # cargar datos
    # Clientes
    clientes = datos.Tabla("clientes")
    clientes.buscar("id", alumnos.registro["cliente_id"])
    # Cursos
    cursos = datos.Tabla("cursos")
    cursos.filtro = "finalizado IS NULL"
    cursos.orden = "curso"
    cursos.filtrar()
    #Tipo de pago
    tipo_pago = datos.Tabla("tipo_pago")
    # Formulario
    htm.campo_oculto("id", frm.getvalue("id"))
    htm.input_label("Nombre:", clientes.registro["nombre"])
    #Curso
    htm.input_combo("Curso:", "curso_id", cursos.resultado, ["id", "curso"], alumnos.registro["curso_id"])
    htm.input_combo("Tipo de pago:", "tipo_pago_id", tipo_pago.resultado, ["id", "tipo"], alumnos.registro["tipo_pago_id"])
    htm.input_numero("Cuota:", "cuota", alumnos.registro["cuota"])
    htm.input_numero("Cuotas pagas:", "pago", alumnos.registro["pago"])
    htm.botones("alu.py?accion=listado")
    htm.form_edicion_fin()
    pag.fin()
def actualizar(frm):
    """Actualizar datos de un alumno"""
    pag = pagina.Pagina("Actualizando datos", 10)
    ident = frm.getvalue("id")
    alumnos = datos.Tabla("alumnos")
    alumnos.buscar("id", ident)
    alumnos.registro["curso_id"] = frm.getvalue("curso_id")
    alumnos.registro["tipo_pago_id"] = frm.getvalue("tipo_pago_id")
    alumnos.registro["cuota"] = frm.getvalue("cuota")
    alumnos.registro["pago"] = frm.getvalue("pago")
    alumnos.actualizar()
    htm.redirigir("alu.py?accion=listado")
    pag.fin()
def reporte():
    """Reporte de alumnos"""
    pag = pagina.Pagina("Reporte de alumnos")
    htm.encabezado_tabla(["Filtrar por sucursal"])
    htm.formulario("alu_suc.py")
    print """<tr><td>Sucursal:
        <INPUT TYPE="radio" NAME="suc" VALUE="Costa"> Costa
        <INPUT TYPE="radio" NAME="suc" VALUE="Carrasco"> Carrasco
        <INPUT TYPE="submit" VALUE="Ver"></TD></tr>"""
    htm.fin_formulario()
    htm.fin_tabla()
    pag.fin()
def drop_out(frm):
    """Por hacer"""
    alumnos = datos.Tabla("alumnos")
    alumnos.ir_a(frm.getvalue("id"))
    cliente_id = alumnos.registro["cliente_id"]
    # eliminar alumno
    clientes = datos.Tabla("clientes")
    clientes.ir_a(cliente_id)
    # cambiar categoría de clientes a Drop-Out
    #TODO: OJO verificar si no es alumno activo de otro grupo
    clientes.ir_a(cliente_id)
    clientes.registro["categoria_id"] = 3
    #TODO: no me queda claro si lleva otras modificaciones un Drop Out
if __name__ == "__main__":
    form = cgi.FieldStorage()
    accion = form.getvalue("accion", "listado")
    if accion == "listado":
        listado(form)
    elif accion == "nuevo":
        nuevo()
    elif accion == "agregar":
        agregar(form)
    elif accion == "editar":
        editar(form)
    elif accion == "actualizar":
        actualizar(form)
    elif accion == "drop-out":
        drop_out(form)
    elif accion == "eliminar":
        # TODO: chequear toda esta rutina
        pagi = pagina.Pagina("Eliminando alumnos", 10)
        alu = datos.Tabla("alumnos")
        alu.borrar(form.getvalue("id"))
        htm.redirigir("alu.py?accion=listado")
        # NOTA: NO cambia el estatus del cliente
        # Borrar por este método es una ANOMALIA
        pagi.fin()

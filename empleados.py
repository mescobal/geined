#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Manejo de empleados"""
import cgi
import cgitb; cgitb.enable()
import funciones
import pagina
import datos
import htm
def listado(frm):
    """Listado de empleados"""
    pag = pagina.Pagina("Listado de empleados", 4)
    print(htm.encabezado("Listado de empleados", "Dirección", "geined.py?accion=direccion"))
    print("<table class='barra'>")
    print("<tr><td>")
    print(htm.boton("Nuevo", "empleados.py?accion=nuevo"))
    print("</td><td>")
    htm.formulario("empleados.py?accion=listado")
    print('<input type="text" name="busqueda"><input type="submit" class="boton" VALUE="Buscar">')
    htm.fin_formulario()
    print('</td></tr></table>')
    # Bases de datos
    empleados = datos.Tabla("empleados")
    cat_empleados = datos.Tabla("cat_empleados")
    empleados.orden = "nombre"
    # cargar datos
    busqueda = frm.getvalue("busqueda", "")
    if busqueda != "":
        empleados.filtro = 'nombre LIKE "' + busqueda + '%"'
    empleados.filtrar()
    htm.encabezado_tabla(["Nombre", "Categoria", "CI", "Teléfonos", "Activo", "Acciones"])
    for fila in empleados.resultado:
        print("<tr class='fila_datos'>")
        ident = fila["id"]
        cat_empleados.ir_a(fila["categoria_id"])
        activo = "No"
        if fila["activo"] == 1:
            activo = "Si"
        print(htm.td(fila["nombre"]) +
              htm.td(cat_empleados.registro["categoria"]) +
              htm.td(fila["ci"]) +
              htm.td(fila["telefono"]) +
              htm.td(activo))
        print('<td>')
        htm.boton_detalles("emp_ver.php?id=" + str(ident))
        htm.boton_editar("empleados.py?accion=editar&id=" + str(ident))
        # htm.boton_eliminar("empleados.py?accion=eliminar&id=" + str(ident))
        # Ver más abajo porqué lo saco
        print('</td></tr>')
    htm.fin_tabla()
    pag.fin()

def nuevo():
    """Nuevo empleado"""
    # bases de datos
    cat_empleados = datos.Tabla("cat_empleados")
    codigoss = datos.Tabla("codigoss")
    
    cat_empleados.orden = "categoria"
    cat_empleados.filtrar()
    codigoss.filtrar()
    
    pag = pagina.Pagina("Nuevo empleado", nivel=4, fecha=2)
    htm.form_edicion("Nuevo empleado", "empleados.py?accion=agregar")    
    htm.input_texto("Nombre", "nombre", "")
    htm.input_combo("Categoría:", "categoria_id", cat_empleados.resultado, ["id", "categoria"], "")
    htm.input_texto("CI:", "ci", "")
    htm.input_texto("Dirección:", "direccion", "")
    htm.input_texto("Teléfono:", "telefono", "")
    htm.input_texto("eMail:", "email", "")
    htm.input_texto('Sexo:', 'sexo', '')
    htm.input_fecha('F.Nac.:', 'f_nac', funciones.fecha_a_mysql(funciones.hoy()))
    htm.input_texto('E.Civil:', 'e_civil', '')
    htm.input_fecha2("Fecha de ingreso", "ingreso", funciones.fecha_a_mysql(funciones.hoy()))
    htm.input_numero('Hijos (para DGI):', 'hijos', '')
    htm.input_check("Exclusión de mínimo no imponible:", "emni", "1")
    htm.input_combo("Código de Seguro de Salud:", "codigoss", codigoss.resultado,
        ["id", "codigo"], "")
    htm.input_check("Activo:", "activo", "1")
    htm.input_memo("Notas:", "notas", "")
    htm.botones("empleados.py?accion=listado")
    htm.form_edicion_fin()
    pag.fin()

def agregar(frm):
    """ Agrega empleado a la base de datos """
    # bases de datos
    empleados = datos.Tabla("empleados")
    empleados.buscar("nombre", frm.getvalue("nombre"))
    if empleados.encontrado:
        htm.duplicado("empleados.py?accion=listado")
    else:
        empleados.nuevo()
        empleados.registro["nombre"] = frm.getvalue("nombre")
        empleados.registro["categoria_id"] = frm.getvalue("categoria_id")
        empleados.registro["ci"] = frm.getvalue("ci")
        empleados.registro["direccion"] = frm.getvalue("direccion")
        empleados.registro["telefono"] = frm.getvalue("telefono")
        empleados.registro["email"] = frm.getvalue("email")
        empleados.registro["sexo"] = frm.getvalue("sexo")
        empleados.registro["f_nac"] = funciones.fecha_a_mysql(frm.getvalue("f_nac"))
        empleados.registro["e_civil"] = frm.getvalue("e_civil")
        empleados.registro["ingreso"] = funciones.fecha_a_mysql(frm.getvalue("ingreso"))
        empleados.registro["notas"] = frm.getvalue("notas")
        empleados.registro["hijos"] = frm.getvalue("hijos")
        empleados.registro["codigoss"] = frm.getvalue("codigoss")
        empleados.registro["emni"] = frm.getvalue("emni")
        empleados.registro["activo"] = frm.getvalue("activo")
        empleados.insertar()
        listado(frm)

def editar(frm):
    """ Edición de datos de un empleado """
    # bases de datos
    cat_empleados = datos.Tabla("cat_empleados")
    codigoss = datos.Tabla("codigoss")
    empleados = datos.Tabla("empleados")
    # Buscar en datos
    cat_empleados.orden = "categoria"
    cat_empleados.filtrar()
    codigoss.filtrar()
    empleados.ir_a(frm.getvalue("id"))
    pag = pagina.Pagina("Edición de empleado", nivel=4, fecha=2)
    htm.form_edicion("Edición de empleado", "empleados.py?accion=actualizar")
    print(htm.hidden("id", frm.getvalue("id")))
    htm.input_texto("Nombre", "nombre", empleados.registro["nombre"])
    htm.input_combo("Categoría:", "categoria_id", cat_empleados.resultado, ["id", "categoria"], 
        empleados.registro["categoria_id"])
    htm.input_texto("CI:", "ci", empleados.registro["ci"])
    htm.input_texto("Dirección:", "direccion", empleados.registro["direccion"])
    htm.input_texto("Teléfono:", "telefono", empleados.registro["telefono"])
    htm.input_texto("eMail:", "email", empleados.registro["email"])
    htm.input_texto('Sexo:', 'sexo', empleados.registro["sexo"])
    htm.input_fecha('F.Nac.:', 'f_nac', empleados.registro["f_nac"])
    htm.input_texto('E.Civil:', 'e_civil', empleados.registro["e_civil"])
    htm.input_fecha2("Fecha de ingreso", "ingreso", empleados.registro["ingreso"])
    htm.input_numero('Hijos (para DGI):', 'hijos', empleados.registro["hijos"])
    htm.input_check("Exclusión de mínimo no imponible:", "emni", empleados.registro["emni"])
    htm.input_combo("Código de Seguro de Salud:", "codigoss", codigoss.resultado, ["id", "codigo"], 
        empleados.registro["codigoss"])
    htm.input_check("Activo:", "activo", empleados.registro["activo"])
    htm.input_memo("Notas:", "notas", empleados.registro["notas"])
    htm.botones("empleados.py?accion=listado")
    htm.form_edicion_fin()
    pag.fin()
    
def actualizar(frm):
    """ Actualiza datos de un empleado """
    empleados = datos.Tabla("empleados")
    empleados.ir_a(frm.getvalue("id"))
    # TODO: debería chequear que el nuevo nombre no esté duplicado
    # La alternativa es que no se pueda modificar el nombre
    empleados.registro["nombre"] = frm.getvalue("nombre")
    empleados.registro["categoria_id"] = frm.getvalue("categoria_id")
    empleados.registro["ci"] = frm.getvalue("ci")
    empleados.registro["direccion"] = frm.getvalue("direccion")
    empleados.registro["telefono"] = frm.getvalue("telefono")
    empleados.registro["email"] = frm.getvalue("email")
    empleados.registro["sexo"] = frm.getvalue("sexo")
    empleados.registro["f_nac"] = funciones.fecha_a_mysql(frm.getvalue("f_nac"))
    empleados.registro["e_civil"] = frm.getvalue("e_civil")
    empleados.registro["ingreso"] = funciones.fecha_a_mysql(frm.getvalue("ingreso"))
    empleados.registro["notas"] = frm.getvalue("notas")
    empleados.registro["hijos"] = frm.getvalue("hijos")
    empleados.registro["codigoss"] = frm.getvalue("codigoss")
    empleados.registro["emni"] = frm.getvalue("emni")
    empleados.registro["activo"] = frm.getvalue("activo")
    empleados.actualizar()
    listado(frm)
def eliminar(frm):
    """Eliminar una categoría de empleados"""
    # no lo implemento porque habría que eliminar cada empleado o convertirlo a
    # categoria
    # por ahora no es necesario y me da pereza
    listado(frm)
if __name__ == "__main__":
    form = cgi.FieldStorage()
    accion = form.getvalue("accion", "listado")
    if accion == "nuevo":
        nuevo()
    elif accion == "agregar":
        agregar(form)
    elif accion == "editar":
        editar(form)
    elif accion == "actualizar":
        actualizar(form)
    elif accion == "eliminar":
        eliminar(form)
    else:
        listado(form)

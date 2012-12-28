#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Lista de clientes"""
import cgi
import cgitb ; cgitb.enable()
import htm
import datos
import funciones
import pagina
def listado(frm):
    """Listado de clientes"""
    pag = pagina.Pagina("Listado de clientes", 10)
    print(htm.encabezado("Clientes", "Recepción", "geined.py?accion=recepcion"))
    print("<table class='tabla_barra'><tr>")
    print(htm.td(htm.boton("Nuevo", "cli.py?accion=nuevo")))
    print("<td>")
    print("<form action='cli.py?accion=listado' method='post'>")
    print(htm.texto_barra("Buscar texto:"))
    print("<input title='Teclee texto a buscar' type='text' name='busqueda'>")
    print("<input type='submit' class='boton' value='Buscar'>")
    print("</td><td>")
    print("</form>")
    print("<form action='cli.py?accion=listado' method='post'>")
    print(htm.texto_barra("Filtrar por tipo de cliente:"))
    print """<select name="filtro" title="Filtro por tipo de cliente">
        <option value="0">Todos</option>
        <option value="1">Desconocidos</option>
        <option value="2">Alumnos</option>
        <option value="3">Drop-outs</option>
        <option value="4">Ex-Alumnos</option>
        <option value="5">En espera</option>
        <option value="6">Interesados</option>
        <option value="7">No contactar</option>
        <option value="8">Expulsados</option>
        </select><input type="submit" class='boton' value="Filtrar">"""
    print("</form>")
    print '</td>'
    print "</tr></table>"
    # cargar datos
    clientes = datos.Tabla("clientes")
    if frm.has_key("busqueda"):
        clientes.filtro = " nombre like '%" + str(frm["busqueda"].value) + "%'"
        clientes.orden = " nombre "
    else:
        if frm.has_key("filtro"):
            clientes.filtro = "categoria_id='" + str(frm["filtro"].value) + "'"
            clientes.orden = " nombre "
        else:
            clientes.orden = "nombre"
            clientes.limite = "30"
    clientes.filtrar()
    htm.encabezado_tabla(["Nº", "Nombre", "Teléfono", "Categoría", "Notas", 
        "Acciones"])
    for fila in clientes.resultado:
        ident = str(fila["id"])
        htm.fila_resaltada()
        print(htm.td(ident))
        print(htm.td(fila["nombre"]))
        print(htm.td(fila["telefono"]))
        # categoria
        cat_clientes = datos.Tabla("cat_clientes")
        cat_clientes.ir_a(fila["categoria_id"])
        print(htm.td(cat_clientes.registro["categoria"]))
        print(htm.td(fila["notas"][0:60] + "..."))
        print '<td>'
        htm.boton_detalles("cli_ver.php?id=" + ident)
        htm.boton_editar("cli.py?accion=editar&id=" + ident)
        htm.boton_eliminar("cli.py?accion=eliminar&id=" + ident)
        print '</td></tr>'
    htm.fin_tabla()
    pag.fin()
def nuevo():
    """Pagina de datos de nuevo cliente"""
    # Base de datos
    cat_clientes = datos.Tabla("cat_clientes")
    cat_clientes.filtrar()
    pag = pagina.Pagina("Nuevo cliente", nivel=10, fecha=1)
    htm.form_edicion("Nuevo cliente", "cli.py?accion=agregar")
    htm.input_texto('Nombre:', 'nombre', '')
    htm.input_texto('Direccion:', 'direccion', '')
    htm.input_texto('Teléfono:', 'telefono', '')
    htm.input_texto('E-Mail:', 'email', '')
    htm.input_combo('Categoría:', 'categoria_id', 
        cat_clientes.resultado, ["id", "categoria"], '')
    htm.input_texto('CI:', 'ci', '')
    htm.input_fecha("Ultimo contacto:", "ultimo_contacto", 
        funciones.fecha_a_mysql(funciones.hoy()))
    htm.input_memo("Notas:", "notas", "")
    htm.botones("cli.py?accion=listado")
    htm.form_edicion_fin()
    pag.fin()
def agregar(frm):
    """Agrega un nuevo cliente"""
    #pag = pagina.Pagina("Agregando clientes", 10)
    clientes = datos.Tabla("clientes")
    clientes.buscar("nombre", frm["nombre"].value)
    if clientes.num_filas == 0:
        clientes.registro["nombre"] = frm["nombre"].value
        clientes.registro["direccion"] = frm["direccion"].value
        clientes.registro["telefono"] = frm["telefono"].value
        clientes.registro["email"] = frm["email"].value
        clientes.registro["ci"] = frm["ci"].value
        clientes.registro["categoria_id"] = frm["categoria_id"].value
        clientes.registro["ultimo_contacto"] = \
            funciones.fecha_a_mysql(frm["ultimo_contacto"].value)
        clientes.registro["notas"] = frm["notas"].value
        clientes.insertar()
        listado(frm)
        # htm.redirigir("cli.py?accion=listado")
    else:
        pag = pagina.Pagina("Problema al agregar clientes", 10)
        htm.duplicado('cli.py?accion=listado')
        pag.fin()
    # pag.fin()
def editar(frm):
    """Formulario de edicion de clientes"""
    pag = pagina.Pagina("Edicion de clientes", nivel=10, fecha=1)
    clientes = datos.Tabla("clientes")
    clientes.ir_a(frm["id"].value)
    cat_clientes = datos.Tabla("cat_clientes")
    htm.form_edicion("Edición de datos del cliente", 
        "cli.py?accion=actualizar")
    htm.campo_oculto("id", frm["id"].value)
    htm.input_texto('Nombre:', 'nombre', clientes.registro["nombre"])
    htm.input_texto('CI:', 'ci', clientes.registro["ci"])
    htm.input_texto('Dirección:', 'direccion', clientes.registro["direccion"])
    htm.input_texto('Telefono:', 'telefono', clientes.registro["telefono"])
    htm.input_texto('E-Mail:', 'email', clientes.registro["email"])
    htm.input_combo('Categoría:', 'categoria_id', cat_clientes.resultado, 
        ["id", "categoria"], clientes.registro["categoria_id"])
    if clientes.registro["ultimo_contacto"] == None:
        clientes.registro["ultimo_contacto"] = \
            funciones.fecha_a_mysql("01/01/01")
    htm.input_fecha("Ultimo contacto:", "ultimo_contacto", 
        clientes.registro["ultimo_contacto"])
    htm.input_memo("Notas:", "notas", clientes.registro["notas"])
    htm.botones("cli.py?accion=listado")
    htm.form_edicion_fin()
    pag.fin()
def actualizar(frm):
    """Actualiza datos de la tabla clientes"""
    pag = pagina.Pagina("Actualizando datos de clientes", 10)
    clientes = datos.Tabla("clientes")
    clientes.ir_a(frm["id"].value)
    clientes.registro["nombre"] = frm["nombre"].value
    clientes.registro["direccion"] = frm["direccion"].value
    clientes.registro["telefono"] = frm["telefono"].value
    clientes.registro["email"] = frm["email"].value
    clientes.registro["categoria_id"] = frm["categoria_id"].value
    clientes.registro["ci"] = frm["ci"].value
    clientes.registro["ultimo_contacto"] = \
        funciones.fecha_a_mysql(frm.getvalue("ultimo_contacto","01/01/01"))
    clientes.registro["notas"] = frm["notas"].value
    clientes.actualizar()
    htm.redirigir("cli.py?accion=listado")
    pag.fin()
def eliminar(frm):
    """Elimina cliente tomando precaucion de eliminar datos hijos eliminables"""
    # debería haber un paso de comprobación de nivel de autorización ?
    # Recuperar variables */
    pag = pagina.Pagina("Eliminacion de registros", 5)
    ident = str(frm["id"].value)
    filtro = "id = '" + ident + "'"
    # Verificar boletas a su nombre
    dat = datos.Datos()
    sql = "SELECT COUNT(*) as numero FROM bol_cont WHERE cliente_id='" +\
        ident + "'"
    dat.cursor.execute(sql)
    fil = dat.cursor.fetchone()
    numero = fil["numero"]
    if numero == 0:
        # Borrar tablas hijas
        llamadas = datos.Tabla("llamadas")
        llamadas.filtro = filtro
        llamadas.borrar_filtro()
        cta_clientes = datos.Tabla("cta_clientes")
        cta_clientes.filtro = filtro
        cta_clientes.borrar_filtro()
        alumnos = datos.Tabla("alumnos")
        alumnos.filtro = filtro
        alumnos.borrar_filtro()
        clientes = datos.Tabla("clientes")
        clientes.borrar(ident)
        htm.redirigir("cli.py?accion=listado")
    else:
        print(htm.h3("NO se pudo eliminar este cliente: tiene BOLETAS " + \
            "CONTADO a su nombre"))
        print(htm.button("Volver","cli.py?accion=listado"))
        pag.fin()
def main():
    """PRincipal"""
    form = cgi.FieldStorage(keep_blank_values = True)
    accion = form.getvalue("accion", "listado")
    if accion == 'listado':
        listado(form)
    elif accion == 'nuevo':
        nuevo()
    elif accion == "agregar":
        agregar(form)
    elif accion == "editar":
        editar(form)
    elif accion == "actualizar":
        actualizar(form)
    elif accion == "eliminar":
        eliminar(form)
    
if __name__ == "__main__":
    main()
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import cgitb; cgitb.enable()
import datos
import htm
import cgi
import funciones
import pagina
"""Listado de interesados"""
def listado():
    """Listado de Interesados"""
    pag = pagina.Pagina("Listado de interesados", 5)
    clientes = datos.Tabla("clientes")
    alumnos = datos.Tabla("alumnos")
    alumnos.orden = "id DESC"
    cursos = datos.Tabla("cursos")
    clientes.filtro = "categoria_id=6"
    clientes.orden = "ultimo_contacto DESC"
    clientes.filtrar()
    total = clientes.num_filas
    print("<table><tr><td>")
    htm.button("Volver", "geined.py?accion=academico")
    htm.button("Busqueda compleja", "int.py?accion=compleja")
    print("</td></tr></table>")
    htm.h3("Hay: " + str(total) + " interesados")
    htm.encabezado_tabla(["Nº", "Nombre", "Telefono", "eMail", "Ultimo curso",
        "Ultimo contacto", "Notas", "Acciones"])
    for fila in clientes.resultado:
        ident = str(fila['id'])
        alumnos.buscar("cliente_id", ident)
        if alumnos.encontrado:
            curso_id = alumnos.registro["curso_id"]
            cursos.buscar("id", curso_id)
            if cursos.encontrado:
                curso = cursos.registro["curso"]
            else:
                curso = "Desconocido"
        else:
            curso = "Nunca cursó"
        htm.fila_resaltada()
        print(htm.td(ident))
        print(htm.td(fila['nombre']))
        print(htm.td(fila['telefono']))
        print(htm.td(fila['email']))
        print(htm.td(curso))
        print(htm.td(funciones.mysql_a_fecha(fila["ultimo_contacto"])))
        print(htm.td(fila['notas']))
        print('<td>')
        htm.boton_editar("int.py?accion=editar&id=" + ident)
        htm.boton_detalles("int.py?accion=detalles&id=" + ident)
        print('</td></tr>')      
    htm.fin_tabla()
    htm.button("Volver", "geined.py?accion=academico")
    pag.fin()

def editar(frm):
    """Edición de interesados"""
    pag = pagina.Pagina("Edición de clientes", nivel=5, fecha=1)
    clientes = datos.Tabla("clientes")
    clientes.buscar("id", frm.getvalue("id"))
    cat_clientes = datos.Tabla("cat_clientes")
    htm.form_edicion("Editar datos de cliente", "int.py?accion=actualizar")
    htm.campo_oculto("id", frm.getvalue("id"))
    htm.input_texto('Nombre:', 'nombre', clientes.registro["nombre"])
    htm.input_texto('Dirección:', 'direccion', clientes.registro["direccion"])
    htm.input_texto('Telefono:', 'telefono', clientes.registro["telefono"])
    htm.input_texto('E-Mail:', 'email', clientes.registro["email"])
    htm.input_combo('Categoría:', 'categoria_id', cat_clientes.resultado, ["id", "categoria"], clientes.registro["categoria_id"])
    htm.input_texto('CI:', 'ci', clientes.registro["ci"])
    htm.input_fecha("Ultimo contacto:", "ultimo_contacto", funciones.mysql_a_fecha(clientes.registro["ultimo_contacto"]))
    htm.input_memo("Notas:", "notas", clientes.registro["notas"])
    htm.botones("int.py?accion=listado")
    pag.fin()

def actualizar(frm):
    """Actualizar datos del cliente"""
    clientes = datos.Tabla("clientes")
    clientes.buscar("id", frm.getvalue("id"))
    clientes.registro["nombre"] = frm.getvalue("nombre")
    clientes.registro["direccion"] = frm.getvalue("direccion")
    clientes.registro["telefono"] = frm.getvalue("telefono")
    clientes.registro["email"] = frm.getvalue("email")
    clientes.registro["categoria_id"] = frm.getvalue("categoria_id")
    clientes.registro["ci"] = frm.getvalue("ci")
    clientes.registro["ultimo_contacto"] = funciones.fecha_a_mysql(frm.getvalue("ultimo_contacto"))
    clientes.registro["notas"] = frm.getvalue("notas")
    clientes.actualizar()
    listado()

def imprimir():
    """Imprimir informe sobre interesados"""
    pag = pagina.Pagina("Listado de interesados", 5, fecha=0, tipo="informe")
    clientes = datos.Tabla("clientes")
    clientes.filtro = "categoria_id=6"
    clientes.filtrar()
    htm.h3("Hay un total de " + str(clientes.num_filas) + " interesados")
    htm.encabezado_tabla(["Nº", "Nombre", "Telefono", "eMail", "Notas"])
    for fila in clientes.resultado:
        print("<tr>")
        ident = fila['id']
        print(htm.td(str(ident)))
        print(htm.td(fila['nombre']))
        print(htm.td(fila['telefono']))
        print(htm.td(fila['email']))
        print(htm.td(fila['notas']))
        print('</tr>')
    htm.fin_tabla()
    htm.button("<--","int.py?accion=listado")
    pag.fin()

def detalles(frm):
    """Detalles del cliente / drop-out"""
    pag = pagina.Pagina("Detalles del cliente interesado", 5)
    # Bases de datos
    clientes = datos.Tabla("clientes")
    alumnos = datos.Tabla("alumnos")
    cursos = datos.Tabla("cursos")
    empleados = datos.Tabla("empleados")
    depositos = datos.Tabla("depositos")
    # Procesamiento de datos
    id_cliente = frm.getvalue("id")
    clientes.buscar("id", id_cliente)
    alumnos.filtro = "cliente_id = " + str(id_cliente)
    alumnos.orden = "id DESC"
    alumnos.filtrar()
    htm.button("Volver", "int.py")
    htm.h3("Datos de: " + clientes.registro["nombre"])
    htm.encabezado_tabla(["Nº", "Curso", "Sucursal", "Docente", "Notas"])
    for fila in alumnos.resultado:
        htm.fila_resaltada()
        cursos.buscar("id", fila["curso_id"])
        print(htm.td(str(cursos.registro["id"])))
        print(htm.td(cursos.registro["curso"]))
        depositos.buscar("id", cursos.registro["deposito_id"])
        print(htm.td(depositos.registro["deposito"]))
        empleados.buscar("id", cursos.registro["empleado_id"])
        print(htm.td(empleados.registro["nombre"]))
        print(htm.td(cursos.registro["notas"]))
    htm.fin_tabla()
    pag.fin()
def compleja():
    """Formulario para búsqueda compleja de interesados"""
    pag = pagina.Pagina("Busqueda compleja de interesados", nivel=5, fecha=2)
    # filtros
    htm.form_edicion("Criterios", "int.py?accion=informe")
    print("<tr><td>Buscar:</td><td>interesados ...</td></tr>")
    htm.input_fecha("Entre:", "fecha1", "")
    htm.input_fecha2("Y:", "fecha2", "")
    htm.botones("int.py")
    htm.form_edicion_fin()
    pag.fin()
    
def informe(frm):
    """Informe de interesados"""
    pag = pagina.Pagina("Informe de interesados", nivel=5, fecha=0, tipo="informe")
    htm.h2("Criterios de búsqueda: interesados en período")
    # Recuperar FORM
    fecha_inicio = frm.getvalue("fecha1", 0)
    fecha_fin = frm.getvalue("fecha2", 0)
    # Datos
    clientes = datos.Tabla("clientes")
    alumnos = datos.Tabla("alumnos")
    cursos = datos.Tabla("cursos")
    clientes.orden = "ultimo_contacto DESC"
    alumnos.orden = "id DESC"
    htm.h3("Entre la fecha:" + str(fecha_inicio))
    htm.h3("Y la fecha:" + str(fecha_fin))
    # FILTRADO: 
    # Separar los que son Interesados
    clientes.filtro = "categoria_id = 6"
    # Separar los que tiene ultimo contacto entre INICIO y FIN
    if fecha_inicio != 0 and fecha_inicio != "//":
        clientes.filtro = clientes.filtro + " AND ultimo_contacto > " + funciones.fecha_a_mysql(fecha_inicio)
    if fecha_fin != 0 and fecha_fin != "//":
        clientes.filtro = clientes.filtro + " AND ultimo_contacto < " + funciones.fecha_a_mysql(fecha_fin)
    clientes.filtrar()
    htm.button("...", "int.py?accion=compleja")
    htm.encabezado_tabla(["Nº", "Nombre", "Telefono", "Correo", "Ultimo curso", "Utimo contacto", "Notas"])
    for fila in clientes.resultado:
        htm.fila_resaltada()
        print(htm.td(fila["id"]))
        print(htm.td(fila["nombre"]))
        print(htm.td(fila["telefono"]))
        print(htm.td(fila["email"]))
        alumnos.buscar("cliente_id", fila["id"])
        if alumnos.encontrado:
            cursos.buscar("id", alumnos.registro["curso_id"])
            curso = cursos.registro["curso"]
        else:
            curso = "---"
        print(htm.td(curso))
        print(htm.td(funciones.mysql_a_fecha(fila["ultimo_contacto"])))
        print(htm.td(fila["notas"]))
        print("</tr>")
    htm.fin_tabla()
    htm.button("...", "int.py?accion=compleja")
    pag.fin()
def main():
    """Principal"""
    form = cgi.FieldStorage()
    accion = form.getvalue("accion", "listado")
    if accion == "listado":
        listado()
    elif accion == "editar":
        editar(form)
    elif accion == "actualizar":
        actualizar(form)
    elif accion == "imprimir":
        imprimir()
    elif accion == "detalles":
        detalles(form)
    elif accion == "compleja":
        compleja()
    elif accion == "informe":
        informe(form)
    else:
        listado()

if __name__ == "__main__":
    main()
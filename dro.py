#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cgitb; cgitb.enable()
import datos
import htm
import cgi
import funciones
import pagina
def listado(frm):
    """Listado de Drop-Outs"""
    pag = pagina.Pagina("Listado de drop-outs", 5)
    print(htm.encabezado("Listado de drop-outs", "Académico", 
                         "geined.py?accion=academico"))
    clientes = datos.Tabla("clientes")
    alumnos = datos.Tabla("alumnos")
    depositos = datos.Tabla("depositos")
    alumnos.orden = "id DESC"
    cursos = datos.Tabla("cursos")
    clientes.filtro = "categoria_id=3"
    clientes.orden = "ultimo_contacto DESC"
    clientes.filtrar()
    total = clientes.num_filas
    print("<table class='barra'><tr><td>")
    htm.button("Busqueda compleja", "dro.py?accion=compleja")
    # htm.button("Imprimir", "dro.py?accion=imprimir")
    print("</td><td> Filtrar por sucursal:</td><td>")
    print("<form action='dro.py?accion=listado' method='post'>")
    print """<select name="filtro" title="Filtro por Sucursal">
        <option value="">Todos</option>
        <option value="1">Central</option>
        <option value="2">Costa de Oro</option>
        <option value="3">Carrasco</option>
        </select><input type="submit" value="Filtrar">"""
    print("</form>")
    filtro_sucursal = frm.getvalue("filtro", "")
    print("</td></tr></table>")
    htm.h3("Hay: " + str(total) + " drop-outs")
    if filtro_sucursal != "":
        depositos.buscar("id", filtro_sucursal)
        htm.h2("Filtrado por sucursal:" + depositos.registro["deposito"])
    htm.encabezado_tabla(["Nº", "Nombre", "Telefono", "eMail", "Ultimo curso",
        "Ultimo contacto", "Notas", "Acciones"])
    for fila in clientes.resultado:
        ident = str(fila['id'])
        alumnos.buscar("cliente_id", ident)
        if alumnos.encontrado:
            curso_id = alumnos.registro["curso_id"]
            cursos.buscar("id", curso_id)
            ident = str(fila['id'])
            if filtro_sucursal != "":
                if str(cursos.registro["deposito_id"]) == filtro_sucursal:
                    print("<tr class='fila_datos'>")
                    curso = cursos.registro["curso"]
                    print(htm.td(ident) +
                        htm.td(fila['nombre']) +
                        htm.td(fila['telefono']) +
                        htm.td(fila['email']) +
                        htm.td(curso) +
                        htm.td(funciones.mysql_a_fecha(fila["ultimo_contacto"])) +
                        htm.td(fila['notas']))
                    print('<td>')
                    htm.boton_editar("dro.py?accion=editar&id=" + ident)
                    htm.boton_detalles("dro.py?accion=detalles&id=" + ident)
                    print('</td></tr>')
            else:
                print("<tr class='fila_datos'>")
                curso = cursos.registro["curso"]
                print(htm.td(ident) +
                    htm.td(fila['nombre']) +
                    htm.td(fila['telefono']) +
                    htm.td(fila['email']) +
                    htm.td(curso) +
                    htm.td(funciones.mysql_a_fecha(fila["ultimo_contacto"])) +
                    htm.td(fila['notas']))
                print('<td>')
                htm.boton_editar("dro.py?accion=editar&id=" + ident)
                htm.boton_detalles("dro.py?accion=detalles&id=" + ident)
                print('</td></tr>')
        else:
            print("<tr class='fila_datos'>")
            print(htm.td(ident) +
                htm.td(fila['nombre']) +
                htm.td(fila['telefono']) +
                htm.td(fila['email']) +
                htm.td("DESCONOCIDO") +
                htm.td(funciones.mysql_a_fecha(fila["ultimo_contacto"])) +
                htm.td(fila['notas']))
            print('<td>')
            htm.boton_editar("dro.py?accion=editar&id=" + ident)
            # htm.boton_detalles("dro.py?accion=detalles&id=" + ident)
            print('</td></tr>')
    htm.fin_tabla()
    pag.fin()

def editar(frm):
    """Edición de drop-outs"""
    pag = pagina.Pagina("Edición de clientes", nivel=5, fecha=1)
    clientes = datos.Tabla("clientes")
    clientes.buscar("id", frm.getvalue("id"))
    cat_clientes = datos.Tabla("cat_clientes")
    htm.form_edicion("Editar datos de cliente", "dro.py?accion=actualizar")
    htm.campo_oculto("id", frm.getvalue("id"))
    htm.input_texto('Nombre:', 'nombre', clientes.registro["nombre"])
    htm.input_texto('Dirección:', 'direccion', clientes.registro["direccion"])
    htm.input_texto('Telefono:', 'telefono', clientes.registro["telefono"])
    htm.input_texto('E-Mail:', 'email', clientes.registro["email"])
    htm.input_combo('Categoría:', 'categoria_id', cat_clientes.resultado, 
                    ["id", "categoria"], clientes.registro["categoria_id"])
    htm.input_texto('CI:', 'ci', clientes.registro["ci"])
    htm.input_fecha("Ultimo contacto:", "ultimo_contacto", 
                    funciones.mysql_a_fecha(clientes.registro["ultimo_contacto"]))
    htm.input_memo("Notas:", "notas", clientes.registro["notas"])
    htm.botones("dro.py?accion=listado")
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
    listado(frm)

def imprimir():
    """Imprimir informe sobre drop-outs"""
    pag = pagina.Pagina("Listado de drop-outs", 5, fecha=0, tipo="informe")
    clientes = datos.Tabla("clientes")
    clientes.filtro = "categoria_id=3"
    clientes.filtrar()
    htm.h3("Hay un total de " + str(clientes.num_filas) + " drop-outs")
    htm.encabezado_tabla(["Nº", "Nombre", "Telefono", "eMail", "Notas"])
    for fila in clientes.resultado:
        print("<tr>")
        ident = fila['id']
        print(htm.td(str(ident)) +
            htm.td(fila['nombre']) +
            htm.td(fila['telefono']) +
            htm.td(fila['email']) +
            htm.td(fila['notas']))
        print('</tr>')
    htm.fin_tabla()
    print(htm.button("<--","dro.py?accion=listado"))
    pag.fin()

def detalles(frm):
    """Detalles del cliente / drop-out"""
    pag = pagina.Pagina("Detalles del cliente / drop-out", 5)
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
    htm.h3("Datos de: " + clientes.registro["nombre"])
    htm.encabezado_tabla(["Nº", "Curso", "Sucursal", "Docente", "Notas"])
    i = 0
    for fila in alumnos.resultado:
        htm.fila_alterna(i)
        cursos.buscar("id", fila["curso_id"])
        depositos.buscar("id", cursos.registro["deposito_id"])
        empleados.buscar("id", cursos.registro["empleado_id"])
        print(htm.td(str(cursos.registro["id"])) +
            htm.td(cursos.registro["curso"]) +
            htm.td(depositos.registro["deposito"]) +
            htm.td(empleados.registro["nombre"]) +
            htm.td(cursos.registro["notas"]))
    htm.fin_tabla()
    pag.fin()
def compleja():
    pag = pagina.Pagina("Busqueda compleja de drop-outs", nivel=5, fecha=2)
    tipo_curso = datos.Tabla("tipo_curso")
    depositos = datos.Tabla("depositos")
    # filtros
    tipo_curso.orden = "tipo"
    tipo_curso.filtrar()
    depositos.orden = "deposito"
    depositos.filtrar()
    htm.form_edicion("Criterios", "dro.py?accion=informe")
    print("<tr><td>Buscar:</td><td>drop-outs ...</td></tr>")
    htm.input_check("Por sucursal:", "suc", "0")
    htm.input_combo("Sucursal:", "deposito_id", depositos.resultado, 
                    ["id", "deposito"], "CUALQUIERA")
    htm.input_check("Por tipo:", "tip", "0")
    htm.input_combo("Tipo:", "tipo_id", tipo_curso.resultado, 
                    ["id", "tipo"], "")
    htm.input_texto('Dias:', 'dias', '')
    htm.input_texto('Horas:', 'horas', '')
    htm.input_fecha("Entre:", "fecha1", "")
    htm.input_fecha2("Y:", "fecha2", "")
    htm.botones("dro.py")
    htm.form_edicion_fin()
    pag.fin()
def informe(frm):
    pag = pagina.Pagina("Informe de Drop-Outs", nivel=5, fecha=0, 
                        tipo="informe")
    htm.h2("Criterios. de búsqueda:")
    # Recuperar FORM
    por_suc = frm.getvalue("suc")
    por_tip = frm.getvalue("tip")
    deposito_id = frm.getvalue("deposito_id", 0)
    tipo_id = frm.getvalue("tipo_id", 0)
    dias = frm.getvalue("dias", "")
    horas = frm.getvalue("horas","")
    fecha_inicio = frm.getvalue("fecha1", 0)
    fecha_fin = frm.getvalue("fecha2", 0)
    # Datos
    clientes = datos.Tabla("clientes")
    clientes.orden = "nombre"
    alumnos = datos.Tabla("alumnos")
    alumnos.orden = "id DESC"
    cursos = datos.Tabla("cursos")
    tipo_curso = datos.Tabla("tipo_curso")
    # Seteo
    deposito = "CUALQUIERA"
    if por_suc == "1":
        depositos = datos.Tabla("depositos")
        depositos.buscar("id", deposito_id)
        deposito = depositos.registro["codigo"]
    tipo = "CUALQUIERA"
    if por_tip == "1":
        tipo_curso = datos.Tabla("tipo_curso")
        tipo_curso.buscar("id", tipo_id)
        tipo = tipo_curso.registro["codigo"]
    htm.h3("Sucursal: " + deposito)
    htm.h3("Tipo de curso: " + tipo)
    htm.h3("Dias: " + dias)
    htm.h3("Horas: " + horas)
    htm.h3("Entre la fecha:" + str(fecha_inicio))
    htm.h3("Y la fecha:" + str(fecha_fin))
    # FILTRADO: 
    # Separar los que son Drop-outs
    clientes.filtro = "categoria_id = 3"
    # Separar los que tiene ultimo contacto entre INICIO y FIN
    if fecha_inicio != 0 and fecha_inicio != "//":
        clientes.filtro = clientes.filtro + " AND ultimo_contacto > " + funciones.fecha_a_mysql(fecha_inicio)
    if fecha_fin != 0 and fecha_fin != "//":
        clientes.filtro = clientes.filtro + " AND ultimo_contacto < " + funciones.fecha_a_mysql(fecha_fin)
    clientes.filtrar()
    htm.button("...", "dro.py?accion=compleja")
    htm.encabezado_tabla(["Nº", "Nombre", "Telefono", "Correo", "Ultimo curso", 
                          "Utimo contacto", "Notas"])
    for fila in clientes.resultado:
        flag = True
        # ver alumno
        alumnos.buscar("cliente_id", fila["id"])
        if not alumnos.encontrado:
            flag = False
        else:
            # Ver el curso:
            cursos.buscar("id", alumnos.registro["curso_id"])
            # Ver si coincide el tipo de curso
            if tipo != "CUALQUIERA":
                flag = flag and tipo in cursos.registro["curso"]
            # Ver si coincide la sucursal
            if deposito != "CUALQUIERA":
                flag = flag and deposito in cursos.registro["curso"]
            # Ver si coinciden los días
            if dias != "":
                flag = flag and dias in cursos.registro["curso"]
            # Ver si coinciden las horas
            if horas != "":
                flag = flag and horas in cursos.registro["curso"]
            # Si el flag da OK
            if flag:
                # Imprimir linea con datos del cliente
                print("<tr class='fila_datos'>")
                print(htm.td(fila["id"]) +
                    htm.td(fila["nombre"]) +
                    htm.td(fila["telefono"]) +
                    htm.td(fila["email"]) +
                    htm.td(cursos.registro["curso"]) +
                    htm.td(funciones.mysql_a_fecha(fila["ultimo_contacto"])) +
                    htm.td(fila["notas"]))
                print("</tr>")
        # Fin Loop
    htm.fin_tabla()
    print(htm.button("...", "dro.py?accion=compleja"))
    pag.fin()
if __name__ == "__main__":
    form = cgi.FieldStorage()
    accion = form.getvalue("accion", "listado")
    if accion == "listado":
        listado(form)
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
        listado(form)

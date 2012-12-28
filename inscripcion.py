#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Inscripcion en un unico programa"""
import cgi
import cgitb; cgitb.enable()
import datos
import htm
import pagina
def ins_cliente(frm):
    """Inscripcion: agregar cliente"""
    pag = pagina.Pagina("Inscripción - Paso 1", 4)
    print(htm.h2("Elegir cliente")) 
    print(htm.table(
        htm.tr(
            htm.td('<form action = "alu_inscripcion1.py" method="post">' +
                '<input type="text" name="busqueda">' +
                '<input type="submit" value="Buscar"></form>') +
            htm.td(htm.button("Volver", "geined.py?accion=recepcion"))
            )
        )
    )
    busqueda = frm.getvalue("busqueda", "")
    clientes = datos.Tabla("clientes")
    cat_clientes = datos.Tabla("cat_clientes")
    clientes.orden = 'nombre'
    if busqueda != "":
        clientes.filtro = 'nombre LIKE "%' + busqueda + '%" '
    clientes.filtrar()
    i = 0
    htm.encabezado_tabla(["Nombre", "Categoría", "Notas", "Acciones"])
    for fila in clientes.resultado:
        ident = fila['id']
        htm.fila_alterna(i)
        print(htm.td(fila['nombre']))
        cat_clientes.ir_a(fila["categoria_id"])
        categoria = cat_clientes.registro['categoria']
        print(htm.td(categoria))
        print(htm.td(fila['notas']))
        print(htm.td(
            htm.button("Inscribir", "alu_inscripcion2.py?cliente_id=" + 
            str(ident))))
        print('</tr>')
        i = i +1
    htm.fin_tabla()
    print(htm.button('Volver', 'geined.py?accion=recepcion'))
    pag.fin()
def ins_curso(frm):
    """Segundo paso de inscripción: agrega curso"""
    clientes = datos.Tabla("clientes")
    cliente_id = frm.getvalue("cliente_id", "")
    clientes.ir_a(cliente_id)
    pag = pagina.Pagina("Inscripción: paso 2", 4)
    print(htm.h2("Elegir curso para: " + clientes.registro['nombre']))
    # elegir curso
    print('<table><tr><td>')
    print(htm.button('Volver', 'geined.py?accion=recepcion'))
    print("""</td><td>
        <form action = "alu_inscipcion2.py?cliente_id='.$cliente_id.'" method="post">
            <input type="text" name="busqueda">
            <input type="submit" value="Buscar">
        </form>
        </td></tr></table>""")
    # cargar datos
    # OJO! Solo cursos abiertos
    busqueda = frm.getvalue("busqueda", "")
    cursos = datos.Tabla("cursos")
    empleados = datos.Tabla("empleados")
    depositos = datos.Tabla("depositos")
    tipo_curso = datos.Tabla("tipo_curso")
    cursos.orden = "curso"
    if busqueda != "":
        cursos.filtro = 'curso LIKE LIKE "%' + str(busqueda) + '%" AND finalizado IS NULL '
    else:
        cursos.filtro = "finalizado IS NULL"
    cursos.filtrar()
    htm.encabezado_tabla(["Nº", "Curso", "Docentes", "Sucursal", "Tipo",
        "Dias", "Horario", "Notas", "Acciones"])
    i = 0
    for fila in cursos.resultado:
        htm.fila_alterna(i)
        ident = fila['id']
        print(htm.td(str(ident)))
        print(htm.td(fila['curso']))
        # D O C E N T E
        empleados.ir_a(fila["empleado_id"])
        print(htm.td(empleados.registro["nombre"]))
        # SUCURSAL
        depositos.ir_a(fila["deposito_id"])
        print(htm.td(depositos.registro["deposito"]))
        # T I P O
        tipo_curso.ir_a(fila["tipo_id"])
        print(htm.td(tipo_curso.registro["tipo"]))
        print(htm.td(fila['dias']))
        print(htm.td(fila['horas']))
        print(htm.td(fila['notas']))
        print('<td>')
        print(htm.button("Continuar", "alu_inscripcion3.py?cliente_id=" + 
            str(cliente_id) + "&curso_id=" + str(ident)))
        i = i + 1
    htm.fin_tabla()
    print(htm.button('Volver', 'geined.py?accion=recepcion'))
    pag.fin()
def ins_confirmar(frm):
    """Inscripcion, tercer paso: confirmar datos"""
    pag = pagina.Pagina("Inscripción: confirmar datos", 4)
    # Recuperar variables
    cliente_id = frm.getvalue("cliente_id", 0)
    curso_id = frm.getvalue("curso_id", 0)
    clientes = datos.Tabla("clientes")
    tipo_pago = datos.Tabla("tipo_pago")
    tipo_pago.filtrar()
    cursos = datos.Tabla("cursos")
    clientes.ir_a(cliente_id)
    cursos.ir_a(curso_id)  
    htm.formulario("alu_inscribir.py")
    htm.encabezado_tabla(["Campo", "Valor"])
    # CLiente
    print(htm.hidden("cliente_id", cliente_id))
    print('<tr><td>Nombre:</td><td>' + clientes.registro['nombre'] + '</td></tr>')
    # Curso
    print(htm.hidden("curso_id", curso_id))
    print('<tr><td>Curso:</td><td>' + cursos.registro['curso'] + '</td></tr>')
    htm.input_combo("Tipo de pago:", "tipo_pago_id", tipo_pago.resultado, ["id", "tipo"], "")
    htm.input_numero("Cuota:", "cuota", "")
    # Definir el asunto PAGO
    htm.botones("geined.py?accion=recepcion")
    htm.fin_formulario()
    htm.fin_tabla()
    pag.fin()
def inscribir(frm):
    """Rutina principal para inscribir alumno"""
    # @TODO: Falta considerar que pasa si no se ingresan variables POST
    cliente_id = frm.getvalue("cliente_id")
    curso_id = frm.getvalue("curso_id")
    alumnos = datos.Tabla("alumnos")
    alumnos.filtro = " (cliente_id = '%s') AND (curso_id = '%s')" % (cliente_id, curso_id)
    alumnos.filtrar()
    if alumnos.num_filas == 0:
        alumnos.registro["cliente_id"] = cliente_id
        alumnos.registro["curso_id"] = curso_id
        alumnos.registro["tipo_pago_id"] = frm.getvalue("tipo_pago_id")
        alumnos.registro["cuota"] = frm.getvalue("cuota")
        alumnos.insertar()
        # se cambia la categoría del cliente
        clientes = datos.Tabla("clientes")
        clientes.ir_a(cliente_id)
        clientes.resultado["categoria_id"] = 2
        clientes.actualizar()
        pag = pagina.Pagina("Inscripciones", 10)
        print(htm.h2("Alumno inscripto"))
        print(htm.button("Ir a caja","caja.php?accion=listado"))
        print(htm.button("Volver","geined.py?accion=recepcion"))
        pag.fin()
    else:
        htm.duplicado("geined.py?accion=recepcion")
if __name__ == "__main__":
    form = cgi.FieldStorage()
    if "cliente_id" not in form:
        ins_cliente(form)
    elif "curso_id" not in form:
        ins_curso(form)
    elif "confirmado" not in form:
        ins_confirmar(form)
    else:
        inscribir(form)
        

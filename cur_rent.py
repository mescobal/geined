#!/usr/bin/env python 
# -*- coding: utf8 -*-
"""Rentabilidad por cursos"""
import cgitb; cgitb.enable()
import cgi
import funciones
import datos
import htm
import pagina
def seleccionar():
    """Seleccionar sucursal"""
    pag = pagina.Pagina("Rentabilidad de cursos", 3)
    print(htm.h2("Seleccionar sucursal"))
    depositos = datos.Tabla("depositos")
    depositos.filtrar()
    for fila in depositos.resultado:
        print(htm.button(fila["deposito"], "cur_rent.py?accion=listado&deposito_id=" +\
            str(fila["id"])))
    print(htm.button("Volver","geined.py?accion=financiero"))
    pag.fin()
def listado(frm, estilo):
    """Listado de rentabilidad por curso"""
    # Recuperar variables
    deposito_id = frm.getvalue('deposito_id', 1)
    # datos
    depositos = datos.Tabla("depositos")
    depositos.buscar("id", deposito_id)
    cod_suc = depositos.registro["codigo"]
    # Buscar registros 
    if estilo == "reporte":
        pag = pagina.Pagina("Rentabilidad de cursos de " + \
            depositos.registro["deposito"], nivel=5, tipo="informe")
    else:
        pag = pagina.Pagina("Rentabilidad de cursos de " + \
            depositos.registro["deposito"], 5)
    print(htm.encabezado("Rentabilidad de cursos", "Volver", "geined.py?accion=financiero"))
    print("<table class='tabla_barra'><tr>")
    print(htm.td(htm.boton("Reporte", "cur_rent.py?accion=reporte&deposito_ud=" + str(deposito_id))))
    print("</tr></table>")
    cursos = datos.Tabla("cursos")
    cursos.filtro = "curso LIKE '" + cod_suc + "%' AND finalizado IS NULL"
    cursos.orden = "curso"
    cursos.filtrar()
    
    alumnos = datos.Tabla("alumnos")
    tipo_curso = datos.Tabla("tipo_curso")
    empleados = datos.Tabla("empleados")
    salario = datos.Tabla("salario")
    clientes = datos.Tabla("clientes")
    tipo_pago = datos.Tabla("tipo_pago")
    
    # Listar CURSOS
    tot_alumnos = 0
    ganancia = 0
    for fila in cursos.resultado:
        # Alumnos - se contempla excluir drop-outs
        alumnos.filtro = "curso_id = " + str(fila["id"]) + \
            " AND (finalizado IS NULL)"
        alumnos.filtrar()
        subtotal = alumnos.num_filas
        tot_alumnos = tot_alumnos + subtotal
        tot_ing = 0
        # Calcular las horas x semana del curso para rentabilidad
        tipo_curso.buscar("id", fila["tipo_id"])
        rubro = tipo_curso.registro["rubro"]
        horas = ver_horas(rubro)
        duracion = tipo_curso.registro["duracion"]
        # Empleados
        empleados.buscar("id", fila["empleado_id"])
        docente = empleados.registro["nombre"]
        # Buscar en salarios la hora semanal mensual        
        salario.filtro = "(fecha <= '" + \
            funciones.fecha_a_mysql(funciones.hoy()) + \
            "') AND (cat_empleado_id =" + \
            str(empleados.registro["categoria_id"]) + ")"
        salario.orden = "fecha DESC"
        salario.filtrar()
        hsm = salario.registro["hora_semanal"]
        print(htm.h3(cursos.registro["curso"] + " [Nº alumnos: " + str(subtotal) +\
            ", Docente: " + docente))
        print("<table><tr><td><table>")
        # Listado de alumnos
        for alumno in alumnos.resultado:
            clientes.buscar("id", alumno["cliente_id"])
            htm.fila_resaltada()
            print(htm.td(clientes.registro["nombre"]))
            # Tipo de pago
            tipo_pago.buscar("id", alumno["tipo_pago_id"])
            if not tipo_pago.encontrado:
                pago = "Desconocido"
            else:
                pago = tipo_pago.registro["tipo"]
            print(htm.td(pago))
            # Se ajusta el monto de la cuota si el pago es del módulo
            if tipo_pago.registro["id"] == 12:
                cuota = alumno["cuota"] / duracion
            else:
                cuota = alumno["cuota"]
            htm.linea_moneda(cuota)
            tot_ing = tot_ing + cuota
            print("</tr>")
        print("</table>")
        ing_fee = tot_ing - (tot_ing * 0.10)
        print("</td><td>")
        htm.encabezado_tabla(["Campo", "Valor"])
        htm.input_label("Nº de horas:", horas)
        htm.input_label("Duración:", duracion)
        print("<tr>")
        print(htm.td("Ingreso bruto:"))
        htm.linea_moneda(tot_ing * duracion)
        print("</tr><tr>")
        ing_net = ing_fee * duracion
        print(htm.td("Ingreso neto (s/fee):"))
        htm.linea_moneda(ing_net)
        print("</tr><tr>")
        print(htm.td("HSM del docente:"))
        htm.linea_moneda(hsm)
        print("</tr><tr>")
        print(htm.td("Salario mensual:"))
        htm.linea_moneda(hsm * horas)
        print("</tr><tr>")
        sal_cur = hsm * horas * duracion
        print(htm.td("Salario del curso:"))
        htm.linea_moneda(sal_cur)
        print("</tr><tr>")
        print(htm.td("Aguinaldo:"))
        htm.linea_moneda(sal_cur/12)
        print("</tr>")
        valor = sal_cur / 12
        print(htm.tr(htm.td("Sal.Vac.:") +
            htm.td(funciones.moneda(valor), "right")))
        print("<tr>")
        print(htm.td("Enero y Febrero") +
            htm.td(funciones.moneda((sal_cur/12) * 2), "right"))
        print("</tr><tr>")
        sal_tot = sal_cur + ((sal_cur/12) * 4)
        print(htm.td("Total salario docente:") +
            htm.td(funciones.moneda(sal_tot), "right"))
        print("</tr><tr>")
        ganancia_sub = funciones.to_decimal(ing_net) - sal_tot
        ganancia = ganancia + ganancia_sub
        print(htm.td("Ganancia del curso:") +
            htm.td(funciones.moneda(ganancia_sub), "right"))
        print("</tr>")
        htm.fin_tabla()
        htm.fin_tabla()
        print("<br />")
        print(htm.hr())
        print("<br />")
    print(htm.h2("Ganancia total por cursos: " + funciones.moneda(ganancia)))
    print(htm.h2("Nº total de alumnos: " + str(tot_alumnos)))
    print(htm.button("Volver", "cur_rent.py?accion=listado"))
    pag.fin()

def ver_horas(rubro):
    """Devuelve número de horas semanales del curso según rubro"""
    tabla = {"411011":3, "411012":3, "411013":4, "411014":4, "41015":6,
        "411016":6, "411021":2, "411022":2}
    if str(rubro) in tabla:
        horas = tabla[str(rubro)]
    else:
        horas = 0
    return horas
    
def main():
    """Principal"""
    form = cgi.FieldStorage()
    accion = form.getvalue("accion", "seleccionar")
    if form.getvalue("deposito_id", "") == "":
        accion = "seleccionar"
    else:
        accion = "listado"
    if accion == "seleccionar":
        seleccionar()
    elif accion == "listado":
        listado(form, "listado")
    elif accion == "reporte":
        listado(form, "reporte")

if __name__ == "__main__":
    # Rutina para evitar ejecución ante importacion
    main()
    

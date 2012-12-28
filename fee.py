#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Rutina para cálculo del fee """
import cgitb; cgitb.enable()
import funciones
import datos
import htm
import csv
import cgi
import StringIO
import pagina
# Listar pagos x cuotas realizados entre 2 fechas
# Discriminado x sucursal
def error(texto=""):
    """Pagina que genera error se selecciona central"""
    pag = pagina.Pagina("Error", 20)
    print(htm.h2("La sucursal central NO paga Fee"))
    print("Tipo de error:" + texto)
    print(htm.button("Volver","fee.py?accion=parametros"))
    pag.fin()
def reporte(frm):
    """Reporte de fee"""
    listado_basico(frm, "informe")
def listado(frm):
    """Genera un listado básico"""
    listado_basico(frm, "comun")
def listado_basico(frm, formato):
    """Listado de fee"""
    if not frm.has_key("deposito_id"):
        pagina.error_variable("fee.py")
    else:
        deposito_id = frm.getvalue('deposito_id')
        if (deposito_id != "2") and (deposito_id != "3"):
            error(str(type(deposito_id)) + " ----" )
        elif (not frm.has_key("finicio")) or (not frm.has_key("ffinal")):
            pagina.error_variable("fee.py")
        else:
            pag = pagina.Pagina("Listado para pago de Fee", nivel=5, fecha=0, 
                                tipo=formato)
            # Datos
            depositos = datos.Tabla("depositos")
            # buscar registros
            depositos.buscar("id", deposito_id)
            sucursal = depositos.registro['deposito']
            print(htm.h2("Pago de Fee sucursal: " + sucursal))
            clientes = datos.Tabla("clientes")
            bol_det = datos.Tabla("bol_det")
            bol_cont = datos.Tabla("bol_cont")
            # Recuperación de variables
            fi = funciones.fecha_a_mysql(frm['finicio'].value)
            ff = funciones.fecha_a_mysql(frm['ffinal'].value)
            if deposito_id == "2":
                rubros = ["411011", "411013", "411015", "411021", "412001"]
            if deposito_id == "3":
                rubros = ["411012", "411014", "411016", "411022", "412002"]
            htm.h3("Desde " + frm["finicio"].value + " hasta " + \
                frm["ffinal"].value)
            if formato != "informe":
                print(htm.button("Formato reporte",
                                 "fee.py?accion=reporte&deposito_id=" + 
                                 str(deposito_id) + "&finicio=" + 
                                 frm["finicio"].value + "&ffinal=" + 
                                 frm["ffinal"].value))
                print(htm.button("Exportar a panilla",
                                 "fee.py?accion=csv&deposito_id=" + 
                                 str(deposito_id) + 
                                 "&finicio=" + fi + "&ffinal=" + ff))
                print(htm.button("Volver","fee.py?accion=parametros"))
            # Seleccionar todas las boletas contado entre fi y ffinal
            bol_cont.orden = " fecha "
            bol_cont.filtro = "fecha BETWEEN '" + fi + "' AND '" + ff + "'"
            bol_cont.filtrar()
            # print(bol_cont.filtro)
            i = 0
            total = 0
            htm.encabezado_tabla(["Nº", "Fecha", "Nombre", "CI", "Curso", 
                                  "Cuota"])
            for fila in bol_cont.resultado:
                # Recuperar variables
                ident = fila['id']
                cliente_id = fila['cliente_id']
                fecha = fila['fecha']
                # Buscar registros
                clientes.buscar("id", cliente_id)
                bol_det.buscar("bol_cont_id", ident)
                for row in bol_det.resultado:
                    # si el rubro corresponde a cuota de la sucursal 
                    # seleccionada, se lista
                    rub_bol = str(row['rubro'])
                    if rub_bol in rubros:
                        htm.fila_alterna(i)
                        print(htm.td(ident))
                        print(htm.td(funciones.mysql_a_fecha(fecha)))
                        print(htm.td(clientes.registro["nombre"]))
                        print(htm.td(clientes.registro["ci"]))
                        print(htm.td(row['detalle']))
                        print(htm.td(funciones.moneda(row['total']), "right" ))
                        print('</tr>')
                        total = total + row['total']
                        # acumular valores para suma
                        i = i + 1
            print(htm.tfoot(htm.tr(htm.td("Total:") +
                htm.td() + htm.td() + htm.td() + 
                htm.td(funciones.moneda(total), "right"))))
            htm.fin_tabla()
            if formato != "informe":
                print(htm.button("Volver","fee.py?accion=parametros"))
            else:
                print(htm.button("...", "fee.py?accion=parametros"))
            pag.fin()
            # al finalizar: calcular monto total, porcentaje y fee
def exp_csv(frm):
    """Rutina para exportar a archivo CSV"""
    if not frm.has_key("deposito_id"):
        pagina.error_variable("fee.py")
    else:
        deposito_id = frm.getvalue("deposito_id")
        if (deposito_id != "2") and (deposito_id != "3"):
            error(str(type(deposito_id)) + "----")
        elif (not frm.has_key("finicio")) or (not frm.has_key("ffinal")):
            pagina.error_variable("fee.py")
        else:
            # Comienza proceso real
            depositos = datos.Tabla("depositos")
            bol_cont = datos.Tabla("bol_cont")
            clientes = datos.Tabla("clientes")
            bol_det = datos.Tabla("bol_det")
            finicio = frm.getvalue("finicio")
            ffinal = frm.getvalue("ffinal")
            # Se asume por defectos rubros de sucursal Costa
            rubros = ["411011", "411013", "411015", "411017", "411021", 
                      "412001"]
            if deposito_id == "1":
                htm.redirigir("fee.py?accion=error")
            if deposito_id == "2":
                rubros = ["411011", "411013", "411015", "411017", "411021", 
                          "412001"]
            if deposito_id == "3":
                rubros = ["411012", "411014", "411016", "411018", "411022", 
                          "412002"]
            # buscar registros
            depositos.buscar("id", deposito_id)
            sucursal = depositos.registro['deposito']
            # Salida a una cadena
            salida = StringIO.StringIO()           
            feecsv = csv.DictWriter(salida, ["No", "Fecha", "Nombre", 
                                             "Detalle", "Monto"])
            # Seleccionar todas las boletas contado entre fi y ffinal
            bol_cont.filtro = "fecha BETWEEN '" + finicio + "' AND '" + \
                ffinal + "'"
            bol_cont.orden = "fecha"
            bol_cont.filtrar()
            filename = "fee_" + sucursal[0:2] + "_" + finicio + "_" + ffinal + \
                ".csv"
            total = 0
            for fila in bol_cont.resultado:
                # Recuperar variables */
                fecha = fila['fecha']
                # Buscar registros
                clientes.buscar("id", fila["cliente_id"])
                nombre = clientes.registro['nombre']
                bol_det.buscar("bol_cont_id", fila["id"])
                for row in bol_det.resultado:
                    # si el rubro corresponde a cuota de la sucursal 
                    # seleccionada, se lista
                    rub_bol = str(row['rubro'])
                    if rub_bol in rubros:
                        feecsv.writerow({"No":str(fila["id"]), 
                                         "Fecha":funciones.mysql_a_fecha(fecha),
                            "Nombre":nombre, "Detalle":row["detalle"], 
                            "Monto":row["total"]})
                        total = total + row['total']
                        # acumular valores para suma
            feecsv.writerow({"Nombre":"TOTAL", "Monto":total})
            HEADERS = '\r\n'.join([
                    "Content-type: %s;",
                    "Content-Disposition: attachment; filename=%s",
                    "Content-Title: %s",
                    "Content-Length: %i",
                    "\r\n", # empty line to end headers
                ])
            length = len(salida.getvalue())
            print(
                HEADERS % ('text/csv', filename, filename, length)
                )
            print(salida.getvalue())
            salida.close()
    
def parametros():
    """Definición de parámetros para el cálculo del fee"""
    # recuperacion de variables
    # búsqueda de datos
    pag = pagina.Pagina("Cálculo de fee: seleccionar sucursal", nivel=5, 
                        fecha=2)
    depositos = datos.Tabla("depositos")
    depositos.filtrar()
    htm.form_edicion("Datos sobre el Fee", "fee.py?accion=listado")
    htm.input_combo("Sucursal:", "deposito_id", depositos.resultado, 
                    ["id", "deposito"], "2")
    htm.input_fecha("Fecha de inicio:", "finicio", 
                    funciones.fecha_a_mysql(funciones.hoy()))
    htm.input_fecha2("Fecha de finalización:", "ffinal", 
                     funciones.fecha_a_mysql(funciones.hoy()))
    htm.botones("geined.py?accion=administracion")
    htm.form_edicion_fin()
    pag.fin()
if __name__ == '__main__':
    form = cgi.FieldStorage()
    accion = "parametros"
    if form.has_key("accion"):
        accion = form["accion"].value
    if accion == "parametros":
        parametros()
    elif accion == "listado":
        listado(form)
    elif accion == "error":
        error()
    elif accion == "csv":
        exp_csv(form)
    elif accion == "reporte":
        reporte(form)
    else:
        pagi = pagina.Pagina("Error", 20)
        htm.h2("Faltan variables para completar la acción")
        htm.button("Volver", "fee.py")
        pagi.fin()

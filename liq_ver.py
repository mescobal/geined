#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Rutina de manejo de sueldo individual"""
import cgitb; cgitb.enable()
import cgi
import htm
import pagina
import funciones
import datos
import calc_sueldos
import ConfigParser

def listado(frm):
    """ Listado de Detalle de Liquidacion """
    # Recuperacion de variables 
    liquidacion_id = frm.getvalue("liquidacion_id")
    # Bases de datos
    liquidacion = datos.Tabla("liquidacion")
    empleados = datos.Tabla("empleados")
    det_liquidacion = datos.Tabla("det_liquidacion")
    # Búsquedas
    liquidacion.ir_a(liquidacion_id)
    det_liquidacion.buscar("liquidacion_id", liquidacion_id)
    # Seteo de totales
    total_horas_semanales = 0
    total_horas_reloj = 0
    total_nominal = 0
    total_descuentos = 0
    total_adelantos = 0
    total_liquido = 0
    total_irpf = 0
    # pagina
    pag = pagina.Pagina("Detalle de liquidación de sueldos")
    print(htm.encabezado("Detalle de liquidación de sueldos", 
                         "Listado de liquidaciones", 
        "liq.py?accion=listado"))
    print("<div class='barra'>Fecha: " + \
        funciones.mysql_a_fecha(liquidacion.registro["fecha"]) + \
        " - Corresponde a: " + liquidacion.registro["corresponde"] + "  " + \
        htm.boton("Nuevo", "liq_ver.py?accion=nuevo&liquidacion_id=" + \
        str(liquidacion_id)))
    htm.encabezado_tabla(["Empleado", "HS", "HR", "Nominal", "CESS",
        "IRPF", "Adelantos", "Líquido", "Acciones"])
    # detalle de liquidacion
    for fila in det_liquidacion.resultado:
        empleado_id = fila["empleado_id"]
        nominal = fila["nominal"]
        #Búsqueda de registros
        empleados.ir_a(empleado_id)
        # Cálculos
        total_nominal = total_nominal + nominal
        descuentos = fila["bps"] + fila["disse"] + fila["frl"]
        total_descuentos = total_descuentos + descuentos
        adelantos = fila["adelantos"]
        total_adelantos = total_adelantos + adelantos
        liquido = nominal - descuentos -fila["irpf"] - adelantos
        total_liquido = total_liquido + liquido
        total_horas_semanales = total_horas_semanales + fila["horas_sem"]
        total_horas_reloj = total_horas_reloj + fila["horas_reloj"]
        # total_extras = total_extras + fila["extras"]
        total_irpf = total_irpf + fila["irpf"]
        # Celdas        
        print("<tr class='fila_datos'>")
        print(htm.td(empleados.registro["nombre"]))
        print(htm.td(fila["horas_sem"], "right"))
        print(htm.td(fila["horas_reloj"], "right"))
        # print(htm.td(funciones.moneda(fila["extras"]), "right"))
        print(htm.td(funciones.moneda(nominal), "right"))
        print(htm.td(funciones.moneda(descuentos), "right"))
        print(htm.td(funciones.moneda(fila["irpf"]), "right"))
        print(htm.td(funciones.moneda(adelantos), "right"))
        print(htm.td(funciones.moneda(liquido), "right"))
        print("<td>")
        htm.boton_eliminar("liq_ver.py?accion=eliminar&id=" + str(fila["id"]))
        print(htm.button("Recibo",  "liq_ver.py?accion=recibo&id=" + \
            str(fila["id"])))
        print(htm.button("Chequear", "liq_ver.py?accion=chequear&id=" + \
            str(fila["id"])))
        print("</td></tr>")
    print("<tfoot>")
    print(htm.tr(
                 htm.td("Totales") +
                 htm.td(total_horas_semanales,  "right") + 
                 htm.td(total_horas_reloj, "right") +
                 htm.td(funciones.moneda(total_nominal),  "right") +
                 htm.td(funciones.moneda(total_descuentos),  "right") +
                 htm.td(funciones.moneda(total_irpf),  "right") +
                 htm.td(funciones.moneda(total_adelantos),  "right") +
                 htm.td(funciones.moneda(total_liquido),  "right") +
                 htm.td("")))
    print("</tfoot>")
    htm.fin_tabla()
    liquidacion.registro["liquido"] = total_liquido
    liquidacion.registro["bps"] = total_descuentos
    liquidacion.registro["dgi"] = total_irpf
    liquidacion.actualizar()
    pag.fin()
def nuevo(frm):
    """Nuevo detalle de liquidacion de sueldos"""
    # Recuperar variables
    liquidacion_id = frm.getvalue("liquidacion_id")
    # Bases de datos
    empleados = datos.Tabla("empleados")
    liquidacion = datos.Tabla("liquidacion")
    # Buscar BDD
    liquidacion.ir_a(liquidacion_id)
    empleados.orden = "nombre"
    empleados.filtro = "activo=1"
    empleados.filtrar()
    # Pagina
    pag = pagina.Pagina("Liquidación de horas trabajadas", 4)
    htm.form_edicion("Liquidación de horas trabajadas", 
                     "liq_ver.py?accion=agregar")
    print(htm.hidden("liquidacion_id", liquidacion_id))
    htm.input_combo('Empleado', 'empleado_id', 
                    empleados.resultado, ["id", "nombre"], '')
    htm.input_numero('Horas semanales:', 'horas_sem', '')
    htm.input_numero('Horas reloj:', 'horas_reloj', '')
    # htm.input_numero('Extras:', 'extras', '')
    htm.input_numero('Adelantos:', 'adelantos', '')
    htm.input_numero('Aporte CJJPP:', 'cjp', '')
    htm.input_numero("Aguinaldo:", "aguinaldo", "")
    htm.botones("liq_ver.py?accion=listado&liquidacion_id=" + \
        str(liquidacion_id))
    htm.form_edicion_fin()
    pag.fin()
def agregar(frm):
    """Agregar un item a liquidacion de sueldos"""
    # Insertar registro
    # Recuperar variables
    liquidacion_id = frm.getvalue("liquidacion_id")
    empleado_id = frm.getvalue("empleado_id")
    # Bases de datos
    det_liquidacion = datos.Tabla("det_liquidacion")
    liquidacion = datos.Tabla("liquidacion")
    salario = datos.Tabla("salario")
    empleados = datos.Tabla("empleados")
    # Buscar bases de datos
    liquidacion.ir_a(liquidacion_id)
    empleados.ir_a(empleado_id)
    cat_empleado_id = empleados.registro["categoria_id"]
    fecha = liquidacion.registro["fecha"]
    salario.filtro = "fecha <= '" + str(fecha) + "' AND cat_empleado_id=" + \
        str(cat_empleado_id)
    salario.orden = "fecha DESC"
    salario.filtrar()
    # @todo: no hay deteccion de errores en parámetros
    # Insertar registro
    det_liquidacion.nuevo()
    det_liquidacion.registro["liquidacion_id"] = liquidacion_id
    det_liquidacion.registro["empleado_id"] = empleado_id
    det_liquidacion.registro["horas_sem"] = frm.getvalue("horas_sem")
    det_liquidacion.registro["valor_hs"] = salario.registro["hora_semanal"]
    det_liquidacion.registro["ficto_semanal"] = salario.registro["ficto_semanal"]
    det_liquidacion.registro["horas_reloj"] = frm.getvalue("horas_reloj")
    #det_liquidacion.registro["extras"] = frm.getvalue("extras")
    #det_liquidacion.registro["adelantos"] = frm.getvalue("adelantos")
    det_liquidacion.registro["cjp"] = frm.getvalue("cjp")
    det_liquidacion.registro["aguinaldo"] = frm.getvalue("aguinaldo")
    det_liquidacion.insertar()
    #pag = pagina.Pagina("Ver id insertada", 20)
    # print(htm.h2(str(det_liquidacion.id_insertada)))
    #pag.fin()
    # det_liquidacion.ir_a(det_liquidacion.id_insertada)    
    det_liquidacion.ir_a(det_liquidacion.id_insertada)
    #pag = pagina.Pagina("Datos sobre insercion", 5)
    #print("<div class='barra'")
    #print(str(htm.h1(det_liquidacion.id_insertada)))
    #print("</div>")
    #pag.fin()
    # Calculos de liquidación de sueldos a partir de un registro 
    # de det_liquidacion"""
    sueldo = calc_sueldos.Sueldo(det_liquidacion.registro)
    det_liquidacion.registro["sueldo"] = sueldo.sueldo_semanal
    det_liquidacion.registro["valor_hr"] = sueldo.hora_reloj
    det_liquidacion.registro["sueldo_reloj"] = sueldo.sueldo_reloj
    det_liquidacion.registro["nominal"] = sueldo.nominal
    det_liquidacion.registro["antiguedad"] = sueldo.antiguedad
    det_liquidacion.registro["bps"] = sueldo.bps
    det_liquidacion.registro["disse"] = sueldo.seguro_salud
    det_liquidacion.registro["frl"] = sueldo.frl
    det_liquidacion.registro["irpf"] = sueldo.anticipo_irpf
    det_liquidacion.registro["liquido"] = sueldo.liquido
    det_liquidacion.registro["porcentaje_fonasa"] = sueldo.porcentaje_fonasa
    det_liquidacion.actualizar()
    listado(frm)
def editar(frm):
    """Editar detalle de liquidacion"""
    # Recuperación de variables
    # Base de datos
    det_liquidacion = datos.Tabla("det_liquidacion")
    empleados = datos.Tabla("empleados")
    # Buscar datos
    det_liquidacion.ir_a(frm.getvalue("id"))
    empleado_id = det_liquidacion.registro["empleado_id"]
    empleados.ir_a(empleado_id)
    nombre = empleados.registro["nombre"]
    # Pagina
    pag = pagina.Pagina("Edicion", 4)
    htm.form_edicion("Edicion de liquidacion de horas", 
                     "liq_ver.py?accion=actualizar")
    print(htm.hidden("liquidacion_id", 
                     det_liquidacion.registro["liquidacion_id"]))
    print(htm.hidden("id", frm.getvalue("id")))
    htm.input_label("Empleado:", nombre)
    htm.input_numero("Horas semanales:", "horas_sem", 
                     det_liquidacion.registro["horas_sem"])
    htm.input_numero("Horas reloj:", "horas_reloj", 
                     det_liquidacion.registro["horas_reloj"])
    #htm.input_numero("Extras:", 
    #                    "extras", det_liquidacion.registro["extras"])
    #htm.input_numero("Adelantos:", "adelantos", 
    #                  det_liquidacion.registro["adelantos"])"""
    htm.input_numero("Aguinaldo:", "aguinaldo", 
                     det_liquidacion.registro["aguinaldo"])
    htm.input_numero("Aportes CJJPP:", "cjp", det_liquidacion.registro["cjp"])
    htm.botones("liq_ver.py?accion=listado&liquidacion_id=" + \
        str(det_liquidacion.registro["liquidacion_id"]))
    htm.form_edicion_fin()
    pag.fin()
def actualizar(frm):
    """Actualizar datos de detalle de liquidacion"""
    # Recuperación de variables
    liquidacion_id = frm.getvalue("liquidacion_id")
    empleado_id = frm.getvalue("empleado_id")
    # Bases de datos
    det_liquidacion = datos.Tabla("det_liquidacion")
    liquidacion = datos.Tabla("liquidacion")
    salario = datos.Tabla("salario")
    empleados = datos.Tabla("empleados")
    # Buscar bases de datos
    liquidacion.ir_a(liquidacion_id)
    empleados.ir_a(empleado_id)
    cat_empleado_id = empleados.registro["categoria_id"]    
    fecha = liquidacion.registro["fecha"]
    salario.filtro = "fecha <= '" + str(fecha) + "' AND cat_empleado_id=" + \
        str(cat_empleado_id)
    salario.orden = "fecha DESC"
    salario.filtrar()    
    # Modificar
    det_liquidacion.registro["liquidacion_id"] = frm.getvalue("liquidacion_id")
    det_liquidacion.registro["empleado_id"] = frm.getvalue("empleado_id")
    det_liquidacion.registro["horas_sem"] = frm.getvalue("horas_sem")
    det_liquidacion.registro["valor_hs"] = salario.registro["hora_semanal"]
    det_liquidacion.registro["ficto_semanal"] = salario.registro["ficto_semanal"]
    det_liquidacion.registro["horas_reloj"] = frm.getvalue("horas_reloj")
    det_liquidacion.registro["extras"] = frm.getvalue("extras")
    det_liquidacion.registro["adelantos"] = frm.getvalue("adelantos")
    det_liquidacion.registro["cjp"] = frm.getvalue("cjp")
    det_liquidacion.registro["aguinaldo"] = frm.getvalue("aguinaldo")
    # Calculos
    sueldo = calc_sueldos.Sueldo(det_liquidacion.registro)
    det_liquidacion.registro["sueldo"] = sueldo.sueldo_semanal
    det_liquidacion.registro["valor_hr"] = sueldo.hora_reloj
    det_liquidacion.registro["sueldo_reloj"] = sueldo.sueldo_reloj
    det_liquidacion.registro["nominal"] = sueldo.nominal
    det_liquidacion.registro["antiguedad"] = sueldo.antiguedad
    det_liquidacion.registro["bps"] = sueldo.bps
    det_liquidacion.registro["disse"] = sueldo.seguro_salud
    det_liquidacion.registro["frl"] = sueldo.frl
    det_liquidacion.registro["irpf"] = sueldo.anticipo_irpf
    det_liquidacion.registro["liquido"] = sueldo.liquido
    det_liquidacion.registro["porcentaje_fonasa"] = sueldo.porcentaje_fonasa
    det_liquidacion.actualizar()
    listado(frm)
def recibo(frm):
    """Nuevo recibo de sueldos"""
    # Recuperación de variables
    detalle_id = frm.getvalue("id")
    # BDD
    det_liquidacion = datos.Tabla("det_liquidacion")
    empleados = datos.Tabla("empleados")
    cat_empleados = datos.Tabla("cat_empleados")
    liquidacion = datos.Tabla("liquidacion")
    # Buscar
    det_liquidacion.ir_a(detalle_id)
    empleados.ir_a(det_liquidacion.registro["empleado_id"])
    cat_empleados.ir_a(empleados.registro["categoria_id"])
    liquidacion.ir_a(det_liquidacion.registro["liquidacion_id"])
    pag = pagina.Pagina("Recibo de sueldo", nivel=4, tipo="recibo")
    config = ConfigParser.ConfigParser()
    config.readfp(open("./conf/geined.conf"))
    print(htm.table(
        htm.tr(
            htm.td(htm.h2(config.get("empresa", "nombre"))) + 
            htm.td("<b>Corresponde a:</b>") +
            htm.td("<b>" + liquidacion.registro["corresponde"] + "</b>") +
            htm.td(htm.img("./img/minilogo.png"), align="right", colspan=4)) +
        htm.tr(
            htm.td(config.get("empresa", "direccion")) +
            htm.td("M.T.S.S.:") +
            htm.td(config.get("empresa", "mtss")) +
            htm.td("R.U.C.:") +
            htm.td(config.get("empresa", "ruc"))) +
        htm.tr(
            htm.td(config.get("empresa", "grupo")) +
            htm.td("Nº planilla MTSS:") +
            htm.td(config.get("empresa", "planilla")) +
            htm.td("B.S.E.:") +
            htm.td(config.get("empresa", "bse"))) +
        htm.tr(
            htm.td(config.get("empresa", "subgrupo")) +
            htm.td("") +
            htm.td("") +
            htm.td("B.P.S.:") +
            htm.td(config.get("empresa", "bps")))))
    # @todo: poner sector correctamente
    print("</br>")
    # @todo: pasar fecha a formato mes - año 
    print(htm.table(
        htm.tr(
            htm.td(htm.b(empleados.registro["nombre"]), colspan=2) +
            htm.td("Categoría:") +
            htm.td(cat_empleados.registro["categoria"]) +
            htm.td("Empleado:") +
            htm.td(empleados.registro["id"])) +
        htm.tr(
            htm.td("CI:") +
            htm.td(empleados.registro["ci"]) +
            htm.td("Sector:") +
            htm.td("sector a rellenar") +
            htm.td("Fecha:") +
            htm.td(funciones.mysql_a_fecha(liquidacion.registro["fecha"]))) +
        htm.tr(
            htm.td("Ingreso:") +
            htm.td(funciones.mysql_a_fecha(empleados.registro["ingreso"])) +
            htm.td("Turno:") +
            htm.td("Decreto 611/80") +
            htm.td("Liq.:") +
            htm.td("Todas las liquidaciones"))))
    # TODO: acomodar hora semanal
    liquido = det_liquidacion.registro["liquido"]
    liquido_redondeado = funciones.redondeo(liquido)
    redondeo = liquido_redondeado - liquido
    total_descuentos = det_liquidacion.registro["bps"] + det_liquidacion.registro["disse"] + \
        det_liquidacion.registro["frl"] + det_liquidacion.registro["irpf"]
    print("---------------------")
    print(htm.table(
        htm.tr(
            htm.td(
                htm.table(
                    htm.caption("Nominal") +
                    htm.tr(
                        htm.td("Horas semanales:") +
                        htm.td(funciones.moneda(det_liquidacion.registro["valor_hs"]), "right") +
                        htm.td(det_liquidacion.registro["horas_sem"], "right") +
                        htm.td(funciones.moneda(det_liquidacion.registro["sueldo"]), "right")) +
                    htm.tr(
                        htm.td("Horas comunes:") +
                        htm.td(funciones.moneda(det_liquidacion.registro["valor_hr"]), "right") +
                        htm.td(det_liquidacion.registro["horas_reloj"], 
                               "right") +
                        htm.td(funciones.moneda(det_liquidacion.registro["sueldo_reloj"]), "right")) +
                    htm.tr(
                        htm.td("Antigüedad:") + htm.td("") + htm.td("") +
                        htm.td(funciones.moneda(det_liquidacion.registro["antiguedad"]), "right")) +
                    htm.tr(
                        htm.td(htm.b("Total nominal:")) + htm.td("") + htm.td("") +
                        htm.td(funciones.moneda(det_liquidacion.registro["nominal"]), "right")))) +
            htm.td(
                htm.table(
                    htm.caption("Descuentos") +
                    htm.tr(htm.td("BPS") +
                        htm.td("15%") +
                        htm.td(funciones.moneda(det_liquidacion.registro["bps"]), "right")) +
                    htm.tr(htm.td("FONASA") + 
                        htm.td(str(funciones.numero(det_liquidacion.registro["porcentaje_fonasa"],1)) + "%") +
                        htm.td(funciones.moneda(det_liquidacion.registro["disse"]), "right")) +
                    htm.tr(htm.td("FRL") +
                        htm.td("0,125%") +
                        htm.td(funciones.moneda(det_liquidacion.registro["frl"]), "right")) +
                    htm.tr(htm.td("Adelanto IRPF") + htm.td("") +
                        htm.td(funciones.moneda(det_liquidacion.registro["irpf"]), "right")) +
                    htm.tr(htm.td(htm.b("Total descuentos:")) + htm.td("") +
                        htm.td(funciones.moneda(total_descuentos), "right")) +
                    htm.tr(htm.td("Total neto:") + htm.td("") +
                        htm.td(funciones.moneda(liquido), "right")) +
                    htm.tr(htm.td("Redondeo:") + htm.td("") +
                        htm.td(funciones.moneda(redondeo), "right")) +
                    htm.tr(htm.td(htm.h2("Líquido a cobrar:")) + htm.td("") +
                        htm.td(funciones.moneda(liquido_redondeado), 
                               "right"))))) +
        htm.tr(
            htm.td("La empresa declara haber efectuado los aportes de seguridad correspondientes " + \
                " a los haberes del mes anterior según decreto 337/92.", 
                colspan=2)) +
        htm.tr(
            htm.td(htm.h2("Son " + funciones.a_palabras(liquido_redondeado)), 
                   colspan=2)) +
        htm.tr(
            htm.td("Por " + config.get("empresa", "nombre") +\
                ": ______________________") +
            htm.td("Firma del trabajador:____________________________________"))
        )
    )           
    print(htm.button('...',"liq_ver.py?accion=listado&liquidacion_id=" + \
        str(det_liquidacion.registro["liquidacion_id"])))
    pag.fin()            
def chequear(frm):
    """Rutina para chequear irpf"""
    # Recuperacion de valores
    det_liquidacion_id = frm.getvalue("id")
    # Bases de datos
    det_liquidacion = datos.Tabla("det_liquidacion")
    det_liquidacion.ir_a(det_liquidacion_id)
    liquidacion_id = det_liquidacion.registro["liquidacion_id"]
    sueldo = calc_sueldos.Sueldo(det_liquidacion.registro)
    pag = pagina.Pagina("Revisión de cálculo de IRPF", 20, tipo="recibo")
    print(htm.table(
        htm.tr(
            htm.td("Irpf 1") + htm.td(sueldo.montos_irpf[1])) +
        htm.tr(
            htm.td("Irpf 2") + htm.td(sueldo.montos_irpf[2])) +
        htm.tr(
            htm.td("Irpf 3") + htm.td(sueldo.montos_irpf[3])) +
        htm.tr(
            htm.td("Irpf 4") + htm.td(sueldo.montos_irpf[4])) +
        htm.tr(
            htm.td("Deducible 1") + htm.td(sueldo.montos_deducible[1])) +
        htm.tr(
            htm.td("Deducible 2") + htm.td(sueldo.montos_deducible[2])) +
        htm.tr(
            htm.td("Total IRPF") + htm.td(sueldo.anticipo_irpf))))
    print(htm.button("Volver", "liq_ver.py?accion=listado&liquidacion_id=" + \
        str(liquidacion_id)))
    pag.fin()
def eliminar(frm):
    """Eliminar registro detalle liquidacion de sueldos"""
    det_liquidacion = datos.Tabla("det_liquidacion")
    det_liquidacion.borrar(frm.getvalue("id"))
    listado(frm)
def main():
    """Principal"""
    form = cgi.FieldStorage()
    accion = form.getvalue("accion", "listado")
    if accion == "nuevo":
        nuevo(form)
    elif accion == "agregar":
        agregar(form)
    elif accion == "editar":
        editar(form)
    elif accion == "actualizar":
        actualizar(form)
    elif accion == "eliminar":
        eliminar(form)
    elif accion == "recibo":
        recibo(form)
    elif accion == "chequear":
        chequear(form)
    else:
        listado(form)

if __name__ == "__main__":
    main()
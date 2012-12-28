#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Manejo de informes financieros"""
import cgi
import cgitb; cgitb.enable()
import funciones
import datos
# import graficos
import pagina
import htm
def menu(frm):
    """Menú de informes financieros"""
    # Recuperar variables
    ano = frm.getvalue('ano',  str(funciones.ano_actual()))
    # Pagina
    pag = pagina.Pagina("Informes financieros", 4)
    print(htm.encabezado("Informes financieros", "Administración financiera", 
                         "geined.py?accion=financiero"))
    print("<table class='tabla_barra'><tr><td>")
    print(htm.button("Exportar a Planilla", "inf_fin.py?accion=exportar"))
    print(htm.button("Reportes",  'inf_fin.py?accion=listado'))
    print("</td><td>")
    htm.formulario("inf_fin.py?accion=calcular")
    print("Seleccione año:")
    print(htm.hidden("accion", "calcular"))
    htm.seleccionar_ano()
    print('<input type="submit" value="Recalcular" />')
    htm.fin_formulario()
    print("</td>")
    print("</tr></table>")
    print(htm.h2("Ingresos y egresos"))
    print("<table>")
    # INGRESOS
    linea_informe("Ingresos", "", 0, 0, "si")
    # Ingresos por ventas
    ingresos = - saldo_rubro("4",  ano)
    linea_informe("", "Ingresos por ventas",  0, ingresos)
    # GASTOS POR VENTAS
    gastos_ventas = saldo_rubro("511",  ano)
    no_operativos = saldo_rubro("52",  ano)
    gxv = gastos_ventas + no_operativos
    linea_informe("", "Gastos por ventas",  0, gxv)
    # MARGEN BRUTO
    margen_bruto = ingresos - gxv
    linea_informe("", "Margen bruto", 0, margen_bruto, "si")
    # GASTOS OPERATIVOS
    linea_informe("Gastos operativos", "", 0, 0, "Si")
    # Salarios 
    salarios_doc = saldo_rubro("512",  ano)
    salarios_nd = saldo_rubro("513",  ano)
    sociales = saldo_rubro("514",  ano)
    otras_rem = saldo_rubro("515",  ano)
    salarios = salarios_doc + salarios_nd + sociales + otras_rem
    linea_informe("", "Salarios y honorarios", salarios, 0)
    # Gastos académicos
    academicos = saldo_rubro("516",  ano)
    linea_informe("", "Gastos académicos",  academicos, 0)
    # Gastos administrativos
    administrativos = saldo_rubro("517",  ano)
    linea_informe("", "Gastos administrativos",  administrativos,  0)
    # Gastos local y equipos
    local = saldo_rubro("518",  ano)
    linea_informe("", "Gastos de local y equipos",  local, 0)
    # Gastos promocion
    publicidad = saldo_rubro("519",  ano)
    linea_informe("", "Gastos publicidad y promoción",  publicidad,  0)
    # Total de gastos
    gastos = salarios + academicos + administrativos + local + publicidad
    linea_informe("",  "Total de gastos", gastos, 0, "si")
    # Ingresos netos
    ing_netos = margen_bruto - gastos
    linea_informe("Ingreso neto", "", 0, ing_netos, "si")
    print('</table>')
    print(htm.hr())
    print(htm.h2("Activo y pasivo"))
    print("<table>")
    linea_informe("Activo", "", 0, 0, "si")
    linea_informe("Activo corriente", "", 0, 0)
    caja_ef = saldo_rubro("11101",  ano)
    caja_ch = saldo_rubro("11102",  ano)
    depositar  = saldo_rubro("111018", ano)
    caja = caja_ef + caja_ch - depositar
    linea_informe("", "Caja", 0, caja)
    linea_informe("", "Para depositar", 0, depositar)
    banco = saldo_rubro("11103",  ano) + saldo_rubro("112",  ano)
    linea_informe("", "Banco",  0, banco)
    caja_vo = saldo_rubro("113",  ano)
    linea_informe("", "Vouchers en caja",  0,  caja_vo)
    deudores = saldo_rubro("114",  ano)
    linea_informe("", "Deudores",  0, deudores)
    inventario = saldo_rubro("115", ano)
    linea_informe("", "Inventario",  0, inventario)
    suma_corriente = caja + depositar + banco + deudores + inventario + caja_vo
    linea_informe("", "Total corriente", 0, suma_corriente, "si")
    ac_fijo = saldo_rubro("122",  ano)
    linea_informe("Activo fijo", "", 0,ac_fijo)
    linea_informe("Total activo", "", 0, suma_corriente + ac_fijo, "si")
    linea_informe("Pasivo", "", 0, 0, "si")
    d_sueldos = saldo_rubro("213",  ano)
    linea_informe("", "Sueldos adeudados",  d_sueldos, 0)
    ac_varios = saldo_rubro("211001", ano)
    bookstore = saldo_rubro("211008", ano)
    linea_informe("", "Acreedores varios", ac_varios, 0)
    linea_informe("", "Bookstore",  bookstore, 0)
    t_pasivo = saldo_rubro("2",  ano)
    otros = t_pasivo - d_sueldos - ac_varios - bookstore
    linea_informe("Total pasivo", "", t_pasivo, 0, "si")
    patri = saldo_rubro("3",  ano)
    t_activo = saldo_rubro("1",  ano)
    c_patri = t_activo - t_pasivo
    linea_informe("Patrimonio", "", 0, patri, "si")
    linea_informe("Patrimonio calculado", "", 0, c_patri)
    linea_informe("Balance", "", 0, patri-c_patri, "si")
    print('</table>')

    pag.fin()
def linea_informe(titulo="", subtitulo="", gasto=0, ingreso=0, negrita="no"):
    """ IMprime una linea de informe financiero"""
    htm.fila_resaltada()
    if negrita == "no":
        print(htm.td(titulo))
        print(htm.td(subtitulo))
        if gasto !=0:
            print(htm.td(funciones.moneda(gasto),  align="right"))
        else:
            print(htm.td())
        if ingreso != 0:
            print(htm.td(funciones.moneda(ingreso), align="right"))
        else:
            print(htm.td())
    else:
        print(htm.td(htm.b(titulo)))
        print(htm.td(htm.b(subtitulo)))
        if gasto !=0:
            print(htm.td(htm.b(funciones.moneda(gasto)),  align="right"))
        else:
            print(htm.td())
        if ingreso != 0:
            print(htm.td(htm.b(funciones.moneda(ingreso)), align="right"))
        else:
            print(htm.td())
    print(htm.tr())
def saldo_rubro(rubro, ano):
    # Calcula el saldo del año para un grupo de rubros
    # Datos
    transacciones = datos.Tabla("transacciones")
    cuentas = datos.Tabla('cuentas')
    cuentas.filtro = "rubro like '" + str(rubro) + "%'"
    cuentas.filtrar()
    total = 0
    for cuenta in cuentas.resultado:
        transacciones.filtro = "cuenta_id=" + str(cuenta['id']) + " and year(fecha)=" + ano
        transacciones.filtrar()
        for item in transacciones.resultado:
            total = total + item["debe"] - item['haber']
    return total
def listado():
    """Listado de informes financieros"""
    pag = pagina.Pagina("Informe financiero", 3)
    print(htm.encabezado("Informes financiero", "Administración financiera", 
        "geined.py?accion=financiero"))
    print("<table class='tabla_barra'><tr>")
    print(htm.td(htm.boton("Nuevo", "inf_fin.py?accion=nuevo")))
    print("</tr></table>")
    htm.encabezado_tabla(["Fecha", "Conclusiones", "Acciones"])
    inf_fin = datos.Tabla("inf_fin")
    inf_fin.orden = "fecha"
    inf_fin.filtrar()
    for fila in inf_fin.resultado:
        htm.fila_resaltada()
        print(htm.td(funciones.mysql_a_fecha(fila["fecha"])))
        print(htm.td(fila["conclusion"]))
        print('<td>')
        htm.boton_detalles('inf_fin.py?accion=ver&id=' + str(fila['id']))
        htm.boton_editar('inf_fin.py?accion=editar&id=' + str(fila['id']))
        htm.boton_eliminar("inf_fin.py?accion=eliminar&id=" + str(fila['id']))
        print('</td></tr>')
    htm.fin_tabla()
    pag.fin()
def ver(frm):
    """Ver detalles de un informe financiero"""
    pag = pagina.Pagina("Informe financiero", 3)
    print(htm.encabezado("Detalle de Informe financiero", "Listado de informes", 
        "inf_fin.py?accion=listado"))
    inf_fin = datos.Tabla("inf_fin")
    inf_fin.ir_a(frm.getvalue("id"))
    #encabezado('Informe financiero');
    # generar_datos(); YA NO SE USA, USA DATOS ESCRITOS HASTA 2007
    #TODO: armar generador de datos para 2008 en adelante
    #generar_graficos();
    print("<table class='fila_datos'>")
    print("<caption>Informe al 28 de agosto de 2007</caption>")
    print("<tr>")
    print(htm.td(htm.b("Evolución del estado de la cuenta corriente")))
    print(htm.td(inf_fin.registro["bancos"]))
    print("</tr><tr>")
    print(htm.td(htm.img("img/cta_cte_mes.png")))
    print(htm.td(htm.img("img/cta_cte_acu.png")))
    print("</tr><tr>")
    # =========================
    print(htm.td(htm.b("Evolución de los gastos")))
    print(htm.td(inf_fin.registro["egresos"]))
    print("</tr><tr>")
    print(htm.td(htm.img("img/egresos_mes.png")))
    print(htm.td(htm.img("img/egresos_acu.png")))
    print("</tr><tr>")
    # =========================
    print(htm.td(htm.b("Evolución de los ingresos")))
    print(htm.td(inf_fin.registro["ingresos"]))
    print("</tr><tr>")
    print(htm.td(htm.img("img/ingresos_mes.png")))
    print(htm.td(htm.img("img/ingresos_acu.png")))
    print("</tr><tr>")
    # =========================
    print(htm.td(htm.b("Evolución de la ganancia")))
    print(htm.td(inf_fin.registro["ganancia"]))
    print("</tr><tr>")
    print(htm.td(htm.img("img/ganancia_mes.png")))
    print(htm.td(htm.img("img/ganancia_acu.png")))
    print("</tr><tr>")
    # =========================
    print(htm.td(htm.b("Conclusiones")))
    print(htm.td(inf_fin.registro["conclusion"]))
    print("</tr><tr>")
    print(htm.td(htm.b('Recomendaciones')))
    print(htm.td(inf_fin.registro["recomendaciones"]))
    print("</tr><table>")
    pag.fin()
def nuevo():
    """Nuevo informe financiero"""
    pass
    #inicio();
    #encabezado_fecha("Nuevo Informe Financiero");
    #boton("Volver","inf_fin.php?accion=listado");
    #formulario('inf_fin.php?accion=agregar');
    #$arr = array("Campo","Valor");
    #encabezado_tabla($arr);
    #input_fecha('Fecha:','fecha',fecha_a_mysql(date('d/m/Y')));
    #input_memo("Cuenta corriente:",'bancos','');
    #input_memo("Bancos baso 0:",'bancosb0','');
    #input_memo("Egresos",'egresos','');
    #input_memo("Ingresos",'ingresos','');
    #input_memo("Ganancia:",'ganancia','');
    #input_memo("Conclusión:",'conclusion','');
    #input_memo("Recomendaciones:",'recomendaciones','');
    #fin_tabla();
    #botones();
    #echo '</form>';
    #script_fecha();
    #boton("Volver","inf_fin.php?accion=listado");
    #fin();
#}
def agregar(frm):
    """Agregar un informe financiero"""
    inf_fin = datos.Tabla("inf_fin")
    inf_fin.nuevo()
    inf_fin.registro["fecha"] = funciones.fecha_a_mysql(frm.getvalue('fecha'))
    inf_fin.registro["bancos"] = frm.getvalue("bancos")
    inf_fin.registro["egresos"] = frm.getvalue("egresos")
    inf_fin.registro['ingresos'] = frm.getvalue('ingresos')
    inf_fin.registro['ganancia'] = frm.getvalue('ganancia')
    inf_fin.registro['conclusion'] = frm.getvalue('conclusion')
    inf_fin.registro['recomendaciones'] = frm.getvalue('recomendaciones')
    inf_fin.agregar()
    listado()
def editar(frm):
    """Editar un informe financiero"""
    inf_fin = datos.Tabla("inf_fin")
    inf_fin.ir_a(frm.getvalue('id'))
    #encabezado_fecha("Editar Informe Financiero");
    #boton("Volver","inf_fin.php?accion=listado");
    #formulario('inf_fin.php?accion=actualizar');
    #campo_oculto('id',$_GET['id']);
    #$arr = array("Campo","Valor");
    #encabezado_tabla($arr);
    #input_fecha('Fecha:','fecha',$fil['fecha']);
    #input_memo("Cuenta corriente:",'bancos',$fil['bancos']);
    #input_memo("Bancos baso 0:",'bancosb0',$fil['bancosb0']);
    #input_memo("Egresos",'egresos',$fil['egresos']);
    #input_memo("Ingresos",'ingresos',$fil['ingresos']);
    #input_memo("Ganancia:",'ganancia',$fil['ganancia']);
    #input_memo("Conclusión:",'conclusion',$fil['conclusion']);
    #input_memo("Recomendaciones:",'recomendaciones',$fil['recomendaciones']);
    #fin_tabla();
    #botones();
    #echo '</form>';
    #script_fecha();
    #boton("Volver","inf_fin.php?accion=listado");
    #fin();
def actualizar(frm):
    """Actualizar datos de un informe financiero"""
    inf_fin = datos.Tabla("inf_fin")
    inf_fin.ir_a(frm.getvalue("id"))
    inf_fin.registro["fecha"] = funciones.fecha_a_mysql(frm.getvalue('fecha'))
    inf_fin.registro["bancos"] = frm.getvalue("bancos")
    inf_fin.registro["egresos"] = frm.getvalue("egresos")
    inf_fin.registro['ingresos'] = frm.getvalue('ingresos')
    inf_fin.registro['ganancia'] = frm.getvalue('ganancia')
    inf_fin.registro['conclusion'] = frm.getvalue('conclusion')
    inf_fin.registro['recomendaciones'] = frm.getvalue('recomendaciones')
    inf_fin.actualizar()
    listado()
def eliminar(frm):
    """ Eliminar un registro de informe financiero"""
    inf_fin = datos.Tabla("inf_fin")
    inf_fin.borrar(frm.getvalue("id"))
    listado()
def main():
    """Principal"""
    form = cgi.FieldStorage()
    accion = form.getvalue("accion", "menu")
    if accion == "menu":
        menu(form)
    elif accion == 'listado':
        listado()
    elif accion == "nuevo":
        nuevo()
    elif accion == "agregar":
        agregar(form)
    elif accion == "editar":
        editar(form)
    elif accion == "ver":
        ver(form)
    elif accion == "actualizar":
        actualizar(form)
    elif accion == 'eliminar':
        eliminar(form)
        
if __name__ == "__main__":
    main()
    

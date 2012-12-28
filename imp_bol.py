#!/usr/bin/env python
import cgitb; cgitb.enable()
import cgi
import htm
import funciones
import datos
import pagina
def impbol(frm):
    """Imprimir boleta"""
    boleta_id = frm['boleta_id'].value
    deposito_id = frm['deposito_id'].value
    caja_id = frm['caja_id'].value
    cliente_id = frm['cliente_id'].value
    cola = "deposito_id=" + str(deposito_id) + "&caja_id=" + str(caja_id) + "&cliente_id=" + str(cliente_id) + "&boleta_id=" + str(boleta_id)
    boletas = datos.Tabla("bol_cont")
    cajas = datos.Tabla("cajas")
    clientes = datos.Tabla("clientes")
    boletas.buscar("id", boleta_id)
    caja_id = boletas.registro["caja_id"]
    cajas.buscar("id", caja_id)
    cliente_id = boletas.registro['cliente_id']
    # -----------------------------------------
    hoja = {}
    fecha = funciones.mysql_a_fecha(boletas.registro['fecha'])
    clientes.buscar("id", cliente_id)
    nombre = clientes.registro['nombre']
    direccion = clientes.registro['direccion']
    pag = pagina.Pagina("Boleta contado", 5, tipo="boleta")
    lin = ' ' * 90
    for i in range(0,70):
        hoja[i] = lin
    desp = 34
    hoja[0] = funciones.substr_replace(hoja[0], fecha, 80)
    hoja[0 + desp] = funciones.substr_replace(hoja[0 + desp], fecha, 80)
    hoja[3] = funciones.substr_replace(hoja[3], nombre, 20)
    hoja[3 + desp] = funciones.substr_replace(hoja[3 + desp], nombre, 20)
    hoja[5] = funciones.substr_replace(hoja[5], direccion, 20)
    hoja[5 + desp] = funciones.substr_replace(hoja[5 + desp], direccion, 20)
    detalle = datos.Tabla("bol_det")
    detalle.filtro = "bol_cont_id = '" + str(boleta_id) + "'"
    detalle.filtrar()
    hoja[7] = funciones.substr_replace(hoja[7], "Cantidad", 4)
    hoja[7] = funciones.substr_replace(hoja[7], "Detalle", 13)
    hoja[7] = funciones.substr_replace(hoja[7], "Precio", 79-6)
    hoja[7] = funciones.substr_replace(hoja[7], "Total", 95-5)
    hoja[7 + desp] = funciones.substr_replace(hoja[7 + desp], "Cantidad", 4)
    hoja[7 + desp] = funciones.substr_replace(hoja[7 + desp], "Detalle", 13)
    hoja[7 + desp] = funciones.substr_replace(hoja[7 + desp], "Precio", 79-6)
    hoja[7 + desp] = funciones.substr_replace(hoja[7 + desp], "Total", 95-5)
    conta = 8
    totbol = 0
    for fila in detalle.resultado:
        cantidad = str(fila["cantidad"])
        detalle = fila['detalle'].strip()
        unitario = funciones.moneda(fila['unitario'])
        total = funciones.moneda(fila['total'])
        if (len(detalle) > 57):
            detalle = detalle[0:57]
        hoja[conta] = funciones.substr_replace(hoja[conta], cantidad, 6)
        hoja[conta] = funciones.substr_replace(hoja[conta], detalle, 13)
        hoja[conta] = funciones.substr_replace(hoja[conta], unitario, 80 - len(unitario))
        hoja[conta] = funciones.substr_replace(hoja[conta], total, 96 - len(total))
        # Segunda hoja
        hoja[conta + desp] = funciones.substr_replace(hoja[conta + desp], cantidad, 6)
        hoja[conta + desp] = funciones.substr_replace(hoja[conta + desp], detalle, 13)
        hoja[conta + desp] = funciones.substr_replace(hoja[conta + desp], unitario, 80 - len(unitario))
        hoja[conta + desp] = funciones.substr_replace(hoja[conta + desp], total, 96 - len(total))
        # Total
        totbol = totbol + fila['total']
        conta = conta + 1
    total_boleta = funciones.moneda(totbol)
    hoja[17] = funciones.substr_replace(hoja[17], total_boleta, 96 - len(total_boleta))
    hoja[17 + desp] = funciones.substr_replace(hoja[17 + desp], total_boleta, 96 - len(total_boleta))
    # Cargar linea desde archivo
    pie_bol = open("pie_bol.txt")
    linea = pie_bol.readline()
    linea = linea[0:30]
    hoja[20] = funciones.substr_replace(hoja[20], linea, 6 - len(linea))
    hoja[20 + desp] = funciones.substr_replace(hoja[20 + desp], linea, 6 - len(linea))
    # agregado para imprimir nota al pie de boleta
    print("<pre>")
    offset_y = 5
    for i in range(0,offset_y):
        print('')
    for i in range(0,60):
        print(hoja[i] + "</br>")
    print("</pre>")
    #htm.button("...",cola)
    print "<script type='text/javascript'>"
    print "window.print();"
    print "</script>"
    htm.redirigir("caja_ver.php?accion=listado&" + cola)
    pag.fin()
if __name__ == "__main__":
    form = cgi.FieldStorage()
    if form.has_key("boleta_id"):
        impbol(form)
    else:
        pagina.error_variable("bol.py")
    
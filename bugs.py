#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Lista pedidos solucionados desde última versión"""
import htm
import datos
import funciones
import pagina
def main():
    """Rutina principal para despliegue de lista de errores"""
    pag = pagina.Pagina("Cambios", 20)
    dbase = datos.Tabla("desarrollo")
    fecha_inicio = funciones.fecha_a_mysql('1/10/2008')
    sql = "SELECT * FROM desarrollo WHERE fecha>'" + fecha_inicio
    sql = sql + "' AND estado='100' ORDER BY id DESC"
    dbase.cursor.execute(sql)
    numero = dbase.cursor.rowcount
    fil = dbase.cursor.fetchall()
    print(htm.button("Volver","geined.py"))
    print(htm.h3("Version: 1.0.1 - " + str(numero) + " pedidos atendidos desde la versión anterior"))
    i = 0
    htm.encabezado_tabla(["Nº", "Resumen", "Detalle"])
    for fila in fil:
        htm.fila_alterna(i)
        print(htm.td(fila['id']))
        print(htm.td(fila['detalle']))
        print(htm.td(fila['notas']))
        i = i + 1
        print '</tr>'
    htm.fin_tabla()
    pag.fin()
if __name__ == "__main__":
    main()

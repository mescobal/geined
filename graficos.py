#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Conjunto de rutinas para generar graficos"""
import datos
import os
def escribir_archivo(archivo, datos):
    """Escibir datos en un archivo"""
    f = open(archivo, 'w')
    f.write("0\n")
    for i in range(2, 13):
        f.write(str(datos[i]) + "\n")
    f.close()
def generar_archivos(titulo, resultado):
    """Generar un TXT a partir de un año de balance"""
    for fila in resultado:
        pass
    #    $a = mysql_fetch_row($res);
    #    $b = mysql_fetch_row($res);
    #    $c = mysql_fetch_row($res);
    #    $d = mysql_fetch_row($res);
    #    $e = mysql_fetch_row($res);
    #    escribir_archivo("txt/".$titulo.'_2003.txt',$a);
    #    escribir_archivo("txt/".$titulo.'_2004.txt',$b);
    #    escribir_archivo("txt/".$titulo.'_2005.txt',$c);
    #    escribir_archivo("txt/".$titulo.'_2006.txt',$d);
    #    escribir_archivo("txt/".$titulo.'_2007.txt',$e);
def generar_graficos():
    """Generación de gráficas para informe financiero"""
    pass
    #    $sql_cta_cte_mes = 'SELECT * FROM balcom WHERE item LIKE "Banco 200%"';
    #    $sql_cta_cte_acu = 'SELECT * FROM balcom WHERE item LIKE "Banco Acu 200%"';
    #    $sql_egresos_mes = 'SELECT * FROM balcom WHERE item LIKE "Egresos 200%"';
    #    $sql_egresos_acu = 'SELECT * FROM balcom WHERE item LIKE "Egresos Acu 200%"';
    #    $sql_ingresos_mes='SELECT * FROM balcom WHERE item LIKE "Ingresos 200%"';
    #    $sql_ingresos_acu='SELECT * FROM balcom WHERE item LIKE "Ingresos Acu 200%"';
    #    $sql_ganancia_mes ='SELECT * FROM balcom WHERE item LIKE "Ganancia 200%"';
    #    $sql_ganancia_acu ='SELECT * FROM balcom WHERE item LIKE "Ganancia Acu 200%"';
    #    generar_archivos("cta_cte_mes",$sql_cta_cte_mes);
    #    generar_archivos("cta_cte_acu",$sql_cta_cte_acu);
    #    generar_archivos("egresos_mes",$sql_egresos_mes);
    #    generar_archivos("egresos_acu",$sql_egresos_acu);
    #    generar_archivos("ingresos_mes",$sql_ingresos_mes);
    #    generar_archivos("ingresos_acu",$sql_ingresos_acu);
    #    generar_archivos("ganancia_mes",$sql_ganancia_mes);
    #    generar_archivos("ganancia_acu",$sql_ganancia_acu);
    #    exec('gnuplot graficos.gp');
def escribir_datos(filtro, archivo):
    """Escribir datos a un archivo de texto"""
    os.unlink(archivo)
    balcom = datos.Tabla("balcom")
    balcom.filtro = filtro
    balcom.filtrar()
    #    $sql = 'SELECT * FROM balcom WHERE item = "'.$filtro.'"';
    #    $res = mysql_query($sql);
    #    $fil = mysql_fetch_array($res);
    #    $handle = fopen($file, 'w');
    #    fwrite($handle, '0');
    #    fwrite($handle, $fil['enero']);
    #    fwrite($handle, $fil['febrero']);
    #    fwrite($handle, $fil['marzo']);
    #    fwrite($handle, $fil['abril']);
    #    fwrite($handle, $fil['mayo']);
    #    fwrite($handle, $fil['junio']);
    #    fwrite($handle, $fil['julio']);
    #    fwrite($handle, $fil['agosto']);
    #    fwrite($handle, $fil['setiembre']);
    #    fwrite($handle, $fil['octubre']);
    #    fwrite($handle, $fil['noviembre']);
    #    fwrite($handle, $fil['diciembre']);
    #    fclose($handle);
def generar_datos():
    pass
    # exportar datos desde mysql (balcom) hasta cada archivo.txt
    #    escribir_datos("Banco 2003","txt/cta_cte_mes_2003.txt")
    #    escribir_datos("Banco 2004","txt/cta_cte_mes_2004.txt")
    #    escribir_datos("Banco 2005","txt/cta_cte_mes_2005.txt")
    #    escribir_datos("Banco 2006","txt/cta_cte_mes_2006.txt")
    #    escribir_datos("Banco 2007","txt/cta_cte_mes_2007.txt")
    #    escribir_datos("Banco Acu 2003","txt/cta_cte_acu_2003.txt")
    #    escribir_datos("Banco Acu 2004","txt/cta_cte_acu_2004.txt")
    #    escribir_datos("Banco Acu 2005","txt/cta_cte_acu_2005.txt")
    #    escribir_datos("Banco Acu 2006","txt/cta_cte_acu_2006.txt")
    #    escribir_datos("Banco Acu 2007","txt/cta_cte_acu_2007.txt")
    #    escribir_datos("Egresos Acu 2003","txt/egresos_acu_2003.txt")
    #    escribir_datos("Egresos Acu 2004","txt/egresos_acu_2004.txt")
    #    escribir_datos("Egresos Acu 2005","txt/egresos_acu_2005.txt")
    #    escribir_datos("Egresos Acu 2006","txt/egresos_acu_2006.txt")
    #    escribir_datos("Egresos Acu 2007","txt/egresos_acu_2007.txt")
    #    escribir_datos("Ganancia 2003","txt/ganancia_mes_2003.txt")
    #    escribir_datos("Ganancia 2004","txt/ganancia_mes_2004.txt")
    #    escribir_datos("Ganancia 2005","txt/ganancia_mes_2005.txt")
    #    escribir_datos("Ganancia 2006","txt/ganancia_mes_2006.txt")
    #    escribir_datos("Ganancia 2007","txt/ganancia_mes_2007.txt")
    #    escribir_datos("Egresos 2003","txt/egresos_mes_2003.txt")
    #    escribir_datos("Egresos 2004","txt/egresos_mes_2004.txt")
    #    escribir_datos("Egresos 2005","txt/egresos_mes_2005.txt")
    #    escribir_datos("Egresos 2006","txt/egresos_mes_2006.txt")
    #    escribir_datos("Egresos 2007","txt/egresos_mes_2007.txt")
    #    escribir_datos("Ingresos Acu 2003","txt/ingresos_acu_2003.txt")
    #    escribir_datos("Ingresos Acu 2004","txt/ingresos_acu_2004.txt")
    #    escribir_datos("Ingresos Acu 2005","txt/ingresos_acu_2005.txt")
    #    escribir_datos("Ingresos Acu 2006","txt/ingresos_acu_2006.txt")
    #    escribir_datos("Ingresos Acu 2007","txt/ingresos_acu_2007.txt")
    #    escribir_datos("Ganancia Acu 2003","txt/ganancia_acu_2003.txt")
    #    escribir_datos("Ganancia Acu 2004","txt/ganancia_acu_2004.txt")
    #    escribir_datos("Ganancia Acu 2005","txt/ganancia_acu_2005.txt")
    #    escribir_datos("Ganancia Acu 2006","txt/ganancia_acu_2006.txt")
    #    escribir_datos("Ganancia Acu 2007","txt/ganancia_acu_2007.txt")
    #    escribir_datos("Ingresos 2003","itxt/ngresos_mes_2003,txt")
    #    escribir_datos("Ingresos 2004","txt/ingresos_mes_2004,txt")
    #    escribir_datos("Ingresos 2005","txt/ingresos_mes_2005,txt")
    #    escribir_datos("Ingresos 2006","txt/ingresos_mes_2006,txt")
    #    escribir_datos("Ingresos 2007","txt/ingresos_mes_2007,txt")
    #    escribir_datos("Egresos Acu 2003","txt/egresos_acu_2003.txt")
    #    escribir_datos("Egresos Acu 2004","txt/egresos_acu_2004.txt")
    #    escribir_datos("Egresos Acu 2006","txt/egresos_acu_2006.txt")
    #    escribir_datos("Egresos Acu 2005","txt/egresos_acu_2005.txt")
    #    escribir_datos("Egresos Acu 2007","txt/egresos_acu_2007.txt")
if __name__ == "__main__":
    print "No es ejecutable"

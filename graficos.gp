set terminal png transparent nocrop enhanced font arial 8 size 500,300
set datafile separator ","
set style data linespoints
set output 'img/cta_cte_mes.png'
set xlabel "Meses"
set xmtics
set parametric
set xrange [1:12]
set title "Cuenta corriente mes a mes"
plot 'txt/cta_cte_mes_2003.txt' using 1 title "2003" ,\
 'txt/cta_cte_mes_2004.txt' using 1 title "2004" , \
 'txt/cta_cte_mes_2005.txt' using 1 title "2005" , \
 'txt/cta_cte_mes_2006.txt' using 1 title "2006" , \
 'txt/cta_cte_mes_2007.txt' using 1 title "2007"

set output 'img/cta_cte_acu.png'
set title "Cuenta corriente acumulada"
plot 'txt/cta_cte_acu_2003.txt' using 1 title "2003" ,\
 'txt/cta_cte_acu_2004.txt' using 1 title "2004" , \
 'txt/cta_cte_acu_2005.txt' using 1 title "2005" , \
 'txt/cta_cte_acu_2006.txt' using 1 title "2006" , \
 'txt/cta_cte_acu_2007.txt' using 1 title "2007"

set output 'img/egresos_mes.png'
set title "Egresos mes a mes"
plot 'txt/egresos_mes_2003.txt' using 1 title "2003" ,\
 'txt/egresos_mes_2004.txt' using 1 title "2004" , \
 'txt/egresos_mes_2005.txt' using 1 title "2005" , \
 'txt/egresos_mes_2006.txt' using 1 title "2006" , \
 'txt/egresos_mes_2007.txt' using 1 title "2007"

set output 'img/egresos_acu.png'
set title "Egresos acumulados"
plot 'txt/egresos_acu_2003.txt' using 1 title "2003" ,\
 'txt/egresos_acu_2004.txt' using 1 title "2004" , \
 'txt/egresos_acu_2005.txt' using 1 title "2005" , \
 'txt/egresos_acu_2006.txt' using 1 title "2006" , \
 'txt/egresos_acu_2007.txt' using 1 title "2007"

set output 'img/ingresos_mes.png'
set title "Ingresos mes a mes"
plot 'txt/ingresos_mes_2003.txt' using 1 title "2003" ,\
 'txt/ingresos_mes_2004.txt' using 1 title "2004" , \
 'txt/ingresos_mes_2005.txt' using 1 title "2005" , \
 'txt/ingresos_mes_2006.txt' using 1 title "2006" , \
 'txt/ingresos_mes_2007.txt' using 1 title "2007"

set output 'img/ingresos_acu.png'
set title "Ingresos acumulados"
plot 'txt/ingresos_acu_2003.txt' using 1 title "2003" ,\
 'txt/ingresos_acu_2004.txt' using 1 title "2004" , \
 'txt/ingresos_acu_2005.txt' using 1 title "2005" , \
 'txt/ingresos_acu_2006.txt' using 1 title "2006" , \
 'txt/ingresos_acu_2007.txt' using 1 title "2007"

set output 'img/ganancia_mes.png'
set title "Ganancia mes a mes"
plot 'txt/ganancia_mes_2003.txt' using 1 title "2003" ,\
 'txt/ganancia_mes_2004.txt' using 1 title "2004" , \
 'txt/ganancia_mes_2005.txt' using 1 title "2005" , \
 'txt/ganancia_mes_2006.txt' using 1 title "2006" , \
 'txt/ganancia_mes_2007.txt' using 1 title "2007"

set output 'img/ganancia_acu.png'
set title "Ganancia acumulada"
plot 'txt/ganancia_acu_2003.txt' using 1 title "2003" ,\
 'txt/ganancia_acu_2004.txt' using 1 title "2004" , \
 'txt/ganancia_acu_2005.txt' using 1 title "2005" , \
 'txt/ganancia_acu_2006.txt' using 1 title "2006" , \
 'txt/ganancia_acu_2007.txt' using 1 title "2007"

set terminal png transparent nocrop enhanced font arial 8 size 500,250 
set datafile separator ","
set style data linespoints

set output 'cta_cte_mes.png'
set title "Cuenta corriente mes a mes" 
plot 'cta_cte_mes_2003.txt' using 1 title "2003" ,\
 'cta_cte_mes_2004.txt' using 1 title "2004" , \
 'cta_cte_mes_2005.txt' using 1 title "2005" , \
 'cta_cte_mes_2006.txt' using 1 title "2006" , \
 'cta_cte_mes_2007.txt' using 1 title "2007"
 
set output 'cta_cte_acu.png'
set title "Cuenta corriente acumulada" 
plot 'cta_cte_acu_2003.txt' using 1 title "2003" ,\
 'cta_cte_acu_2004.txt' using 1 title "2004" , \
 'cta_cte_acu_2005.txt' using 1 title "2005" , \
 'cta_cte_acu_2006.txt' using 1 title "2006" , \
 'cta_cte_acu_2007.txt' using 1 title "2007"

set output 'egresos_mes.png'
set title "Egresos mes a mes" 
plot 'egresos_mes_2003.txt' using 1 title "2003" ,\
 'egresos_mes_2004.txt' using 1 title "2004" , \
 'egresos_mes_2005.txt' using 1 title "2005" , \
 'egresos_mes_2006.txt' using 1 title "2006" , \
 'egresos_mes_2007.txt' using 1 title "2007"
 
set output 'egresos_acu.png'
set title "Egresos acumulados" 
plot 'egresos_acu_2003.txt' using 1 title "2003" ,\
 'egresos_acu_2004.txt' using 1 title "2004" , \
 'egresos_acu_2005.txt' using 1 title "2005" , \
 'egresos_acu_2006.txt' using 1 title "2006" , \
 'egresos_acu_2007.txt' using 1 title "2007"

set output 'ingresos_mes.png'
set title "Ingresos mes a mes" 
plot 'ingresos_mes_2003.txt' using 1 title "2003" ,\
 'ingresos_mes_2004.txt' using 1 title "2004" , \
 'ingresos_mes_2005.txt' using 1 title "2005" , \
 'ingresos_mes_2006.txt' using 1 title "2006" , \
 'ingresos_mes_2007.txt' using 1 title "2007"
 
set output 'ingresos_acu.png'
set title "Ingresos acumulados" 
plot 'ingresos_acu_2003.txt' using 1 title "2003" ,\
 'ingresos_acu_2004.txt' using 1 title "2004" , \
 'ingresos_acu_2005.txt' using 1 title "2005" , \
 'ingresos_acu_2006.txt' using 1 title "2006" , \
 'ingresos_acu_2007.txt' using 1 title "2007"

set output 'ganancia_mes.png'
set title "Ganancia mes a mes" 
plot 'ganancia_mes_2003.txt' using 1 title "2003" ,\
 'ganancia_mes_2004.txt' using 1 title "2004" , \
 'ganancia_mes_2005.txt' using 1 title "2005" , \
 'ganancia_mes_2006.txt' using 1 title "2006" , \
 'ganancia_mes_2007.txt' using 1 title "2007"
 
set output 'ganancia_acu.png'
set title "Ganancia acumulada" 
plot 'ganancia_acu_2003.txt' using 1 title "2003" ,\
 'ganancia_acu_2004.txt' using 1 title "2004" , \
 'ganancia_acu_2005.txt' using 1 title "2005" , \
 'ganancia_acu_2006.txt' using 1 title "2006" , \
 'ganancia_acu_2007.txt' using 1 title "2007"

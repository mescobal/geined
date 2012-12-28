set terminal png transparent nocrop enhanced font arial 8 size 500,250 
set output 'a.png'
#set ytics border in scale 1,0.5 mirror norotate  offset character 0, 0,0
set datafile separator ","
#set ytics   (80.0000, 85.0000, 90.0000, 95.0000, 100.000, 105.000)
set title "Demo of plotting financial data" 
#set xrange [ 0 : 12 ] noreverse nowriteback
#set yrange [ -200000 : 200000 ] noreverse nowriteback
set lmargin 9
set rmargin 2
set style data linespoints
plot 'a.txt' using 1 title "2003" ,\
 'b.txt' using 1 title "2004" , \
 'c.txt' using 1 title "2005" , \
 'd.txt' using 1 title "2006" , \
 'e.txt' using 1 title "2007" 




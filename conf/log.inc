<?php
$login='mescobal' ;
$bdd = 'Alianza' ;
$pass='pacu2000' ;
$host='localhost' ;
#$host = "alicarrasco.homelinux.net";
$conexion = mysql_connect($host,$login,$pass) or die ('No me pude conectar al servidor');
$db = mysql_select_db($bdd,$conexion) or die ('No pude seleccionar la base de datos');
?>

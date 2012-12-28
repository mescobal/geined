<?php
$login='usuario' ;
$bdd = 'Alianza' ;
$pass='clave' ;
$host='localhost' ;
$conexion = mysql_connect($host,$login,$pass) or die ('No me pude conectar al servidor');
$db = mysql_select_db($bdd,$conexion) or die ('No pude seleccionar la base de datos');
?>

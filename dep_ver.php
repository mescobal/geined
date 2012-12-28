<?php
include('funciones.php');
include('auth.inc');
/* CREATE TABLE `depositos` (
   `id` bigint(1) NOT NULL auto_increment,
  `deposito` char(50) default NULL,
  `codigo` char(2) default NULL,
  PRIMARY KEY  (`id`) */
if (!$_GET['accion']) $accion='listado';
else $accion=$_GET['accion'];
Encabezado('Detalles de depósito');
$sql1 = 'SELECT * FROM depositos WHERE id = "' . $_GET['id'] . '"';
$res1 = mysql_query($sql1);
$fil1 = mysql_fetch_array($res1);
echo '<h2>Depósito: '.$fil1['deposito'].'</h2>';
boton("Existencias",'dep_ver.php?id='.$_GET['id'].'&accion=stock');
boton("Comprobantes",'dep_ver.php?id='.$_GET['id'].'&accion=comprobantes');
boton('Volver','dep.php?accion=listado');
?>

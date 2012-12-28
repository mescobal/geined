<?php
include('funciones.php');
/* CREATE TABLE `proveedores` (
  `id` bigint(1) NOT NULL auto_increment,
  `proveedor` char(50) default NULL,
  `cuenta_id` bigint(20) default NULL,
  `telefono` char(50) default NULL,
  `direccion` char(50) default NULL,
  `email` char(50) default NULL,
  `ruc` char(50) default NULL,*/
autorizacion(5);
if(!$_GET['accion']){
	$accion='listado';
}
else{
	$accion=$_GET['accion'];
}
encabezado('Detalles de proveedor');
$sql1 = 'SELECT * FROM proveedores WHERE id = "' . $_GET['id'] . '"';
$res1 = mysql_query($sql1);
$fil1 = mysql_fetch_row($res1);
echo '<h2>Proveedor: '.$fil1[1].'</h2>';
echo '<h3>Telefono: '.$fil1[3].'</h3>';
boton("Estado de cuenta",'pro_ver.php?id='. $_GET['id'].'&accion=cuenta');
boton('Volver','pro.php?accion=listado');
?>

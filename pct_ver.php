<?php
include('funciones.php');
autorizacion(4);
encabezado_informe('Detalles de rubro');
$sql_cue='SELECT id,CONCAT(rubro," ", nombre) FROM cuentas ORDER BY rubro';
$res_cue = mysql_query($sql_cue);
$sql1='SELECT * FROM transacciones WHERE cuenta_id="'.$_GET['cuenta_id'] .'" ORDER BY fecha';	
$resultado = mysql_query($sql1);
encabezado_tabla(array("Nº","Fecha","Detalle","Cuenta","Debe","Haber","Saldo"));
$saldo=0;
for ($i = 0; $i < mysql_num_rows($resultado); $i++) {
	$row = mysql_fetch_array($resultado);
	echo '<tr>';
	celda($row['id']);
	celda(mysql_a_fecha($row['fecha']));
	celda($row['detalle']);
	// Cuenta
	$sql_cta = 'SELECT * FROM cuentas WHERE id="' . $row['cuenta_id'] . '"';
	$res_cta = mysql_query($sql_cta);
	$fil_cta = mysql_fetch_row($res_cta);
	celda($fil_cta[1]);
	linea_moneda($row['debe']);
	linea_moneda($row['haber']);
	$saldo = $saldo + $row['haber'] - $row['debe'];
	linea_moneda($saldo);
	echo '</tr>';
}
fin_tabla();
boton("Volver",'cuentas.py?accion=listado');
fin();
?>
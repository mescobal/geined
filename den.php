<?php
include('funciones.php');
function nuevo(){
	$sql_cta='SELECT * FROM cuentas ORDER BY rubro';
 	$res_cta = mysql_query($sql_cta);
	encabezado_fecha("Nuevo asiento doble entrada");
	echo '<form action="den.php?accion=agregar" name="f" method="post">';
	encabezado_tabla(array("Campo","Valor","Referencia"));
	input_fecha("Fecha:","fecha",fecha_a_mysql(date('d/m/y')));
	input_texto("Detalle:","detalle","");
	echo '<tr><td>Debe:</td><td><input type="text" name="debe" value="" onChange="codifica()" /></td>';
	echo '<td><input disabled size="80" value="desconocido" name="lbldebe" /></td></tr>';
	echo '<tr><td>Haber:</td><td><input type="text" name="haber" value="" onChange="codifica()" /></td>';
	echo '<td><input disabled size="80" value="desconocido" name="lblhaber" /></td></tr>';
	input_numero("Monto:","monto","");
	fin_tabla();
	botones();
	fin_formulario();
	script_fecha();
	echo '<SCRIPT LANGUAGE="JavaScript">
		function codifica(){';
  echo 'arr = [];
    arr2 = [];
		valor1 = document.f.debe.value;
		valor2 = document.f.haber.value;';
  for($i=0;$i<mysql_numrows($res_cta);$i++){
    $fil_cta = mysql_fetch_array($res_cta);
    echo 'arr[' .$fil_cta['rubro'] .']="' .$fil_cta['nombre'].'";';
  }
  echo 'document.f.lbldebe.value=arr[valor1];
			document.f.lblhaber.value=arr[valor2]; 
    }
		</SCRIPT>';
	script_noenter();
	boton("Volver","transacciones.py");
	fin();
}
function agregar(){
	$r_debe = $_POST['debe'];
	$r_haber = $_POST['haber'];
	
	$sql_debe = 'SELECT * FROM cuentas WHERE rubro="' . $r_debe . '"';
	$res_debe = mysql_query($sql_debe) or die('Consulta inv�lida: '.mysql_error());
	$fil_debe= mysql_fetch_array($res_debe);
	$id_debe = $fil_debe['id'];
	
	$sql_haber = 'SELECT * FROM cuentas WHERE rubro="' . $r_haber . '"';
	$res_haber = mysql_query($sql_haber) or die('Consulta inv�lida: '.mysql_error());
	$fil_haber= mysql_fetch_array($res_haber);
	$id_haber = $fil_haber['id'];
	
	$sql = 'INSERT INTO transacciones SET 
	fecha = "' . fecha_a_mysql($_POST['fecha']) . '",
	detalle = "' . $_POST['detalle'] . '",
	cuenta_id= "' . $id_debe. '",
	debe = "' . $_POST['monto'] . '",
	haber= "0"';
	$result = mysql_query($sql) or die('Consulta inv�lida: ' . mysql_error());
	
	$sql = 'INSERT INTO transacciones SET 
	fecha = "' . fecha_a_mysql($_POST['fecha']) . '",
	detalle = "' . $_POST['detalle'] . '",
	cuenta_id= "' . $id_haber. '",
	debe = "0",
	haber= "' . $_POST['monto'] . '"';
	$result = mysql_query($sql) or die('Consulta inv�lida: ' . mysql_error());
	redirigir("den.php?accion=nuevo");
}
autorizacion(4);
if(!$_GET['accion']){
	$accion = 'listado';
}
else $accion = $_GET['accion'];
switch ($accion){
	case 'nuevo':
		nuevo();
		break;
	case 'agregar':
		agregar();
		break;
}
?>
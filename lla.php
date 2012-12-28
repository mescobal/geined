<?php
include('funciones.php');
include('datos.php');
function listado(){
	encabezado('Llamadas telefónicas');
	$cliente_id = $_GET['cliente_id'];
	$sql1 = "SELECT * FROM clientes WHERE id='$cliente_id'";
	$res1 = mysql_query($sql1);
	$fil1 = mysql_fetch_array($res1);
	// cli_ver
	echo '<h2>Cliente: '.$fil1['nombre'].'</h2>';
	echo 'Telefono: ' . $fil1['telefono'] . '<br /><br />';
	boton("Nuevo",'lla.php?accion=nuevo&cliente_id='.$cliente_id);
	encabezado_tabla(array("Fecha","Notas","Acciones"));
	$sql3 = "SELECT * FROM llamadas WHERE cliente_id='$cliente_id'";
	$res3 = mysql_query($sql3);
	for ($i=0;$i<mysql_num_rows($res3);$i++){
		$fil3=mysql_fetch_array($res3);
		$id = $fil3['id'];
		echo '<tr>';
		celda(mysql_a_fecha($fil3['fecha']));
		celda($fil3['notas']);
		echo '<td>';
		boton("Editar","lla.php?accion=editar&id=$id&cliente_id=$cliente_id");
		boton("Borrar","lla.php?accion=confirmar&id=$id&cliente_id=$cliente_id");
		echo '</td></tr>';
	}
	fin_tabla();
	boton("Volver","cli_ver.php?accion=listado&id=$cliente_id");
	fin();
}
function editar(){
	encabezado_fecha('Edición de llamada telefónica');
	$sql='SELECT * FROM llamadas WHERE id="' . $_GET['id'].'"';
	$resultado = mysql_query($sql);
	$fila=mysql_fetch_row($resultado);
	$cliente_id = $_GET['cliente_id'];
	echo '<table><thead><th>Campo</th><th>Valor</th></thead>';
	echo '<form action="lla.php?accion=actualizar" method="POST">';
	echo '<input type="hidden" name="id" value="'.$_GET['id'].'">';
	echo '<input type="hidden" name="cliente_id" value="'.$cliente_id.'">';
	input_fecha('Fecha:','fecha',$fila[2]);
	input_texto('Notas:','notas',$fila[3]);
	botones();
	fin_formulario();
	fin_tabla();
	boton('Volver','lla.php?accion=listado&cliente_id='.$cliente_id);
	script_fecha();
	fin();
}
function actualizar(){
	$id = $_POST['id'];
	$cliente_id = $_POST['cliente_id'];
	$sql = 'UPDATE llamadas SET 
		fecha = "'. fecha_a_mysql($_POST['fecha']) . '",
		notas = "'. $_POST['notas'] . '" WHERE id = "' . $_POST['id'] . '"';
	$result = mysql_query($sql) or die('Invalid query: ' . mysql_error());
	header( 'Location: lla.php?accion=listado&cliente_id='.$cliente_id ) ;
}
function nuevo(){
	encabezado_fecha('Nueva llamada');
	$cliente_id = $_GET['cliente_id'];
  encabezado_tabla(array("Campo","Valor"));
	formulario("lla.php?accion=agregar");
  campo_oculto("cliente_id",$cliente_id);
	input_fecha('Fecha:','fecha',fecha_a_mysql(date('d/m/Y')));
	input_texto('Notas:','notas','');
	botones();
  fin_formulario();
  fin_tabla();
	script_fecha();
	boton('Volver','lla.php?accion=listado&cliente_id='.$cliente_id);
	fin();
}
function agregar(){
	$cliente_id = $_POST['cliente_id'];
	$sql = 'INSERT INTO llamadas SET 
		cliente_id = "' . $cliente_id . '",
		fecha = "' . fecha_a_mysql($_POST['fecha']) . '",
		notas = "' . $_POST['notas'] .'"';
	$result = mysql_query($sql) or die('Consulta inválida: ' . mysql_error());
	header( 'Location: lla.php?accion=listado&cliente_id='.$cliente_id ) ;
}
if (!$_GET['accion']) {$accion = 'listado';}
else $accion = $_GET['accion'];
if($_GET['cliente_id']) $cliente_id = $_GET['cliente_id'];
else $cliente_id = '1';
switch ($accion){
	case 'listado':
		listado();
		break;
	case 'editar':
		Editar();
		Break;
	case 'actualizar':
		actualizar();
		break;
	case 'nuevo':
		nuevo();
		break;
	case 'agregar':
		agregar();
		break;
	case 'confirmar':
		$cliente_id=$_GET['cliente_id'];
		Confirmar_Borrar($_GET['id'],'lla.php');
		boton('Volver','lla.php?accion=listado&cliente_id='.$cliente_id);
		break;
	case 'eliminar':
		autorizacion(10);
		$sql_cli = 'SELECT * FROM llamadas WHERE id="' .$_POST['id'].'"';
		$res_cli = mysql_query($sql_cli);
		$fil_cli = mysql_fetch_array($res_cli);
		$cliente_id = $fil_cli['cliente_id'];
		borrar('llamadas',$_POST['id'],'lla.php?accion=listado&cliente_id='.$cliente_id);
		break;
}
?>
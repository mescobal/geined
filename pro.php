<?php
include('funciones.php');
include('datos.php');
function listado(){
	autorizacion(5);
	encabezado('Listado de Proveedores');
	boton("Nuevo","pro?accion=nuevo");
	boton("Volver","geined.py?accion=sistema");
	//cargar datos
	$sql1='select * from proveedores order by proveedor';
	$res1 = mysql_query($sql1);	
	encabezado_tabla(array("Nº","Proveedor","Rubro","Telefonos","Direccion","eMail","Acciones"));
	$i = 0;
	while($fil1 = mysql_fetch_array($res1)){
		fila_alterna($i);
		$id = $fil1['id'];
		$fil_cta = buscar_registro("cuentas","id",$fil1['cuenta_id']);
		$rubro = $fil_cta['rubro'];
		celda($id);
		celda($fil1['proveedor']);
		// Rubro
		celda($rubro);
		celda($fil1['telefono']);
		celda($fil1['direccion']);
		celda($fil1['email']);
		echo '<td>';
		//boton("Detalles",'pro_ver.php?id='.$fil1['id']);
		boton("Editar","pro.php?accion=editar&id=$id");
		boton("Borrar","pro.php?accion=confirmar&id=$id");
		echo '</td></tr>';
		$i = $i + 1;
	}
	fin_tabla();
	boton('Volver','geined.py?accion=sistema');
}
function nuevo(){
	autorizacion(4);
	encabezado('Nuevo proveedor');
	$sql2 = 'SELECT * FROM proveedores';
	$res2 = mysql_query($sql2);
	$sql_cta='SELECT id,CONCAT(rubro," ", nombre) FROM cuentas ORDER BY rubro';
	$res_cta=mysql_query($sql_cta);
	encabezado_tabla(array("Campo","Valor"));
	formulario("pro.php?accion=agregar");
	input_texto('Nombre:','proveedor','');
	input_combo('Rubro:','cuenta_id',$res_cta,'');
	input_texto('Telefono:','telefono','');
	input_texto('Direccion:','direccion','');
	input_texto('eMail:','email','');
	botones();
	fin_formulario();
	fin_tabla();
	boton('Volver','pro.php?accion=listado');
}
function agregar(){
	$sql2 = 'SELECT * FROM proveedores WHERE proveedor = "' .$_POST['proveedor'] . '"';
	$res2 = mysql_query($sql2);
	if (mysql_num_rows($res2)==0) {
		$sql = 'INSERT INTO proveedores SET 
		proveedor = "' . $_POST['proveedor'] .'", 
		cuenta_id = "' . $_POST['cuenta_id'] .'",
		direccion="' . $_POST['direccion']   .'", 
		telefono = "' . $_POST['telefono']   .'", 
		email = "' . $_POST['email'] . '"';
		$result = mysql_query($sql) or die('Invalid query: ' . mysql_error());
		header( 'Location: pro.php?accion=listado' ) ;
	}
	else {
		duplicado('cli.py?accion=listado');
	}
}
function editar(){
	autorizacion(4);
	encabezado('Edición de proveedor');
	$sql1='select * from proveedores where id="' . $_GET['id'].'"';
	//cargar datos
	$res1 = mysql_query($sql1);
	$fil1=mysql_fetch_row($res1);
	$sql_cta='SELECT id,CONCAT(rubro," ", nombre) FROM cuentas ORDER BY rubro';
	$res_cta=mysql_query($sql_cta);
	encabezado_tabla(array("Campo","Valor"));
	formulario("pro.php?accion=actualizar");
	campo_oculto("id",$_GET['id']);
	input_texto('Nombre:','proveedor',$fil1[1]);
	input_combo('Rubro:','cuenta_id',$res_cta,$fil1[2]);
	input_texto('Telefono:','telefono',$fil1[3]);
	input_texto('Direccion:','direccion',$fil1[4]);
	input_texto('eMail:','email',$fil1[5]);
	botones();
	fin_formulario();
	fin_tabla();
	boton('Volver','pro.php?accion=listado');
}
function actualizar(){
	$sql = 'UPDATE proveedores SET 
	proveedor = "' . $_POST['proveedor'] .'", 
	cuenta_id = "' . $_POST['cuenta_id'] .'",
	direccion="' . $_POST['direccion']   .'", 
	telefono = "' . $_POST['telefono']   .'", 
	email = "' . $_POST['email'] . '" WHERE id = "' .$_POST['id'] .'"';
	$result = mysql_query($sql) or die('Invalid query: ' . mysql_error());
	header( 'Location: pro.php?accion=listado' ) ;
}
if (!$_GET['accion']) $accion='listado';
else $accion=$_GET['accion'];
switch($accion){
case 'listado':
	listado();
	break;
case 'nuevo':
	nuevo();
	break;
case 'agregar':
	agregar();
	break;
case 'editar':
	editar();
	break;
case 'actualizar':
	actualizar();
	break;
case 'confirmar':
	confirmar_borrar($_GET['id'],'pro.php');
	boton('Volver','cli.py?accion=listado');
	break;
case 'eliminar':
	autorizacion(1);
	borrar('proveedores',$_POST['id'],'pro.php?accion=listado');
	break;
}
?>

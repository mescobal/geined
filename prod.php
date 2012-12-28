<?php
include('funciones.php');
include('datos.php');
function listado(){
	encabezado('Listado de Productos');
	boton("Nuevo","prod.php?accion=nuevo");
	boton('Volver','geined.py?accion=administracion');
	//cargar datos
	$sql='SELECT * FROM productos ORDER BY producto';
	$resultado = mysql_query($sql);	
	encabezado_tabla(array("Nº","Producto","Rubro","Precio","Acciones"));
	while ($row = mysql_fetch_array($resultado)) {
		echo '<tr>';
		celda($row['id']);
		celda($row['producto']);
		celda($row['rubro']);
		celda(moneda($row['precio']));
		echo '<td>';
		boton("Detalle",'prod_ver.php?cuenta_id='.$row['id']);
		boton("Editar",'prod.php?id='.$row['id'].'&accion=editar');
		boton("Borrar",'prod.php?accion=confirmar&id=' .$row['id']);
		echo '</td></tr>';
	}
	fin_tabla();
	boton("Volver",'geined.py?accion=administracion');
	fin();
}
function nuevo(){
	/* Entrada */
	encabezado('Nuevo Producto');
	$sql_cta='SELECT * FROM cuentas ORDER BY rubro';
 	$res_cta = mysql_query($sql_cta);
	echo '<SCRIPT LANGUAGE="JavaScript">
		function codifica(){';
	echo 'arr = [];
		valor1 = document.f.rubro.value;';
	for($i=0;$i<mysql_numrows($res_cta);$i++){
    	$fil_cta = mysql_fetch_array($res_cta);
    	echo 'arr[' .$fil_cta['rubro'] .']="' .$fil_cta['nombre'].'";';
  	}
	echo 'document.f.lblrubro.value=arr[valor1];
    }
	</SCRIPT>';
  	encabezado_tabla(array("Campo","Valor"));
	echo '<form action="prod.php?accion=agregar" name="f" method="post">';
	input_texto('Producto:','producto','');
	echo '<tr><td>Rubro:</td><td><input type="text" name="rubro" value="" onChange="codifica()" /> - <input disabled size="80" value="desconocido" name="lblrubro" /></td></tr>';
	input_numero("Precio:","precio","");
	botones();
	fin_formulario();
	fin_tabla();
	boton('Volver','prod.php?accion=listado');
}
function agregar(){
	$sql_dup = 'SELECT * FROM productos WHERE producto="'.$_POST['producto'].'"';
	$res_dup = mysql_query($sql_dup);
	$rows = mysql_num_rows($res_dup);
	if ($rows==0){
		$sql = 'INSERT INTO productos SET 
		producto = "'.$_POST['producto'] .'", 
		rubro = "' . $_POST['rubro'].'", 
		precio = "' . $_POST['precio'].'"';
		$result = mysql_query($sql) or die('Consulta inválida: ' . mysql_error());
		redirigir("prod.php?accion=listado") ;
	}
	else {
		duplicado('prod.php?accion=listado');
	}
}
function editar(){
	/* Entrada */
	encabezado('Edición de Producto');
	$sql_cta='SELECT * FROM cuentas ORDER BY rubro';
 	$res_cta = mysql_query($sql_cta);
	echo '<SCRIPT LANGUAGE="JavaScript">
		function codifica(){';
	echo 'arr = [];
		valor1 = document.f.rubro.value;';
	for($i=0;$i<mysql_numrows($res_cta);$i++){
    	$fil_cta = mysql_fetch_array($res_cta);
    	echo 'arr[' .$fil_cta['rubro'] .']="' .$fil_cta['nombre'].'";';
  	}
	echo 'document.f.lblrubro.value=arr[valor1];
    }
	</SCRIPT>';
	$fil = buscar_registro("productos","id",$_GET['id']);
  	encabezado_tabla(array("Campo","Valor"));
	echo '<form action="prod.php?accion=actualizar" name="f" method="post">';
	campo_oculto("id",$_GET['id']);
	input_texto('Producto:','producto',$fil['producto']);
	echo '<tr><td>Rubro:</td><td><input type="text" name="rubro" value="'.$fil['rubro'].'" onChange="codifica()" /> - <input disabled size="80" value="desconocido" name="lblrubro" /></td></tr>';
	input_numero("Precio:","precio",$fil['precio']);
	botones();
	fin_formulario();
	fin_tabla();
	echo '<script language="javascript">codifica();</script>';
	boton('Volver','prod.php?accion=listado');
}
function actualizar(){
	$sql = 'UPDATE productos SET 
		rubro = "' . $_POST['rubro'] . '",
		producto = "' . $_POST['producto'] . '",
		precio = "' . $_POST['precio']. '" WHERE id = "' . $_POST['id'] . '"';
	$result = mysql_query($sql) or die('Invalid query: ' . mysql_error());
	redirigir("prod.php?accion=listado");
}
autorizacion(4);
if (!$_GET['accion']) {$accion = 'listado';}
else $accion = $_GET['accion'];
switch ($accion){
	case 'listado':
		listado();
		break;
	case 'editar':
		editar();
		break;
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
		confirmar_borrar($_GET['id'],'cuentas.py');
		boton('Volver','cuentas.py?accion=listado');
		break;
	case 'eliminar':
		borrar('cuentas',$_POST['id'],'cuentas.py?accion=listado');
		break;
}
?>
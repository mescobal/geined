<?php
include('funciones.php');
include('datos.php');
autorizacion(5);
if (!$_GET['accion']){
        $accion="editar";
    }
else {
    $accion = $_GET['accion'];
}
switch ($accion) {
    case 'editar':
        editar();
        break;
	case 'guardar':
		guardar();
		break;
}
function editar(){
	$deposito_id = $_GET['deposito_id'];
    $caja_id = $_GET['caja_id'];
    $cliente_id = $_GET['cliente_id'];
    $boleta_id = $_GET['boleta_id'];
    $cola = "deposito_id=$deposito_id&caja_id=$caja_id&cliente_id=$cliente_id&boleta_id=$boleta_id";
    /* ----------------------------------------- */
	encabezado("Cobranza de recargos");
	nota("Por el momento no se calcula automáticamente el recargo debiendo ser calculado e ingresado de forma manual");
	formulario("bolrec.php?accion=guardar&$cola");
	encabezado_tabla(array("Campo","Valor"));
	input_texto("Detalle:","detalle","");
	input_numero("Monto:","monto","");
	fin_tabla();
	botones();
	fin_formulario();
	boton("Volver","bolcon.php?accion=listado&$cola");
}
function guardar(){
	$deposito_id = $_GET['deposito_id'];
    $caja_id = $_GET['caja_id'];
    $cliente_id = $_GET['cliente_id'];
    $boleta_id = $_GET['boleta_id'];
	// @annotation Definir el rol del campo producto_id
	$producto_id = 10;
	$cantidad = 1;
	$detalle = $_POST['detalle'];
	$unitario= $_POST['monto'];
	$total = $unitario * $cantidad;
	$rubro =412000-1;
	$rubro = $rubro + $deposito_id;
    $cola = "deposito_id=$deposito_id&caja_id=$caja_id&cliente_id=$cliente_id&boleta_id=$boleta_id";
    /* ----------------------------------------- */
	// @annotation Guardar como linea en la boleta
	/* guarda linea en mov bol cont 
     * id bol_con_id producto_id cantidad detalle unitario total rubro */
    $sql_bol = "INSERT INTO bol_det SET bol_cont_id='$boleta_id', 
        producto_id='$producto_id', cantidad='$cantidad',
        detalle ='$detalle', unitario='$unitario',
        total='$total', rubro='$rubro'";
    $result = mysql_query($sql_bol);
	redirigir("bolcon.php?accion=listado&$cola");
}
?>

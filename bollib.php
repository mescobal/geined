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
    $sql_bie = "SELECT * FROM bie_cam";
    $res_bie = mysql_query($sql_bie);
    encabezado("Cobranza de libro");
    formulario("bollib.php?accion=guardar&$cola");
    encabezado_tabla(array("Campo","Valor"));
    input_combo("Seleccione libro:","biecam_id",$res_bie,"id");
    input_numero("Cantidad","cantidad","1");
    fin_tabla();
    botones();
    fin_formulario();
    boton("Volver","bolcon.php?accion=listado&$cola");
}
function guardar(){
    /* Recuperar variables */
    $deposito_id = $_GET['deposito_id'];
    $caja_id = $_GET['caja_id'];
    $cliente_id = $_GET['cliente_id'];
    $boleta_id = $_GET['boleta_id'];
    // @annotation Definir el rol del campo producto_id
    // Arbitrario: producto_id = 2 es un libro
    $producto_id = 2;
    $cantidad = $_POST['cantidad'];
    // Va en extra_id
    $biecam_id = $_POST['biecam_id'];
    $extra_id = $biecam_id;
    $fil_bie = buscar_registro("bie_cam","id",$biecam_id);
    $detalle = $fil_bie['descripcion'];
    $unitario= $fil_bie['precio'];
    $total = $unitario * $cantidad;
    /* VERITIFICAR SI ES EL RUBRO CORRECTO */
    /* Rubro previo 413000-1 */
    $rubro =115020-1;
    $rubro = $rubro + $deposito_id;
    $cola = "deposito_id=$deposito_id&caja_id=$caja_id&cliente_id=$cliente_id&boleta_id=$boleta_id";
    /* ----------------------------------------- */
    // @annotation Guardar como linea en la boleta
    /* guarda linea en mov bol cont 
     * id bol_con_id producto_id cantidad detalle unitario total rubro */
    linea_boleta($boleta_id,$producto_id,$cantidad,$detalle,$unitario,$total,$rubro,$extra_id);
    redirigir("bolcon.php?accion=listado&$cola");
}
?>

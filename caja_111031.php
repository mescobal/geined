<?php
/*! Movimientos de caja Deposito MN */
include('funciones.php');
include('datos.php');
autorizacion(5);
if(!$_GET['accion']){
    $accion="ingresar";
} else {
    $accion=$_GET['accion'];
}
switch($accion){
    case 'ingresar':
        ingresar();
        break;
    case 'guardar':
        guardar();
        break;
}
function guardar(){
    /* Recuperacion de variables */
    $id = $_GET['id'];
    $deposito_id = $_GET['deposito_id'];
    $caja_id = $_GET['caja_id'];
    $cola = "deposito_id=$deposito_id&caja_id=$caja_id";
    $receptor = $_POST['receptor'];
    $efectivo = $_POST['efectivo'];
    $cheques = $_POST['cheques'];
    $vouchers = $_POST['vouchers'];
    $otros = $_POST['otros'];
    /* Buscar registro */
    $fil_caj = buscar_registro("cajas","id",$caja_id);
    $fecha = $fil_caj['fecha'];
    $fil_dep = buscar_registro("depositos","id",$deposito_id);
    $sucursal = $fil_dep['deposito'];    
    /* Guardar linea de caja */
    $c_efectivo = -$efectivo;
    $c_cheques = -$cheques;
    $c_vouchers = -$vouchers;
    $c_otros = -$otros;
    $detalle = "Depósito realizado por $receptor";
	$documento_id = movcaja_add($caja_id,$detalle,-$efectivo,-$cheques,-$vouchers,-$otros);
    /* Guardar contabilidad */
    /* Para cada uno: Efectivo, Cheques, Vouchers, Otros */
    /* Definir rubro DEBE */
    if($efectivo<>0){
		$rub_deb = "111031";
        /* Definir rubro HABER */
        switch($deposito_id){
            case '1':
                $rub_hab = "111018";
                break;
            case '2':
                $rub_hab = "111011";
                break;
            case '3':
                $rub_hab = "111012";
                break;
        }
        /* guardar linea contabilidad */
        asiento_doble($fecha,$detalle,$rub_deb,$rub_hab,$efectivo,$documento_id);
		movcaja_cont($documento_id);
    }
    if($cheques<>0){
		$rub_deb = "111031";
        /* Definir rubro HABER */
        switch($deposito_id){
            case '1':
                $rub_hab = "111027";
                break;
            case '2':
                $rub_hab = "111021";
                break;
            case '3':
                $rub_hab = "111022";
                break;
        }
        /* guardar linea contabilidad */
        asiento_doble($fecha,$detalle,$rub_deb,$rub_hab,$cheques,$documento_id);
		movcaja_cont($documento_id);
    }
    if($vouchers<>0){
		$rub_deb = "113009";
        /* Definir rubro HABER */
        switch($deposito_id){
            case '1':
                $rub_hab = "113010";
                break;
            case '2':
                $rub_hab = "113002";
                break;
            case '3':
                $rub_hab = "113003";
                break;
        }
        /* guardar linea contabilidad */
        asiento_doble($fecha,$detalle,$rub_deb,$rub_hab,$vouchers,$documento_id);
		movcaja_cont($documento_id);
    }
    if($otros<>0){
		/* Asumo DE FORMA ARRIESGADA que es un depósito de moneda extranjera */
		$rub_deb = "111032";
        /* Definir rubro HABER */
        switch($deposito_id){
            case '1':
                $rub_hab = "111029";
                break;
            case '2':
                $rub_hab = "111025";
                break;
            case '3':
                $rub_hab = "111026";
                break;
        }
        /* guardar linea contabilidad */
        asiento_doble($fecha,$detalle,$rub_deb,$rub_hab,$otros,$documento_id);
		movcaja_cont($documento_id);
    }
    /* Generar documento para imprimir */
    encabezado_informe("Deposito bancario / vouchers");
    echo "<h2>Se deposita de: $sucursal</h2>";
    echo "<h3>A cargo de: $receptor</h3>";
    echo "Con fecha ".mysql_a_fecha($fecha).", el siguiente detalle:";
    encabezado_tabla(array("Concepto","Monto"));
    echo "<tr><td>Efectivo: </td><td>".moneda($efectivo)."</td></tr>";
    echo "<tr><td>Cheques: </td><td>".moneda($cheques)."</td></tr>";
    echo "<tr><td>Vouchers: </td><td>".moneda($vouchers)."</td></tr>";
    echo "<tr><td>Otros: </td><td>".moneda($otros)."</td></tr>";
    echo "<tr><td>Total: </td><td>".moneda($efectivo+$cheques+$vouchers+$otros)."</td></tr>";
    fin_tabla();
    echo "Identificación del documento: $documento_id";
    echo '<br /><br />';
    echo "<div align='right'>Firma del receptor</div>";
    echo "<div align='right'>Copia para caja</div>";
    linea();
    echo '<br /><br />';
    echo "<h1>Salida de caja para depósito</h1>";
    echo "<h2>Sale de: $sucursal</h2>";
    echo "<h3>A cargo de: $receptor</h3>";
    echo "Con fecha ".mysql_a_fecha($fecha).", el siguiente detalle:";
    encabezado_tabla(array("Concepto","Monto"));
    echo "<tr><td>Efectivo: </td><td>".moneda($efectivo)."</td></tr>";
    echo "<tr><td>Cheques: </td><td>".moneda($cheques)."</td></tr>";
    echo "<tr><td>Vouchers: </td><td>".moneda($vouchers)."</td></tr>";
    echo "<tr><td>Otros: </td><td>".moneda($otros)."</td></tr>";
    echo "<tr><td>Total: </td><td>".moneda($efectivo+$cheques+$vouchers+$otros)."</td></tr>";
    fin_tabla();
    echo "Identificación del documento: $documento_id";
    echo '<br /><br />';
    echo "<div align='right'>Firma del cajero</div>";
    echo "<div align='right'>Copia para contabilidad</div>";
    linea();
    fin();
    /* Redirigir */
    echo '<script type="text/javascript">
    window.print();
    </script>';
    redirigir("caja_ver.php?accion=listado&$cola");
}
function ingresar(){
    /* Recuperacion de variables */
    $id = $_GET['id'];
    $deposito_id = $_GET['deposito_id'];
    $caja_id = $_GET['caja_id'];
    $cola = "deposito_id=$deposito_id&caja_id=$caja_id";
    /* buscar registros */
    $fil_dep = buscar_registro("depositos","id",$deposito_id);
    $sucursal = $fil_dep['deposito'];
    encabezado("Salida de caja a Depósito bancario / de Vouchers");
    formulario("caja_111031.php?accion=guardar&$cola");
    echo "<h2>Salida de: $sucursal</h2>";
    encabezado_tabla(array("Campo","Valor"));
    echo "<tr>";
    input_texto("Deposita:","receptor","Mariana Porta");
    input_numero("Efectivo:","efectivo",0);
    input_numero("Cheques:","cheques",0);
    input_numero("Vouchers:","vouchers",0);
    input_numero("Otros:","otros",0);
    fin_tabla();
    botones();
    fin_formulario();
    echo '<div align="right">';
    boton("Volver","caja_ver.php?$cola");
    echo '</div>';
    fin();
}
?>

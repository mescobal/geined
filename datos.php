<?php
function datos($tabla,$campo,$clave){
    $sql_det = 'SELECT * FROM '.$tabla.' WHERE '.$campo.'="'.$clave.'"'; 
    $res_det = mysql_query($sql_det);
    return mysql_fetch_array($res_det);
}
function buscar_registro($tabla,$campo,$filtro){
    $sql = 'SELECT * FROM '.$tabla.' WHERE '.$campo.' = "' . $filtro . '"';
    $res = mysql_query($sql);
    $fil = mysql_fetch_array($res);
    return $fil;
}
function asiento_doble($fecha,$detalle,$debe,$haber,$monto,$documento_id){
    $fil_cta = buscar_registro("cuentas","rubro",$debe);
    $cuenta_id=$fil_cta['id'];
    $sql = 'INSERT INTO transacciones SET fecha = "'.$fecha.'",
        detalle = "'.$detalle.'", cuenta_id= "'.$cuenta_id.'",
        debe = "'.$monto.'", haber= "0", documento_id="'.$documento_id.'"';
    $result = mysql_query($sql) or die('Consulta inválida: '.mysql_error());
    $fil_cta = buscar_registro("cuentas","rubro",$haber);
    $cuenta_id =$fil_cta['id'];
    $sql = 'INSERT INTO transacciones SET fecha = "'.$fecha.'",
        detalle = "'.$detalle.'", cuenta_id= "'.$cuenta_id.'",
        debe = "0", haber= "'.$monto.'", documento_id="'.$documento_id.'"';
    $result = mysql_query($sql) or die('Consulta inválida: '.mysql_error());
}
function linea_boleta($bol,$prod,$cantidad,$detalle,$unitario,$total,$rubro,$extra_id){
    /*! Genera una línea en bol_det */
    $sql_bol = "INSERT INTO bol_det SET bol_cont_id='$bol', 
        producto_id='$prod', cantidad='$cantidad',
        detalle ='$detalle', unitario='$unitario',
        total='$total', rubro='$rubro', extra_id='$extra_id'";
    $result = mysql_query($sql_bol);
    }
function cta_cli_add($cliente_id,$detalle,$debe,$haber,$fecha){
    /*! Agregar a la cuenta del cliente */
    $sql = "INSERT INTO cta_clientes SET cliente_id='$cliente_id',
        grupo_id='0', concepto='$detalle',debe='$debe', haber='$haber', 
        fecha='$fecha'";
    $res = mysql_query($sql);
}
function movcaja_add($caja_id,$detalle,$efectivo,$cheques,$vouchers,$otros){
    /*! Agrega una línea al movimiento de caja */
    $sql = "INSERT INTO mov_caja SET 
    caja_id = '$caja_id', detalle = '$detalle',
    efectivo ='$efectivo',
    cheques = '$cheques',
    vouchers ='$vouchers',
    otros = '$otros'";
    $res = mysql_query($sql)  or die('Invalid query: ' . mysql_error());
    $resultado = mysql_insert_id();
    return $resultado;
}
function movcaja_cont($movcaja_id,$valor=1){
    /*! modifica una línea de caja para marcarla como agregada a la contabilidad */
    $sql = "UPDATE mov_caja SET contabilizado='$valor' WHERE id='$movcaja_id'";
    $res = mysql_query($sql) or die("SQL inválido: ".mysql_error());
}
/* Cuidado, estas funciones hacen uso de "redirigir" que esta en funciones */
function borrar($bdd,$id,$pagina){
    $sql = 'DELETE from ' . $bdd . ' WHERE id = "' . $id . '"';
    $result = mysql_query($sql) or die('Error: ' . mysql_error());
    //header( 'Location: ' . $pagina);
    redirigir($pagina);
}
function borrar_busqueda($bdd,$var,$val,$pagina){
    $sql = "DELETE from $bdd WHERE $var ='$val'";
    $result = mysql_query($sql) or die('Error: ' . mysql_error());
    //header( 'Location: ' . $pagina);
    redirigir($pagina);
}
function suma_cons($rubro,$ano){
	if($ano==2008){
		$cons = "consolidado";
	} else {
    	$cons = "consolidado".$ano;
	}
    $sql = "SELECT * FROM $cons WHERE rubro='$rubro'";
    $res = mysql_query($sql);
    $fil = mysql_fetch_array($res);
    $sum = +$fil['enero']+$fil['febrero']+$fil['marzo']+$fil['abril']+$fil['mayo']
    +$fil['junio']+$fil['julio']+$fil['agosto']+$fil['setiembre']+$fil['octubre']
    +$fil['noviembre']+$fil['diciembre'];
    return -$sum;
}
?>

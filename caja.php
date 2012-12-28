<?php
include("funciones.php");
include("datos.php");
function listado(){
    /*! Listado de cajas
    @param $deposito_id
    @return Código HTML 
    */
    /* Recuperación de variables */
    $deposito_id = $_GET['deposito_id'];
    /* Búsqueda de registros */
    $fil_dep = buscar_registro("depositos","id",$deposito_id);
    $sucursal = $fil_dep['deposito'];
    /* Inicio de la página */
    encabezado('Listado de Cajas en '.$sucursal);
    # Limito la búsqueda a 50 para que no interfiera con el resto de la operativa
    # TODO: permitir ver listados anteriores !!!!!!!!!!!!!!!!!!!!!!!!!!
    $sql_caja = 'SELECT * FROM cajas WHERE deposito_id = "'.$deposito_id.'" ORDER BY id DESC LIMIT 50';
    $res1 = mysql_query($sql_caja);
    boton("Nuevo","caja.php?accion=nuevo&deposito_id=$deposito_id");
    boton("Volver","geined.py?accion=recepcion");
    encabezado_tabla(array("Nº","Fecha","Cierre","Efectivo(C)","Cheques(C)","Vouchers(C)","Otros(C)","Movimientos","Acciones"));
    $i = 0;
    while($fil1 = mysql_fetch_array($res1)){
        fila_alterna($i);
        /* Recuperación de variables */
        $id = $fil1['id'];
        /* Ver si esa caja tiene movimientos */
        $sql_mov = 'SELECT * FROM mov_caja WHERE caja_id="'.$id.'"';
        $res_mov = mysql_query($sql_mov);
        $filas = mysql_num_rows($res_mov);
        celda($id);
        celda(mysql_a_fecha($fil1['fecha']));
        celda(mysql_a_fecha($fil1['cierre']));
        linea_moneda($fil1['c_efectivo']);
        linea_moneda($fil1['c_cheques']);
        linea_moneda($fil1['c_vouchers']);
        linea_moneda($fil1['c_otros']);
        echo "<td align='center'>$filas</td>";
        echo '<td>';
        boton("Reporte","caja_ver.php?accion=muestra&caja_id=$id&deposito_id=$deposito_id");
        if($fil1['cerrado']!=1){
            boton("Detalles","caja_ver.php?accion=listado&caja_id=$id&deposito_id=$deposito_id");
            // eliminar la opción de borrar si la caja no está vacía
            if ($filas<1){
                echo '<input type=button value="Borrar" onClick="if(confirm('."'¿Desea borrar este registro?'".')){ window.location='."'caja.php?accion=eliminar&id=$id&deposito_id=$deposito_id';".'}">';
            }
        }
        echo '</td></tr>';
        $i = $i + 1;
    }
    fin_tabla();
    boton("Volver",'geined.py?accion=recepcion');
}
function nuevo(){
    /* Entrada: deposito_id */
    $deposito_id = $_GET['deposito_id'];
    $fil_dep = buscar_registro("depositos","id",$deposito_id);
    $sucursal = $fil_dep['deposito'];
    encabezado_fecha("Nueva caja en $sucursal");
    //ver si la última caja está cerrada
    $sql_caj = 'SELECT * FROM cajas WHERE deposito_id="'.$_GET['deposito_id'].'" ORDER BY id DESC';
    $res_caj = mysql_query($sql_caj);
    $fil_caj = mysql_fetch_array($res_caj);
    $numrec = mysql_num_rows($res_caj);
    if (($fil_caj['cerrado']!=1) and ($numrec > 0)){
        echo '<p>Debe cerrar la caja anterior antes de abrir una nueva.</p>';
        boton("Volver",'caja.php?accion=listado&deposito_id='.$_GET['deposito_id']);
        fin();
    }
    else {
        // Para esa sucursal
        nota("Si los valores de apertura sugeridos no coinciden con los valores arrojados por el arqueo de caja, debe agregar un movimiento de caja correspondiente a quebranto INMEDIATAMENTE luego de abrir la caja");
        formulario('caja.php?accion=agregar&deposito_id='.$_GET['deposito_id']);
        $sql_pre = 'SELECT * FROM cajas WHERE deposito_id="'.$_GET['deposito_id'].'" ORDER BY id DESC';
        $res_pre = mysql_query($sql_pre);
        $fil_pre = mysql_fetch_array($res_pre);
        encabezado_tabla(array("Campo","Valor"));
        campo_oculto("deposito_id",$_GET['deposito_id']);
        input_fecha('Fecha:','fecha',fecha_a_mysql(date('d/m/Y')));
        input_numero('Apertura - Efectivo:','a_efectivo',$fil_pre['c_efectivo']);
        input_numero('Apertura - Cheques:','a_cheques',$fil_pre['c_cheques']);
        input_numero('Apertura - Vouchers:','a_vouchers',$fil_pre['c_vouchers']);
        input_numero('Apertura - Otros:','a_otros',$fil_pre['c_otros']);
        botones();
        fin_tabla();
        fin_formulario();
        script_fecha();
        boton('Volver','caja.php?accion=listado&deposito_id='.$_GET['deposito_id']);
    }
}
function agregar(){
    $sql = 'INSERT INTO cajas SET 
            apertura = "' . date('YmdHis') . '",
            fecha = "' . fecha_a_mysql($_POST['fecha']).'",
            deposito_id="' . $_POST['deposito_id'] . '",
            a_efectivo = "' . $_POST['a_efectivo'] . '",
            a_cheques= "' . $_POST['a_cheques'] . '", 
            a_vouchers = "' . $_POST['a_vouchers'] . '", 
            a_otros= "' . $_POST['a_otros'] . '"';
    $result = mysql_query($sql) or die('Invalid query: ' . mysql_error());
    redirigir('caja.php?accion=listado&deposito_id='.$_POST['deposito_id']);
}
function editar(){
    autorizacion(5);
    $sql_dep = 'SELECT * FROM depositos WHERE id="'.$_GET['sucursal'].'"';
    $res_dep = mysql_query($sql_dep);
    $fil_dep = mysql_fetch_array($res_dep);
    encabezado_fecha('Edición de caja en '.strtoupper($fil_dep['deposito']));
    encabezado_tabla(array("Campo","Valor"));
    formulario('caja.php?accion=actualizar');
    $sql1='select * from cajas where id="' . $_GET['id'].'"';
    //cargar datos
    $res1 = mysql_query($sql1);
    $fil1=mysql_fetch_row($res1);
    $sql2 = 'SELECT * FROM depositos';
    $res2 = mysql_query($sql2);
    campo_oculto("id",$_GET['id']);
    campo_oculto("deposito_id",$fil1[11]);
    input_fecha('Fecha:','fecha',$fil1[1]);
    input_numero('Efectivo (A)','a_efectivo',$fil1[3]);
    input_numero('Cheques (A)','a_cheques',$fil1[4]);
    input_numero('Vouchers (A)', 'a_vouchers',$fil1[5]);
    input_numero('Otros (A)','a_otros',$fil1[6]);
    input_numero('Efectivo (C)','c_efectivo',$fil1[7]);
    input_numero('Cheques (C)','c_cheques',$fil1[8]);
    input_numero('Vouchers (C)', 'c_vouchers',$fil1[9]);
    input_numero('Otros (C)','c_otros',$fil1[10]);
    botones();
    script_fecha();
    boton('Volver','caja.php?accion=listado');
}
function actualizar(){
    $sql_mov = 'SELECT 
    SUM(efectivo) AS se, SUM(cheques) AS sc, SUM(vouchers) AS sv, SUM(otros) AS so 
    FROM mov_caja 
    WHERE caja_id = "' .$_POST['id'] . '"';
    $res_mov = mysql_query($sql_mov);
    $fil_mov = mysql_fetch_array($res_mov);
    $efectivo = $_POST['a_efectivo'] + $fil_mov['se'];
    $cheques  = $_POST['a_cheques']  + $fil_mov['sc'];
    $vouchers = $_POST['a_vouchers'] + $fil_mov['sv'];
    $otros    = $_POST['a_otros']    + $fil_mov['so'];
    $sql = 'UPDATE cajas SET 
        deposito_id = "' .$_POST['deposito_id'] . '",     
        fecha = "'       . fecha_a_mysql($_POST['fecha']).'",
        a_efectivo = "'  . $_POST['a_efectivo'] . '", 
        a_cheques  = "'  . $_POST['a_cheques'] . '",
        a_vouchers = "'  . $_POST['a_vouchers'] . '",
        a_otros = "'     . $_POST['a_otros'] . '",
        c_efectivo ="'   .$efectivo . '",
        c_cheques  ="'   .$cheques . '",
        c_vouchers ="'   .$vouchers . '",
        c_otros = "'     .$otros .'",
        cierre  = "'     . date('YmdHis') . ' WHERE id = "' .$_POST['id'].'"';
    $result = mysql_query($sql) or die('Invalid query: ' . mysql_error());
    redirigir('caja.php?accion=listado');
}
function sucursal(){
    encabezado("Caja: seleccionar sucursal");
    boton("Central","caja.php?accion=listado&deposito_id=1");
    boton("Costa de Oro","caja.php?accion=listado&deposito_id=2");
    boton("Carrasco","caja.php?accion=listado&deposito_id=3");
    boton("Volver","geined.py?accion=recepcion");
    fin();
}

/* INICIO DE BUCLE PRINCIPAL */
autorizacion(6);
if (!$_GET["accion"]){
    $accion="listado";
}
else{
    $accion=$_GET["accion"];
}
if(!$_GET['deposito_id']){
    if(!$_SESSION['deposito_id']){
        $deposito_id=1;
    } else {
        $deposito_id = $_SESSION['deposito_id'];
    }
    redirigir("caja.php?accion=listado&deposito_id=$deposito_id");
}
else {
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
    case 'eliminar':
        $id = $_GET['id'];
        $deposito_id = $_GET['deposito_id'];
        borrar('cajas',$id,"caja.php?accion=listado&deposito_id=$deposito_id");
        break;
    case 'cerrar':
        cerrar();
        break;
    case 'cierre_confirmado':
        cierre_confirmado();
        break;
    }
}
?>

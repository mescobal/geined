<?php
include('funciones.php');
include('funcajax.php');
include('datos.php');
function mostrar_apertura($fil_caj){
    echo '<TABLE><TR>';
    celda("Apertura");
    celda("Efectivo");
    celda("Cheques");
    celda("Vouchers");
    celda("Otros");
    echo '</TR><TR>';
    celda(mysql_a_fecha($fil_caj['fecha']));
    celda(moneda($fil_caj['a_efectivo']));
    celda(moneda($fil_caj['a_cheques']));
    celda(moneda($fil_caj['a_vouchers']));
    celda(moneda($fil_caj['a_otros']));
    echo '</TR></TABLE>';
}
function mostrar_cierre($tote,$totc,$totv,$toto){
    echo '<table><tr><td><h3>Cierre</h3></td><td><h3>Acciones</h3></td></tr><td>';
    echo '<TABLE><TR>';
    celda("Apertura");
    celda("Efectivo");
    celda("Cheques");
    celda("Vouchers");
    celda("Otros");
    echo '</TR><TR>';
    celda(date('d/m/Y'));
    celda(moneda($tote));
    celda(moneda($totc));
    celda(moneda($totv));
    celda(moneda($toto));
    echo '</TR></TABLE>';
    echo '</td><td>';
}
function error_caja(){
    /* Genera error si no esta alguna de las variables requeridas */
    encabezado("Error al ver listado");
    echo "<h2>Hay alguna variable no definida</h2>";
    echo "<p>Para entrar al listado de movimientos, debe pasar primero por el listado de cajas.</p>";
    echo "<p>Si no lo hace, el sistema no sabe a que caja esta haciendo referencia en esta operacion.</p>";
    boton("Volver","geined.py?accion=recepcion");
    end;
    }
function listado(){
    /*! Genera listado de detalle de caja del dia
     @param accion, deposito_id
     @return formulario, volver
     */
    /* Recuperar variables */
    $continuar = 1;
    if(!$_GET['deposito_id']){
        $continuar = 0;
    } else {
        $deposito_id = $_GET['deposito_id'];
    }
    if(!$_GET['caja_id']){
        $continuar = 0;
    } else {
        $caja_id = $_GET['caja_id'];
    }
    /* Si la caja no existe tiene que generar error */
    $verificar = mysql_query("SELECT * FROM cajas WHERE id=$caja_id");
    if(!$verificar){
        /* Generar error si la caja ya esta cerrada */
        $continuar = 0;
    } else {
        $filas = mysql_fetch_array($verificar);
        if($filas['cerrado']==1){
            $continuar = 0;
        }
    }
    if($continuar == 1){
        $cola = "deposito_id=$deposito_id&caja_id=$caja_id";
        $fil_caj = buscar_registro("cajas","id",$caja_id);
        /* Buscar registros */
        $fil_dep = buscar_registro("depositos","id",$deposito_id);
        $deposito = $fil_dep['deposito'];
        /* Comienza página */
        encabezado("Listado de movimientos de caja de $deposito");
        echo '<table><tr><td><h3>Apertura</h3></td><td><h3>Movimientos</h3></td></tr>';
        echo '<tr><td>';
        mostrar_apertura($fil_caj);
        echo '</td><td>';
        boton("Entrada","caja_ver.php?accion=nuevo&tipo=entrada&$cola");
        boton("Entrada por cursos", "caja_curso.py?accion=nuevo&$cola");
        boton("Salida","caja_ver.php?accion=nuevo&tipo=salida&$cola");
        boton("Devolución por cursos", "caja_curso.py?accion=devolucion&$cola");
        boton("Boleta contado","bolcon.php?accion=buscar_cliente&$cola");
        boton("Volver","caja.php?accion=listado&deposito_id=$deposito_id&caja_id=$caja_id");
        otros_movimientos($deposito_id,$cola);
        echo '</td></tr></table>';
        tabla(); 
        linea();
    } else {
        error_caja();   
    }
}
function tabla(){
    /* imprime la tabla
    Entrada: caja_id, deposito_id
    Salida: codigo HTML
    */
    $caja_id = $_GET['caja_id'];
    $deposito_id = $_GET['deposito_id'];
    $fil_caj = buscar_registro("cajas","id",$caja_id);
    $tot_efectivo = $fil_caj['a_efectivo'];
    $tot_cheques = $fil_caj['a_cheques'];
    $tot_vouchers = $fil_caj['a_vouchers'];
    $tot_otros = $fil_caj['a_otros'];
    $sql_mov = 'SELECT * FROM mov_caja WHERE caja_id = "' . $caja_id . '"';
    $res_mov = mysql_query($sql_mov);
    encabezado_tabla(array("Nº","Detalle","Efectivo","Cheques","Vouchers","Otros","Acciones"));
    for ($i = 0; $i < mysql_num_rows($res_mov); $i++){
        $fil_mov = mysql_fetch_array($res_mov);
        echo '<tr>';
        $id=$fil_mov['id'];
        celda($fil_mov['id']);
        celda($fil_mov['detalle']);
        linea_moneda($fil_mov['efectivo']);
        linea_moneda($fil_mov['cheques']);
        linea_moneda($fil_mov['vouchers']);
        linea_moneda($fil_mov['otros']);
        echo '<td>';
        if ((strstr($fil_mov['detalle'],"Boleta contado Nº interno")==FALSE) and (strstr($fil_mov["detalle"], "Ingreso por cursos: ") ==FALSE) and (strstr($fil_mov["detalle"], "Devolución por cursos: ") == FALSE)) {
            boton("Editar","caja_ver.php?accion=editar&id=$id&deposito_id=$deposito_id&caja_id=$caja_id");
            btnConfirmarBorrar("caja_ver.php?accion=eliminar&id=$id&caja_id=$caja_id&deposito_id=$deposito_id");
        }
        echo '</td>';
        $tot_efectivo = $tot_efectivo + $fil_mov['efectivo'];
        $tot_cheques = $tot_cheques + $fil_mov['cheques'];
        $tot_vouchers = $tot_vouchers + $fil_mov['vouchers'];
        $tot_otros = $tot_otros + $fil_mov['otros'];
        echo '</tr>';
    }
    echo '<tr><td></td></tr>';
    echo '<tr>';
    celda("-");
    celda("Sub-Totales");
    linea_moneda($tot_efectivo-$fil_caj['a_efectivo']);
    linea_moneda($tot_cheques-$fil_caj['a_cheques']);
    linea_moneda($tot_vouchers-$fil_caj['a_vouchers']);
    linea_moneda($tot_otros-$fil_caj['a_otros']);
    echo '<td>';
    linea();
    echo '</td></tr></table>';
    fin_tabla();
    mostrar_cierre($tot_efectivo,$tot_cheques,$tot_vouchers,$tot_otros);
    echo '<input type=button value="Cerrar caja" onClick="if(confirm('."'¿Desea cerrar esta caja?'".')) window.location='."'caja_ver.php?accion=cerrar&caja_id=$caja_id&deposito_id=$deposito_id';".'">';
    echo '</td></tr></table>';
}
function muestra(){
    encabezado_informe('Detalle de caja');
    $caja_id = $_GET['caja_id'];
    $fil_caj = buscar_registro("cajas","id",$caja_id);
    echo '<TABLE><TR>';
    celda("Apertura");
    celda("Efectivo");
    celda("Cheques");
    celda("Vouchers");
    celda("Otros");
    echo '</TR><TR>';
    celda(mysql_a_fecha($fil_caj['fecha']));
    //celda(moneda($fil_caj['a_efectivo']));
    linea_moneda($fil_caj['a_efectivo']);
    celda(moneda($fil_caj['a_cheques']));
    celda(moneda($fil_caj['a_vouchers']));
    celda(moneda($fil_caj['a_otros']));
    echo '</TR></TABLE>';
    linea();
    $sql_mov = 'SELECT * FROM mov_caja WHERE caja_id = "' . $caja_id . '"';
    $res_mov = mysql_query($sql_mov);
    encabezado_tabla(array("Nº","Detalle","Efectivo","Cheques","Vouchers","Otros"));
    for ($i = 0; $i < mysql_num_rows($res_mov); $i++){
        echo '<tr>';
        $fil_mov = mysql_fetch_array($res_mov);
        celda($fil_mov['id']);
        celda($fil_mov['detalle']);
        celda(moneda($fil_mov['efectivo']));
        celda(moneda($fil_mov['cheques']));
        celda(moneda($fil_mov['vouchers']));
        celda(moneda($fil_mov['otros']));
        echo '</tr>';
    }
    echo '</TABLE>';
    linea();
    echo '<TABLE><TR>';
    celda("Cierre:");
    celda("Efectivo");
    Celda("Cheques");
    Celda("Vouchers");
    Celda("Otros");
    echo '</TR><TR>';
    Celda(mysql_a_fecha($fil_caj['cierre']));
    Celda(moneda($fil_caj['c_efectivo']));
    Celda(moneda($fil_caj['c_cheques']));
    Celda(moneda($fil_caj['c_vouchers']));
    Celda(moneda($fil_caj['c_otros']));
    echo '</TR></TABLE>';
    //boton('Volver','caja.php?accion=listado&deposito_id='.$_GET['deposito_id']);
    boton("Volver",'caja.php?accion=listado&deposito_id='.$_GET['deposito_id']);
}
function agregar(){
    /*Rutina para agregar un registro al movimiento de cajas
    Entrada: deposito_id, caja_id (POST mediante campos ocultos)
    Salida: redirigida al listado (refresh)*/
    $efectivo = $_POST['efectivo'];
    $cheques= $_POST['cheques'];
    $vouchers= $_POST['vouchers'];
    $otros= $_POST['otros'];
    if($_GET['tipo']=='salida'){
        $efectivo = -$efectivo;
        $cheques = -$cheques;
        $vouchers = -$vouchers;
        $otros = -$otros;
    }
    $deposito_id = $_GET['deposito_id'];
    $caja_id = $_GET['caja_id'];
    $cola = "deposito_id=$deposito_id&caja_id=$caja_id";
    $sql = 'INSERT INTO mov_caja SET 
    caja_id = "' . $_POST['caja_id'] . '",
    detalle = "' . $_POST['detalle'] . '",
    efectivo = "' .$efectivo. '",
    cheques = "' .$cheques. '",
    vouchers = "' .$vouchers. '",
    otros = "' .$otros. '"';
    $result = mysql_query($sql)  or die('Invalid query: ' . mysql_error());
    redirigir("caja_ver.php?accion=listado&$cola");
}
function editar(){
    /* edición de movimiento de caja
    Entrada: id, caja_id, deposito_id
    Salida: hacia la rutina que procesa el formulario
    */
    $id = $_GET['id'];
    $deposito_id = $_GET['deposito_id'];
    $caja_id = $_GET['caja_id'];
    $cola = "deposito_id=$deposito_id&caja_id=$caja_id";
    encabezado("Editar movimiento de caja");
    formulario("caja_ver.php?accion=actualizar&$cola");
    $fil=buscar_registro("mov_caja","id",$id);
    encabezado_tabla(array("Campo","Valor"));
    campo_oculto("id",$_GET['id']);
    campo_oculto("caja_id",$caja_id);
    campo_oculto("deposito_id",$deposito_id);
    input_texto('Detalle:','detalle',$fil['detalle']);
    input_numero('Efectivo:','efectivo',$fil['efectivo']);
    input_numero('Cheques:','cheques',$fil['cheques']);
    input_numero('Vouchers:','vouchers',$fil['vouchers']);
    input_numero('Otros:','otros',$fil['otros']);
    fin_tabla();
    botones();
    fin_formulario();
    boton("Volver","caja_ver.php?accion=listado&$cola");
}
function actualizar(){
    /* Actualiza un movimiento de caja
    Entrada: deposito_id, caja_id
    Salida: se redirige al listao
    */
    $deposito_id = $_POST['deposito_id'];
    $caja_id = $_POST['caja_id'];
    $sql = 'UPDATE mov_caja SET 
    detalle = "' . $_POST['detalle'] . '",
    efectivo = "' .$_POST['efectivo'] . '",
    cheques = "' . $_POST['cheques'] . '",
    vouchers = "' . $_POST['vouchers'] . '",
    otros = "' . $_POST['otros'] . '" WHERE id="'.$_POST['id'].'"';
    $result = mysql_query($sql)  or die('Invalid query: ' . mysql_error());
    redirigir('caja_ver.php?accion=listado&deposito_id='.$_POST['deposito_id'].'&caja_id='.$_POST['caja_id']);
}
function cerrar(){
    $caja_id = $_GET['caja_id'];
    /*^sumar datos de apertura */
    $fil_caj = buscar_registro("cajas","id",$caja_id);
    $apef = $fil_caj['a_efectivo'];
    $apch = $fil_caj['a_cheques'];
    $apvo = $fil_caj['a_vouchers'];
    $apot = $fil_caj['a_otros'];
    $deposito_id = $fil_caj['deposito_id'];
    /* calcular totales */
    $sql_mov = 'SELECT SUM(efectivo) as SE, SUM(cheques) as SC, SUM(vouchers) as SV, SUM(otros) as SO FROM mov_caja WHERE caja_id="'.$caja_id.'"';
    $res_mov = mysql_query($sql_mov);
    $fil_mov = mysql_fetch_array($res_mov);
    $tote = $fil_mov['SE']+$apef;
    $totc = $fil_mov['SC']+$apch;
    $totv = $fil_mov['SV']+$apvo;
    $toto = $fil_mov['SO']+$apot;
    $cierre = fecha_a_mysql(date('d/m/Y'));
    /* Exportar los movimientos a contabilidad */
    /* Marcar caja como cerrada */
    $sql_caj = 'UPDATE cajas SET c_efectivo="'.$tote.'", c_cheques="'.$totc.'", c_vouchers="'.$totv.'", c_otros="'.$toto.'", cerrado="1", cierre="'.$cierre.'" WHERE  id="'.$caja_id.'"';
    $result = mysql_query($sql_caj)  or die('Invalid query: ' . mysql_error());
    /* Volver al listado de cajas */
    redirigir("caja.php?accion=listado&deposito_id=$deposito_id");
}
function nuevo(){
    /* agrega un movimiento a los movimientos de caja
    Entrada: deposito_id, caja_id (GET)
    Salida: redirigida a listado (refresh)
    */
    $deposito_id = $_GET['deposito_id'];
    $caja_id = $_GET['caja_id'];
    $tipo = $_GET['tipo'];
    $cola = "deposito_id=$deposito_id&caja_id=$caja_id";
    if($tipo=="salida"){
        encabezado("Nueva SALIDA de caja");
    } else {
        encabezado("Nuevo movimiento de caja");
    }
    formulario("caja_ver.php?accion=agregar&tipo=$tipo&$cola");
    encabezado_tabla(array("Campo","Valor"));
    campo_oculto("caja_id",$caja_id);
    input_texto("Detalle:","detalle","");
    input_numero("Efectivo:","efectivo",0);
    input_numero("Cheques:","cheques",0);
    input_numero("Vouchers:","vouchers",0);
    input_numero("Otros:","otros",0);
    fin_tabla();
    botones();
    fin_formulario();
    boton("Volver","caja_ver.php?accion=listado&$cola");
}
function confirmar_cierre(){
    $caja_id = $_GET['caja_id'];
    $deposito_id = $_GET['deposito_id'];
    //Abrir la caja caja_id
    //Calcular los totales
    $sql = 'SELECT SUM("efectivo") as SE,SUM("cheques") as SC, SUM("vouchers") as SV, SUM("otros") as SO FROM mov_caja WHERE caja_id="'.$caja_id.'"';
    $res = mysql_query($sql);
    $fil = mysql_fetch_array($res);
    $marcador = 0;
    //Compararlo con el arqueo
    if($fil['SE']!=$_POST['efectivo']) $marcador = 1;
    if($fil['SC']!=$_POST['cheques']) $marcador = 1;
    if($fil['SV']!=$_POST['vouchers']) $marcador = 1;
    if($fil['SO']!=$_POST['otros']) $marcador = 1;
    //Si es igual: cierra la caja y vuelve al listado
    if($marcador=0){
        $sql_cierre = 'UPDATE caja SET c_efectivo="'.$_POST['efectivo'].'", c_cheques="'.$_POST['cheques'].'", c_vouchers="'.$_POST['vouchers'].'", c_otros="'.$_POST['otros'].'" WHERE id="'.$caja_id.'"';
        redirigir("caja.php?accion=listado&id=$caja_id");
    }
    else {
        //Si da distinto: vuelve al formulario de cierre
        echo '<script language="JavaScript">alert("No coinciden las cifras del arqueo con el cierre");</script>';
        redirigir("caja_ver.php?accion=cerrar&caja_id=$caja_id&deposito_id=$deposito_id");
    }
}
function otros_movimientos($deposito_id,$cola){
    echo '<form name="menu" >
    <select name="menu" size="1" style="background-color:#FFFFD7">
        <option selected value="caja_ver.php?'.$cola.'">Otros movimientos... </option>
        <option value="caja_111018.php?'.$cola.'">Salida para depósito MN</option>
    </select>
    <input type="button" value="Ir" 
    onClick="location=document.menu.menu.options[document.menu.menu.selectedIndex].value">
    </form>';
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
    case 'muestra':
        muestra();
        break;
    case 'editar':
        editar();
        break;
    case 'actualizar':
        actualizar();
        break;
    case 'cerrar':
        cerrar();
        break;
    case 'tabla':
        tabla();
        break;
    case 'confirmar_cierre':
        confirmar_cierre();
        break;
    case 'confirmar_borrar':
        $caja_id=$_GET['caja_id'];
        $deposito_id=$_GET['deposito_id'];
        $id = $_GET['id'];
        confirmar_borrar($id,"caja_ver.php?accion=listado&caja_id=$caja_id&deposito_id=$deposito_id");
        boton("Volver","caja_ver.php?accion=listado&caja_id=$caja_id&deposito_id=$deposito_id");
        break;
    case 'eliminar':
        $id = $_GET['id'];
        $deposito_id = $_GET['deposito_id'];
        $caja_id = $_GET['caja_id'];
        borrar('mov_caja',$id,"caja_ver.php?accion=listado&caja_id=$caja_id&deposito_id=$deposito_id");
        break;
}
?>

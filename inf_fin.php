<?php
include('funciones.php');
include('datos.php');
include('graficos.php');
function listado(){
    inicio();
    encabezado("Informe financiero");
    $arr = array("Fecha","Conclusiones","Acciones");
    encabezado_tabla($arr);
    $res = mysql_query("SELECT * FROM inf_fin ORDER BY fecha") or die('Invalid query: ' . mysql_error());;
    boton('Nuevo','inf_fin.php?accion=nuevo');
    for($i=0;$i<mysql_num_rows($res);$i++){
        $fil = mysql_fetch_array($res);
        echo '<tr>';
        celda(mysql_a_fecha($fil['fecha']));
        celda($fil['conclusion']);
        echo '<td>';
        boton("Detalles",'inf_fin.php?accion=ver&id='.$fil['id']);
        boton("Editar",'inf_fin.php?accion=editar&id='.$fil['id']);
        boton("Borrar",'inf_fin.php?accion=confirmar&id='.$fil['id']);
        echo '</td></tr>';
    }
    fin_tabla();
    boton("Volver","geined.py?accion=administracion");
    fin();
}
function ver(){
    inicio();
    $res = mysql_query('SELECT * FROM inf_fin WHERE id= '.$_GET['id']);
    $fil = mysql_fetch_array($res);
    encabezado('Informe financiero');
    //generar_datos();
    generar_graficos();
    boton('Editar','inf_fin.php?accion=editar&id='.$_GET['id']);
    boton('Borrar','inf_fin.php?accion=confirmar&id='.$_GET['id']);
    boton('Volver','inf_fin.php?accion=listado');
    echo '<H2>Informe al 28 de agosto de 2007</H2>';
    echo '<H3>Evolución del estado de la cuenta corriente</H3>';
    echo $fil['bancos'].'<br/>';
    echo '<IMG SRC="img/cta_cte_mes.png">';
    echo '<IMG SRC="img/cta_cte_acu.png">';
    echo '<HR>';
    echo '<H3>Evolución de los gastos</H3>';
    echo $fil['egresos'].'<br/>';
    echo '<IMG SRC="img/egresos_mes.png">';
    echo '<IMG SRC="img/egresos_acu.png">';
    echo '<HR>';
    echo '<H3>Evolución de ingresos</H3>';
    echo $fil['ingresos'].'<br/>';
    echo '<IMG SRC="img/ingresos_mes.png">';
    echo '<IMG SRC="img/ingresos_acu.png">';
    echo '<HR>';
    echo '<H3>Evolución de la ganancia</H3>';
    echo $fil['ganancia'].'<br/>';
    echo '<IMG SRC="img/ganancia_mes.png">';
    echo '<IMG SRC="img/ganancia_acu.png">';
    echo '<HR>';
    echo '<H3>Conclusión</H3>';
    echo $fil['conclusion'].'<br/>';
    echo '<HR>';
    echo '<H3>Recomendaciones</H3>';
    echo $fil['recomendaciones'].'<br/>';
    echo '<HR>';
    fin();
}
function nuevo(){
    inicio();
    encabezado_fecha("Nuevo Informe Financiero");
    boton("Volver","inf_fin.php?accion=listado");
    formulario('inf_fin.php?accion=agregar');
    $arr = array("Campo","Valor");
    encabezado_tabla($arr);
    input_fecha('Fecha:','fecha',fecha_a_mysql(date('d/m/Y')));
    input_memo("Cuenta corriente:",'bancos','');
    input_memo("Bancos baso 0:",'bancosb0','');
    input_memo("Egresos",'egresos','');
    input_memo("Ingresos",'ingresos','');
    input_memo("Ganancia:",'ganancia','');
    input_memo("Conclusión:",'conclusion','');
    input_memo("Recomendaciones:",'recomendaciones','');
    fin_tabla();
    botones();
    echo '</form>';
    script_fecha();
    boton("Volver","inf_fin.php?accion=listado");
    fin();
}
function agregar(){
    $sql = 'INSERT INTO inf_fin SET
    fecha = "'. fecha_a_mysql($_POST['fecha']) . '",
    bancos = "' . $_POST['bancos'] . '",
    bancosb0="'. $_POST['bancosb0'].'",
    egresos="'.$_POST['egresos'].'",
    ingresos="'.$_POST['ingresos'].'",
    ganancia="'.$_POST['ganancia'].'",
    conclusiones="'.$_POST['conclusion'] . '",
    recomendaciones= "' . $_POST['recomendaciones'] .'"';
    $res = mysql_query($sql) or die('Invalid query: ' . mysql_error());
    header( 'Location: inf_fin.php?accion=listado' );
}
function editar(){
    inicio();
    $sql = 'SELECT * FROM inf_fin WHERE id="' . $_GET['id'] .'"';
    $res = mysql_query($sql);
    $fil = mysql_fetch_array($res);
    encabezado_fecha("Editar Informe Financiero");
    boton("Volver","inf_fin.php?accion=listado");
    formulario('inf_fin.php?accion=actualizar');
    campo_oculto('id',$_GET['id']);
    $arr = array("Campo","Valor");
    encabezado_tabla($arr);
    input_fecha('Fecha:','fecha',$fil['fecha']);
    input_memo("Cuenta corriente:",'bancos',$fil['bancos']);
    input_memo("Bancos baso 0:",'bancosb0',$fil['bancosb0']);
    input_memo("Egresos",'egresos',$fil['egresos']);
    input_memo("Ingresos",'ingresos',$fil['ingresos']);
    input_memo("Ganancia:",'ganancia',$fil['ganancia']);
    input_memo("Conclusión:",'conclusion',$fil['conclusion']);
    input_memo("Recomendaciones:",'recomendaciones',$fil['recomendaciones']);
    fin_tabla();
    botones();
    echo '</form>';
    script_fecha();
    boton("Volver","inf_fin.php?accion=listado");
    fin();
}
function actualizar(){
    $sql = 'UPDATE inf_fin SET
    fecha = "'. fecha_a_mysql($_POST['fecha']) . '",
    bancos = "' . $_POST['bancos'] . '",
    bancosb0="'. $_POST['bancosb0'].'",
    egresos="'.$_POST['egresos'].'",
    ingresos="'.$_POST['ingresos'].'",
    ganancia="'.$_POST['ganancia'].'",
    conclusion="'.$_POST['conclusion'] . '",
    recomendaciones= "' . $_POST['recomendaciones'] .'" WHERE id="' . $_POST['id'] .'"';
    $res = mysql_query($sql) or die('Invalid query: ' . mysql_error());
    header( 'Location: inf_fin.php?accion=listado' );
}
if($_GET['accion']==''){
    $accion='listado';
}
else{
    $accion=$_GET['accion'];
}
switch($accion) {
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
    case 'ver':
        ver();
        break;
    case 'actualizar':
        actualizar();
        break;
    case 'confirmar':
        confirmar_borrar($_GET['id'],'inf_fin.php');
        boton('Volver','inf_fin.php?accion=listado');
        break;
    case 'eliminar':
        borrar('inf_fin',$_POST['id'],'inf_fin.php?accion=listado');
        break;
}
?>

<?php
include('funciones.php');
include('datos.php');
if (!$_GET['accion']){
    $accion='categoria';
} else {
    $accion=$_GET['accion'];
}
switch($accion){
    case 'categoria':
        categoria();
        break;
    }
function categoria(){
    encabezado('Clientes por categoria');
    boton("Volver","geined.py?accion=academico");
    // Datos de la categoria
    $sql_ccl = 'SELECT * FROM cat_clientes WHERE id="'.$_GET['id'].'"';
    $res_ccl = mysql_query($sql_ccl);
    $row_ccl = mysql_fetch_row($res_ccl);
    echo '<h2>'.$row_ccl[1] . '</h2>';
    encabezado_tabla(array("Nº","Nombre","Telefono","Notas","Acciones"));
    $sql_cli = 'SELECT * FROM clientes WHERE categoria_id="'.$_GET['id'].'"';
    $res_cli = mysql_query($sql_cli);
    $i = 0;
    while($fil_cli = mysql_fetch_array($res_cli)){
        fila_alterna($i);
        celda($fil_cli['id']);
        celda($fil_cli['nombre']);
        celda($fil_cli['telefono']);
        celda($fil_cli['notas']);
        echo '<td>';
        boton("Detalles",'lla.php?accion=listado&id='.$fil_cli['id']);
        boton("Editar",'cli.py?accion=editar&id=' . $fil_cli['id']);
        echo '</td></tr>';
        $i =  $i +1;
    }
    fin_tabla();
    boton('Volver','geined.py?accion=academico');
}
?>

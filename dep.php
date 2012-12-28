<?php
include('funciones.php');
include('datos.php');
function listado(){
    /*! Listado de depósitos */
    encabezado('Listado de Depósitos');
    boton("Nuevo","dep.php?accion=nuevo");
    boton("Volver",'geined.py?accion=sistema');
    //cargar datos
    $sql='SELECT * FROM depositos';
    $resultado = mysql_query($sql);
    encabezado_tabla(array("Nº","Depósito","Código","Acciones"));
    for ($i = 0; $i < mysql_num_rows($resultado); $i++) {
        echo '<tr>';
        $row = mysql_fetch_array($resultado);
        celda($row['id']);
        celda($row['deposito']);
        celda($row['codigo']);
        echo '<td>';
        boton("Detalle",'dep_ver?accion=detalle&id='.$row['id']);
        boton("Editar",'dep.php?id='.$row['id'].'&accion=editar');
        boton("Borrar",'dep.php?accion=confirmar&id='.$row['id']);
        echo '</td></tr>';
    }
    fin_tabla();
    boton('Volver','geined.py?accion=sistema');
    fin();
}
function editar(){
    encabezado('Edición de Depósito');
    encabezado_tabla(array("Campo","Valor"));
    formulario("dep.php?accion=actualizar");
    $sql='select * from depositos where id="' . $_GET['id'].'"';
    //cargar datos
    $resultado = mysql_query($sql);
    $fila=mysql_fetch_array($resultado);
    campo_oculto("id",$_GET['id']);
    input_texto("Depósito:","deposito",$fila['deposito']);
    input_texto("Código:","codigo",$fila['codigo']);
    botones();
    fin_formulario();
    fin_tabla();
    boton('Volver','dep.php?accion=listado');
    fin();
}
function actualizar(){
    $id = $_POST['id'];
    $sql = 'UPDATE depositos SET
        deposito = "' . $_POST['deposito'] . '",
        codigo = "' . $_POST['codigo'] . '" WHERE id = "' . $_POST['id'] . '"';
    $result = mysql_query($sql) or die('Invalid query: ' . mysql_error());
    header( 'Location: dep.php?accion=listado' );
}
function nuevo(){
    autorizacion(1);
    encabezado('Nuevo Depósito');
    encabezado_tabla(array("Campo","Valor"));
    formulario("dep.php?accion=agregar");
    input_texto("Depósito:","deposito","");
    input_texto("Código:","codigo","");
    botones();
    fin_formulario();
    fin_tabla();
    boton('Volver','dep.php?accion=listado');
}
function agregar(){
    $id = $_POST['id'];
    $sql1 = 'SELECT * FROM depositos WHERE deposito="'.$_POST['deposito'].'"';
    $res1 = mysql_query($sql1);
    if (mysql_num_rows($res1)==0){
        $sql = 'INSERT INTO depositos SET
            deposito = "' .$_POST['deposito'] .'",
            codigo = "' .$_POST['codigo'] . '" ';
        $result = mysql_query($sql) or die('Consulta inválida: ' . mysql_error());
        header( 'Location: dep.php?accion=listado' ) ;
    }
    else {
        duplicado('dep.php?accion=listado');
    }
}
autorizacion(2);
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
        Confirmar_Borrar($_GET['id']);
        boton('Volver','dep.php?accion=listado');
        break;
    case 'eliminar':
        autorizacion(1);
        borrar('depositos',$_POST['id'],'dep.php?accion=listado');
        break;
}
?>

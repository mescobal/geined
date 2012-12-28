<?php
session_start();
include('funciones.php');
if(!$_GET['accion']){
    $accion='editar';
} else {
    $accion=$_GET['accion'];
}
switch($accion){
    case 'editar':
        editar();
        break;
    case 'cambiar':
        cambiar();
        break;
    }
function editar(){
    encabezado("Cambio (virtual) de sucursal");
    boton("Central","suc.php?accion=cambiar&deposito_id=1");
    boton("Costa","suc.php?accion=cambiar&deposito_id=2");
    boton("Carrasco","suc.php?accion=cambiar&deposito_id=3");
    fin();
}
function cambiar(){
    $deposito_id = $_GET['deposito_id'];
    $_SESSION['deposito_id']=$deposito_id;
    /* redirigir("geined.py?accion=principal"); */
    /* pasa a script en python que pone cookie adecuada */
    redirigir("suc.py?deposito_id=".$deposito_id);
}
?>

<?php
/* Mensaje al pie de boleta */
include('funciones.php');
autorizacion(5);
if(!$_GET['accion']){
    $accion="ver";
} else {
    $accion=$_GET['accion'];
}
switch($accion){
    case 'ver':
        ver();
        break;
    case 'guardar':
        guardar();
        break;
}
function ver(){
    encabezado("Mensaje al pie de boleta");
    $pie_bol = 'pie_bol.txt';
    $fh = fopen($pie_bol, 'r');
    $linea = fgets($fh);
    fclose($fh);
    echo "<h2>Linea actual:</h2>";
    nota("Recuerde que la lína al pie de boleta es común a todas las sucursales");
    formulario("menpie.php?accion=guardar");
    echo '<table><tr>';
    input_texto("Mensaje:","mensaje",$linea,80);
    echo '</tr>';
    botones();
    fin_formulario();
    fin_tabla();
    boton("Volver","geined.py?accion=recepcion");
}
function guardar(){
    $texto = $_POST['mensaje'];
    $pie_bol = "pie_bol.txt";
    $fh = fopen($pie_bol, 'w') or die("No puedo abrir el archivo");
    $stringData = $texto;
    fwrite($fh, $stringData);
    fclose($fh);
    redirigir("geined.py?accion=recepcion");
}
?>

<?php
include('funciones.php');
include('datos.php');
if (!$_GET['accion']){
    $accion='listado';
}
else{
    $accion=$_GET['accion'];
}
/* Recuperar variables */
$cliente_id = $_GET['id'];
encabezado('Detalles del cliente');
$fil1 = buscar_registro("clientes","id",$cliente_id);
encabezado_tabla(array("Cliente:",$fil1['nombre']));
echo '<tr>';
celda("Dirección:"); celda($fil1["direccion"]);
echo '</tr>';
echo'<tr>';
celda("Teléfono:"); celda($fil1["telefono"]);
echo '</tr>';
echo '<tr>';
celda("eMail:"); celda($fil1["email"]);
echo '</tr>';
$sql_catcli = 'SELECT * FROM cat_clientes WHERE id="'.$fil1[7].'"';
$res_catcli = mysql_query($sql_catcli);
$fil_catcli = mysql_fetch_row($res_catcli);
$categoria = $fil_catcli[1];
echo '<tr>';
celda("Categoría:"); celda($categoria);
echo '</tr>';
echo '<tr>';
celda("CI:"); celda($fil1["ci"]);
echo '</tr>';
echo '<tr>';
celda("Notas:"); celda($fil1["notas"]);
echo '</tr>';
$sql_alu = "SELECT * FROM alumnos WHERE cliente_id = '$cliente_id'";
$res_alu = mysql_query($sql_alu);
while($fil_alu = mysql_fetch_array($res_alu)){
    echo '<tr>';
    $fil_cur = buscar_registro("cursos","id",$fil_alu['curso_id']);
    if($fil_alu['finalizado']==1){
        celda("Cursó:");
    } else {
        celda("Inscripto en:");
    }
    celda($fil_cur['curso']);
    echo '</tr>';
}
fin_tabla();
boton("Estado de cuenta",'ctacli.php?id='.$fil1['id'].'&accion=listado');
boton("Llamadas",'lla.php?accion=listado&cliente_id='.$_GET['id']);
boton("Notas",'cli_ver.php?id='.$_GET['id'].'&accion=notas');
boton("Escolaridad",'cli_ver.php?id='.$_GET['id'].'&accion=escolaridad');
boton("Documentos",'cli_ver.php?id='.$_GET['id'].'&accion=documentos');
boton("Volver","cli.py?accion=listado");
?>

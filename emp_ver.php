<?php
include('funciones.php');
include('datos.php');
encabezado('Detalles del empleado');
$id = $_GET['id'];
$fil1 = buscar_registro("empleados","id",$id);
echo '<h2>Empleado: '.$fil1['nombre'].'</h2>';
echo 'Telefono: ' . $fil1['telefono'] . '<br /><br />';
boton("Estado de cuenta","emp_ver.php?id='.$fil1[0].'&accion=cuentas");
boton("Sueldos","emp_ver.php?id=$id&accion=sueldos");
boton("Volver","empleados.py?accion=listado");
fin();
?>

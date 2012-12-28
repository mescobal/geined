<?php
include("funciones.php");
include("datos.php");
autorizacion(5);
if(!$_GET['accion']){
    $accion="listado";
} else {
    $accion = $_GET['accion'];
}
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
case 'devolver':
    devolver();
    break;
}
function listado(){
    encabezado("Prestamo de material a empleados");
    // extra_id=1 es PRESTAMO DE MATERIAL
    $sql_pre = "SELECT * FROM cta_empleados WHERE extra_id=1";
    $res_pre = mysql_query($sql_pre);
    $i=0;
    boton("Nuevo","presmat.php?accion=nuevo");
    boton("Volver","geined.py?accion=comprobantes");
    encabezado_tabla(array("Nº","Empleado","Fecha","Detalle","Debe","Haber","Saldo","Acciones"));
    while($fil_pre=mysql_fetch_array($res_pre)){
        $id = $fil_pre['id'];
        fila_alterna($i);
        $id=$fil_pre['id'];
        $empleado_id = $fil_pre['empleado_id'];
        celda($id);
        $fil_emp = buscar_registro("empleados","id",$empleado_id);
        celda($fil_emp['nombre']);
        celda(mysql_a_fecha($fil_pre['fecha']));
        celda($fil_pre['detalle']);
        linea_moneda($fil_pre['debe']);
        linea_moneda($fil_pre['haber']);
        $saldo = $saldo - $fil_pre['debe'] + $fil_pre['haber'];
        linea_moneda($saldo);
        echo '<td>';
        boton("Ver cuenta","ctaempleados.py?accion=listado&id=$empleado_id");
        boton("Devolución","presmat.php?accion=devolver&id=$id");
        echo '</td></tr>';
        $i=$i+1;
    }
    fin_tabla();
    boton("Volver","geined.py?accion=comprobantes");
    fin();
}
function nuevo(){
    $sql_emp = "SELECT * FROM empleados ORDER BY nombre";
    $res_emp = mysql_query($sql_emp);
    $sql_bie = "SELECT * FROM bie_cam ORDER BY descripcion";
    $res_bie = mysql_query($sql_bie);
    encabezado_fecha("Prestamo de material a empleados");
    formulario("presmat.php?accion=agregar");
    // empleado_id
    input_combo("Empleado:","empleado_id",$res_emp,"");
    /* Problema: es complicado armar un formulario de prestamo de material que
    se traduzca en movimientos en la cuenta del empleado,
    que se traduzca en cambios en el inventario
    que se traduzca en cambios en la contabilidad
    Requiere de mas pienso */
    encabezado_tabla(array("Campo","Valor"));
    // fecha
    input_fecha("Fecha","fecha",fecha_a_mysql(date('d/m/y')));
    // biecam_id
    input_combo("Material:","biecam_id",$res_bie,"");
    // cantidad
    input_numero("Cantidad:","cantidad","1");
    fin_tabla();
    botones();
    fin_formulario();
    script_fecha(); 
    fin();
}
function agregar(){
    $biecam_id = $_POST['biecam_id'];
    $empleado_id = $_POST['empleado_id'];
    $fecha2 = fecha_a_mysql($_POST['fecha']);
    $fil_bie = buscar_registro("bie_cam","id",$biecam_id);
    $material = $fil_bie['descripcion'];
    // monto ---- dato secundario
    $precio = $fil_bie['precio'];
    //deposito_id POR DEFECTO ES LA SUCURSAL EN LA QUE ESTA, OJO SI ES CENTRAL
    $deposito_id = $_SESSION['deposito_id'];
    $fil_suc = buscar_registro("depositos","id",$deposito_id);
    $sucursal = $fil_suc['deposito'];
    //extra_id valor arbitrario: 1 es material
    $extra_id = 1;
    $detalle = "Prestamo de $material en sucursal $sucursal";
    $sql = "INSERT INTO cta_empleados SET empleado_id = $empleado_id,
    fecha = '$fecha2', detalle ='$detalle', debe = $precio, haber = 0, extra_id = $extra_id";
    $res = mysql_query($sql);
    redirigir("presmat.php?accion=listado");
    /* operacion sobre cta_empleados */
    /* No altera stock porque no son libros a la venta sino material docente */
    /* NO altera contabilidad porque son dentro del mismo rubro */
}
function devolver(){
    $id = $_GET['id'];
    $fil_cta = buscar_registro("cta_empleados","id",$id);
    $empleado_id = $fil_cta['empleado_id'];
    $fecha2 = fecha_a_mysql(date('d/m/y'));
    $detalle = $fil_cta['detalle'];
    $precio = $fil_cta['debe'];
    $extra_id = $fil_cta['extra_id'];
    $sql = "INSERT INTO cta_empleados SET empleado_id = $empleado_id,
    fecha = '$fecha2', detalle ='$detalle', debe = 0, haber = $precio, extra_id = $extra_id";
    if($precio!=0){
        $res = mysql_query($sql);
    }
    redirigir("presmat.php?accion=listado");
}
?>

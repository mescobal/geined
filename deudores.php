<?php
include('funciones.php');
include('datos.php');
function listado(){
    //Conceptualizacion de deudores
    //ALUMNOS que PAGARON ultima cuota antes del 12 del mes previo
    // Opcion: ordenar alumnos por ultima cuota paga
    $sql_alu = "SELECT * FROM alumnos WHERE tipo_pago_id<10";
    $res_alu = mysql_query($sql_alu);
    mysql_query("TRUNCATE TABLE deudores");
    while($fil_alu=mysql_fetch_array($res_alu)){
        $alumno_id = $fil_alu['id'];
        $cliente_id=$fil_alu['cliente_id'];
        $arr_cliid=$cliente_id;
        $sql_bol = "SELECT * FROM bol_cont WHERE cliente_id=$cliente_id ORDER BY fecha";
        $res_bol = mysql_query($sql_bol);
        while($fil_bol=mysql_fetch_array($res_bol)){
            $id_bol = $fil_bol['id'];
            $sql_det = "SELECT * FROM bol_det WHERE bol_cont_id=$id_bol";
            $res_det = mysql_query($sql_det);
            while($fil_det = mysql_fetch_array($res_det)){
                if($fil_det['producto_id']==1){
                    $fecha=$fil_bol['fecha'];
                }
            }
        }
        $fil_cli = buscar_registro("clientes","id",$cliente_id);
        $curso_id = $fil_alu['curso_id'];
        $sql_deu = "INSERT INTO deudores SET cliente_id=$cliente_id,
            curso_id = $curso_id, ultima ='$fecha', extra = $alumno_id";
        $res_deu = mysql_query($sql_deu);
    }
    encabezado("Listado de deudores");
    nota("Excluye alumnos registrados como Famliares o Garantia");
    boton("Volver","geined.py?accion=recepcion");
    encabezado_tabla(array("Nombre","Curso","Ultima cuota paga","Acciones"));
    $sql_deu = "SELECT * FROM deudores ORDER BY ultima";
    $res_deu = mysql_query($sql_deu);
    while($fil_deu = mysql_fetch_array($res_deu)){
        $alumno_id = $fil_deu['extra'];
        $cliente_id = $fil_deu['cliente_id'];
        $fil_cli = buscar_registro("clientes","id",$cliente_id);
        celda($fil_cli['nombre']);
        $curso_id = $fil_deu['curso_id'];
        $fil_cur = buscar_registro("cursos","id",$curso_id);
        celda($fil_cur['curso']);
        celda(mysql_a_fecha($fil_deu['ultima']));
        echo "<td>";
        boton("Editar","alu.py?accion=editar&id=$alumno_id");
        boton("Ver cliente","cli_ver.php?id=$cliente_id");
        boton("Ver grupo","cur_ver.py?id=$curso_id");
        echo "</td></tr>";
    }
    fin_tabla();
    boton("Volver","geined.py?accion=recepcion");
    fin();
}
$accion='listado';
if (!$_GET['accion']) {$accion='listado';}
else $accion=$_GET['accion'];
switch($accion) {
    case 'listado':
        listado();
        break;
}
?>

<?php
include('funciones.php');
include('datos.php');
autorizacion(5);
if (!$_GET['accion']){
        $accion="cuota";
    }
else {
    $accion = $_GET['accion'];
}
switch ($accion) {
    case 'guardar':
        guardar();
        break;
    case 'cuota':
        if (!$_GET['alumno_id']){
            buscar_alumno();
        }
        else {
            cuota();
        }
        break;
}
function buscar_alumno(){
	/*! Busca un alumno para cobrarle una cuota 
		agrega a la cola el alumno_id */
    /* Entrada */
    $deposito_id = $_GET['deposito_id'];
    $caja_id = $_GET['caja_id'];
    $cliente_id = $_GET['cliente_id'];
    $boleta_id = $_GET['boleta_id'];
    $cola = "deposito_id=$deposito_id&caja_id=$caja_id&cliente_id=$cliente_id&boleta_id=$boleta_id";
	// Busca en alumnos, no en clientes
    $sql_alu = 'SELECT * FROM alumnos WHERE cliente_id = "'.$cliente_id.'"';
	// SI se puede cobrar una cuota de un curso finalizado!
	//@annotation ACLARAR cuando se trata de un curso cerrado
    $res_alu = mysql_query($sql_alu);
    $filas = mysql_num_rows($res_alu);
    if ($filas==0){
        encabezado("Error al seleccionar cliente");
        echo "<h3>El cliente que usted seleccionó no está registrado como alumno,</br>";
        echo "Por este motivo no se le puede cobrar una cuota.</br>";
        echo "Debe inscribir primero a este cliente en algún curso.</h3>";
        linea();
        boton("Volver","bolcon.php?accion=listado&boleta_id=$boleta_id&deposito_id=$deposito_id&caja_id=$caja_id&cliente_id=$cliente_id");
        fin();
    }
    else {
        encabezado("Seleccionar curso");
		echo '<h2>Cursos abiertos</h2>';
		encabezado_tabla(array("Curso","Cuota","Acciones"));
		$i=0;
		while($fil_alu=mysql_fetch_array($res_alu)){
            $alumno_id = $fil_alu['id'];
            $fil_cur = buscar_registro("cursos","id",$fil_alu['curso_id']);
			if($fil_curso['finalizado']<>1){
				fila_alterna($i);
				celda($fil_cur['curso']);
				celda(moneda($fil_alu['cuota']));
				echo '<td>';
				boton("Seleccionar","bolcuo.php?&alumno_id=$alumno_id&$cola");
				echo '</td></tr>';
				$i = $i+1;
			}
        }
        fin_tabla();
		echo '<h2>Cursos cerrados</h2>';
		encabezado_tabla(array("Curso","Cuota","Acciones"));
		$i=0;
		while($fil_alu=mysql_fetch_array($res_alu)){
            $alumno_id = $fil_alu['id'];
            $fil_cur = buscar_registro("cursos","id",$fil_alu['curso_id']);
			if($fil_curso['finalizado']==1){
				fila_alterna($i);
				celda($fil_cur['curso']);
				celda(moneda($fil_alu['cuota']));
				echo '<td>';
				boton("Seleccionar","bolcuo.php?&alumno_id=$alumno_id&$cola");
				echo '</td></tr>';
				$i = $i+1;
			}
        }
        fin_tabla();
    }
}
function guardar(){
    /* entrada = cola anterior */
    /* Guarda linea de cuota en bol_det */
    $deposito_id = $_GET['deposito_id'];
    $caja_id = $_GET['caja_id'];
    $cliente_id = $_GET['cliente_id'];
    $boleta_id = $_GET['boleta_id'];
    $alumno_id = $_GET['alumno_id'];
	// el producto es un curso
    $producto_id = 1;
    $cantidad = $_POST['cantidad'];
    $detalle = $_POST['detalle'];
    $unitario = $_POST['unitario'];
    $grupo_id = $_POST['grupo_id'];
	$extra_id = $alumno_id;
    $cola = "deposito_id=$deposito_id&caja_id=$caja_id&cliente_id=$cliente_id&boleta_id=$boleta_id";
    $total = $unitario;
    // Para determinar el rubro: buscar en el curso el TIPO DE CURSO
    $fil_cur = buscar_registro("cursos","id",$grupo_id);
    $tipo_curso_id = $fil_cur['tipo_id'];
    // Buscar rubro en tipo de curso
    $fil_tip = buscar_registro("tipo_curso","id",$tipo_curso_id);
    $rubro = $fil_tip['rubro'];
    // Buscar en el curso el DEPOSITO
    $deposito_curso = $fil_cur['deposito_id'];
    // Si el deposito es 3, sumar 1 al rubro.
    if ($deposito_curso == 3){
    	$rubro = $rubro + 1;
	}
    $fecha=fecha_a_mysql(date('d/m/Y'));
    /* guarda linea en mov bol cont: id bol_con_id producto_id cantidad detalle unitario total rubro */
    linea_boleta($boleta_id,$producto_id,$cantidad,$detalle,$unitario,$total,$rubro,$extra_id);
    redirigir("bolcon.php?accion=listado&$cola");
}
function cuota(){
	/*! junta variables correspondientes a una cuota */
    /* Verificar variables de entrada */
    $deposito_id = $_GET['deposito_id'];
    $caja_id = $_GET['caja_id'];
    $cliente_id = $_GET['cliente_id'];
    $boleta_id = $_GET['boleta_id'];
    $alumno_id = $_GET['alumno_id'];
    $cola = "deposito_id=$deposito_id&caja_id=$caja_id&cliente_id=$cliente_id&boleta_id=$boleta_id&alumno_id=$alumno_id";
	// FIXME cuando se genera el detalle de una cuota 2 veces, no actualiza n de n
	// Alumno
    $sql_alu = 'SELECT * FROM alumnos WHERE cliente_id="'.$cliente_id.'"';
    $fil_alu = buscar_registro("alumnos","id",$alumno_id);
	$cuotas = $fil_alu['pago'];
	// Curso
    $fil_cur = buscar_registro("cursos","id",$fil_alu['curso_id']);
    $curso = $fil_cur['curso'];
    $grupo_id = $fil_cur['id'];
    $tipo_curso_id = $fil_cur['tipo_id'];
	// Tipo curso
	$fil_tip = buscar_registro("tipo_curso","id",$tipo_curso_id);
	$tot_cuotas = $fil_tip['duracion'];
	$pago_actual = $cuotas + 1;
    $monto = moneda($fil_alu['cuota']);
    $tipo_pago_id = $fil_alu['tipo_pago_id'];
    $fil_tpa = buscar_registro("tipo_pago","id",$tipo_pago_id);
    $tipopago = $fil_tpa['tipo'];
    $descuento = $fil_tpa['descuento'];
	// FIXME falta agregar cuota n de n
    $detalle = "Cuota de: $curso ($tipopago)";
    /* TODO: buscar rubro según tipo de curso */
    $fil_tcu = buscar_registro("tipo_curso","id",$tipo_curso_id);
    $rubro = $fil_tcu['rubro'];
    $fil_rub = buscar_registro("cuentas","rubro",$rubro);
    $nom_rubro = $fil_rub['nombre'];
    /* Despliegue de página */
    encabezado("Cobranza de cuota");
    formulario("bolcuo.php?accion=guardar&$cola");
    campo_oculto("bol_cont_id",$boleta_id);
    campo_oculto("cantidad","1");
    campo_oculto("unitario",$fil_alu['cuota']);
    campo_oculto("detalle",$detalle);
    campo_oculto("grupo_id",$grupo_id);
    encabezado_tabla(array("Campo","Valor"));
    echo "<tr><td>Detalle:</td><td>$detalle</td></tr>";
    echo "<tr><td>Tipo de pago:</td><td>$tipopago</td></tr>";
    echo "<tr><td>Monto:</td><td>$monto</td></tr>";
    fin_tabla();
    botones();
    fin_formulario();
	echo "<h2>Cuotas previas</h2>";
	$sql_cuo = "SELECT * FROM bol_det WHERE extra_id=$alumno_id AND producto_id=1 ORDER BY id";
	$res_cuo = mysql_query($sql_cuo);
	encabezado_tabla(array("Fecha","Detalle","Monto"));
	$fila=0;
	while($fil_cuo=mysql_fetch_array($res_cuo)){
		$boleta_id = $fil_cuo['bol_cont_id'];
		$fil_bol = buscar_registro("bol_cont","id",$boleta_id);
		$fecha = mysql_a_fecha($fil_bol['fecha']);
		fila_alterna($fila);
		celda($fecha);
		celda($fil_cuo['detalle']);
		linea_moneda($fil_cuo['total']);
		echo "</tr>";
	}
	fin_tabla();
    boton("Volver","bolcon.php?accion=listado&$cola");
}
?>

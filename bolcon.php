<?php
include('funciones.php');
include('datos.php');
function listado(){
    /*! Listado de boletas contado */
    /* Entrada: deposito_id, cliente_id */
    $deposito_id = $_GET['deposito_id'];
    $caja_id = $_GET['caja_id'];
    $cliente_id = $_GET['cliente_id'];
    $boleta_id = $_GET['boleta_id'];
    $cola = "deposito_id=$deposito_id&caja_id=$caja_id&cliente_id=$cliente_id&boleta_id=$boleta_id";
    /* ----------------------------------------- */
    $fil_dep = buscar_registro("depositos","id",$deposito_id);
    $sucursal = $fil_dep['deposito'];
    encabezado(empresa() . " $sucursal: boleta contado");
    script_noenter();
    $fil_bol = buscar_registro("bol_cont","id",$boleta_id);
    $fil_cli = buscar_registro("clientes","id",$cliente_id);
    $nombre = $fil_cli['nombre'];
    $direccion = $fil_cli['direccion'];
    echo '<table><tr><td>';
    /* Datos del cliente */
    echo '<table><tbody><tr><td>Fecha:</td><td align="right">';
    echo date('d/m/Y');
    echo  "</td></tr><tr><td>Nombre:</td><td>$nombre</td></tr><tr><td>Domicilio:</td><td>$domicilio</td></tr></tbody></table>";
    echo '</td><td>';
    /* Botonera */
    boton("Cuota","bolcuo.php?accion=cuota&id&$cola");
    boton("Libros","bollib.php?accion=editar&$cola");
    boton("Recargos","bolrec.php?accion=editar&$cola");
    boton("Matricula","bolmat.php?accion=editar&$cola");
    //boton("Módulo","bolmod.php?accion=editar&$cola");
    //boton("Imprimir","bolcon.php?accion=imprimir&$cola");
    boton("Volver","bolcon.php?accion=cancelar&$cola");
    /* si salgo de la boleta, no se graba eliminar toda la boleta y sus movimientos */
    echo '</td></tr></table>';
    /* Listado de movimientos */
    encabezado_tabla(array("Cantidad","Detalle","P.Unitario","Total","Acciones"));
    $sql_det = "SELECT * FROM bol_det WHERE bol_cont_id='$boleta_id'";
    $res_det = mysql_query($sql_det);
    $total=0;
    while ($fil = mysql_fetch_array($res_det)){
        echo '<tr>';
        celda($fil['cantidad']);
        celda($fil['detalle']);
        linea_moneda($fil['unitario']);
        linea_moneda($fil['total']);
        $total = $total + $fil['total'];
        echo '<td>';
        //boton("Editar","bolcon.php?accion=editar");
        //boton("Borrar","bolcon.php?accion=borrar");
        echo '</td></tr>';
    }
    fin_tabla();
    /* rutina de verificación para que no se guarde si no pagó está en el javascript*/
    $formac = "bolcon.php?accion=guardar&$cola";
    echo '<form id="bol" name="bol" action="'.$formac.'" method="POST">';
    echo "<input type='hidden' id='cola' value='$cola'>";
    echo '<h2>TOTAL: $<input type="text" id="to" name="total" value="'.$total.'" readonly="1" /></h2>';
    echo '<h3>Forma de pago</h3>';
    echo '<table><tbody>';
    echo '<tr>';
    echo '<td align="right">Efectivo:<input align="right" type="text" id="ef" name="efectivo" value="0" onchange="recalcular('."'ef'".');"></td>';
    echo '<td align="right">Cheques:<input align="right" type="text" id="ch" name="cheques" value="0" onchange="recalcular('."'ch'".');"></td>';
    echo '<td align="right">Vouchers:<input align="right" type="text" id="vo" name="vouchers" value="0" onchange="recalcular('."'vo'".');"></td>';
    echo '<td align="right">Otros:<input align="right" type="text" id="ot" name="otros" value="0" onchange="recalcular('."'ot'".');"></td>';
    echo '</tr>';
    fin_tabla();
    echo '<table><tbody><tr><td>Vuelto:</td><td><h3>$<input type="text" id="vu" name="vu"  value="'.$vuelto.'" readonly="1" /></h3></td></tr>';
    fin_tabla();
    echo '<span id="boton"></td><tr></span>';
    fin_formulario();
    echo '<script type="text/javascript">
    function recalcular(campo){
        var caracteresPermitidos ="0123456789.,-";
        var ef=0; var ch=0; var vo=0; var ot=0;var total=0;
        ef = parseFloat(document.getElementById("ef").value);
        ch = parseFloat(document.getElementById("ch").value);
        vo = parseFloat(document.getElementById("vo").value);
        ot = parseFloat(document.getElementById("ot").value);
        pago = ef + ch + vo + ot;
        total = parseFloat(document.getElementById("to").value);
        vuelto = pago-total;
        var str = document.getElementById(campo).value;
        flag = true;
        for(index=0;index<str.length;index++){
            myChar = str.charAt(index);
            if(caracteresPermitidos.indexOf(myChar)==-1){
                flag = false;
            }
        }
        if (flag==false){
            alert("Hay letras en los campos numericos");
        }
        if (vuelto<0){
            vuelto=0;
            document.getElementById("boton").innerHTML = "";
        } else {
            document.getElementById("boton").innerHTML =
    "<input type='."'submit'"." value="."'Aceptar'".'>
    <input type='."'button'"." value="."'Imprimir'"."onClick=parent.location="."'bolcon.php?accion=imprimir&".$cola."'>".';
        }
        document.getElementById("vu").value = vuelto;
    }
    </script>';
    fin();
}
function cancelar(){
    $deposito_id = $_GET['deposito_id'];
    $caja_id = $_GET['caja_id'];
    $cliente_id = $_GET['cliente_id'];
    $boleta_id = $_GET['boleta_id'];
    $cola = "deposito_id=$deposito_id&caja_id=$caja_id&cliente_id=$cliente_id&boleta_id=$boleta_id";
    /* ----------------------------------------- */
    //si salgo de la boleta, borrar la boleta con todos los movimientos
    // borrar los bol_det
    $sql = "DELETE FROM bol_det WHERE bol_cont_id = '$boleta_id'";
    $res = mysql_query($sql);
    // borrar bol_cont
    $sql = "DELETE FROM bol_cont WHERE id = '$boleta_id'";
    $res = mysql_query($sql);
    redirigir("caja_ver.php?accion=listado&$cola");
}
function guardar(){
    /* Entrada: deposito_id, cliente_id */
    /* Viene de bolcon */
    /* Actualiza datos de una boleta contado */
    $deposito_id = $_GET['deposito_id'];
    $caja_id = $_GET['caja_id'];
    $cliente_id = $_GET['cliente_id'];
    $boleta_id = $_GET['boleta_id'];
    $cola = "deposito_id=$deposito_id&caja_id=$caja_id&cliente_id=$cliente_id&boleta_id=$boleta_id";
    /* campos: id caja_id fecha cliente_id efe che vou otr total flag */
    $efectivo = $_POST['efectivo'];
    $cheques = $_POST['cheques'];
    $vouchers = $_POST['vouchers'];
    $otros = $_POST['otros'];
    $total = $_POST['total'];
    $vuelto = $_POST['vu'];
    $efectivo = $efectivo - $vuelto;
    $fecha = fecha_a_mysql(date('d/m/Y'));
    /* Buscar cliente */
    $fil_cli = buscar_registro("clientes","id",$cliente_id);
    $nombre = $fil_cli['nombre'];
    $detalle = "Boleta contado Nº interno: $boleta_id, $nombre";
    $sql = "UPDATE bol_cont SET caja_id='$caja_id', fecha='$fecha',
    cliente_id='$cliente_id', efectivo = '$efectivo', cheques='$cheques',
    vouchers='$vouchers', otros='$otros', total='$total'
    WHERE id='$boleta_id'";
    $resultado = mysql_query($sql);
    /* Guarda linea en caja del dia */
    $sql = "INSERT INTO mov_caja SET caja_id ='$caja_id',
    detalle = '$detalle', efectivo = '$efectivo',
    cheques = '$cheques', vouchers = '$vouchers',
    otros = '$otros'";
    $result = mysql_query($sql)  or die('SQL inválido: ' . mysql_error());
    // Ciclar x movimientos para generar asientos y demás
    $sql_mov = "SELECT * FROM bol_det WHERE bol_cont_id='$boleta_id'";
    $res_mov = mysql_query($sql_mov);
    $tot_mov = 0;
    while ($row = mysql_fetch_array($res_mov)){
        // para cada mov_bol dentro de ese boleta
        $monto = $row['total'];
        $tot_mov = $tot_mov + $monto;
        $rubro_haber = $row['rubro'];
        $subrub = substr($rubro_haber,0,3);
        $producto_id = $row['producto_id'];
        $extra_id = $row['extra_id'];
        $tot_cuota = 0;
        $cantidad = $row['cantidad'];
        // graba transaccion en otros como rubro $rubro_debe es la caja de origen
        switch ($deposito_id){
            case '1':
                $rubro_debe = 111018;
                break;
            case '2':
                $rubro_debe = 111025;
                break;
            case '3':
                $rubro_debe = 111026;
                break;
        }
        // pasar el monto a OTROS como rubro
        asiento_doble($fecha,$detalle,$rubro_debe,$rubro_haber,$monto,$boleta_id);
        // Genera movimientos específicos según el producto
        switch($producto_id){
            case '1':
                // el producto es una cuota
                // asignar una cuota paga al alumno
                // guardar linea en cuenta corriente del cliente
                $detalle_cuota = $row['detalle'];
                cta_cli_add($cliente_id,$detalle_cuota,0,$monto,$fecha);
                // agregar al alumno la cuota paga
                $fil_alu = buscar_registro("alumnos","id",$alumno_id);
                $pagos = $fil_alu['pago'];
                $pagos = $pagos + 1;
                $alumno_id = $extra_id;
                $sql_alu = "UPDATE alumnos SET pago='$pagos' WHERE id='$alumno_id'";
                $res = mysql_query($sql_alu) or die("Error: ".mysql_error());
                break;
            case '2':
                //El producto es un libro
                // Para detectar existencias: biecam_id y deposito_id
                // biecam_id es el extra_id
                $biecam_id = $extra_id;
                $sql_exi = "SELECT * FROM existencias WHERE deposito_id='$deposito_id' AND  biecam_id='$biecam_id'";
                $res_exi = mysql_query($sql_exi);
                // OJO: es probable que no esté ingresado en existencias
                if(mysql_num_rows($res_exi)==0){
                    // en ese caso tener previsto crear una línea en existencias
                    // Descontarlo del stock correspondiente en existencias
                    $cant_lib = -$cantidad;
                    // y asignarle una cantidad negativa al stock
                    // para que después se pueda corregir
                    $sql_ins = "INSERT INTO existencias SET bie_cam_id='$biecam_id',
                    deposito_id='$deposito_id', cantidad='$cant_lib'";
                } else {
                    $fil_exi = mysql_fetch_array($res_exi);
                    $cant_lib = $fil_exi['cantidad'] - $cantidad;
                    // Modificación propuesta por Gustavo
                    $sql_ins = "UPDATE existencias SET cantidad= '$cant_lib' WHERE deposito_id='$deposito_id' AND bie_cam_id='$biecam_id'";
                    // Original:
                    // $sql_ins = "UPDATE existencias SET cantidadbie_cam_id='$biecam_id', deposito_id='$deposito_id', cantidad='$cant_lib'";                    
                }
                $res = mysql_query($sql_ins);
                break;
        }
    }
    // despues de terminar el bucle, ciclar x transacciones con ese documento_id
    /* al final del ciclo, sacar de otros y pasar a EF CH VO */
    $rubro_otros = $rubro_debe;
    switch ($deposito_id){
        case '1':
            $rubro_ef = 111018;
            $rubro_ch = 111018;
            $rubro_vo = 111018;
            break;
        case '2':
            $rubro_ef = 111011;
            $rubro_ch = 111021;
            $rubro_vo = 113002;
            break;
        case '3':
            $rubro_ef = 111012;
            $rubro_ch = 111022;
            $rubro_vo = 113003;
            break;
    }
    // Hacer que no se procesen asientos con cifra 0
    // Efectivo
    if($efectivo!=0){
        asiento_doble($fecha,$detalle,$rubro_ef,$rubro_otros,$efectivo,$boleta_id);
    }
    //Cheques
    if($cheques!=0){
        asiento_doble($fecha,$detalle,$rubro_ch,$rubro_otros,$cheques,$boleta_id);
    }
    // Vouchers
    if($vouchers!=0){
        asiento_doble($fecha,$detalle,$rubro_vo,$rubro_otros,$vouchers,$boleta_id);
    }
    // No se toma en cuenta el rubro OTROS porque se supone que ya queda
    redirigir("bolcon.php?accion=imprimir&$cola");
}
function nuevo(){
    $fecha = fecha_a_mysql(date('d/m/Y'));
    $deposito_id=$_GET['deposito_id'];
    $caja_id = $_GET['caja_id'];
    $cliente_id = $_GET['cliente_id'];
    $cola = "deposito_id=$deposito_id&caja_id=$caja_id&cliente_id=$cliente_id";
    $sql_bol = "INSERT INTO bol_cont SET caja_id = '$caja_id',  cliente_id='$cliente_id', fecha='$fecha'";
    $result = mysql_query($sql_bol) or die('Invalid query: ' . mysql_error());
    /* Ultimo registro insertado */
    $boleta_id=mysql_insert_id();
    redirigir("bolcon.php?accion=listado&boleta_id=$boleta_id&$cola");
}
function buscar_cliente(){
    /* Entrada: caja_id, cliente_id, deposito_id */
    $deposito_id=$_GET['deposito_id'];
    $caja_id = $_GET['caja_id'];
    $cola = "deposito_id=$deposito_id&caja_id=$caja_id";
    encabezado("Buscar cliente (boleta contado)");
    echo '<table><tr><td>';
    boton("Volver","geined.py?accion=recepcion&$cola");
    echo '</td><td>';
    formulario("bolcon.php?accion=buscar_cliente&$cola");
    echo '<input type="text" name="busqueda">
        <input type="submit" VALUE="Buscar"></form>';
    echo '</td></tr></table>';
    //cargar datos
    if ($_POST['busqueda']<>''){
        $sql1='SELECT * from clientes where nombre like "%' .$_POST['busqueda'] .'%" order by nombre';
    }
    else {
        $sql1='select * from clientes order by nombre LIMIT 20';
    }
    $res1 = mysql_query($sql1);
    if ($res1==0)    {
        echo 'Error ' . mysql_error();
    }
    else {
        encabezado_tabla(array("Nombre","Teléfono","eMail","Categoría","Acciones"));
        for ($i = 0; $i < mysql_num_rows($res1); $i++){
            echo '<tr>';
            $fil1 = mysql_fetch_array($res1);
            celda($fil1['nombre']);
            celda($fil1['telefono']);
            celda($fil1['email']);
            // Categoria
            $sql2 = 'SELECT * FROM cat_clientes WHERE id="' . $fil1['categoria_id'] . '"';
            $res2 = mysql_query($sql2);
            if ($res2==0){
                $categoria='';
            }
            else {
                $fil2 = mysql_fetch_array($res2);
                $categoria=$fil2['categoria'];
            }
            celda($categoria);
            echo '<td>';
            $cliente_id = $fil1['id'];
            boton("Seleccionar","bolcon.php?accion=nuevo&cliente_id=$cliente_id&$cola");
            echo '</td>';
            echo '</tr>';
        }
        fin_tabla();
    }
    boton("Volver",'geined.py?accion=recepcion');
    fin();
}
function buscar_sucursal(){
    encabezado("Caja: seleccionar sucursal");
    boton("Central","bolcon.php?accion=listado&deposito_id=1");
    boton("Costa de Oro","bolcon.php?accion=listado&deposito_id=2");
    boton("Carrasco","bolcon.php?accion=listado&deposito_id=3");
    boton("Volver","geined.py?accion=recepcion");
    fin();
}
function imprimir(){
    $deposito_id = $_GET['deposito_id'];
    $caja_id = $_GET['caja_id'];
    $cliente_id = $_GET['cliente_id'];
    $boleta_id = $_GET['boleta_id'];
    $cola = "deposito_id=$deposito_id&caja_id=$caja_id&cliente_id=$cliente_id&boleta_id=$boleta_id";
    /* ----------------------------------------- */
    $fil_bol = buscar_registro("bol_cont","id",$boleta_id);
    $fecha = mysql_a_fecha($fil_bol['fecha']);
    $cliente_id = $fil_bol['cliente_id'];
    $fil_cli = buscar_registro("clientes","id",$cliente_id);
    $nombre = $fil_cli['nombre'];
    $direccion = $fil_cli['direccion'];
    encabezado_boleta();
    $lin = str_repeat(' ',90);
    for($i=0;$i<=70;$i++){
        $hoja[$i]=$lin;
    }
    $desp = 40;
    $hoja[0]=substr_replace($hoja[0],$fecha,80);
    $hoja[0+$desp]=substr_replace($hoja[0+$desp],$fecha,80);
    $hoja[3]=substr_replace($hoja[3],$nombre,20);
    $hoja[3+$desp]=substr_replace($hoja[3+$desp],$nombre,20);
    $hoja[5]=substr_replace($hoja[5],$direccion,20);
    $hoja[5+$desp]=substr_replace($hoja[5+$desp],$direccion,20);
    $sql_det = "SELECT * FROM bol_det WHERE bol_cont_id='$boleta_id'";
    $res_det = mysql_query($sql_det);
    $hoja[8] = substr_replace($hoja[8],"Cantidad",4,8);
    $hoja[8] = substr_replace($hoja[8],"Detalle",13,7);
    $hoja[8] = substr_replace($hoja[8],"Precio",79-6,6);
    $hoja[8] = substr_replace($hoja[8],"Total",95-5,5);
    $hoja[8+$desp] = substr_replace($hoja[8+$desp],"Cantidad",4,8);
    $hoja[8+$desp] = substr_replace($hoja[8+$desp],"Detalle",13,7);
    $hoja[8+$desp] = substr_replace($hoja[8+$desp],"Precio",79-6,6);
    $hoja[8+$desp] = substr_replace($hoja[8+$desp],"Total",95-5,5);
    $conta = 9;
    $totbol=0;
    while($fila = mysql_fetch_array($res_det)){
        $cantidad = trim($fila['cantidad']);
        $detalle = trim($fila['detalle']);
        $unitario = moneda($fila['unitario']);
        $total = moneda($fila['total']);
        if (strlen($detalle)>57) $detalle=substr($detalle,0,57);
        $hoja[$conta]= substr_replace($hoja[$conta],$cantidad,6,strlen($cantidad));
        $hoja[$conta]= substr_replace($hoja[$conta],$detalle,13,strlen($detalle));
        $hoja[$conta]= substr_replace($hoja[$conta],$unitario,80-strlen($unitario),strlen($unitario));
        $hoja[$conta]= substr_replace($hoja[$conta],$total,96-strlen($total),strlen($total));
        // Segunda hoja
        $hoja[$conta+$desp]= substr_replace($hoja[$conta+$desp],$cantidad,6,strlen($cantidad));
        $hoja[$conta+$desp]= substr_replace($hoja[$conta+$desp],$detalle,13,strlen($detalle));
        $hoja[$conta+$desp]= substr_replace($hoja[$conta+$desp],$unitario,80-strlen($unitario),strlen($unitario));
        $hoja[$conta+$desp]= substr_replace($hoja[$conta+$desp],$total,96-strlen($total),strlen($total));
        // Total
        $totbol=$totbol + $fila['total'];
        $conta = $conta + 1;
    }
    $total_boleta = moneda($totbol);
    $hoja[19] = substr_replace($hoja[20],$total_boleta,96-strlen($total_boleta),strlen($total_boleta));
    $hoja[19+$desp] = substr_replace($hoja[20+$desp],$total_boleta,96-strlen($total_boleta),strlen($total_boleta));
    /* Cargar linea desde archivo */
    $pie_bol = 'pie_bol.txt';
    $fh = fopen($pie_bol, 'r');
    $linea = fgets($fh);
    fclose($fh);
    $hoja[22] = substr_replace($hoja[22],$linea,6,strlen($linea));
    $hoja[22+$desp] = substr_replace($hoja[22+$desp],$linea,6,strlen($linea));
    echo "<pre>";
    for($i=0;$i<=70;$i++){
        echo $hoja[$i]."</br>";
    }
    echo "</pre>"    ;
    //boton("IMPRIMIR","bolcon.php?accion=guardar&$cola");
    echo '<script type="text/javascript">
    window.print();
    </script>';
    redirigir("caja_ver.php?accion=listado&$cola");
    //redirigir("bolcon.php?accion=guardar&$cola");
    fin();
}
/* INICIO DE BUCLE PRINCIPAL */
autorizacion(5);
if (!$_GET["accion"]){
    $accion="listado";
}
else{
    $accion=$_GET["accion"];
}
if(!$_GET['deposito_id']){
    //@annotation cambiar esto seleccionar_sucursal();
}
else {
    if(!$_GET['cliente_id']){
        buscar_cliente();
    }
    else {
        switch($accion){
            case 'listado':
                listado();
                break;
            case 'nuevo':
                nuevo();
                break;
            case 'buscar_cliente':
                buscar_cliente();
                break;
            case 'cuota':
                cuota();
                break;
            case 'guardar':
                guardar();
                break;
            case 'cancelar':
                cancelar();
                break;
            case 'imprimir':
                # imprimir();
                $deposito_id = $_GET['deposito_id'];
                $caja_id = $_GET['caja_id'];
                $cliente_id = $_GET['cliente_id'];
                $boleta_id = $_GET['boleta_id'];
                $cola = "deposito_id=$deposito_id&caja_id=$caja_id&cliente_id=$cliente_id&boleta_id=$boleta_id";
                redirigir("imp_bol.py?$cola");
                break;
        }
    }
}
?>

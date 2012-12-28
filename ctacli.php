<?php
include('funciones.php');
include('datos.php');
function listado(){
    encabezado('Estado de cuenta del cliente');
    //DATOS DEL CLIENTE
    if(!$_GET['cliente_id']){
        $cliente_id=$_GET['id'];
    }
    else {
        $cliente_id=$_GET['cliente_id'];
    }
    $sql_cli = 'SELECT * FROM clientes WHERE id="' .$cliente_id . '"';
    $res_cli = mysql_query($sql_cli);
    $fil_cli = mysql_fetch_array($res_cli);
    echo '<h2>'.$fil_cli['nombre'].'</h2>';
    echo '<h3>'.$fil_cli['direccion'].'</h3>';
    echo '<h4>'.$fil_cli['telefono'].'</h4>';
  boton("Nuevo",'ctacli.php?accion=nuevo&cliente_id='.$cliente_id);
  boton("Imprimir",'ctacli.php?accion=imprimir&cliente_id='.$cliente_id);
    //cargar datos
    $sql_cta='SELECT * FROM cta_clientes WHERE cliente_id="' . $cliente_id .'"  ORDER BY fecha';
    $res_cta = mysql_query($sql_cta);
  encabezado_tabla(array("Nº","Fecha","Concepto","Debe","Haber"));
    for ($i = 0; $i < mysql_num_rows($res_cta); $i++) {
        $fil_cta = mysql_fetch_array($res_cta);
        echo '<tr>';
        celda($fil_cta['id']);
    celda(mysql_a_fecha($fil_cta['fecha']));
    celda($fil_cta['concepto']);
    linea_moneda($fil_cta['debe']);
    linea_moneda($fil_cta['haber']);
    echo '</tr>';
    }
    $sql_saldo = 'SELECT SUM(debe) as D, SUM(haber) as H FROM cta_clientes WHERE  cliente_id="'.$cliente_id.'"';
    $res_saldo = mysql_query($sql_saldo);
    $fil_saldo = mysql_fetch_row($res_saldo);
    $debe = $fil_saldo[0];
    $haber= $fil_saldo[1];
    $saldo = $haber - $debe;
    echo '<TR><TD></TD><TD>Subtotales</TD><TD></TD><TD ALIGN=RIGHT>'.moneda($debe).'</TD><TD>'.moneda($haber).'</TD></TR>';
    echo '<TR><TD></TD><TD>Saldo</TD><TD ALIGN=RIGHT>'.Moneda($saldo).'</TD><TD></TD></TR>';
    echo '</tbody></table>';
    boton('Volver','cli_ver.php?id='.$_GET['id']);
}
if ($nivel>5) No_Autorizado();
if (!$_GET['accion']) {$accion = 'listado';}
else $accion = $_GET['accion'];
switch ($accion){
    // L I S T A D O
    case 'listado':
        listado();
        break;
    case 'editar':
        editar();
        break;
    case 'actualizar':
        $id = $_POST['id'];
        $sql = 'UPDATE cta_clientes SET 
            concepto= "' . $_POST['concepto'] . '",
            fecha="' . fecha_a_mysql($_POST['fecha']) . '",
            debe="' .$_POST['debe'] . '",
            haber="' .$_POST['haber'] . '"    WHERE id = "' . $id . '"';
        $result = mysql_query($sql) or die('Consulta inválida: ' . mysql_error());
        Header( 'Location: ctacli.php?accion=listado&id='.$_POST['cliente_id']) ;
        break;
    case 'nuevo':
        autorizacion(5);
        encabezado_fecha('Nueva entrada a la cuenta del cliente');
        echo '<table><thead><th>Campo</th><th>Valor</th></thead>';
        echo '<form action="ctacli.php?accion=agregar" method="POST">';
        $cliente_id = $_GET['cliente_id'];
        //cargar datos
        echo '<input type="hidden" name="cliente_id" value="'.$cliente_id.'">';
        echo '</td></tr>';
        echo '<tr><td>Fecha:</td>
            <td><input type="text" 
                       name="fecha" 
                       value="' . fecha_a_mysql(date('d/m/Y')) .'" 
                       id="f_date_b"/>
                <BUTTON TYPE="reset" ID="f_trigger_b">...</BUTTON></td>
            </tr>';
        echo '<tr><td>Concepto:</td>
            <td><input type="text" name="concepto"></td></tr>';
        echo '<tr><td>Debe:</td>
            <td><input type="text" name="debe"></td></tr>';
        echo '<tr><td>Haber:</td>
            <td><input type="text" name="haber"></td></tr>';
            Botones();
        echo '</form></table>';
        script_fecha();
        boton('Volver',"ctacli.php?accion=listado&id=$cliente_id");
        Break;
    case 'agregar':
        $cliente_id = $_POST['cliente_id'];
        $sql = 'INSERT INTO cta_clientes SET 
        fecha    = "' . fecha_a_mysql($_POST['fecha']) . '",
        cliente_id="' . $cliente_id        . '",
        concepto = "' . $_POST['concepto'] . '",
        debe     = "' . $_POST['debe'].      '",
        haber    = "' . $_POST['haber'].     '"';
        $result = mysql_query($sql) or die('Consulta inválida: ' . mysql_error());
        header( 'Location: ctacli.php?accion=listado&cliente_id='.$cliente_id ) ;
        break;
    case 'confirmar':
        confirmar_borrar($_GET['id']);
        boton('Volver al listado','ccl.py?accion=listado');
        break;
    case 'eliminar':
        autorizacion(2);
        borrar('cat_clientes',$_POST['id'],'ccl.py?accion=listado');
        break;
    case 'imprimir':
        encabezado_informe('Estado de cuenta al '.date('d/m/Y'));
        //DATOS DEL CLIENTE
        if(!$_GET['cliente_id']){
        $cliente_id=$_GET['id'];
        }
        else {
        $cliente_id=$_GET['cliente_id'];
        }
        $sql_cli = 'SELECT * FROM clientes WHERE id="' .$cliente_id . '"';
        $res_cli = mysql_query($sql_cli);
        $fil_cli = mysql_fetch_row($res_cli);
        echo '<H2>'.$fil_cli[1].'</H2>';
        echo '<H3>'.$fil_cli[2].'</H3>';
        echo '<H4>'.$fil_cli[8].'</H4>';
        //cargar datos
        $sql_cta='SELECT * FROM cta_clientes WHERE cliente_id="' . $cliente_id .'"  ORDER BY fecha';
        $res_cta = mysql_query($sql_cta);
        echo '<table><thead> <tr>';
        echo '<TH>Nº</TH>
            <TH>Fecha</TH>
            <TH>Concepto</TH>
            <TH>Debe</TH>
            <TH>Haber</TH></TR></THEAD><TBODY>';
        for ($i = 0; $i < mysql_num_rows($res_cta); $i++) {
            $fil_cta = mysql_fetch_row($res_cta);
            echo '<tr>';
            echo '<TD>'.$fil_cta[0].'</TD>';
            echo '<TD>'.mysql_a_fecha($fil_cta[6]).'</TD>';
            echo '<TD>'.$fil_cta[3].'</TD>';
            echo '<TD ALIGN=RIGHT>'.Moneda($fil_cta[4]).'</TD>';
            echo '<TD ALIGN=RIGHT>'.Moneda($fil_cta[5]).'</TD>';
              echo '</tr>';
        }
        $sql_saldo = 'SELECT SUM(debe) as D, SUM(haber) as H FROM cta_clientes WHERE cliente_id="'.$cliente_id.'"';
        $res_saldo = mysql_query($sql_saldo);
        $fil_saldo = mysql_fetch_row($res_saldo);
        $debe = $fil_saldo[0];
        $haber= $fil_saldo[1];
        $saldo = $haber - $debe;
        echo '<TR ALIGN=RIGHT><TD></TD><TD>Subtotales</TD><TD></TD><TD>'.Moneda($debe).'</TD><TD>'.Moneda($haber).'</TD></TR></TBODY></TABLE>';
        echo '<BR /><BR />';
        echo '<TABLE><TR><TD>Saldo: </TD><TD>'.Moneda($saldo).'</TD></TR></table>';
        boton(' ... ','cli.py?accion=listado');
        break;
    }
?>

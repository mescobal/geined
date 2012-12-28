<?php
/*! @file
Funciones globales utilizadas por todo el sistema
*/
include('./conf/log.inc');
function empresa(){
    // Lee del archivo de configuración el nombre de la empres
    $ini_array = parse_ini_file("conf/geined.conf", true);
    $empresa = $ini_array["empresa"]["nombre"];
    return $empresa;
}
function inicio(){
    /*! función general para iniciar página
    @param ninguno
    @return cadena de texto con encabezado html*/
    header('Content-Type: text/html; charset=utf-8');
}
function estilo(){
    /*! Agrega un enlace a hoja de estilo
    @param ninguno
    @return enlace a hoja de estilo geined.css */
    echo '<link type="text/css" href="./css/geined2.css" rel="stylesheet" />';
}
function encabezado($titulo){
    inicio();
    echo '<head>';
    echo '<script type="text/javascript" src="geined.js" charset="utf-8"></script>';
    echo "<title>$titulo</title>";
    estilo();
    echo '</head><body><div id="envoltura">';
    echo "<table width='100%'><tr><td><img src='./conf/logo.png'
/></td><td><h1>$titulo</h1></td><td>";
    switch($_SESSION['deposito_id']){
        case '1':
            $sucursal = "Central";
            break;
        case '2':
            $sucursal = "Costa de Oro";
            break;
        case '3':
            $sucursal = "Carrasco";
            break;
        }
    echo "</td></tr><tr><td>Usted se encuentra en: $sucursal</td><td>";
    echo '<a href="geined.py">Inicio</a> | <a href="des.py">Reportar error</a> | <a href="suc.php">Cambiar de sucursal</a>';
    echo "</td></tr></table>";
}
function encabezado_login($titulo){
    inicio();
    echo '<head>';
    echo "<title>$titulo</title>";
    estilo();
    echo '</head><body><div id="env_fina">';
    echo "<table width='100%'><tr><td><img src='./conf/logo.png'
/></td><td><h1>$titulo</h1></td></tr></table>";
}
function encabezado_menu($texto){
    echo "<h2>$texto</h2>";
}
function imagen_menu($imagen,$enlace,$texto){
    echo '<td align="center"><a href="'.$enlace.'"><img src="./img/'.$imagen.'" width="64"
height="64" align="top" border="0"></a>'.$texto.'</td>';
}
function encabezado_informe($titulo){
    inicio();
    echo "<title>$titulo</title>";
    echo '<link type="text/css" href="./css/greyscale.css" rel="stylesheet" />';
    echo '</head><body>';
    echo '<H1>'.$titulo.'</H1>';
}
function encabezado_recibo($titulo){
    /*! Encabezado para recibo de sueldos
    @param $titulo
    @return Código HTML
    */
    inicio();
    echo "<title>$titulo</title>";
    echo '<link type="text/css" href="./css/recibo.css" rel="stylesheet" />';
    echo '</head><body>';
    echo '<h1>'.$titulo.'</h1>';
}
function encabezado_boleta(){
    inicio();
    echo "<title>Boleta</title>";
    //echo '<link type="text/css" href="./css/boleta.css" rel="stylesheet" />';
    echo '<link type="text/css" href="./css/boleta2.css" rel="stylesheet" />';
    echo '</head><body>';
}
function encabezado_fecha($titulo){
    /*! Encabezado que incluye javascript para manejo de fechas
    @param ninguno
    @return codigo html que incluye vínculos a javascript
    */
    inicio();
    echo "<title>$titulo</title>";
    estilo();
    echo '<style type="text/css">@import url(./js/calendar-win2k-1.css);</style>';
    echo '<script type="text/javascript" src="./js/calendar.js"></script>';
    echo '<script type="text/javascript" src="./js/lang/calendar-es.js"></script>';
    echo '<script type="text/javascript" src="./js/calendar-setup.js"></script>';
    echo '</head><body><div id="envoltura">';
    echo "<h1>$titulo</h1>";
}
function nota($texto){
    echo '<table width="100%"><tr><td><span class="nota">'.$texto.'</span></td></tr></table>';
}
function botones(){
    echo '<tr><td><input type="submit" value="Aceptar"></td><tr>';
    }
function moneda($numero){
    $moneda = number_format($numero, 2);
    $moneda = '$' . $moneda;
    return $moneda;
     }
function mysql_a_fecha($fecha){
     ereg( "([0-9]{2,4})-([0-9]{1,2})-([0-9]{1,2})", $fecha, $mifecha);
     $lafecha=$mifecha[3]."/".$mifecha[2]."/".$mifecha[1];
     return $lafecha;
 }
function fecha_a_mysql($fecha){
     ereg( "([0-9]{1,2})/([0-9]{1,2})/([0-9]{2,4})", $fecha, $mifecha);
     $lafecha=$mifecha[3]."-".$mifecha[2]."-".$mifecha[1];
     return $lafecha;
 }
function duplicado($pagina){
    encabezado('Error');
    nota('Ya existe un dato igual al que usted intenta agregar.
    Verifique el dato e inténtelo nuevamente');
    boton('Volver',$pagina);
}
function error_variables($pagina){
    encabezado("Error");
    nota("Faltan variables para completar la operación");
    boton("Volver", $pagina);
    }
function confirmar_borrar($id,$pagina){
  encabezado('Confirmar eliminación de registro');
  nota('¿Esta seguro que desea eliminar este registro?');
    echo '<form action="'.$pagina.'?accion=eliminar" method="post">';
    echo '<input type="hidden" name="id" value="'. $id.'">';
  echo '<input type="submit" value="Confirmar"></form>';
  boton('Volver',$pagina);
}
function celda($texto){
    echo '<TD>'.$texto.'</TD>';
}
function linea_moneda($texto){
    echo '<td align="right">'.moneda($texto).'</td>';
}
function linea_numero($texto){
    echo '<TD ALIGN=RIGHT>'.number_format($texto,2,'.','').'</TD>';
}
function no_autorizado(){
    inicio();
    encabezado('Acceso no autorizado');
    nota('Usted no se encuentra autorizado para ver esta página');
    boton('Volver','geined.py');
    fin();
}
function script_fecha(){
echo '<script type="text/javascript">
    Calendar.setup({
    inputField     :    "f_date_b",           //*
    ifFormat       :    "%d/%m/%Y",
    showsTime      :    false,
    button         :    "f_trigger_b",        //*
    step           :    1
    });
    </script>';
}
function script_fecha2(){
echo '<script type="text/javascript">
    Calendar.setup({
    inputField     :    "f_date_b2",           //*
    ifFormat       :    "%d/%m/%Y",
    showsTime      :    false,
    button         :    "f_trigger_b2",        //*
    step           :    1
    });
    </script>';
}
function script_noenter(){
    echo '<script type="text/javascript">
    function stopRKey(evt) {
  var evt = (evt) ? evt : ((event) ? event : null);
  var node = (evt.target) ? evt.target : ((evt.srcElement) ? evt.srcElement : null);
  if ((evt.keyCode == 13) && (node.type=="text"))  {return false;}
    }
    document.onkeypress = stopRKey;
    </script>';
}
function input_fecha($texto,$campo,$valor){
echo '<tr><td>'.$texto.'</td><td><input type="text" name="'.$campo.'" id="f_date_b" value="' . mysql_a_fecha($valor).'"/><BUTTON TYPE="reset" ID="f_trigger_b">...</button>';
echo '</TD></TR>';
}
function input_fecha2($texto,$campo,$valor){
echo '<tr><td>'.$texto.'</td><td><input type="text" name="'.$campo.'" id="f_date_b2" value="' . mysql_a_fecha($valor).'"/><BUTTON TYPE="reset" ID="f_trigger_b2">...</button>';
echo '</TD></TR>';
}
function input_texto($texto,$campo,$valor,$ancho=20){
    echo "<tr><td>$texto</td>";
    echo "<td><input type='text' name='$campo' value='$valor' size='$ancho'/></td></tr>";
}
function input_numero($texto,$campo,$valor){
echo '<tr><td>'.$texto.'</td><td><input type="text" name="'.$campo.'"
            value="' . number_format($valor,2,'.','').'"></td></tr>';
}
function input_memo($texto,$campo,$valor){
    echo '<tr><td>'.$texto.'</td>';
    echo '<td><textarea name="'.$campo.'" rows="10" cols="50">' .$valor . '</textarea></td></tr>';
}
function formulario($accion){
    echo '<form action="'.$accion.'" method="POST">';
}
function fin_tabla(){
    echo '</tbody></table>';
}
function input_combo($texto,$campo,$resultado,$valor){
    echo '<TR><TD>'.$texto.'</TD>';
    echo '<TD><SELECT NAME="'.$campo.'">';
    for($i=0; $i < mysql_num_rows($resultado); $i++){
        $fil = mysql_fetch_row($resultado);
        echo '<option value="' . $fil[0] .'"';
        if($fil[0]==$valor){
            echo 'selected="selected"';
        }
        echo '>'.$fil[1].'</option>';
    }
    echo '</select></td></tr>';
}
function boton($texto,$accion){
    echo '<input type="button" value="'.$texto.'" onClick=parent.location="'.$accion.'" />';
}
function btnNuevaVentana($texto,$accion){
    echo '<input type="button" value="'.$texto.'" onClick=window.open("'.$accion.'") />';
}
function fin(){
    echo '</div></body></html>';
}
function imagen($imagen){
    echo '<img src="./img/'.$imagen.'" width="64" height="64" border="0">';
}
function encabezado_tabla($arr){
    echo '<table width="100%"><thead><tr>';
    foreach($arr as $a){
        echo "<th>$a</th>";
    }
    echo '</tr></thead><tbody>';
}
function campo_oculto($variable,$dato){
    echo '<input type="hidden" name="'.$variable.'" value="'.$dato.'">';
}
function fin_formulario(){
    echo '</form>';
}
function input_check($texto,$variable,$valor){
    echo '<TR><TD>';
    echo $texto;
    if($valor=="1"){
        $adicional= "checked";
    }
    echo '</TD><TD><INPUT TYPE="checkbox" NAME="'.$variable.'" VALUE="1"'.$adicional.'></TD></TR>';

}
function autorizacion($niv){
    // 20: cualquiera
    // 10: docente
    // 5: recepcion
    // 4: Adriana
    // 3: Hassan / Leo
    // 2: Mariana
    // 1: Marcelo
    @session_start();
    if ($_SESSION['auth']!='yes') {
        redirigir("no_autorizado.html");
    }
    $sql = 'SELECT * FROM usuarios WHERE usuario="' . $_SESSION['logname'] . '"';
    $res = mysql_query($sql);
    if ($res==0){
        //header("location: no_autorizado.html");
        redirigir("no_autorizado.html");
    }
    $fil = mysql_fetch_row($res);
    $nivel = $fil[4];
    if($nivel>$niv){
        //header("location: no_autorizado.html");
        redirigir("no_autorizado.html");
    }
}
function session_started(){
  if(isset($_SESSION)){ return true; }else{ return false; }
}
function linea(){
    echo '<hr />';
}
function redirigir($url){
echo '<script type="text/javascript">
window.location = "' .$url.'";
</script>';
}
function btnConfirmarBorrar($url){
    echo '<input type=button value="Borrar" onClick="if(confirm('."'¿Desea borrar este registro?'".')) window.location='."'".$url."';".'">';
}
function btnConfirmar($boton,$texto,$url){
    echo '<input type=button value="'.$boton.'" onClick="if(confirm('."'$texto'".')) window.location='."'".$url."';".'">';
}
function fila_alterna($i){
    print ($i % 2) ? "<tr>" : "<tr class='odd'>";
    }
?>

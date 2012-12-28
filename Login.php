<?php
/* Programa: Login.php
 * Descripción: programa de registro de usuario sistema Geined*/
session_start();
include('funciones.php');
$sql = 'SELECT * FROM usuarios WHERE usuario="'.$_POST[fusername].'"';
$result = mysql_query($sql) or die('No pude ejecutar la consulta.');
$num = mysql_num_rows($result);
/* Si la clave es 'inhabilitado' salir del sistema */
if ($_POST['fpassword']=="inhabilitado"){
    redirigir("no_habilitado.html");
}
if ($num == 1) {
    $sql_usu = 'SELECT * FROM usuarios WHERE usuario ="'.$_POST['fusername'] . '" AND clave ="'.$_POST['fpassword'] . '"';
    $result2 = mysql_query($sql_usu) or die('No pude realizar la segunda búsqueda.');
    $num2 = mysql_num_rows($result2);
    if ($num2 > 0)  {
        $_SESSION['auth']='yes';
        $logname=$_POST['fusername'];
        $_SESSION['logname'] = $logname;
        $fil_usu = mysql_fetch_array($result2);
        $_SESSION['deposito_id']=$fil_usu['deposito_id'];
        if ($_POST["parametro"] != "no_registrar"){
            # Si NO viene de login PY Mandar a login.py con parametro=no_registrar
            echo "<form id='autolog' action='login.py' method='post'>";
            campo_oculto("fusuario",$_POST["fusername"]);
            campo_oculto("fclave",$_POST["fpassword"]);
            campo_oculto("parametro","registrar");
            campo_oculto("vienede","php");
            echo "</form>";
            echo "Procesando entrada (PHP), espere por favor...";
            echo "<script language='JavaScript' type='text/javascript'>\n";
            echo "<!--\n";
            echo "document.getElementById('autolog').submit();\n";
            echo "//-->\n";
            echo "</script>";
            #Inaceptable por motivos de seguridad:
            #redirigir('log.py?fusuario='.$_POST['fusername'].'&fclave='.$_POST['fpassword'].'&parametro=no_registrar');
        }
        else {
            #De lo contrario ir al menu principal
            redirigir("geined.py?accion=principal");
        }
    }
    else  {
        unset($do);
        $message='El usuario '. $_POST[fusername] . ' existe, pero la clave de acceso es incorrecta. Por favor intentelo nuevamente. <br>';
        encabezado_login("Entrada");
        echo "<h3>$message</h3>";
        formulario("Login.php");
        encabezado_tabla(array("Campo","Valor"));
        input_texto("Usuario:","fusername","");
        echo '<tr><td>Clave:</td><td><input type="password" name="fpassword"></td></tr>';
        fin_tabla();
        echo '<input type="hidden" name="parametro" value="registrar">';
        botones();
        fin_formulario();
        fin();
    }
}
elseif ($num == 0) {
    unset($do);
    $message = 'El nombre de usuario ingresado no existe. Por favor intentelo de nuevo.<br>';
    encabezado_login("Entrada");
    echo "<h3>$message</h3>";
    formulario("Login.php");
    encabezado_tabla(array("Campo","Valor"));
    input_texto("Usuario:","fusername","");
    echo '<tr><td>Clave:</td><td><input type="password" name="fpassword"></td></tr>';
    fin_tabla();
    echo '<input type="hidden" name="parametro" value="registrar">';
    botones();
    fin_formulario();
    fin();
}
?>

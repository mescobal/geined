<?php
/*! @file
    Programa LAMB para códigos de salud de BPS
*/
include('funciones.php');
include('datos.php');
function listado(){
    /*! Listado de códigos de seguro de salud
    @param ninguno
    @return Código HTML para listado de seguro de salud
    */
    encabezado('Listado de códigos del Seguro de Salud');
    boton("Nuevo","codss.php?accion=nuevo");
    boton('Volver','geined.py?accion=sistema');
    //cargar datos
    $sql='SELECT * FROM codigoss';
    $resultado = mysql_query($sql);
    $i=0;
    encabezado_tabla(array("Nº","Categoria","Acciones"));
    while($row = mysql_fetch_array($resultado)){
        fila_alterna($i);
        $id = $row['id'];
        celda($id);
        celda($row['codigo']);
        echo '<td>';
        boton("Detalles","codss.php?accion=ver&id=$id");
        boton("Editar","codss.php?accion=editar&id=$id");
        boton("Borrar","codss.php?accion=confirmar&id=$id");
        echo '</td>';
        $i = $i + 1;
    }
    fin_tabla();
    boton('Volver','geined.py?accion=sistema');
    fin();
}
function nuevo(){
    /*! Formulario para nuevo código de Seguro de Salud
    @param ninguno
    @return Código HTML 
    */
    autorizacion(2);
    encabezado('Nuevo código de Seguro de Salud');
    encabezado_tabla(array("Campo","Valor"));
    formulario("codss.php?accion=agregar");
    input_texto("Código:","codigo","");
    botones();
    fin_formulario();
    fin_tabla();
    boton('Volver','codss.php?accion=listado');
}
function agregar(){
    /*! Agrega registro a la base de datos codigoss
    @param $_POST
    @return redirige a listado 
    */
    $sql1 = 'SELECT * FROM codigoss WHERE codigo="'.$_POST['codigo'].'"';
    $res1 = mysql_query($sql1);
    if (mysql_num_rows($res1)==0){
        $sql = 'INSERT INTO codigoss SET codigo = "' . $_POST['codigo'].'"';
        $result = mysql_query($sql) or die('Consulta inválida: ' . mysql_error());
        redirigir("cem.php?accion=listado");
    }
    else {
        duplicado('codss.php?accion=listado');
    }
}
function editar(){
    /*! Edición de código de Seguro de Salud
    @param $_GET['id']
    @return Código HTML 
    */
    autorizacion(2);
    encabezado('Edición de Código de Seguro de Salud');
    encabezado_tabla(array("Campo","Valor"));
    formulario("codss.php?accion=actualizar");
    $sql='SELECT * FROM codigoss WHERE id="' . $_GET['id'].'"';
    //cargar datos
    $resultado = mysql_query($sql);
    $fila=mysql_fetch_array($resultado);
    campo_oculto("id",$_GET['id']);
    input_texto("Código:","codigo",$fila['codigo']);
    botones();
    fin_formulario();
    fin_tabla();
    boton('Volver','codss.php?accion=listado');
}
function actualizar(){
    /*! Actualiza registro de Código de Seguro de Salud
    @param $_POST
    @return SQL, redirige a Listado 
    */
    $id = $_POST['id'];
    $sql = 'UPDATE codigoss SET codigo= "' . $_POST['codigo'] . 
        '" WHERE id = "' . $_POST['id'] . '"';
    $result = mysql_query($sql) or die('Invalid query: ' . mysql_error());
    redirigir('codss.php?accion=listado');
}
function detalle(){
    /*! Listado de empleados por código de Seguro de Salud
    @param $_GET['id']
    @return Código HTML 
    */
    autorizacion(5);
    encabezado('Detalles de Código de Seguro de Salud');
    $sql1 = 'SELECT * FROM codigoss WHERE id = "' . $_GET['id'] . '"';
    $res1 = mysql_query($sql1);
    $fil1 = mysql_fetch_array($res1);
    // cli_ver
    echo '<h2>'.$fil1['codigo'].'</h2>';
    encabezado_tabla(array("Nombre","CI","Direccion","Telefono","eMail","Ingreso","Notas","Acciones"));
    $sql2 = 'SELECT * FROM empleados WHERE codigoss="'.$_GET['id'].'"';
    $res2 = mysql_query($sql2);
    $i = 0;
    while($fil2=mysql_fetch_array($res2)){
        fila_alterna($i);
        Celda($fil2['nombre']);
        Celda($fil2['ci']);
        Celda($fil2['direccion']);
        Celda($fil2['telefono']);
        Celda($fil2['email']);
        Celda($fil2['ingreso']);
        Celda($fil2['notas']);
        echo '<td>';
        boton("Detalles",'emp_ver.php?id='.$fil['id']);
        echo '</tr>';
        $i = $i + 1;
    }
    fin_tabla();
    boton('Volver','codss.php?accion=listado'); 
}
autorizacion(3);
if (!$_GET['accion']) $accion = 'listado';
else $accion=$_GET['accion'];
switch ($accion) {
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
    case 'confirmar':
        confirmar_borrar($_GET['id'],'cem.php');
        break;
    case 'eliminar':
        autorizacion(2);
        borrar('codigoss',$_POST['id'],'codss.php');
        break;
    case 'ver':
        detalle();
        break;
}
?>

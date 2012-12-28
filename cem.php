<?php
include('funciones.php');
include('datos.php');
function listado(){
    encabezado('Listado de categorías de empleados');
    boton("Nuevo","cem.php?accion=nuevo");
    boton('Volver','geined.py?accion=sistema');
    //cargar datos
    $sql='SELECT * FROM cat_empleados';
    $resultado = mysql_query($sql);
    $i=0;
    encabezado_tabla(array("Nº","Categoria","Acciones"));
    while($row = mysql_fetch_array($resultado)){
        fila_alterna($i);
        $id = $row['id'];
        celda($id);
        celda($row['categoria']);
        echo '<td>';
        boton("Detalles","cem.php?accion=ver&id=$id");
        boton("Editar","cem.php?accion=editar&id=$id");
        boton("Borrar","cem.php?accion=confirmar&id=$id");
        echo '</td>';
        $i = $i + 1;
    }
    fin_tabla();
    boton('Volver','geined.py?accion=sistema');
    fin();
}
function nuevo(){
    autorizacion(2);
    encabezado('Nueva categoría de empleado');
    encabezado_tabla(array("Campo","Valor"));
    formulario("cem.php?accion=agregar");
    input_texto("Categoria:","categoria","");
    botones();
    fin_formulario();
    fin_tabla();
    boton('Volver','cem.php?accion=listado');
}
function agregar(){
    $sql1 = 'SELECT * FROM cat_empleados WHERE categoria="'.$_POST['categoria'].'"';
    $res1 = mysql_query($sql1);
    if (mysql_num_rows($res1)==0){
        $sql = 'INSERT INTO cat_empleados SET categoria = "' . $_POST['categoria'].'"';
        $result = mysql_query($sql) or die('Consulta inválida: ' . mysql_error());
        header( 'Location: cem.php?accion=listado' ) ;
    }
    else {
        duplicado('cem.php?accion=listado');
    }
}
function editar(){
    autorizacion(2);
    encabezado('Edición de categoría de empleado');
    encabezado_tabla(array("Campo","Valor"));
    formulario("cem.php?accion=actualizar");
    $sql='SELECT * FROM cat_empleados WHERE id="' . $_GET['id'].'"';
    //cargar datos
    $resultado = mysql_query($sql);
    $fila=mysql_fetch_array($resultado);
    campo_oculto("id",$_GET['id']);
    input_texto("Categoría:","categoria",$fila['categoria']);
    botones();
    fin_formulario();
    fin_tabla();
    boton('Volver','cem.php?accion=listado');
}
function actualizar(){
    $id = $_POST['id'];
    $sql = 'UPDATE cat_empleados SET categoria= "' . $_POST['categoria'] . 
        '" WHERE id = "' . $_POST['id'] . '"';
    $result = mysql_query($sql) or die('Invalid query: ' . mysql_error());
    header( 'Location: cem.php?accion=listado' ) ;
}
function detalle(){
    autorizacion(5);
    encabezado('Detalles de categoría de empleado');
    $sql1 = 'SELECT * FROM cat_empleados WHERE id = "' . $_GET['id'] . '"';
    $res1 = mysql_query($sql1);
    $fil1 = mysql_fetch_array($res1);
    // cli_ver
    echo '<h2>'.$fil1['categoria'].'</h2>';
    encabezado_tabla(array("Nombre","CI","Direccion","Telefono","eMail","Ingreso","Notas","Acciones"));
    $sql2 = 'SELECT * FROM empleados WHERE categoria_id="'.$_GET['id'].'"';
    $res2 = mysql_query($sql2);
    if ($res2 != 0){
        for ($i=0;$i<mysql_num_rows($res2);$i++){
            $fil2 = mysql_fetch_array($res2);
            echo '<tr>';
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
        }
        fin_tabla();
    }
    boton('Volver','cem.php?accion=listado');   
}
autorizacion(10);
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
        borrar('cat_empleados',$_POST['id'],'cem.php');
        break;
    case 'ver':
        detalle();
        break;
}
?>

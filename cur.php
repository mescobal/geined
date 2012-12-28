<?php
include('funciones.php');
include('datos.php');
function listado(){
    encabezado('Cursos');
    encabezado_menu('Listado de cursos abiertos');
    echo '<table><tr><td>';
    boton("Nuevo",'cur.php?accion=nuevo');
    boton("Cursos finalizados","cur.php?accion=cerrados");
    boton("Volver","geined.py?accion=academico");
    echo '</td><td>';
    formulario('cur.php');
    echo '<input type="text" name="busqueda"><input type="submit" value="Buscar">';
    fin_formulario();
    echo '</td></tr></table>';
    nota('Notas: CERRAR CURSO: se elimina el curso, todos los alumnos de ese curso se eliminan y los clientes pasan a categoria "en espera"');
    nota('Notas: FINALIZAR CURSO: TODOS los alumnos de ese curso pasan a ser "Ex-Alumnos". Implica finalización normal de un curso');
    //cargar datos: no se cargan los cursos finalizados
    if ($_POST['busqueda']<>''){
        $sql='SELECT * FROM cursos WHERE curso LIKE "%' .$_POST['busqueda'] . '%" AND finalizado IS NULL ORDER BY curso';
    }
    else {
        $sql='SELECT * FROM cursos WHERE finalizado IS NULL  ORDER BY curso';
    }
    $resultado = mysql_query($sql);
    encabezado_tabla(array("Nº","Curso","Docente","Sucursal","Tipo","Acciones"));
    $i=0;
    while($row = mysql_fetch_array($resultado)){
        fila_alterna($i);
        celda($row['id']);
        celda($row['curso']);
        $fil2 = buscar_registro("empleados","id",$row['empleado_id']);
        celda($fil2['nombre']);
        $fil3 = buscar_registro("depositos","id",$row['deposito_id']);
        celda($fil3['deposito']);
        $fil4 = buscar_registro("tipo_curso","id",$row['tipo_id']);
        celda($fil4['tipo']);
        // Acomodar la opcion de borrar un curso para que de de baja a todos los alumnos
        echo '<td>';
        boton("Detalles",'cur_ver.py?id='.$row['id']);
        boton("Editar",'cur.php?accion=editar&id=' . $row['id']);
        boton("Cerrar",'cur.php?accion=confirmar&id='.$row['id']);
        boton("Finalizar",'cur.php?accion=finalizar&id=' . $row['id']);
        echo '</td></tr>';
        $i = $i + 1;
    }
    fin_tabla();
    boton("Volver","geined.py?accion=academico");
    fin();
}
function nuevo(){
    autorizacion(4);
    encabezado('Apertura de curso');
    Nota('La apertura de un curso genera un número único para cada curso. El nombre del curso puede escribirse manualmente o puede generarse automáticamente en un formato estándar: AA-BBBB-CCC-DD:DD donde AA es la sucursal, BBBB es el tipo de curso, CCC los días y DD:DD la hora de inicio.');
    encabezado_tabla(array("Campo","Valor"));
    formulario("cur.php?accion=agregar");
    // CURSOS
    // TIPO DE CURSO
    $sql2 = 'SELECT * FROM tipo_curso';
    $res2 = mysql_query($sql2);
    // DOCENTES
    $sql3 = 'SELECT * FROM empleados WHERE (categoria_id>=2) AND (categoria_id<=7)';
    $res3 = mysql_query($sql3);
    // DEPOSITO
    $sql4 = 'SELECT * FROM depositos';
    $res4 = mysql_query($sql4);
    // Curso
    input_texto('Nombre:','curso','');
    input_check("Generar nombre al guardar:","generar","1");
    input_combo("Docente:","empleado_id",$res3,"");
    input_combo("Sucursal:","deposito_id",$res4,"");
    input_combo("Tipo:","tipo_id",$res2,"");
    input_texto('Dias:','dias','');
    input_texto('Horas:','horas','');
    input_memo("Notas","notas","");
    fin_tabla();
    botones();
    fin_formulario();
    boton('Volver','cur.php?accion=listado');
}
function agregar(){
    $id = $_POST['id'];
    if ($_POST['generar']=='1'){
        // Generar nombre
        // Sucursal + Tipo + Dias + Horas
        $sql_coddep = 'SELECT * FROM depositos WHERE id="'.$_POST['deposito_id'].'"';
        $res_coddep = mysql_query($sql_coddep);
        $fil_coddep = mysql_fetch_row($res_coddep);
        $sql_codtip = 'SELECT * FROM tipo_curso WHERE id="'.$_POST['tipo_id'].'"';
        $res_codtip = mysql_query($sql_codtip);
        $fil_codtip = mysql_fetch_row($res_codtip);
        $nombre = $fil_coddep[2].'-' . $fil_codtip[2].'-'.$_POST['dias'].'-'.$_POST['horas'];
    }
    else {
        //$nombre = $_POST['curso'];
        $nombre = $_POST['curso'];
    }
    $sql2 = 'SELECT * FROM cursos WHERE curso = "' .$nombre . '" AND finalizado<>"1"';
    $res2 = mysql_query($sql2) or die('Error: ' . mysql_error());;
    if (mysql_num_rows($res2)==0) {
        $sql = 'INSERT INTO cursos SET curso = "' . $nombre .
        '", empleado_id="' . $_POST['empleado_id'] .
        '", deposito_id= "' . $_POST['deposito_id'] .
        '", tipo_id = "' . $_POST['tipo_id'] .
        '", dias = "' .$_POST['dias'] .
        '", horas = "' . $_POST['horas'] .
        '", notas = "' . $_POST['notas'].'"';
        $result = mysql_query($sql) or die('Invalid query: ' . mysql_error());
        header( 'Location: cur.php?accion=listado' ) ;
    }
    else {
        duplicado('cur.php?accion=listado');
    }
}
function editar(){
    autorizacion(5);
    encabezado('Edicion de cursos');
    echo '<TABLE><TR><TD>Curso Nº: ' . $_GET['id'].'</TD></TR></TABLE>';
    Nota('Puede generar automáticamente un nombre estándar a partir de los datos del curso
    Los cambios no se grabarán hasta que presione ACEPTAR');
    encabezado_tabla(array("Campo","Valor"));
    formulario("cur.php?accion=actualizar");
    // CURSOS
    $sql1='SELECT * FROM cursos WHERE id="' . $_GET['id'].'"';
    //cargar datos
    $res1 = mysql_query($sql1);
    $fil1= mysql_fetch_array($res1);
    // TIPO DE CURSO
    $sql2 = 'SELECT * FROM tipo_curso';
    $res2 = mysql_query($sql2);
    // DOCENTES
    $sql3 = 'SELECT * FROM empleados';
    $res3 = mysql_query($sql3);
    // DEPOSITO
    $sql4 = 'SELECT * FROM depositos';
    $res4 = mysql_query($sql4);
    // ID
    campo_oculto("id",$_GET['id']);
    input_texto("Nombre:","curso",$fil1['curso']);
    input_check("Generar nombre al guardar:","generar","1");
    input_combo("Docente:","empleado_id",$res3,$fil1['empleado_id']);
    input_combo("Sucursal:","deposito_id",$res4,$fil1['deposito_id']);
    input_combo("Tipo:","tipo_id",$res2,$fil1['tipo_id']);
    input_texto("Días:","dias",$fil1['dias']);
    input_texto("Horas:","horas",$fil1['horas']);
    input_memo("Notas","notas",$fil1['notas']);
    fin_tabla();
    botones();
    fin_formulario();
    boton('Volver','cur.php?accion=listado');
}
function actualizar(){
    $id = $_POST['id'];
    if ($_POST['generar']=='1'){
        // Generar nombre
        // Sucursal + Tipo + Dias + Horas
        $sql_coddep = 'SELECT * FROM depositos WHERE id="'.$_POST['deposito_id'].'"';
        $res_coddep = mysql_query($sql_coddep);
        $fil_coddep = mysql_fetch_row($res_coddep);
        $sql_codtip = 'SELECT * FROM tipo_curso WHERE id="'.$_POST['tipo_id'].'"';
        $res_codtip = mysql_query($sql_codtip);
        $fil_codtip = mysql_fetch_row($res_codtip);
        $nombre = $fil_coddep[2].'-' . $fil_codtip[2].'-'.$_POST['dias'].'-'.$_POST['horas'];
    }
    else {
        //$nombre = $_POST['curso'];
        $nombre = $_POST['curso'];
    }
    $sql = 'UPDATE cursos SET curso = "' . $nombre .
    '", empleado_id= "' . $_POST['empleado_id'] .
    '", deposito_id= "' . $_POST['deposito_id'] .
    '", tipo_id= "' . $_POST['tipo_id'] .
    '", dias= "' . $_POST['dias'] .
    '", horas= "' .$_POST['horas'] .
    '", notas = "' . $_POST['notas'] .
    '" WHERE id = "' . $_POST['id'] .
    '"';
    $result = mysql_query($sql) or die('Invalid query: ' . mysql_error());
    header( 'Location: cur.php?accion=listado' ) ;
}
function cerrados(){
    encabezado("Listado de cursos cerrados");
    boton("Volver","cur.php?accion=listado");
    $sql = "SELECT * FROM cursos WHERE finalizado=1";
    $res = mysql_query($sql);
    $i=0;
    encabezado_tabla(array("Nº","Curso","Docente","Tipo","Dias","Horario"));
    while($fil = mysql_fetch_array($res)){
        fila_alterna($i);
        $id = $fil['id'];
        celda($id);
        celda($fil['curso']);
        $fil_doc = buscar_registro("empleados","id",$fil['empleado_id']);
        celda($fil_doc['nombre']);
        $fil_tip = buscar_registro("tipo_curso","id",$fil['tipo_id']);
        celda($fil_tip['tipo']);
        celda($fil['dias']);
        celda($fil['horas']);
        echo '</td></tr>';
        $i=$i+1;
    }
    fin_tabla();
    boton("Volver","cur.php?accion=listado");
}
autorizacion(10);
if (!$_GET['accion']) $accion='listado';
else $accion=$_GET['accion'];
// DESGLOSE DE ACCIONES
switch ($accion){
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
        confirmar_borrar($_GET['id'],'cur.php');
        break;
    case 'cerrados':
        cerrados();
        break;
    case 'eliminar':
        autorizacion(3);
        borrar('cursos',$_POST['id'],'cur.php?accion=listado');
        $sql_alu = 'SELECT * FROM alumnos WHERE curso_id="'.$_POST['id'].'"';
        $res_alu = mysql_query($sql_alu);
        // Se ponen clientes en categoria "en espera"
        for($i=0;$i<mysql_num_rows($res_alu);$i++){
            $fil_alu = mysql_fetch_row($res_alu);
            $cliente_id = $fil_alu[1];
            $sql_cli = 'UPDATE clientes SET
                categoria_id=5
                WHERE id="'.$cliente_id.'"';
            $res_cli=mysql_query($sql_cli);
            }
        // Se elimina el alumno
        $sql_alu = 'DELETE FROM alumnos WHERE curso_id="'.$_POST['id'].'"';
        header('Location: cur.php?accion=listado');
        break;
    case 'finalizar':
        autorizacion(4);
        encabezado('Finalización de curso');
        nota('Este curso finaliza normalmente. Todos los alumnos de este curso pasan a categoría Ex-Alumno');
        $sql_cur = 'SELECT * FROM cursos WHERE id="'.$_GET['id'].'"';
        $res_cur = mysql_query($sql_cur);
        $fil_cur = mysql_fetch_row($res_cur);
        echo '<H2>'.$fil_cur[1].'</H2>';
        $sql_alu = 'SELECT * FROM alumnos WHERE curso_id="' .$_GET['id'].'"';
        $res_alu = mysql_query($sql_alu);
        echo '<H3>Alumnos:</H3>';
        for($i=0;$i<mysql_num_rows($res_alu);$i++){
            $fil_alu = mysql_fetch_row($res_alu);
            $sql_cli = 'SELECT * FROM clientes WHERE id="' . $fil_alu[1].'"';
            $res_cli = mysql_query($sql_cli);
            $fil_cli = mysql_fetch_row($res_cli);
            echo $fil_cli[1] . '<BR />';
        }
        echo '<FORM ACTION="cur.php?accion=finalizar2" METHOD="post">';
        echo '<INPUT TYPE="hidden" NAME="id" VALUE="'.$_GET['id'] .'">';
        echo '<TABLE>';
        botones();
        echo '</TABLE></FORM>';
        boton('Volver','cur.php?accion=listado');
        break;
    case 'finalizar2':
        // Se pone el flag FINALIZADO de cada alumno a 1
        $sql_alu='UPDATE  alumnos SET    finalizado="1"    WHERE curso_id="'.$_POST['id'].'"';
        // Se pone el flag FINALIZADO de el curso a 1
        $sql_cur='UPDATE cursos SET finalizado="1"    WHERE id="'.$_POST['id'].'"';
        $res_alu = mysql_query($sql_alu) or die('Error: ' . mysql_error());
        $res_cur = mysql_query($sql_cur) or die('Error: ' . mysql_error());
        // Se pone a los clientes como Ex-Alumnos
        $sql_alu = 'SELECT * FROM alumnos WHERE curso_id="' . $_POST['id'].'"';
        $res_alu = mysql_query($sql_alu);
        if(mysql_num_rows($res_alu)!=0){
            for ($i = 0; $i <mysql_num_rows($res_alu); $i++){
                $fil_alu=mysql_fetch_row($res_alu);
                $cliente_id = $fil_alu[1];
                $sql_cli = 'UPDATE clientes SET categoria_id=4 WHERE id="'.$cliente_id.'"';
                $res_cli = mysql_query($sql_cli) or die('Error: ' .mysql_error());
            }
        }
        redirigir('cur.php?accion=listado');
        break;
}
?>

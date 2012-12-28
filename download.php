<?php
include('funciones.php');
autorizacion(5);
encabezado("Bajar archivos");
boton("Volver","geined.py?accion=sistema");
if ($handle = opendir('./uploads')) {
  /* This is the correct way to loop over the directory. */
    encabezado_tabla(array("Archivo","Accion"));
  while (false !== ($file = readdir($handle))) {
        if($file!='.' and $file!='..'){
            echo '<tr>';
            echo "<td>$file</td>";
            echo '<td>';
            boton("Descargar","./uploads/$file");
            echo '</td>';
            echo '</tr>';
            }
    }
  closedir($handle);
}
fin_tabla();
boton("Volver","geined.py?accion=sistema");
?>

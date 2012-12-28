<?php
function encabezado_ajax($titulo,$funcion){
    inicio();
    echo "<title>$titulo</title>";
    estilo();
    echo '<script type="text/javascript" src="geined.js" charset="utf-8"></script>';
    echo '</head><body onload="'.$funcion.'">';
    echo "<h1>$titulo</h1>";
}
function boton_ajax($texto,$url,$target){
    echo '<input type = "button" value = "'
    .$texto.'" onclick = "getData('."'"
    .$url."'".', '."'"
    .$target."'".');"></input>';
}
function titulo_ajax($titulo,$blanco_cierre){
    echo '<span style="float: left; text-align: left"><h4>'.$titulo.'</h4></span>';
    echo '<span style="float: right;text-align: right"><input type="button" onclick=ocultar('."'".$blanco_cierre."'".') value="x"></button></span>';
    echo '<div style="clear: both;"></div>';
}
function form_ajax($id,$target){
    echo '<form id="'.$id.'" method="post" onsubmit= "ocultar('."'".$target."'".');" >';
}
function ajax_submit_button($id,$url,$contenedor){
    echo '<input type="button" value="Enviar" onclick="
        submitform(document.getElementById('."'".$id."'".'),'
        ."'".$url."'".','
        ."'".$cadena."'".'); 
        ocultar('."'".$contenedor."'".'); 
        window.location.reload();
        return false;" />';
    //getData('."'".$otro."','".$blanco."'".'); 
}
?>

<?php
//start the session
session_start();
//check to make sure the session variable is registered
session_unset();
session_destroy();
header( "Location: Salida.html" );
?> 

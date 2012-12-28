<?php
include('./conf/log.inc');
session_start();
if ($_SESSION['auth']!='yes') {
	header('Location: Login.php');
	}
$sql = 'SELECT * FROM usuarios WHERE usuario="' . $_SESSION['logname'] . '"';
$res = mysql_query($sql);
if ($res==0){
	Header('Location: no_autorizado.html');
	}
$fil = mysql_fetch_row($res);
$nivel = $fil[4];
?>

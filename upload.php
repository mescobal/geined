<?
include('funciones.php');
autorizacion(5);
error_reporting(7);
/*
//================================================================================
* phphq.Net Custom PHP Scripts *
//================================================================================
:- Script Name: phUploader
:- Version: 1.2
:- Release Date: June 23rd  2004
:- Last Updated: Dec 10th 2005
:- Author: Scott L. <scott@phphq.net> http://www.phphq.net
:- Copyright (c) 2005 All Rights Reserved
:-
:- This script is free software; you can redistribute it and/or modify
:- it under the terms of the GNU General Public License as published by
:- the Free Software Foundation; either version 2 of the License, or
:- (at your option) any later version.
:-
:- This script is distributed in the hope that it will be useful,
:- but WITHOUT ANY WARRANTY; without even the implied warranty of
:- MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
:- GNU General Public License for more details.
:-http://www.gnu.org/licenses/gpl.txt
:-
//================================================================================
* Description
//================================================================================
:- phUploader is a script for uploading single or multiple images or files to your webiste. You can specify your own file extensions 
:- that are accepted, the file size and naming options.  This was tested with Linux and WindowsXP (EasyPHP) / Windows Server 2003 (IIS6).
:- This script is very useful for temporary file storage or simple sig and avatar hosting.
//================================================================================
* Setup
//================================================================================
:- To setup this script, upload phUploader.php to a folder on your server. Create a new folder named uploads and chmod it to 777.
:- Edit the variables below to change how the script acts. Please read the notes of you don't understand something.
:- Due to many problems with permissions this script will not longer automatically create folders for you, sorry.
//================================================================================
* Frequently Asked Questions
//================================================================================
:- Q1: I always get an error that the files were not uploaded
:-		A1: Make sure you have CHMOD your uploads folder to 777 using your FTP client or similar. If you do not know how to do this ask your host, I am 100% sure they know how, or else you should find another one.
:-		A2: Make sure the uploads folder exists. This is the second most common mistake aside from CHMOD. The folder has to exists so the files have somewhere to go!
:-		A3: If you are having problems uploading after you have chmod the uploads folder 777, try using the full server path in $fullpath below. If you do not know this ask your host.
:-
:- Q2: The page takes forever to load and then times out bringing me to a page cannot be displayed! Stupid script!
:-		A1: This is usually due to a low value in php.ini for max_execution_time. Ask your host to increase the value. Be aware that the time needed depends on the size the file(s) users are upload and the speed of THERE internet connection for uploading the files. If they are on 56k uploading 1mb will take forever, so the value may need to be set very high!
:-		A2: You really can have as many uploads as you want. I tested up to 12 uploads on Windows 2003 Server / XP & Red Hat 9/ Enterprise Linux 3/4. Several reasons could cause this. Your mail server could be rejecting that many at one time, your post_max_size, upload_max_filesize, file_uploads, max_execution_time in php.ini might be set to low or off. Contact your host to resolve this.
:-
:- Q3: How do I edit the colors of the form?
:-		A1: Due to many requests I used CSS instead of hard coding it into the php. I also made it easier to understand. The only bad part is if you are extremely novice you may have problems editing the CSS. Check http://www.w3schools.com/css/default.asp to brush up on CSS to change the colors of this script. The CSS is located near the end of this script.
:-
:- Q4: Can I remove your copyright?
:-		A1: I can't really physically stop you. But it's much appreciated by the people that leave it on there. Some people donate me $15-$20 to take it off. If you donate a small amount to me I might just not care as much.
:-		A2: When I go to your site and see this script no matter how much you tried to edit it to hide the fact, I usually know it's mine and will usually report it to your host if I'm not to busy. ~35 down and counting!
:-		A3: So basically unless I say it's ok just leave it on there.. It doesn't hurt you at all does it? Does that little bit of text just make your balls itch? If it's that bad then go ahead...
:-
:- Q5: You never respond to my emails or in your forums (http://www.phphq.net/forums/)!
:-		A1: I know and I'm sorry. I'm a very busy guy. I'm out of town a lot, and at any given time I have several projects going on. I get a lot of emails about this script, not to mention my other ones. Sometimes I just get too many of the same emails.. I usually clear out my inbox every week on a non specific day.
:-		A2: I only understand English. If you do know English but it's very bad please write in your native language and then translate it to English using http://babelfish.altavista.com/babelfish/tr
:-		A3: You will get a much faster and much more detailed response if you write a decent message. "dude me form don't work see it at blah.com what's wrong??!?!" will get no response, ever. Write in detail what the problem is and what you did to try and fix it. Spend a minute on it, and I'll take some of my time to reply.
:-		A4: Please don't speak in h4x0r language. I do understand it but it's very annoying to me. I will most likely just chuckle and delete it.
:-
/*
//================================================================================
* ! ATTENTION !
//================================================================================
:- Please read the above FAQ before giving up or emailing me. It may sort out your problems!
*/

// Max size PER file in KB, not bytes for simplicity!
$max_file_size="10000";

// Max size for all files COMBINED in KB, not bytes for simplicity!
$max_combined_size="10000";

//How many file uploads do you want to allow at a time?
$file_uploads="2";

//The name of the uploader..
$websitename="Subida de archivos";

// Use random file names? true=yes (recommended), false=use original file name. Random names will help prevent overwritting of existing files!
$random_name=false;

// Please keep the array structure.
$allow_types=array("jpg","gif","png","zip","rar","txt","doc","pdf");

// Path to files folder. If this fails use $fullpath below. With trailing slash
$folder="./uploads/";

// Full url to where files are stored. With Trailing Slash
$full_url="http://alicarrasco.homelinux.net/geined/uploads/";

// Only use this variable if you wish to use full server paths. Otherwise leave this empty! With trailing slash
$fullpath="";

//Use this only if you want to password protect your uploads.
$password=""; 

/*
//================================================================================
* ! ATTENTION !
//================================================================================
: Don't edit below this line unless you know some php. Editing some variables or other stuff could cause undeseriable results!!
*/

// MD5 the password.. why not?
$password_md5=md5($password);

// If you set a password this is how they get verified!
If($password) {
	If($_POST['verify_password']==true) {
		If(md5($_POST['check_password'])==$password_md5) {
			setcookie("phUploader",$password_md5,time()+86400);
			sleep(1); //seems to help some people.
			header("Location: http://".$_SERVER['HTTP_HOST'].$_SERVER['PHP_SELF']);
			exit;
			
		}
	}
}

// The password form, if you set a password and the user has not entered it this will show.
$password_form="";
If($password) {
	If($_COOKIE['phUploader']!=$password_md5) {
		$password_form="<form method=\"POST\" action=\"".$_SERVER['PHP_SELF']."\">\n";
		$password_form.="<table align=\"center\" class=\"table\">\n";
		$password_form.="<tr>\n";
		$password_form.="<td width=\"100%\" class=\"table_header\" colspan=\"2\">Password Required</td>\n";
		$password_form.="</tr>\n";
		$password_form.="<tr>\n";
		$password_form.="<td width=\"35%\" class=\"table_body\">Enter Password:</td>\n";
		$password_form.="<td width=\"65%\" class=\"table_body\"><input type=\"password\" name=\"check_password\" /></td>\n";
		$password_form.="</tr>\n";
		$password_form.="<td colspan=\"2\" align=\"center\" class=\"table_body\">\n";
		$password_form.="<input type=\"hidden\" name=\"verify_password\" value=\"true\">\n";
		$password_form.="<input type=\"submit\" value=\" Verify Password \" />\n";
		$password_form.="</td>\n";
		$password_form.="</tr>\n";
		$password_form.="</table>\n";
		$password_form.="</form>\n";
	}
}

// Function to get the extension a file.
function get_ext($key) { 
	$key=strtolower(substr(strrchr($key, "."), 1));
	// Cause there the same right?
	$key=str_replace("jpeg","jpg",$key);
	return $key;
}

$ext_count=count($allow_types);
$i=0;
foreach($allow_types AS $extension) {
	
	//Gets rid of the last comma for display purpose..
	
	If($i <= $ext_count-2) {
		$types .="*.".$extension.", ";
	} Else {
		$types .="*.".$extension;
	}
	$i++;
}
unset($i,$ext_count); // why not

$error="";
$display_message="";
$uploaded==false;

// Dont allow post if $password_form has been populated
If($_POST['submit']==true AND !$password_form) {

	For($i=0; $i <= $file_uploads-1; $i++) {
					
		If($_FILES['file']['name'][$i]) {
						
			$ext=get_ext($_FILES['file']['name'][$i]);
			$size=$_FILES['file']['size'][$i];
			$max_bytes=$max_file_size*1024;
			
			// For random names
			If($random_name){
				$file_name[$i]=time()+rand(0,100000).".".$ext;
			} Else {
				$file_name[$i]=$_FILES['file']['name'][$i];
			}
			
			//Check if the file type uploaded is a valid file type. 
						
			if(!in_array($ext, $allow_types)) {
							
				$error.= "ExtensiÛn inv·lida para su archivo: ".$_FILES['file']['name'][$i].", solo se permite ".$types." .<br />Su(s) archivo(s) <b>no</b> fue(ron) subido(s).<br />";
							
				//Check the size of each file
							
			} Elseif($size > $max_bytes) {
				
				$error.= "Su archivo: ".$_FILES['file']['name'][$i]." es demasiado grande. El tamaÒo m·ximo permitido es ".$max_file_size."kb.<br />Su(s) archivo(s) <b>no</b> fue(ron) subido(s).<br />";
				
				// Check if the file already exists on the server..
			} Elseif(file_exists($folder.$file_name[$i])) {
				
				$error.= "El archivo: ".$_FILES['file']['name'][$i]." existe en este servidor, por favor renombre su archivo.<br />Su(s) archivo(s) <b>no</b> fue(ron) subido(s).<br />";
				
			}
						
		} // If Files
	
	} // For
	
	//Tally the size of all the files uploaded, check if it's over the ammount.
				
	$total_size=array_sum($_FILES['file']['size']);
	  			
	$max_combined_bytes=$max_combined_size*1024;
				
	If($total_size > $max_combined_bytes) {
		$error.="El tamaÒo m·ximo combinado de los arcvhivos es de ".$max_combined_size."kb<br />";
	}
		
	
	// If there was an error take notes here!
	
	if($error) {
		
		$display_message=$error;
		
	} else {
		
		// No errors so lets do some uploading!
		
		for($i=0; $i <= $file_uploads-1; $i++) {
				
			If($_FILES['file']['name'][$i]) {
				
				If(@move_uploaded_file($_FILES['file']['tmp_name'][$i],$folder.$file_name[$i])) {
					$uploaded=true;
				} Else {
					$display_message.="No pude copiar ".$file_name[$i]." al servidor, por favor, aseg˙rese de que ".$folder." tenga permisos adecuados (777) y que la ruta sea correcta.\n";
				}
			}
				
		} //For
		
	} // Else
	
} // $_POST AND !$password_form

/*
//================================================================================
* Start the form layout
//================================================================================
:- Please know what your doing before editing below. Sorry for the stop and start php.. people requested that I use only html for the form..
*/
?>


<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="es" lang="es">
<head>
<meta http-equiv="Content-Language" content="es-es" />
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title><?php echo $websitename; ?> - rutinas: tomadas de phUploader</title>

<style type="text/css">
	body{
		background-color:#FFFFFF;
		font-family: Verdana, Arial, sans-serif;
		font-size: 12pt;
		color: #000000;
	}
	
	.error_message{
		font-family: Verdana, Arial, sans-serif;
		font-size: 11pt;
		color: #FF0000;
	}
	
	.uploaded_message{
		font-family: Verdana, Arial, sans-serif;
		font-size: 11pt;
		color: #000000;
	}
	
	a:link{
		text-decoration:none;
		color: #000000;
	}
	a:visited{
		text-decoration:none;
		color: #000000;
	}
	a:hover{
		text-decoration:none;
		color: #000000;
	}
	
	
	.table {
		border-collapse:collapse;
		border:1px solid #000000;
		width:450px;
	}
	
	.table_header{
		border:1px solid #070707;
		background-color:#C03738;
		font-family: Verdana, Arial, sans-serif;
		font-size: 11pt;
		font-weight:bold;
		color: #FFFFFF;
		text-align:center;
		padding:2px;
	}
	
	.upload_info{
		border:1px solid #070707;
		background-color:#EBEBEB;
		font-family: Verdana, Arial, sans-serif;
		font-size: 8pt;
		color: #000000;
		padding:4px;
	}
	
	
	.table_body{
		border:1px solid #070707;
		background-color:#EBEBEB;
		font-family: Verdana, Arial, sans-serif;
		font-size: 10pt;
		color: #000000;
		padding:2px;
	}
	
	
	.table_footer{
		border:1px solid #070707;
		background-color:#C03738;
		text-align:center;
		padding:2px;
	}
	
	
	input,select,textarea {
		font-family: Verdana, Arial, sans-serif;
		font-size: 10pt;
		color: #000000;
		background-color:#AFAEAE;
		border:1px solid #000000;
	}
	
	.copyright {
		border:0px;
		font-family: Verdana, Arial, sans-serif;
		font-size: 9pt;
		color: #000000;
		text-align:right;
	}
	
	form{
		padding:0px;
		margin:0px;
	}
</style>

<?
If($password_form) {
	
	Echo $password_form;
	
} Elseif($uploaded==true) {?>

<table align="center"class="table">

	<tr>
		<td class="table_header" colspan="2"><b>Sus archivo(s) fueron subidos!</b> </td>
	</tr>
	<tr>
	<td class="table_body">
	<br />
<?
For($i=0; $i <= $file_uploads-1; $i++) {
	
	If($_FILES['file']['name'][$i]) {
		$file=$i+1;
		
				Echo("<b>File #".$file.":</b> <a href=\"".$full_url.$file_name[$i]."\" target=\"_blank\">".$full_url.$file_name[$i]."</a><br /><br />\n");
	}
				
}

?>
<br />
<a href="<?=$_SERVER['PHP_SELF'];?>">Go Back</a>
<br />
</td>
</tr>
</table>

<?} Else {?>

<?If($display_message){?>
	<div align="center" class="error_message"><?=$display_message;?></div>
	<br />
<?}?>

<form action="<?=$_SERVER['PHP_SELF'];?>" method="post" enctype="multipart/form-data" name="phuploader">
<table align="center"class="table">

	<tr>
		<td class="table_header" colspan="2"><b><?=$websitename;?></b> </td>
	</tr>
	<tr>
		<td colspan="2" class="upload_info">
			<b>Tipos permitidos:</b> <?=$types?><br />
			<b>Tama√±o m√°ximo por archivo:</b> <?=$max_file_size?>kb.<br />
			<b>Tama√±o√± m√°ximo combinado:</b> <?=$max_combined_size?>kb.<br />
		</td>
	</tr>
	<?For($i=0;$i <= $file_uploads-1;$i++) {?>
		<tr>
			<td class="table_body" width="20%"><b>Seleccion archivo:</b> </td>
			<td class="table_body" width="80%"><input type="file" name="file[]" size="30" /></td>
		</tr>
	<?}?>
	<tr>
		<td colspan="2" align="center" class="table_footer">
			<input type="hidden" name="submit" value="true" />
			<input type="submit" value=" Subir archivo(s) " /> &nbsp;
			<input type="reset" name="reset" value=" Limpiar formulario" />
		</td>
	</tr>
</table>
</form>

<?}//Please leave this here.. it really dosen't make people hate you or make your site look bad.. ?>
<table class="table" style="border:0px;" align="center">
	<tr>
		<td><div class="copyright">&copy;<a href="http://www.phphq.net?script=phUploader" target="_blank" title="Uploader Powered By phUploader &lt;www.phphq.net&gt;">phUploader</a></div></td>
	</tr>
</table>
</body>
</html>

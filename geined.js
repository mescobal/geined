xmlhttp = new XMLHttpRequest();
function getData(dataSource, divID){
    var obj = document.getElementById(divID);
    xmlhttp.open("GET", dataSource);
    xmlhttp.onreadystatechange = function() {
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
            obj.innerHTML = xmlhttp.responseText;
        }
    }
    xmlhttp.send(null);
}
function ocultar(divID){
    document.getElementById(divID).innerHTML="";
}
function enviarform (formulario){
  serverPage = "validator.php?sstring=" + thevalue;
  objID = "messagebox";
  var obj = document.getElementById(objID);
  xmlhttp.open("GET", serverPage);
  xmlhttp.onreadystatechange = function() {
    if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
      obj.innerHTML = xmlhttp.responseText;
    }
  }
  xmlhttp.send(null);
}
//Functions to submit a form.
function getformvalues (fobj, valfunc){
    var str = "";
    aok = true;
    var val;
    //Run through a list of all objects contained within the form.
    for(var i = 0; i < fobj.elements.length; i++){
        if(valfunc) {
            if (aok == true){
                val = valfunc (fobj.elements[i].value,fobj.elements[i].name);
                if (val == false){
                    aok = false;
                }
            }
        }
        str += fobj.elements[i].name + "=" + escape(fobj.elements[i].value) + "&";
    }
    //Then return the string values.
    return str;
}
function submitform (theform, serverPage, objID, valfunc){
    var file = serverPage;
    var str = getformvalues(theform,valfunc);
    //If the validation is ok.
    if (aok == true){
        obj = document.getElementById(objID);
        processajax (serverPage, obj, "post", str);
    }
}
function processajax (serverPage, obj, getOrPost, str){
    //Get an XMLHttpRequest object for use.
    xmlhttp = getxmlhttp ();
    if (getOrPost == "get"){
        xmlhttp.open("GET", serverPage);
        xmlhttp.onreadystatechange = function() {
            if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
                obj.innerHTML = xmlhttp.responseText;
            }
        }
        xmlhttp.send(null);
    }
    else {
        xmlhttp.open("POST", serverPage, true);
        xmlhttp.setRequestHeader("Content-Type","application/x-www-form-urlencoded; charset=UTF-8");
        xmlhttp.onreadystatechange = function() {
            if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
                obj.innerHTML = xmlhttp.responseText;
            }
        }
        xmlhttp.send(str);
    }
}
//Function to create an XMLHttp Object.
function getxmlhttp (){
    //Create a boolean variable to check for a valid Microsoft active x instance.
    var xmlhttp = false;
    //Check if we are using internet explorer.
    try {
        //If the javascript version is greater than 5.
        xmlhttp = new ActiveXObject("Msxml2.XMLHTTP");
    } catch (e) {
        //If not, then use the older active x object.
        try {
            //If we are using internet explorer.
            xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
        } catch (E) {
            //Else we must be using a non-internet explorer browser.
            xmlhttp = false;
        }
    }
    // If not using IE, create a
    // JavaScript instance of the object.
    if (!xmlhttp && typeof XMLHttpRequest != 'undefined') {
        xmlhttp = new XMLHttpRequest();
    }
    return xmlhttp;
}
function recalcular(campo,texto){
    if(verificarNumero(document.getElementById(campo))){
        calcular();
    }
else {
        alert("Verificar que se ingresen solo numeros");
    }
}
function calcular(){
    var ef=0; var ch=0; var vo=0; var ot=0;var total=0;
    ef = parseFloat(document.getElementById("ef").value);
    ch = parseFloat(document.getElementById("ch").value);
    vo = parseFloat(document.getElementById("vo").value);
    ot = parseFloat(document.getElementById("ot").value);
    pago = ef + ch + vo + ot;
    total = parseFloat(document.getElementById("to").value);
    vuelto = pago-total;
    if (vuelto<0){
        vuelto=0;
        document.getElementById("boton").innerHTML = "";
    } else {
        ht = "<input type=\"submit\" value=\"Guardar\" />"
        document.getElementById("boton").innerHTML = ht;
    }
    if (typeof vuelto != "number"){
        document.getElementById("boton").innerHTML = "";
        alert("No se permiten letras, solo numeros");
    }
    document.getElementById("vu").value = vuelto;
}
function verificarNumero(cadena){
    /*devuelve verdadero si está dentro de los caracteres permitidos */
    var caracteresPermitidos ="0123456789.,-";
    if(!cadena){
        alert("No es una cadena");
        return false;
    } else {
        var str = cadena.value;
    }
    for(index=0;index<str.length;index++){
        myChar = str.charAt(index);
        if(caracteresPermitidos.indexOf(myChar)==-1){
            return false;
        }
        return true;
    }
}

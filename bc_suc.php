<?php
include("funciones.php");
include("datos.php");
autorizacion(3);
if(!$_POST['ano']){
    $ano = 2003;
} else {
    $ano = $_POST['ano'];
}
encabezado_informe("Comparación de rentabilidad entre sucursales: $ano");
formulario("bc_suc.php");
echo "<table><tr><td>Filtrar por año:</td>
    <td><select name='ano'>
        <option label='2003' value='2003'>2003</option>
        <option label='2004' value='2004'>2004</option>
        <option label='2005' value='2005'>2005</option>
        <option label='2006' value='2006'>2006</option>
        <option label='2007' value='2007'>2007</option>
        <option label='2008' value='2008'>2008</option>
        </select></td>
    <td><input type='submit' value='Ir' /></td><td>";
    boton("Volver","geined.py?accion=financiero");
    echo "</tr></table>";
fin_formulario();
echo "<h2>Ingresos</h2>";
encabezado_tabla(array("Rubro","Costa","Carrasco"));
    echo "<tr>";
        celda("Cursos 3 hs");
        $cos1 = suma_cons("411011",$ano);
        $car1 = suma_cons("411012",$ano);
        linea_moneda($cos1);
        linea_moneda($car1);
        $tot_cos = $tot_cos + $cos1;
        $tot_car = $tot_car + $car1;
    echo "</tr>";
    echo "<tr>";
        celda("Cursos 4 hs");
        $cos1 = suma_cons("411013",$ano);
        $car1 = suma_cons("411014",$ano);
        linea_moneda($cos1);
        linea_moneda($car1);
        $tot_cos = $tot_cos + $cos1;
        $tot_car = $tot_car + $car1;
    echo "</tr>";
    echo "<tr>";
        celda("Cursos 6 hs");
        $cos1 = suma_cons("411015",$ano);
        $car1 = suma_cons("411016",$ano);
        linea_moneda($cos1);
        linea_moneda($car1);
        $tot_cos = $tot_cos + $cos1;
        $tot_car = $tot_car + $car1;
    echo "</tr>";
    echo "<tfoot><tr><td>Total</td><td>".moneda($tot_cos)."</td><td>".moneda($tot_car)."</td></tr></tfoot>";
fin_tabla();
$ing_cos = $tot_cos;
$ing_car = $tot_car;
$tot_cos = 0;
$tot_car = 0;
echo "<h2>Egresos</h2>";
encabezado_tabla(array("Rubro","Costa","Carrasco"));
    echo "<tr>";
        celda("Telefonos:");
        $cos1 = suma_cons("517001",$ano);
        $car1 = suma_cons("517002",$ano);
        linea_moneda($cos1);
        linea_moneda($car1);
        $tot_cos = $tot_cos + $cos1;
        $tot_car = $tot_car + $car1;
    echo "</tr>";
    echo "<tr>";
        celda("Electricidad:");
        $cos1 = suma_cons("518001",$ano);
        $car1 = suma_cons("518002",$ano);
        linea_moneda($cos1);
        linea_moneda($car1);
        $tot_cos = $tot_cos + $cos1;
        $tot_car = $tot_car + $car1;
    echo "</tr>";
    echo "<tr>";
        celda("Calefacción:");
        $cos1 = suma_cons("518003",$ano);
        $car1 = suma_cons("518004",$ano);
        linea_moneda($cos1);
        linea_moneda($car1);
        $tot_cos = $tot_cos + $cos1;
        $tot_car = $tot_car + $car1;
    echo "</tr>";
    echo "<tr>";
        celda("Arrendamientos:");
        $cos1 = suma_cons("518005",$ano);
        $car1 = suma_cons("518006",$ano);
        linea_moneda($cos1);
        // Para carrasco es un 5% de los ingresos
        $car1 = -$ing_cos * 0.05;
        linea_moneda($car1);
        $tot_cos = $tot_cos + $cos1;
        $tot_car = $tot_car + $car1;
    echo "</tr>";
    echo "<tr>";
        celda("Reparaciones y service:");
        $cos1 = suma_cons("518007",$ano);
        $car1 = suma_cons("518008",$ano);
        linea_moneda($cos1);
        linea_moneda($car1);
        $tot_cos = $tot_cos + $cos1;
        $tot_car = $tot_car + $car1;
    echo "</tr>";
    echo "<tr>";
        celda("Mantenimiento:");
        $cos1 = suma_cons("518009",$ano);
        $car1 = suma_cons("518010",$ano);
        linea_moneda($cos1);
        linea_moneda($car1);
        $tot_cos = $tot_cos + $cos1;
        $tot_car = $tot_car + $car1;
    echo "</tr>";
    echo "<tr>";
        celda("Papelería:");
        $cos1 = suma_cons("517003",$ano);
        $car1 = suma_cons("517004",$ano);
        linea_moneda($cos1);
        linea_moneda($car1);
        $tot_cos = $tot_cos + $cos1;
        $tot_car = $tot_car + $car1;
    echo "</tr>";
    echo "<tr>";
        celda("Insumos comp.:");
        $cos1 = suma_cons("517005",$ano);
        $car1 = suma_cons("517006",$ano);
        linea_moneda($cos1);
        linea_moneda($car1);
        $tot_cos = $tot_cos + $cos1;
        $tot_car = $tot_car + $car1;
    echo "</tr>";
    echo "<tr>";
        celda("Fotocopias:");
        $cos1 = suma_cons("517016",$ano);
        $car1 = suma_cons("517017",$ano);
        linea_moneda($cos1);
        linea_moneda($car1);
        $tot_cos = $tot_cos + $cos1;
        $tot_car = $tot_car + $car1;
    echo "</tr>";
    echo "<tr>";
        celda("Quebrantos de caja:");
        $cos1 = suma_cons("517021",$ano);
        $car1 = suma_cons("517022",$ano);
        linea_moneda($cos1);
        linea_moneda($car1);
        $tot_cos = $tot_cos + $cos1;
        $tot_car = $tot_car + $car1;
    echo "</tr>";
    echo "<tfoot><tr><td>Total</td><td>".moneda($tot_cos)."</td><td>".moneda($tot_car)."</td></tr></tfoot>";
fin_tabla();
$eg_cos = $tot_cos;
$eg_car = $tot_car;
$dif_cos = moneda($ing_cos + $eg_cos);
$dif_car = moneda($ing_car + $eg_car);
echo "<table><thead><tr><th></th><th>Costa</th><th>Carrasco</th></tr></thead>
    <tr><td><h2>Saldos:</h2></td>
    <td><h2>$dif_cos</h2></td><td><h2>$dif_car</h2></td></tr></table>";
boton("Volver","geined.py?accion=financiero");
fin();
?>

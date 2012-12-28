<?php
function porcentaje_irpf($franja,$emni){
    if($emni!=0){
        switch($franja){
        case '1':
            $porcentaje = 10;
            break;
        case '2':
            $porcentaje = 15;
            break;
        case '3':
            $porcentaje = 20;
            break;
        case '4':
            $porcentaje = 22;
            break;
        }
    } else {
        switch($franja){
        case '1':
            $porcentaje = 0;
            break;
        case '2':
            $porcentaje=10;
            break;
        case '3':
            $porcentaje = 15;
            break;
        case '4':
            $porcentaje = 20;
            break;
        }
    }
    return $porcentaje;
}
function irpf1($mg,$bcp,$emni){
    /* IMPORTANTE: Cambios del 1/10/08 por cambio de topes */
    /*! Primer nivel de escala del IRPF */
    $escala_1 = $bcp * 7;
    $porcentaje = porcentaje_irpf(1,$emni);
    /* Monto gravado */
    if ($mg > $escala_1){
        $mg_irpf = $escala_1;
    } else {
        $mg_irpf = $mg;
    }
    return $mg_irpf * $porcentaje / 100;
}
function irpf2($mg,$bcp,$emni){
    /*! Segundo nivel de escala de IRPF */
    $escala_1 = $bcp * 7;
    $escala_2 = $bcp *10;
    $porcentaje = porcentaje_irpf(2,$emni);
    /* Monto gravado */
    if ($mg > $escala_2){
        $mg_irpf = $escala_2 - $escala_1;
    } else {
        if($mg <= $escala_1){
            $mg_irpf=0;
        } else {
            $mg_irpf = $mg - $escala_1;
        }
    }
    return $mg_irpf * $porcentaje /100;
}
function irpf3($mg,$bcp,$emni){
    /* Tercer nivel de escala de IRPF */
    $escala_2 = $bcp *10;
    $escala_3 = $bcp * 15;
    $porcentaje = porcentaje_irpf(3,$emni);
    /* Monto gravado */
    if($mg > $escala_3){
        $mg_irpf = $escala_3 - $escala_2;
    } else {
        if ($mg <= $escala_2){
            $mg_irpf = 0;
        } else {
            $mg_irpf = $mg - $escala_2;
        }
    }
    return $mg_irpf * $porcentaje / 100;
}
function irpf4($mg,$bcp,$emni){
    /* Cuarto nivel de escala de IRPF */
    $escala_3 = $bcp * 15;
    $escala_4 = $bcp * 20;
    $porcentaje = porcentaje_irpf(4,$emni);
    /* Monto gravado */
    if($mg > $escala_4){
        $mg_irpf = $escala_4 - $escala_3;
    } else {
        if($mg <= $escala_3){
            $mg_irpf = 0;
        } else {
            $mg_irpf = $mg - $escala_3;
        }
    }
    return $mg_irpf * $porcentaje / 100;
}
function deducible1($monto,$bcp){
    /* IMPORTANTE: cambios en el 1/10/08 por cambio del decreto */
    $escala_1 = $bcp * 3;
    If ($monto <= $escala_1) return $monto;
    Else return $escala_1;
}
function deducible2($monto,$bcp){
    $escala_1 = $bcp * 3;
    $escala_2 = $bcp * 8;
    If ($monto<= $escala_1) return 0;
    Else If ($monto <= $escala_2) return $monto - $escala_1;
}
function irpf_bruto($mg,$bcp,$emni){
    return irpf1($mg,$bcp,$emni) + irpf2($mg,$bcp,$emni) + irpf3($mg,$bcp,$emni) + irpf4($mg,$bcp,$emni);
}
function deducible_bruto($monto,$bcp){
    return deducible1($monto,$bcp) + deducible2($monto,$bcp);
}
function deducciones($cess,$hijos,$bcp,$cjp){
    /* IMPORTANTE cambio el 1/10/08 por cambio del decreto */
    $ded_hijos = $hijos * 13 * $bcp /12;
    $deducciones = $ded_hijos + $cess + $cjp;
    // Aplicar escalas deducciones.
    if($deducciones > $escala_1){
        $ded_1 = $escala_1;
        if($deducciones > $escala_2){
            $ded_2 = $escala_2-$escala_1;
            if($deducciones > $escala_3){
                $ded_3 = $escala_3-$escala_2;
                if($deducciones > $escala_4) $ded_4 = $escala_4-$escala_3;
                else $ded_4 = $deducciones - $escala_3;
            }
        else $ded_3 = $deducciones - $escala_2;
        }
        else $ded_2 = $deducciones - $escala_1;
    }
    else $ded_1 = $deducciones;
    $ded_total = ($ded_1 * 0.10) + ($ded_2 * 0.15) + ($ded_3 * 0.20) + ($ded_4 * 0.22);
    return $ded_total;
}
function deducible($monto_deducible,$bcp){
    /* IMPORTANTE camibio por cambio de decreto el 1/10/08 */
    /* es el monto a deducir pasado x escalas de deducción */
    $escala_desc_1 = $bcp * 2;
    $escala_desc_2 = $bcp * 8;
    $monto_desc_1=deducible1($monto_deducible,$bcp);
    $monto_desc_2=deducible2($monto_deducible,$bcp);
    $irpf_s_ded = ($monto_desc_1 * 10 /100) + ($monto_desc_2 * 15 /100);
    return $irpf_s_ded;
}
function cuota_mutual($hijos,$bcp){
    /* IMPORTANTE camibio por cambio de decreto el 1/10/08 */
    /* Calcula el deducible correspondiente a la cuota mutual */
    return $hijos * $bcp * 13 / 12;
}
function total_deducciones($cess,$cjjpp,$hijos,$bcp){
    /* Calcula la suma de todos los conceptos de deducción
     * NO es el monto a deducir, antes pasa por la escala */
    return Cuota_Mutual($hijos,$bcp) + $cjjpp + $cess;
}
function aportes($nominal,$aguinaldo,$emni,$bcp){
    /* ($fil_det) */
    $monto_grav_irpf = $nominal + $aguinaldo;
    $monto_1 = irpf1($monto_grav_irpf,$bcp,$emni);
    $monto_2 = irpf2($monto_grav_irpf,$bcp,$emni);
    $monto_3 = irpf3($monto_grav_irpf,$bcp,$emni);
    $monto_4 = irpf4($monto_grav_irpf,$bcp,$emni);
    $irpf_sobre_mg = $monto_1 + $monto_2 + $monto_3 + $monto_4;
    if ($emni!=0){
        $por1 = '10%';$por2='15%';$por3='20%';$por4='22%';
    }
    return $irpf_sobre_mg;
}
function a_deducir($empleado_id,$liquidacion_id,$variables_id,$aportes_cjjpp,$aportes_bps){
    $sql_emp = 'SELECT * FROM empleados WHERE id="'.$empleado_id.'"';
    $res_emp = mysql_query($sql_emp);
    $fil_emp = mysql_fetch_array($res_emp);
    $sql_liq = 'SELECT * FROM liquidacion WHERE id="'.$liquidacion_id.'"';
    $res_liq = mysql_query($sql_liq);
    $fil_liq = mysql_fetch_array($res_liq);
    $sql_var = 'SELECT * FROM variables WHERE id="'.$variables_id.'"';
    $res_var = mysql_query($sql_var);
    $fil_var = mysql_fetch_array($res_var);
    $bcp=$fil_var['bcp'];
    $hijos = $fil_emp['hijos'];
    /* IMPORTANTE camibio por cambio de decreto el 1/10/08 */
    $cuotas_mutuales = $hijos * $bcp * 13 / 12 ;
    $deducible_bruto = $cuotas_mutuales + $aportes_cjjpp + $aportes_bps;
    $monto_desc_1=deducible1($deducible_bruto,$bcp);
    $monto_desc_2=deducible2($deducible_bruto,$bcp);
    $a_deducir = ($monto_desc_1 * 10 /100) + ($monto_desc_2 * 15 /100);
    return $a_deducir;
}
function calculo_ss($nominal,$empleado_id,$bcp){
    /* IMPORTANTE: no tengo idea como cambia con el cambio de decreto el 1/10/08 */
    // diferentes posibilidades según el código de SS
    $fil_emp = buscar_registro("empleados","id",$empleado_id);
    $codigoss = $fil_emp['codigoss'];
    $porcentaje = 0;
    $limite = $nominal / $bcp;
    // si el límite es <= 2.5 BCP y NO es vitalicio, el porcentaje es 3
    switch($codigoss){
        case '1':
            if($limite<=2.5){
                $porcentaje = 3;
            } else {
                $porcentaje = 6;
            }
            break;
        case '2':
            if($limite<=2.5){
                $porcentaje = 3;
            } else {
                $porcentaje = 6;
            }
            break;
        case '3':
            $porcentaje = 0;
            break;
        case '5':
            $porcentaje = 0;
            break;
        case '6':
            $porcentaje = 0;
            break;
        case '7':
            $porcentaje = 0;
            break;
        case '8':
            $porcentaje = 0;
            break;
        case '9':
            $porcentaje = 0;
            break;
        case '10':
            $porcentaje = 0;
            break;
        case '12':
            $porcentaje = 0;
            break;
        case '15':
            if($limite<=2.5){
                $porcentaje=3;
            } else {
                $porcentaje=4.5;
            }
            break;
        case '18':
            $porcentaje = 0;
            break;
        case '21':
            $porcentaje = 3;
            break;
        case '22':
            $porcentaje = 0;
            break;
        case '25':
            $porcentaje = 0;
            break;
        case '28':
            if($limite<=2.5){
                $porcentaje=3;
            } else {
                $porcentaje = 4.5;
            }
            break;    
    }
    return $porcentaje;
}
?>

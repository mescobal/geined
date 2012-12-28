#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Rutina de manejo de sueldo individual"""
import cgitb; cgitb.enable()
import funciones
import datos
import datetime
class Sueldo():
    """Calculo de items de liquidación de sueldos"""
    def __init__(self, detalle):
        # Parámetros: detalle (registro de det_liquidacion)
        self.montos_irpf = list()
        self.deduccion = 0
        self.montos_irpf = [0, 0, 0, 0, 0]
        self.montos_deducible = [0, 0, 0]
        liquidacion_id = detalle["liquidacion_id"]
        empleado_id = detalle["empleado_id"]
        # Bases de datos
        liquidacion = datos.Tabla("liquidacion")
        empleados = datos.Tabla("empleados")
        variables = datos.Tabla("variables")
        # buscar bases de datos
        liquidacion.ir_a(liquidacion_id)
        empleados.ir_a(empleado_id)
        # Asignar datos de base de datos
        self.codigo = empleados.registro["codigoss"]
        fecha_liquidacion = liquidacion.registro["fecha"]
        # cat_empleado_id = empleados.registro["categoria_id"]
        hijos = empleados.registro["hijos"]
        self.emni = empleados.registro["emni"]
        ingreso = datetime.date.today()
        if type(empleados.registro["ingreso"]) != type(None):
            ingreso = empleados.registro["ingreso"]
        self.anos_antiguedad = \
            funciones.diff_years(ingreso, fecha_liquidacion)
        # Ver que pasa si no se encuentra
        variables.filtro = "fecha <= '" + str(fecha_liquidacion) + "'"
        variables.orden = "fecha DESC"
        variables.filtrar()
        self.hora_reloj = detalle["valor_hs"] / funciones.to_decimal(4.29)
        self.bcp = variables.registro["bcp"]
        self.sueldo_semanal = detalle["horas_sem"] * detalle["valor_hs"]
        if type(detalle["ficto_semanal"]) == type(None):
            ficto_semanal = 0
        else:
            ficto_semanal = detalle["ficto_semanal"]
        monto_ficto_semanal = detalle["horas_sem"] * ficto_semanal
        self.sueldo_reloj = detalle["horas_reloj"] * self.hora_reloj
        ficto_reloj = ficto_semanal / funciones.to_decimal(4.29)
        monto_ficto_reloj = detalle["horas_reloj"] * ficto_reloj
        aportes_cjjpp = funciones.to_decimal(0.0)
        if detalle["cjp"] is not None:
            aportes_cjjpp = detalle["cjp"]
        #cálculo de antiguedad según especificado en correo electrónico
        self.ficto_nominal = monto_ficto_semanal + monto_ficto_reloj
        self.antiguedad = self.ficto_nominal * \
            funciones.to_decimal(self.anos_antiguedad * 0.02)
        self.nominal = self.sueldo_semanal + self.sueldo_reloj + self.antiguedad
        # nota elimino los EXTRAS del sueldo
        self.bps = self.nominal * variables.registro["bps"] / 100
        self.porcentaje_fonasa = self.calculo_ss()
        self.seguro_salud = self.nominal * \
            funciones.to_decimal(self.porcentaje_fonasa) / \
                funciones.to_decimal(100.0)
        self.frl = self.nominal * variables.registro["frl"] / 100
        self.cess = self.bps + self.seguro_salud + self.frl
        # Cálculo de IRPF
        self.monto_gravado_irpf = self.nominal + detalle["aguinaldo"]
        self.escala_irpf  = [0, 7 * self.bcp, 10 * self.bcp, 15 * \
            self.bcp, 20 * self.bcp]
        self.porcentajes_irpf = [0, 10, 15, 20, 22]
        self.escala_deducible = [0, 3 * self.bcp, 8 * self.bcp]
        self.porcentajes_deducible = [0, 10, 15]
        # Pueden preverse más montos
        self.calculo_irpf()
        total_aporte_irpf = self.montos_irpf[1] + self.montos_irpf[2] + \
            self.montos_irpf[3] + self.montos_irpf[4]
        cuotas_mutuales = funciones.to_decimal(hijos) * self.bcp * \
            funciones.to_decimal(13.0/12.0)
        # Deducible:
        # falta incluir personas con discapacidad a cargo
        # falta incluir fondo de solidaridad
        self.monto_deducible = cuotas_mutuales + aportes_cjjpp + self.cess
        self.calculo_deducible()
        self.anticipo_irpf = total_aporte_irpf - self.deduccion
        if self.anticipo_irpf < 0:
            self.anticipo_irpf = 0
        # Fin cálculo irpf
        self.liquido = self.nominal - self.cess - self.anticipo_irpf - \
            detalle["adelantos"]      
    def calculo_irpf(self):
        """devuelve tramos de irpf"""
        # Intento de rutina genérica
        for item in range(1, 5):
            if self.monto_gravado_irpf > self.escala_irpf[item]:
                # Si el monto es mayor que el tope de la escala, 
                # vale el rango de la escala
                monto = self.escala_irpf[item] - self.escala_irpf[item-1]
            else:
                if self.monto_gravado_irpf <= self.escala_irpf[item-1]:
                    # Si el monto es menor que el rango inferior
                    monto = 0
                else:
                    # si el monto esta entre ambos
                    monto = self.monto_gravado_irpf - self.escala_irpf[item-1]
            self.montos_irpf[item] = funciones.to_decimal(monto * \
                self.porcentaje_irpf(item) / 100)
    def porcentaje_irpf(self, franja):
        """Devuelve porcentaje de IRPF según franja tomando en cuenta el EMNI"""
        self.porcentajes_irpf = [0, 10, 15, 20, 22]
        if self.emni != 0:
            # recordar que los arrays empiezan por cero
            porcentaje = self.porcentajes_irpf[franja]
        else:
            porcentaje = self.porcentajes_irpf[franja - 1]
        return porcentaje
    def calculo_ss(self):
        """Calculo según código de seguridad social"""
        # IMPORTANTE: no tengo idea como cambia con el cambio de decreto 
        # el 1/10/08
        # diferentes posibilidades según el código de SS
        porcentaje = 0
        limite = self.nominal / self.bcp
        # si el límite es <= 2.5 BCP y NO es vitalicio, el porcentaje es 3
        # porcentaje 0 si codigoss = 3, 5, 6, 7, 8, 9, 10, 12, 18, 22, 25
        if self.codigo == 1:
            porcentaje = 6.0
            if limite <= 2.5:
                porcentaje = 3.0
        elif self.codigo == 2:
            porcentaje = 6.0
            if limite <= 2.5:
                porcentaje = 3.0
        elif self.codigo == 15:
            porcentaje = 4.5
            if limite <= 2.5:
                porcentaje = 3.0
        elif self.codigo == 21:
            porcentaje = 3.0
        elif self.codigo == 28:
            porcentaje = 4.5
            if limite <= 2.5:
                porcentaje = 3.0
        else:
            porcentaje = 0.0
        return porcentaje
    def calculo_deducible(self):
        """Calculo de deducible"""
        # Se actualizan cambios del 10/08
        # $escala_desc_1 = $bcp * 5;
        # $escala_desc_2 = $bcp * 10;
        if self.monto_deducible <= self.escala_deducible[1]:
            self.montos_deducible[1] = self.monto_deducible * \
                self.porcentajes_deducible[1] / funciones.to_decimal(100.0)
            self.montos_deducible[2] = funciones.to_decimal(0)
        else:
            self.montos_deducible[1] = self.escala_deducible[1] * \
                funciones.to_decimal(self.porcentajes_deducible[1] / 100.0)
            self.montos_deducible[2] = (self.monto_deducible - \
                self.escala_deducible[1]) * \
                    funciones.to_decimal(self.porcentajes_deducible[2] / 100.0)
        self.deduccion = self.montos_deducible[1] + self.montos_deducible[2]

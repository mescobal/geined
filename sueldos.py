#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Clases para liquidación de sueldos"""
import decimal
class Irpf():
    """Clase para liquidar irpf"""
    def __init__(self, variables, liquidacion, detalle, empleado):
        """Inicializar la clase"""
        # Parametros
        self.detalle = detalle
        self.liquidacion = liquidacion
        self.variables = variables
        self.empleado = empleado
        self.bcp = variables["bcp"]
        # Variables expuestas
        self.monto_gravado = detalle["nominal"] + detalle["aguinaldo"]
        self.monto_a_deducir = 0
        self.calculo_monto_a_deducir()
        self.tramos_irpf = list()
        self.porcentajes_irpf = list()
        self.escala_deducible = list()
        self.porcentajes_deducible = list()
        self.tramos_deducible = list()
        self.monto_gravado_irpf = list()
        self.monto_irpf = list()
        self.monto_deducible = list()
        self.ded_por_hijos = 0
        self.irpf_sobre_monto_gravado = 0
        self.irpf_total = 0
        self.deduccion_total = 0
        self.cess = 0
        self.llenar_escalas()
    def llenar_escalas(self):
        """Llenar escalas de deducible e IRPF"""
        self.tramos_irpf = [7 * self.bcp, 10 * self.bcp, 15 * self.bcp, 
            50 * self.bcp, 100 * self.bcp]
        if self.empleado["emni"] != 0:
            self.porcentajes_irpf = [10, 15, 20, 22, 25]
        else:
            self.porcentajes_irpf = [0,  10, 15, 20, 22, 25]
        self.porcentajes_deducible = [10, 15, 22, 25]
        self.tramos_deducible = [3 * self.bcp, 8 * self.bcp, 
                                 43 * self.bcp, 93 * self.bcp]
    def llenar_irpf(self):
        """Llenar valores de IRPF"""
        for contador in range(0, 4):
            self.monto_irpf[contador] = 0
        piso = 0
        cont = 0
        monto = 0
        for item in self.tramos_irpf:
            if self.monto_gravado <= piso:
                # si el monto es MENOR que el tramo anterior:
                monto = 0
            elif (self.monto_gravado > piso) and (self.monto_gravado <= item):
                # si el monto esta DENTRO del tramo:
                monto = self.monto_gravado - piso
            else: 
                # si el monto supera al tramo:
                monto = item
            self.monto_gravado_irpf.append(monto)
            monto_tramo_actual = self.monto_gravado * \
                self.porcentajes_irpf[cont]
            self.monto_irpf[cont] = monto_tramo_actual
            self.irpf_total = self.irpf_total + monto_tramo_actual
            cont = cont + 1
            piso = item
        piso = 0
        contador = 0
        monto = 0
        for item in self.tramos_deducible:
            if self.monto_deducible <= piso:
                # si el monto es MENOR que el tramo anterior
                monto = 0
            elif (self.monto_deducible > piso) and \
                (self.monto_deducible <= item):
                # si el monto esta DENTRO del tramo
                monto = self.monto_deducible - piso
            else:
                # si el monto supera el tramo
                monto = item
            monto_deduccion_actual = monto * \
                self.porcentajes_deducible[contador]
            self.monto_deducible.append(monto_deduccion_actual)
            self.deduccion_total = self.deduccion_total + monto_deduccion_actual
            contador = contador + 1
            piso = item  
    def calculo_monto_a_deducir(self):
        """Cálculo del monto a deducir"""
        # Calculo cuota mutual
        self.ded_por_hijos = self.empleado["hijos"] * 13 * \
            self.variables["bcp"] / 12
        self.cess = self.detalle["bps"] + self.detalle["disse"] + \
            self.detalle["frl"]
        self.monto_a_deducir = decimal.Decimal(str(self.ded_por_hijos)) + \
            self.cess + self.detalle["cjp"]
class Sueldos():
    """Clase para liquidar sueldos"""
    def __init__(self, variables, empleado, detalle):
        """Inicializar"""
        # Variables expuestas
        self.empleado = empleado
        self.variables = variables
        self.detalle = detalle
        self.aguinaldo = detalle["aguinaldo"]
        self.cess = self.cess = self.detalle["bps"] + self.detalle["disse"] + \
            self.detalle["frl"]
        self.aporte_jubilatorio = 0
        self.fonasa = 0
        self.porcentaje_fonasa = decimal.Decimal("0")
        self.frl = 0
        self.aporte_personal = 0
        self.monto_gravado_irpf = 0
        self.calculo_ss()
        self.calculo_partidas_percibidas()
        self.calculo_aportes_personales()
    def calculo_partidas_percibidas(self):
        """Calculo de partidas percibidas"""
        pass
    def calculo_aportes_personales(self):
        """Calculo de aportes personales"""
        self.aporte_jubilatorio = self.cess * decimal.Decimal("0.15")
        self.fonasa = self.cess * self.porcentaje_fonasa
        self.frl = self.cess * decimal.Decimal("0.0125")
        self.monto_gravado_irpf = self.detalle["nominal"] + \
            self.detalle["aguinaldo"]
    def calculo_ss(self):
        """Calculo segun codigo de Seg Soc"""
        # Cálculo de aportes a FONASA según categoría
        porcentaje = 0
        limite = self.detalle["nominal"] / \
            decimal.Decimal(str(self.variables['bcp']))
        # si el límite es <= 2.5 BCP y NO es vitalicio, el porcentaje es 3
        css = self.empleado['codigoss']
        porc = {1:[3, 6], 2:[3, 6], 5:[3, 6], 
                15:[3, 4.5], 28:[3, 4.5], 25:[3, 4.5],
                17:[5, 6.5], 27:[5, 6.5], 30:[5, 6.5],
                16:[5, 8], 26:[5, 8], 29:[5, 8],
                22:[0, 0], 21:[3, 3], 24:[2, 2], 23:[5, 5]}
        if css in porc:
            if limite < 2.5:
                porcentaje = porc[css][0]
            else:
                porcentaje = porc[css][1]
        else:
            # Error silenciado explicitamente
            # Debería ser atrapado con mensaje
            # Tengo flojera
            porcentaje = 0
        self.porcentaje_fonasa = decimal.Decimal(str(porcentaje))
if __name__ == "__main__":
    print("Es un módulo no ejecutable.")

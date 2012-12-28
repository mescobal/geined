#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Programa para instalar el sistema Geined"""
import os
def ensure_dir(f):
    """Crea un directorio si no existe"""
    d = os.path.dirname(f)
    if not os.path.exists(d):
        os.makedirs(d)
def main():
    # Corroborar depenencias:
    # PHP-PEAR
    # GNUPLOT
    # MYSQL
    # APACHE2
    # PHP + MYSQL
    # PYTHON + MYSQL
    # RUBY + MYSQL
    # Corroborar si existe el directorio destino
    ensure_dir("/var/www/geined")
    # Corroborar los permisos del directorio destino
    # Hacer un respaldo del directorio destino
    # Copia archivos desde el directorio de desarrollo hasta el directorio destino
    # Debería borrar primero todos los archivos existentes en destino
    # Menos los de configuración y los de upload / download
    # Después tomar la versión más reciente producida por Bazaar
    # Y colocarla en <geined>
    # Más tarde generalizarlo para una instalación neutra
    # correr la instalación de exportación a excel en PHP
if __name__ == "__main__":
    main()

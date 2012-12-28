#!/usr/bin/env python
import datos
usuarios = datos.Tabla("usuarios")
usuarios.filtrar()
for j,fila in enumerate(usuarios.resultado):
	print fila
	for k,columna in enumerate(fila):
		print(j, "-", k, "-", columna)


# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt

# Lee un archivo con la evolución de los valores de uno de los pesos.
# Guarda una gráfica que muestra la evolución.
# El formato esperado del archivo es un valor del peso por línea,
# al final del archivo los últimos valores generados.
# numero_peso es i para el peso wi.
def graficar_peso(directorio_guardar, ruta_archivo_peso, numero_peso):
	archivo_peso = open(ruta_archivo_peso, "r")
	valores_peso = []

	while True:
		linea = archivo_peso.readline()
		if linea == "":
			break

		linea = linea.split()[0]
		linea = float(linea)
		valores_peso.append(linea)

	archivo_peso.close()
	indice_peso = list(range(len(valores_peso)))

	# Generar el gráfico
	plt.plot(indice_peso, valores_peso)
	plt.title("Evolucion del peso w_{num}".format(num=numero_peso))
	plt.xlabel("Partidas")
	plt.ylabel("Valor de w_{num}".format(num=numero_peso))
	# Guardar los gráficos con nombre "peso_i.png"
	plt.savefig(directorio_guardar + "/peso{i}.png".format(i=numero_peso))
	plt.close()
'''
Módulo que implementa la propagación hacia atrás de las valoraciones de los tableros.
Se lee de un archivo los valores de entrenamiento.
Los valores de entrenamiento son los valores de la tupla que representa al tablero, junto
con una valoración de entrenamiento para ese tablero (calculada por el jugador AI).
Formato de cada línea del archivo_entrenamiento: [x1 x2 x3 x4 x5 x5 x6 x7 x8] [v_train]
Ejemplo de archivo_entrenamiento para partida ganada (valores sin sentido):
2 2 4 4 6 6 8 8 0.56
1 1 3 3 5 5 7 7 0.68
...
4 4 2 2 1 1 0 0 1
Ejemplo de archivo_entrenamiento para partida perdida (valores sin sentido):
2 2 4 4 6 6 8 8 0.56
1 1 3 3 5 5 7 7 0.68
...
4 4 2 2 1 1 0 0 -1
'''

class Regresion(object):

	def __init__(self, archivo_entrenamiento, archivo_pesos, factor_aprendizaje):
		super(Regresion, self).__init__()
		self.archivo_entrenamiento = archivo_entrenamiento
		self.factor_aprendizaje = factor_aprendizaje
		self.pesos = self.__parsear_archivo_pesos(archivo_pesos)

	# Parsea el archivo con los pesos y los guarda como atributos de la clase
	def __parsear_archivo_pesos(self, archivo_pesos):
		try:
			archivo_pesos = open(archivo_pesos, "r")
		except IOError:
			archivo_pesos.close()
			return "Hubo un error al intentar obtener el archivo"
		pesos = []
		linea = archivo_pesos.readline().split()
		for peso in linea:
			pesos.append(float(peso))
		print(linea)
		archivo_pesos.close()
		return pesos
	
	# Recibe la tupla que representa al tablero
	# Retorna la suma ponderada de los elementos de la tupla
	# El orden de los elementos de la tupla es el especificado en Tablero.py
	def valoracion(self, tupla):
		gane = tupla[2] == 10 if self.color == Color.Blancas else tupla[3] == 10
		perdi = tupla[2] == 10 if self.color == Color.Negras else tupla[3] == 10
		if gane:
			return 1
		elif perdi:
			return -1
		else:
			val = self.pesos[0]
			for i in range(len(tupla)):
				val += self.pesos[i+1]*tupla[i]
			return val

	# Parsea el archvio con los valores de entrenamiento y realiza el ajuste de mínimos cuadrados
	def ajuste_minimos_cuadrados(self):
		try:
			archivo_entrenamiento = open(self.archivo_entrenamiento, "r")
			lista_tuplas_sin_procesar = reversed(list(archivo_entrenamiento))
			archivo_entrenamiento.close()
			for tupla_sin_procesar in lista_tuplas_sin_procesar:
				tupla = []
				tupla = tupla_sin_procesar.split()
				v_train = float(tupla[8])
				for idx, valor in tupla[0:8]:
					tupla[idx] = int(valor)
				v_tupla = valoracion(tupla[0:8])
				error_valoracion = (v_train - v_tupla)
				self.pesos[0] = self.pesos[0] + self.factor_aprendizaje * error_valoracion
				for i in range(len(tupla)):
					self.pesos[i+1] = self.pesos[i+1] + self.factor_aprendizaje * error_valoracion * tupla[i]
				tupla_sin_procesar = readline(tuplas_archivo)
			try:
				archivo_pesos_finales = open("pesos_finales.txt", "w")
				string_pesos = ""
				for peso in pesos:
					string_pesos += peso + " "
				archivo_pesos_finales.write(string_pesos)
				archivo_pesos_finales.close()
			except:
				return "Error excribiendo archivo de pesos finales"
		except:
			print("Error abriendo archivo entrenamiento")

if __name__ == '__main__':
	'''
	reg = Regresion("entrenamiento.txt", "pesos.txt", 0.1)
	reg.ajuste_minimos_cuadrados()
	'''
	archivo_entrenamiento = open('entrenamiento.txt, 'r')
	lista_tuplas_sin_procesar = reversed(list(archivo_entrenamiento))
	archivo_entrenamiento.close()
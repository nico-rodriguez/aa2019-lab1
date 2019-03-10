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

	def __init__(self, archivo_entrenamiento, archivo_pesos):
		super(Regresion, self).__init__()
		self.archivo_entrenamiento = archivo_entrenamiento
		self.pesos = self.__parsear_archivo_pesos(archivo_pesos)

	# Parsea el archivo con los pesos y los guarda como atributos de la clase
	def __parsear_archivo_pesos(self, archivo_pesos):
	    try:
	        archivo_pesos = open(archivo_pesos,"r")
	    except IOError:
	        archivo_pesos.close()
	        return "Hubo un error al intentar obtener el archivo"
	    pesos = []
	    while(linea = archivo_pesos.readline() && (not linea is None)):
	        pesos.append(linea.split())
	    archivo_pesos.close()
	    return pesos

	# Parsea el archvio con los valores de entrenamiento y realiza el ajuste de mínimos cuadrados
	def ajuste_minimos_cuadrados(self):
        error_valoracion = (v_train - v_tupla)
        self.pesos[0] = self.pesos[0] + self.factor_aprendizaje * error_valoracion
        for i in range(len(tupla)):
            self.pesos[i+1] = self.pesos[i+1] + self.factor_aprendizaje * error_valoracion * tupla[i]
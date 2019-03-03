# Constantes globales con las posiciones factibles del tablero
# Se separan en tres listas para saber más fácilmente si una ficha
# llegó a la punta opuesta o todavía no salio de la punta propia
punta_negra = []
punta_blanca = []
parte_media = []

# Para generar la forma de estrella, se estructura la inicialización en cinco loops
# La casilla central de la estrella corresponde a la posición (0,0)
# Se usan coordenadas cartesianas (i,j)
# (algunos loops se hacen de arriba hacia abajo y otros al revés)

# Punta superior de la estrella
for i in range(5, 9, 1):
	for j in range(-8+i, 9-i, 2):
		punta_negra.append((i,j))

# Parte central superior
for i in range(1, 5, 1):
	for j in range(-(8+i), 9+i, 2):
		parte_media.append((i,j))

# Fila horizontal central
for j in range(-8, 9, 2):
	parte_media.append((0,j))

# Parte central inferior
for i in range(-4, 0, 1):
	for j in range(-8+i, 8+(-i)+1, 2):
		parte_media.append((i,j))

# Punta inferior de la estrella
for i in range(-5, -9, -1):
	for j in range(-(8+i), 9+i, 2):
		punta_blanca.append((i,j))

# Constante global con las direcciones posibles (hay que verificar si la dirección cae dentro del tablero)
direcciones = [
			(1,-1),		# noroeste
			(1,1),		# noreste
			(0,-2),		# oeste
			(0,2),		# este
			(-1,-1),	# suroeste
			(-1,1)		# sureste
		]


'''
La clase tablero contiene las posiciones del tablero, las posiciones de las
fichas de los dos jugadores y algunas cantidades de interés como el número
de fichas de cada jugador que llegó a la punta opuesta de la estrella, 
el número de fichas que no salieron aún de la propia punta de la estrella, 
la distancia vertical de las fichas a la punta opuesta de la estrella y 
la cantidad de fichas adyacentes que son de un mismo jugador o de cualquier jugador.
Además, la clase provee métodos para calcular posibles movimientos.
Por fuera de la clase se provee de un método para generar nuevos tableros a partir de 
una lista de posibles movimientos.
'''

class Tablero:

	def __init__(self):

		# Inicializar las piezas de ambos jugadores (blancas y negras)
		# Las negras comienzan en la punta superior de la estrella y las blancas en la punta inferior
		self.negras = punta_negra.copy()
		self.blancas = punta_blanca.copy()

	# Dadas las coordenadas cartesianas de una posición (en una tupla) devuelve True sii la posición pertenece al tablero
	def pertenece_al_tablero(self, pos):

		return pos in punta_negra or pos in punta_blanca or pos in parte_media

	# Dadas las coordenadas cartesianas de una posición (en una tupla) devuelve True sii la posición está ocupada por una ficha
	# No chequea si la posición es factible (si pertence al tablero)
	def posicion_ocupada(self, pos):

		return pos in self.negras or pos in self.blancas

	# Dadas las coordenadas cartesianas de una posición (en una tupla) devuelve una tupla con dos listas:
	# la primera contiene las posiciones adyacentes libres; la segunda, las posiciones adyacentes ocupadas
	def posiciones_adyacentes(self, pos):

		adyacentes_libres = []
		adyacentes_ocupadas = []

		for dir_x,dir_y in direcciones:
			# chequear si la dirección es factible (cae dentro del tablero)
			pos_x, pos_y = pos
			nueva_pos = (pos_x+dir_x, pos_y+dir_y)
			if self.pertenece_al_tablero(nueva_pos):
				if not self.posicion_ocupada(nueva_pos):
					adyacentes_libres.append(nueva_pos)
				else:
					adyacentes_ocupadas.append(nueva_pos)

		return (adyacentes_libres, adyacentes_ocupadas)

	# Dadas las coordenadas cartesianas de una posición (en una tupla) devuelve una lista con las posiciones adyacentes libres
	def posiciones_adyacentes_libres(self, pos):

		adyacentes_libres, _ = self.posiciones_adyacentes(pos)
		return adyacentes_libres

	# Dadas las coordenadas cartesianas de una posición (en una tupla) devuelve una lista con las posiciones adyacentes ocupadas
	def posiciones_adyacentes_ocupadas(self, pos):

		_, adyacentes_ocupadas = self.posiciones_adyacentes(pos)
		return adyacentes_ocupadas

	# Dada la posición de una ficha, devuelve una lista con posibles nuevas posiciones para la misma
	# de acuerdo con las reglas del juego
	def posibles_movimientos(self, pos):

		posibles_movimientos = set()	# conjunto con los posibles movimientos (posiciones libres)
		posibles_saltos = set()			# conjunto que contiene posiciones libres (salvo la posición inicial, que tiene la ficha que se va a mover) desde las que se podría saltar
		#saltos_considerados = set()		# conjunto que contiene posiciones libres que ya fueron consideradas para saltar desde ellas (ayuda a evitar caer en loop infinito)

		adyacentes_libres, adyacentes_ocupadas = self.posiciones_adyacentes(pos)
		posibles_movimientos.update(adyacentes_libres)
		posibles_saltos.add(pos)

		while posibles_saltos:
			actual_pos = posibles_saltos.pop()
			actual_pos_x,actual_pos_y = actual_pos
			for dir_x,dir_y in direcciones:
				ady_pos = (actual_pos_x+dir_x, actual_pos_y+dir_y)
				if self.pertenece_al_tablero(ady_pos):
					# posible salto
					if self.posicion_ocupada(ady_pos):
						ady_pos_x,ady_pos_y = ady_pos
						nueva_pos = (ady_pos_x+dir_x, ady_pos_y+dir_y)
						if self.pertenece_al_tablero(nueva_pos) and not self.posicion_ocupada(nueva_pos) and not(nueva_pos in posibles_movimientos):
							# el salto es posible
							posibles_movimientos.add(nueva_pos)
							posibles_saltos.add(nueva_pos)

		return posibles_movimientos

	# Para debugging
	def imprimir_tablero(self):

		ancho = round(25/2)
		altura = round(17/2)
		casillas_en_rectangulo = 0

		for i in range(altura, -altura-1, -1):
			for j in range(ancho, -ancho-1, -1):
				if (i,j) in punta_negra or (i,j) in punta_blanca or (i,j) in parte_media:
					print("0", end="")
					casillas_en_rectangulo += 1
				else:
					print("*", end="")
			print()

		print(f"Casillas dentro del rectángulo: {casillas_en_rectangulo}")
		print(f"Casillas en instancia de Tablero: {len(punta_negra) + len(punta_blanca) + len(parte_media)}")
		print(f"Fichas blancas: {len(tablero.blancas)}")
		print(f"Fichas negras: {len(tablero.negras)}")

	def imprimir_tablero_con_fichas(self):

		ancho = round(25/2)
		altura = round(17/2)

		for i in range(altura, -altura-1, -1):
			for j in range(ancho, -ancho-1, -1):
				if (i,j) in punta_negra or (i,j) in punta_blanca or (i,j) in parte_media:
					if (i,j) in tablero.blancas:
						print("b", end="")
					elif (i,j) in tablero.negras:
						print("n", end="")
					else:
						print("0", end="")
				else:
					print(" ", end="")
			print()

# tablero_actual es una instancia de Tablero
# movimiento es una lista con dos tuplas: la primera es la posición vieja de una de las fichas;
# la segunda tupla es la nueva posición de la ficha
def nuevo_tablero(tablero_actual, movimiento):
	return Tablero()

# Para debuggeing
if __name__ == '__main__':
	tablero = Tablero()
	tablero.imprimir_tablero()

	print("Posiciones adyacentes")
	print(f"(-8,0): {tablero.posiciones_adyacentes((-8,0))}")
	assert tablero.posiciones_adyacentes((-8,0)) == ([], [(-7, -1), (-7, 1)])
	print(f"(-6,0): {tablero.posiciones_adyacentes((-6,0))}")
	assert tablero.posiciones_adyacentes((-6,0)) == ([], [(-5, -1), (-5, 1), (-6, -2), (-6, 2), (-7, -1), (-7, 1)])
	print(f"(-5,1): {tablero.posiciones_adyacentes((-5,1))}")
	assert tablero.posiciones_adyacentes((-5,1)) == ([(-4, 0), (-4, 2)], [(-5, -1), (-5, 3), (-6, 0), (-6, 2)])

	print("Posibles movimientos")
	tablero.imprimir_tablero_con_fichas()
	print(f"(-8,0) => {tablero.posibles_movimientos((-8,0))}")
	assert tablero.posibles_movimientos((-8,0)) == set()
	print(f"(-6,0) => {tablero.posibles_movimientos((-6,0))}")
	assert tablero.posibles_movimientos((-6,0)) == {(-4, 2), (-4, -2)}
	print(f"(-5,1) => {tablero.posibles_movimientos((-5,1))}")
	assert tablero.posibles_movimientos((-5,1)) == {(-4, 2), (-4, 0)}

	# Testear posibles_movimientos cuando hay varios saltos
	tablero.negras.append((-4,0))
	print("Agregada negra en (-4,0)")
	tablero.blancas.append((-2,0))
	print("Agregada blanca en (-2,0)")
	tablero.imprimir_tablero_con_fichas()
	print(f"(-5,1) => {tablero.posibles_movimientos((-5,1))}")
	assert tablero.posibles_movimientos((-5,1)) == {(-3, -1), (-4, 2), (-1, 1)}
	tablero.blancas.remove((-5,1))
	print("Quitada blanca en (-5,1)")
	tablero.imprimir_tablero_con_fichas()
	print(f"(-7,-1) => {tablero.posibles_movimientos((-7,-1))}")
	assert tablero.posibles_movimientos((-7,-1)) == {(-3, -1), (-1, 1), (-5, 1)}
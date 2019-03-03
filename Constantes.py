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
from abc import abstractmethod
import random
from Tablero import *
from Constantes import *

class Jugador(object):

	#"color" es el string "blancas" o "negras"
	def __init__(self, color, nombre):
		super(Jugador, self).__init__()
		self.color = color
		self.nombre = nombre
	
	# Devuelve el tablero que resulta de efectuar la mejor jugada según la estrategia del jugador	
	@abstractmethod
	def mejor_jugada(self, tablero):
		pass

class Aleatorio(Jugador):

	def __init__(self, color, nombre):
		super(Aleatorio, self).__init__(color, nombre)
	
	def mejor_jugada(self, tablero):
		fichas = tablero.negras if self.color == Color.Negras else tablero.blancas
		while True:
			mover_ficha = random.choice(fichas)
			movimientos = tablero.posibles_movimientos(mover_ficha)
			if movimientos:
				movimiento = random.choice(movimientos)
				tablero.actualizar_tablero(mover_ficha, movimiento, self.color)
				return tablero

class AI(Jugador):

	def __init__(self, color, nombre, pesos):
		super(AI, self).__init__(color, nombre)
		self.pesos = pesos
	
	def mejor_jugada(self, tablero):
		# TODO
		pass
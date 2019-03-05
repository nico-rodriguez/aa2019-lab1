from abc import abstractmethod
import random
from Tablero import *
from Constantes import *

class Jugador(object):

	#"color" es el string "blancas" o "negras"
	def __init__(self, color):
		super(Jugador, self).__init__()
		self.color = color
	
	# Devuelve el tablero que resulta de efectuar la mejor jugada según la estrategia del jugador	
	@abstractmethod
	def mejor_jugada(self, tablero):
		pass

class Aleatorio(Jugador):

	def __init__(self):
		super(Aleatorio, self).__init__()
	
	def mejor_jugada(self, tablero):
		fichas = tablero.negras if self.color = Color.Negras else tablero.blancas
		while True:
			mover_ficha = random.choice(fichas)
			movimientos = tablero.posibles_movimientos(mover_ficha)
			if movimientos:
				return nuevo_tablero(tablero, mover_ficha, random.choice(movimientos))

class AI(Jugador):

	def __init__(self, pesos):
		super(AI, self).__init__()
		self.pesos = pesos
	
	def mejor_jugada(self, tablero):
		# TODO
		pass
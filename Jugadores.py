from abc import abstractmethod
import random
from Tablero import *

class Jugador(object):

	def __init__(self):
		super(Jugador, self).__init__()
	
	# Devuelve el tablero que resulta de efectuar la mejor jugada según la estrategia del jugador	
	@abstractmethod
	def mejor_jugada(self, tablero, fichas):
		pass

class Aleatorio(Jugador):

	def __init__(self):
		super(Aleatorio, self).__init__()
	
	def mejor_jugada(self, tablero, fichas):
		mover_ficha = random.choice(fichas)
		movimientos = tablero.posibles_movimientos(mover_ficha)
		return nuevo_tablero(tablero, mover_ficha, random.choice(movimientos))

class AI(Jugador):

	def __init__(self, pesos):
		super(AI, self).__init__()
		self.pesos = pesos
	
	def mejor_jugada(self, tablero, fichas):
		# TODO
		pass
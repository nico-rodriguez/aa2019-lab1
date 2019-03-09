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
            # filtrar movimientos que llevan hacia atrás
            mover_ficha_x,_ = mover_ficha
            for mov_x,mov_y in movimientos:
                if self.color == Color.Blancas:
                    if mov_x < mover_ficha_x:
                        movimientos.remove((mov_x,mov_y))
                else: #self.color == Color.Negras
                    if mov_x > mover_ficha_x:
                        movimientos.remove((mov_x,mov_y))
            if movimientos:
                movimiento = random.choice(movimientos)
                tablero.actualizar_tablero(mover_ficha, movimiento, self.color)
                return tablero

class AI(Jugador):

    def __init__(self, color, nombre, pesos):
        super(AI, self).__init__(color, nombre)
        self.pesos = pesos
        
    # Recibe la tupla que representa al tablero
    # Retorna la suma ponderada de los elementos de la tupla
    # El orden de los elementos de la tupla es el especificado en Tablero.py
    def valoracion(self, tupla):
        val = pesos[0]
        for i in range(len(tupla)):
            val += pesos[i+1]*tupla[i]
        return val
    
    def mejor_jugada(self, tablero):
        fichas = tablero.negras if self.color == Color.Negras else tablero.blancas
        valoracion_maxima = None
        for pos in fichas:
            for mov in tablero.posibles_movimientos():
                nuevo_posible_tablero = 
        pass

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

    def __init__(self, color, nombre, pesos, entrenando, factor_aprendizaje, factor_propagacion, tasa_decaimiento):
        super(AI, self).__init__(color, nombre)
        self.pesos = pesos
        self.entrenando = entrenando
        self.factor_aprendizaje = factor_aprendizaje
        self.factor_propagacion = factor_propagacion
        self.tasa_decaimiento = tasa_decaimiento
        self.color_oponente = Color.Negras if color == Color.Blancas else Color.Blancas
        
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
            val = pesos[0]
            for i in range(len(tupla)):
                val += pesos[i+1]*tupla[i]
            return val

    # Recibe un tablero y retorna para dicho tablero, el movimiento de la forma (ficha, movimiento)
    # Que tiene la mayor valoracion
    def mejor_jugada(self, tablero):
        valoracion_tablero = self.valoracion(tablero.obtener_tupla)
        fichas = tablero.negras if self.color == Color.Negras else tablero.blancas
        valoracion_maxima = None
        for ficha in fichas:
            for movimiento in tablero.posibles_movimientos(ficha):
                nuevo_posible_tablero = tablero.copy()
                nuevo_posible_tablero.actualizar_tablero(ficha, movimiento, self.color)
                if nuevo_posible_tablero.hay_ganador():
                    # Como es nuestro turno de mover, solo podemos ganar nosotros. De todas formas
                    # se chequea si en este tablero el jugador gana
                    if nuevo_posible_tablero.ganador() == self.color:
                        tablero.actualizar_tablero(ficha_maxima, movimiento_maximo, self.color)
                        if entrenando:
                            actualizar_pesos(self.valoracion(tablero.obtener_tupla), valoracion_tablero, tablero.obtener_tupla)
                        return tablero
                else:
                    # Obtener tablero con mejor jugada del oponente (se asume que hace la mejor jugada)
                    nuevo_posible_tablero = self.mejor_jugada_oponente(nuevo_posible_tablero)
                    valoracion = self.valoracion(nuevo_posible_tablero.obtener_tupla())
                    if valoracion_maxima is None || valoracion > valoracion_maxima:
                        valoracion_maxima = valoracion
                        ficha_maxima = ficha
                        movimiento_maximo = movimiento
        tablero.actualizar_tablero(ficha_maxima, movimiento_maximo, self.color)
        if entrenando:
            actualizar_pesos(valoracion_maxima, valoracion_tablero, tablero.obtener_tupla)
        return tablero
    
    def mejor_jugada_oponente(self, tablero):
        # Miro las posibles jugadas del oponente y considero la "mejor" (la que gana o la que
        # tiene menor valor de valoración
        fichas = tablero.negras if self.color != Color.Negras else tablero.blancas
        valoracion_minima = None
        for ficha in fichas:
            for movimiento in tablero.posibles_movimientos(ficha):
                nuevo_posible_tablero = tablero.copy()
                nuevo_posible_tablero.actualizar_tablero(ficha, movimiento, self.color)
                if nuevo_posible_tablero.hay_ganador():
                    # Como es el turno del oponente, solo puede ganar él. De todas formas
                    # se chequea si en este tablero el jugador gana
                    if nuevo_posible_tablero.ganador() != self.color:
                        tablero_siguiente = tablero.copy()
                        tablero_siguiente.actualizar_tablero(ficha_maxima, movimiento_maximo, self.color)
                        return tablero_siguiente
                else:
                    tablero_siguiente = tablero.copy()
                    tablero_siguiente.actualizar_tablero(ficha, movimiento, self.color_oponente)
                    valoracion = self.valoracion(tablero_siguiente.obtener_tupla())
                    if valoracion_minima is None || valoracion < valoracion_minima:
                        valoracion_minima = valoracion
                        ficha_minima = ficha
                        movimiento_minima = movimiento
        tablero_siguiente = tablero.copy()
        tablero_siguiente.actualizar_tablero(ficha_minima, movimiento_minimo, self.color_oponente)
        return tablero_siguiente
    
    def actualizar_pesos(self, v_train, v_,tupla):
        error_valoracion = (v_train - self.tablero.
        self.pesos[0] = self.pesos[0] + self.factor_aprendizaje * 
        for i in range(1, len(pesos)):
            self.pesos[]

    
    
    

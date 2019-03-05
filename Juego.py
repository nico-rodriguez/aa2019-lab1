from Jugadores import *
from Constantes import *

class Juego:

    #Inicializa el tablero con los jugadores ingresados
    #El "jugador1" siempre es el que mueve primero
    def __init__(self, jugador1, jugador2):
        self.tablero = Tablero()
        self.jugadores = { Color.Blancas : jugador1,
                           Color.Negras  : jugador2 }

    #Aplica la mejor jugada del jugador con color "color", modificando el tablero actual
    #"color" es el string "blancas" o "negras"
    def __jugada(self, color):
        jugador = self.jugadores[color]
        return jugador.mejor_jugada(self.tablero)

    #Retorna la tupla para el tablero actual
    def __obtener_tupla_tablero(self):
        return self.tablero.tupla

    #Retorna true si hay un ganador para el tablero actual
    def __hay_ganador(self):
        return self.tablero.tupla.["fichas_blancas_en_punta_opuesta"] == 10 || 
        self.tablero.tupla.["fichas_negras_en_punta_opuesta"] == 10
    
    #Retorna el ganador solo en caso que haya (hay_ganador == true) sino retorna None
    def __ganador(self):
        if self.tablero.tupla.["fichas_blancas_en_punta_opuesta"] == 10:
            return self.jugadores[Color.Blancas].nombre
        elif self.tablero.tupla.["fichas_negras_en_punta_opuesta"] == 10:
            return self.jugadores[Color.Negras].nombre
        else 
            return None

    #Jugar una partida entre los jugadores que son atributos de la clase Juego
    #Devuelve el color del ganador
    def jugar(self):
        while not self.__hay_ganador():
            self.__jugada(Color.Blancas)
            self.__jugada(Color.Negras)
        return self.__ganador()
from Jugadores import *
from Constantes import *

class Juego:

    #Inicializa el tablero con los jugadores ingresados
    def __init__(self, jugador1, jugador2):
        self.tablero = Tablero()
        self.jugadores = { "blancas" : jugador1,
                           "negras"  : jugador2 }

    #Aplica la jugada ingresada, modificando el tablero actual
    def __jugada(self, ficha, movimiento, color):
        tipo_jugador = jugadores[color.value]
        jugada = mejor_jugada_para_jugador(tipo_jugador)
        (ficha,movimiento) = jugada
        self.tablero = self.tablero.actualizar_tablero(ficha, movimiento, color)

    #Retorna la tupla para el tablero actual
    def __obtener_tupla_tablero(self):
        return self.tablero.tupla

    #Retorna true si hay un ganador para el tablero actual
    def __hay_ganador(self):
        return self.tablero.tupla.["fichas_blancas_en_punta_opuesta"] == 10 || 
        self.tablero.tupla.["fichas_negras_en_punta_opuesta"] == 10
    
    #Retorna el ganador solo en caso que haya (hay_ganador == true) sino retorna NULL
    def __ganador(self):
        if self.tablero.tupla.["fichas_blancas_en_punta_opuesta"] == 10:
            return Color.Blancas
        elif self.tablero.tupla.["fichas_negras_en_punta_opuesta"] == 10:
            return Color.Negras
        else 
            return NULL
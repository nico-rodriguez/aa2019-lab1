import * from Jugadores

class Juego:

    #Inicializa el tablero con los jugadores ingresados
    def __init__(self, jugador1, jugador2):
        self.tablero = Tablero()
        self.jugadores = { "blancas" : jugador1,
                           "negras"  : jugador2 }

    #Aplica la jugada ingresada, modificando el ablero actual
    def jugada(ficha, movimiento, color):
        tipo_jugador = jugadores[color.value]
        jugada = mejor_jugada_para_jugador(tipo_jugador)
        (ficha,movimiento) = jugada
        self.tablero = self.tablero.actualizar_tablero(ficha, movimiento, color)

    #Retorna la tupla para el tablero actual
    def obtener_tupla_tablero():
        return self.tablero.tupla

    #Retorna true si hay un ganador para el tablero actual
    def hay_ganador():
        return self.tablero.tupla.["fichas_blancas_en_punta_opuesta"] == 10 || 
        self.tablero.tupla.["fichas_negras_en_punta_opuesta"] == 10
    
    #Retorna el ganador solo en caso que haya (hay_ganador == true) sino retorna NULL
    def ganador():
        if self.tablero.tupla.["fichas_blancas_en_punta_opuesta"] == 10:
            return Color.Blancas
        elif self.tablero.tupla.["fichas_negras_en_punta_opuesta"] == 10:
            return Color.Negras
        else 
            return NULL
        
from Juego import *
from Jugadores import *
import sys

uso = """
Invocar como python3 Training [jugador1] [jugador2] [numero de partidas]
donde jugador1/2 pueden ser "AI1", "AI2" o "Aleatorio".
En el caso que ambos sean "AI", el jugador1 es la versió más entrenada ("AI1"), mientras
que jugador2 es su versión pervia de 10 partidas atrás ("AI2").
numero de partidas debe ser al menos 100.
"""

jugadores = ["AI1", "AI2", "Aleatorio"]

'''
Jugar a modo de entrenamiento el número de partidas indicas por parámetro.
Imprime en consola el número de partidas ganadas por la AI.

TODO: imponer como condición que al menos uno de los jugadores siempre debe ser la AI
TODO: imprimir solo las victorias de la AI
'''
if __name__ == '__main__':
    print ('Number of arguments:', len(sys.argv), 'arguments.')
    print ('Argument List:', str(sys.argv))
    #Chequear número y valores de los argumentos
    if len(sys.argv) != 3:
        print("***Número incorrecto de parámetros***")
        print(uso)

    jugador1_str = sys.argv[1]
    jugador2_str = sys.argv[2]
    num_partidas = sys.argv[3]

    if not(jugador1_str in jugadores and jugador2_str in jugadores):
        print("***Valores incorrectos para los jugadores***")
        print(uso)
    if num_partidas < 100:
        print("***El número de partidas debe ser al menos de 100***")
        print(uso)

    jugador1 = Aleatorio() if jugador1_str == "Aleatorio" else AI()
    jugador2 = Aleatorio() if jugador1_str == "Aleatorio" else AI()
    juego = Juego(jugador1, jugador2)
    victorias = 0

    for i in range(num_partidas):
        ganador = juego.jugar()
        #Para debugging
        print(ganador)
        print("Victorias = {victorias}")
#TODO: Todo (corra sin ser entrenamiento)
from Juego import *
from Jugadores import *
import sys

uso = """
Invocar como python3 Torneo.py [jugador1] [jugador2] [numero de partidas]
donde jugador pueden ser una ruta a un archivo con pesos para una AI o "Aleatorio".
"""

jugadores = ["Aleatorio"]

'''
Jugar el número de partidas indicas por parámetro.
Imprime en consola el número de partidas ganadas por la AI, en caso que al menos uno de
los jugadores sea la AI.
'''

if __name__ == '__main__':
    print ('Number of arguments:', len(sys.argv), 'arguments.')
    print ('Argument List:', str(sys.argv))
    #Chequear número y valores de los argumentos
    #TODO: cambiar los parametros de entrada a AI y Aleatorio; tener AI1 AI2 como nombres internos
    if len(sys.argv) != 4:
        print("***Número incorrecto de parámetros***")
        print(uso)

    jugador1_str = sys.argv[1]
    jugador2_str = sys.argv[2]
    num_partidas = int(sys.argv[3])

    # jugador1 no es Aleatorio. Cargar archivo con los pesos.
    if not(jugador1_str in jugadores):
    	try:
    		weights_file_1 = open(jugador1_str, 'r')
    	except Exception as e:
    		print('Troeno.py: error abriendo archivo {archivo}'.format(archivo=jugador1_str))
    		raise e
    # jugador2 no es Aleatorio. Cargar archivo con los pesos.
    if not(jugador2_str in jugadores):
    	try:
    		weights_file_2 = open(jugador2_str, 'r')
    	except Exception as e:
    		print('Troeno.py: error abriendo archivo {archivo}'.format(archivo=jugador2_str))
    		raise e

    # Ambos jugadores son AI
    if not(jugador1_str in jugadores) and not(jugador2_str in jugadores):
		jugador1 = AI(Color.Blancas, "AI1", None, False, 0.1)
		jugador2 = AI(Color.Negras, "AI2", None, False, 0.1)
	# Al menos uno de los jugadores no es AI
	else:
		jugador1 = Aleatorio(Color.Blancas, "Aleatorio") if jugador1_str == "Aleatorio" else AI(Color.Blancas, "AI", None, False, 0.1)
    	jugador2 = Aleatorio(Color.Negras, "Aleatorio") if jugador1_str == "Aleatorio" else AI(Color.Negras, "AI", None, False, 0.1)

    victorias = 0

    for i in range(num_partidas):
        juego = Juego(jugador1, jugador2)
        ganador = juego.jugar()
        #Para debugging
        print(ganador)
        
        print("Victorias = {victorias}".format(victorias=victorias))
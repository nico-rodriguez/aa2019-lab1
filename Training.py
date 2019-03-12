from Juego import *
from Jugadores import *
import sys
import datetime
import os

uso = """
Invocar como python3 Training.py [jugador1] [jugador2] [numero de partidas] [diferencia]
donde jugador1 y jugador2 pueden ser una ruta a un archivo con pesos o "Aleatorio".
Los pesos deben estar escritos en una sola línea y separados por espacios.
En el caso en que ambos sean AIs, los pesos de la AI más reciente deben pasarse
en jugador1. La AI que entrena siempre es la que se pasa en jugador 1. 
Al menos uno de los jugadores debe ser una AI.
El parámetro "diferencia" solo es obligatorio cuando ambos jugadores son AI.
Indica el número de partidas de distancia entre el AI y su versión previa.
Debe ser un valor entero y positivo.
"""

'''
Jugar a modo de entrenamiento el número de partidas indicas por parámetro.
Imprime en consola el número de partidas ganadas por la AI en caso que juege una.
'''

if __name__ == '__main__':
    print ('Number of arguments:', len(sys.argv), 'arguments.')
    print ('Argument List:', str(sys.argv))
    #Chequear número y valores de los argumentos
    if not(len(sys.argv) == 4 or len(sys.argv) == 5):
        print("***Número incorrecto de parámetros***")
        print(uso)
        exit()

    jugador1_str = sys.argv[1]
    jugador2_str = sys.argv[2]
    num_partidas = int(sys.argv[3])

    jugadores = []
    diferencia_partidas = None      # Indica las partidas de distancia entre la AI y su versión previa. También indica que juegan dos AIs si no es None.
    print("Creando jugadores")
    # Ambos son AIs. Solo el jugador1 entrena. Le pasa sus pesos a jugador2 cada "diferencia_partidas"
    if jugador1_str != "Aleatorio" and jugador2_str != "Aleatorio":
        lista_pesos_previos = []      # para pasarselos a la "versión previa" de la AI
        jugadores = ["AI1", "AI2"]
        jugador1 = AI(Color.Blancas, "AI1", None, True, 0.1)
        print("Leyendo pesos del jugador 1")
        jugador1.cargar_pesos(jugador1_str)
        jugador2 = AI(Color.Negras, "AI2", None, False, 0.1)
        print("Leyendo pesos del jugador 2")
        jugador1.cargar_pesos(jugador2_str)
        if len(sys.argv) != 5:
            print("***Número incorrecto de parámetros***")
            print(uso)
            exit()
        else:
            diferencia_partidas = int(sys.argv[4])
            if diferencia_partidas <= 0:
                print("***Valor incorrecto en la diferencia de partidas. Debe ser positivo.***")
                print(uso)
                exit()
    # Solo el primero es AI
    elif jugador1_str != "Aleatorio" and jugador2_str == "Aleatorio":
        jugadores = ["AI", "Aleatorio"]
        jugador1 = AI(Color.Blancas, "AI", None, True, 0.1)
        print("Leyendo pesos del jugador 1")
        jugador1.cargar_pesos(jugador1_str)
        jugador2 = Aleatorio(Color.Negras, "Aleatorio")
    # Solo el segundo es AI
    elif jugador1_str == "Aleatorio" and jugador2_str != "Aleatorio":
        jugadores = ["Aleatorio", "AI"]
        jugador1 = AI(Color.Blancas, "AI", None, True, 0.1)
        jugador2 = Aleatorio(Color.Negras, "Aleatorio")
        print("Leyendo pesos del jugador 2")
        jugador1.cargar_pesos(jugador2_str)
    # Ninguno es AI
    else:
        print("***Valores de jugadores incorrectos. Al menos uno debe ser una AI.***")
        print(uso)
        exit()

    victorias = 0

    # Crear un directorio para guardar los datos de entrenamiento
    currentDT = datetime.datetime.now()
    directorio = currentDT.strftime("%Y-%m-%d %H:%M:%S")
    os.mkdir(directorio)
    print("Se crea el directorio {dir}".format(dir=directorio))

    print("Comenzando la serie de partidas")
    for i in range(num_partidas):
        print("Comenzando partida {num}".format(num=i))
        # Crear archivo vacio para los valores de entrenamiento
        try:
            # Se agrega un timestamp al nombre del archivo para que queden ordenados
            ruta_archivo_entrenamiento = directorio + "/" + "partida{num}".format(num=i) + ".txt"
            open(ruta_archivo_entrenamiento, "w").close()
            # Avisar a jugador cual es el archivo sobre el cual escribira las tuplas
            jugador1.set_archivo_entrenamiento(ruta_archivo_entrenamiento)
        except Exception as e:
            print("Trainin.py: Error creando el archivo de entrenamiento")
            raise e
        juego = Juego(jugador1, jugador2)
        ganador = juego.jugar()
        #Para debugging
        print("Partida {partida} => Ganó {ganador}.".format(partida=i, ganador=ganador))
        # Chequear que el ganador sea la AI o la AI más reciente (AI1)
        if "AI" in ganador:
            if ganador != "AI2":
                victorias += 1
        print("Victorias = {victorias}".format(victorias=victorias))
        # Llamar ajuste de minimos cuadrados de Jugadores.py
        jugador1.ajuste_minimos_cuadrados(ruta_archivo_entrenamiento)
        # Decidir y actualizar los pesos de la version previa del AI2
        if not(diferencia_partidas is None):
            # Registrar los pesos para pasarselos a la "versión previa" de la AI
            lista_pesos_previos.append(jugador1.pesos.copy())
            # Comenzar a pasarle los pesos previos de la AI
            if len(lista_pesos_previos) >= diferencia_partidas:
                jugador2.pesos = lista_pesos_previos[0]
                lista_pesos_previos.remove(lista_pesos_previos[0])
                
    print("La AI ganó el {porcentaje}% de las veces".format(porcentaje=victorias/num_partidas*100))

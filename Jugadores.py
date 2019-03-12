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

    @abstractmethod
    def perdi(self, tablero):
        pass

class Aleatorio(Jugador):

    def __init__(self, color, nombre):
        super(Aleatorio, self).__init__(color, nombre)

    # Elije una juagda al azar que lo acerque al objetivo. Se decide esto para que
    # el partido eventualemnte termine    
    def mejor_jugada(self, tablero):
        fichas = tablero.negras.copy() if self.color == Color.Negras else tablero.blancas.copy()
        while True:
            mover_ficha = random.choice(fichas)
            fichas.remove(mover_ficha)
            movimientos = tablero.posibles_movimientos(mover_ficha)
            # filtrar movimientos que llevan hacia atrás
            mover_ficha_x = mover_ficha[0]
            movimientos_aux = movimientos.copy()
            for movimiento in movimientos:
                if self.color == Color.Blancas:
                    if movimiento[0] <= mover_ficha_x:
                        movimientos_aux.remove(movimiento)
                else: #self.color == Color.Negras
                    if movimiento[0] >= mover_ficha_x:
                        movimientos_aux.remove(movimiento)
            if movimientos_aux:
                movimiento = random.choice(movimientos_aux)
                tablero.actualizar_tablero(mover_ficha, movimiento, self.color)
                return tablero
            # no hay fichas que avancen, tengo que mover alguien cualquiera a
            # cualquier lado
            if not fichas:
                fichas = tablero.negras.copy() if self.color == Color.Negras else tablero.blancas.copy()
                ficha_a_mover = random.choice(fichas)
                while not movimientos:
                    fichas.remove(ficha_a_mover)
                    ficha_a_mover = random.choice(fichas)                    
                    movimientos = tablero.posibles_movimientos(ficha_a_mover)
                movimiento = random.choice(movimientos)
                tablero.actualizar_tablero(mover_ficha, movimiento, self.color)
                return tablero
    def perdi(self, tablero):
        return
    
class AI(Jugador):
    
    weights_file_path = "pesos.txt"

    def __init__(self, color, nombre, pesos, entrenando, factor_aprendizaje):
        super(AI, self).__init__(color, nombre)
        if pesos is None:
            self.pesos = []
            for i in range(9):
                self.pesos.append(1/8)
        else:
            self.pesos = pesos
        self.entrenando = entrenando
        self.factor_aprendizaje = factor_aprendizaje
        self.color_oponente = Color.Negras if color == Color.Blancas else Color.Blancas
        self.archivo_entrenamiento = "entrenamiento.txt"
        self.tupla_entrenamiento_a_grabar = None
        
    # FUNCIONES DEL ALGORITMO

    # Recibe la tupla que representa al tablero
    # Retorna la suma ponderada de los elementos de la tupla
    # El orden de los elementos de la tupla es el especificado en Tablero.py
    def valoracion(self, tupla_tablero):
        gane = tupla_tablero[2] == 10 if self.color == Color.Blancas else tupla_tablero[3] == 10
        perdi = tupla_tablero[2] == 10 if self.color == Color.Negras else tupla_tablero[3] == 10
        if gane:
            return 1
        elif perdi:
            return -1
        else:
            val = self.pesos[0]
            for i in range(len(tupla_tablero)):
                val += self.pesos[i+1] * tupla_tablero[i]
            return val

    def perdi(self, tablero):
        if (self.entrenando):
            print("Ai perdio, registrando tupla para propagar")
            valoracion_actual = self.valoracion(tablero.obtener_tupla())
            self.tupla_entrenamiento_a_grabar += [valoracion_actual]
            self.grabar_datos_en_disco(self.tupla_entrenamiento_a_grabar, self.archivo_entrenamiento)
        self.tupla_entrenamiento_a_grabar = None

    # Recibe un tablero y retorna para dicho tablero, el movimiento de la forma (ficha, movimiento)
    # Que tiene la mayor valoracion
    def mejor_jugada(self, tablero):
        # grabar en disco los datos de entrenamiento
        if (self.tupla_entrenamiento_a_grabar is not None and self.entrenando):
            valoracion_actual = self.valoracion(tablero.obtener_tupla())
            self.tupla_entrenamiento_a_grabar += [valoracion_actual]
            self.grabar_datos_en_disco(self.tupla_entrenamiento_a_grabar, self.archivo_entrenamiento)
            self.tupla_entrenamiento_a_grabar = []
        self.tupla_entrenamiento_a_grabar = tablero.obtener_tupla().copy()
        
        # buscar jugada
        fichas = tablero.negras if self.color == Color.Negras else tablero.blancas
        valoracion_maxima = None
        for ficha in fichas:
            for movimiento in tablero.posibles_movimientos(ficha):
                nuevo_posible_tablero = tablero.copy()
                nuevo_posible_tablero.actualizar_tablero(ficha, movimiento, self.color)
                if nuevo_posible_tablero.hay_ganador():
                    movimiento_maximo = movimiento
                    ficha_maxima = ficha
                    print("tablero ganador")
                    nuevo_posible_tablero.imprimir_tablero_con_fichas()
                    tablero.actualizar_tablero(ficha_maxima, movimiento_maximo, self.color)
                    if self.entrenando:
                        print("voy a ganar!!")
                        # se esta grabando la tupla que tiene los valores del tablero y su valoracion al final
                        # esta valoracion final cuenta como la v(tn+1)
                        tupla_ganadora_a_grabar = tablero.obtener_tupla().copy()
                        v_train = self.valoracion(tupla_ganadora_a_grabar)
                        tupla_ganadora_a_grabar += [v_train]
                        print(tupla_ganadora_a_grabar)
                        self.grabar_datos_en_disco(tupla_ganadora_a_grabar, self.archivo_entrenamiento)
                        self.tupla_entrenamiento_a_grabar = None
                        print("tupla deberia estar grabada")
                    return tablero
                else:
                    valoracion = self.valoracion(nuevo_posible_tablero.obtener_tupla())
                    if valoracion_maxima is None or valoracion > valoracion_maxima:
                        valoracion_maxima = valoracion
                        ficha_maxima = ficha
                        movimiento_maximo = movimiento
        tablero.actualizar_tablero(ficha_maxima, movimiento_maximo, self.color)
        return tablero

    # no es necesaria ahora?
    def actualizar_pesos(self, v_train, v_tupla, tupla_tablero):
        error_valoracion = (v_train - v_tupla)
        self.pesos[0] = self.pesos[0] + self.factor_aprendizaje * error_valoracion
        for i in range(len(tupla_tablero)):
            self.pesos[i+1] = self.pesos[i+1] + self.factor_aprendizaje * error_valoracion * tupla_tablero[i]


	# Parsea el archvio con los valores de entrenamiento y realiza el ajuste de mínimos cuadrados
    def ajuste_minimos_cuadrados(self):
        print("ajusto_minimos_cuadrados")
        archivo_entrenamiento = open(self.archivo_entrenamiento, 'r')
        lista_tuplas_sin_procesar_aux = archivo_entrenamiento.readlines()
        lista_tuplas_sin_procesar_aux = [tupla.strip() for tupla in lista_tuplas_sin_procesar_aux]
        lista_tuplas_sin_procesar = list(reversed(lista_tuplas_sin_procesar_aux))
        archivo_entrenamiento.close()
        for tupla_sin_procesar in lista_tuplas_sin_procesar:
            tupla = []
            tupla = tupla_sin_procesar.split()
            v_train = float(tupla[8])
            for idx in range(0,8):
                tupla[idx] = int(tupla[idx])
            v_tupla = self.valoracion(tupla[0:8])
            error_valoracion = (v_train - v_tupla)
            self.pesos[0] = self.pesos[0] + self.factor_aprendizaje * error_valoracion
            for i in range(len(tupla)-1):
                self.pesos[i+1] = self.pesos[i+1] + self.factor_aprendizaje * error_valoracion * tupla[i]
        self.grabar_datos_en_disco(self.pesos, "pesos_finales.txt")

    # FUNCIONES DE MANEJO DE ARCHIVOS

    def set_archivo_entrenamiento(self, ruta_archivo):
        self.archivo_entrenamiento = ruta_archivo

    #  Lee los pesos del archivo de pesos y los carga en los atributos del jugador
    def cargar_pesos(self, ruta_archivo):
        try:
            archivo_pesos=open(ruta_archivo,"r") 
        except IOError: 
            archivo_pesos.close()
            return "Hubo un error al intentar abrir el archivo"
        pesos = []
        linea = archivo_pesos.readline()
        archivo_pesos.close()
        pesos = linea.split()
        pesos = list(map(float, pesos))
        self.pesos = pesos
        return pesos

    # Escribe en el archivo de pesos, los atributos de los pesos
    def guardar_pesos(self, archivo_pesos):
        pesos_a_guardar = self.pesos.copy()
        self.grabar_datos_en_disco(pesos_a_guardar, archivo_pesos)
    
    # dados unos datos en forma de lista y un archivo objetivo, 
    # escribe esos elementos separados por un espacio
    def grabar_datos_en_disco(self, datos, ruta_archivo):
        try:
            archivo=open(ruta_archivo,"a+")
        except IOError: 
            archivo.close()
            return "Hubo un error al intentar abrir/escribir el archivo"
        linea_nueva = ""
        for elemento in datos:
            linea_nueva += (str(elemento) + " ")
        archivo.write(linea_nueva + "\n")
        archivo.close()

if __name__ == '__main__':
    jug = AI(Color.Negras, "AI1", None, True, 0.2)
    jug.guardar_pesos("pesos.txt")
    jug.grabar_datos_en_disco([1,1,3,0,5,5,1,1,0.2], "entrenamiento.txt")
    jug.grabar_datos_en_disco([1,1,3,0,5,5,0,1,0.1], "entrenamiento.txt")
    jug.ajuste_minimos_cuadrados()

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
            val = self.pesos[0]
            for i in range(len(tupla)):
                val += self.pesos[i+1]*tupla[i]
            return val

    # Recibe un tablero y retorna para dicho tablero, el movimiento de la forma (ficha, movimiento)
    # Que tiene la mayor valoracion
    def mejor_jugada(self, tablero):
        valoracion_tablero = self.valoracion(tablero.obtener_tupla())
        fichas = tablero.negras if self.color == Color.Negras else tablero.blancas
        valoracion_maxima = None
        for ficha in fichas:
            for movimiento in tablero.posibles_movimientos(ficha):
                nuevo_posible_tablero = tablero.copy()
                nuevo_posible_tablero.actualizar_tablero(ficha, movimiento, self.color)
                if nuevo_posible_tablero.hay_ganador():
                    tablero.actualizar_tablero(ficha_maxima, movimiento_maximo, self.color)
                    if self.entrenando:
                        # TODO: guardar los pesos y la valoración de entrenamiento (v_train)
                        self.actualizar_pesos(self.valoracion(tablero.obtener_tupla()), valoracion_tablero, tablero.obtener_tupla())
                    return tablero
                else:
                    valoracion = self.valoracion(nuevo_posible_tablero.obtener_tupla())
                    if valoracion_maxima is None or valoracion > valoracion_maxima:
                        valoracion_maxima = valoracion
                        ficha_maxima = ficha
                        movimiento_maximo = movimiento
        tablero.actualizar_tablero(ficha_maxima, movimiento_maximo, self.color)
        if self.entrenando:
            # TODO: guardar los pesos y la valoración de entrenamiento (v_train)
            self.actualizar_pesos(valoracion_maxima, valoracion_tablero, tablero.obtener_tupla())
        return tablero
    
    def actualizar_pesos(self, v_train, v_tupla, tupla):
        error_valoracion = (v_train - v_tupla)
        self.pesos[0] = self.pesos[0] + self.factor_aprendizaje * error_valoracion
        for i in range(len(tupla)):
            self.pesos[i+1] = self.pesos[i+1] + self.factor_aprendizaje * error_valoracion * tupla[i]
    
    def guardar_tupla(self, tupla):
        pesos_a_guardar = tupla.copy().append(valoracion(tupla))
        guardar_tupla(weights_file_path, [tupla])

    def cargar_pesos(file_path):
        try:
            archivo_pesos=open(file_path,"r") 
        except IOError: 
            archivo_pesos.close()
            return "Hubo un error al intentar abrir el archivo"
        pesos = []
        linea = archivo_pesos.readline()
        while(linea != ""):
            pesos.append(map(toFloat,linea.split()))
            linea = archivo_pesos.readline()
        archivo_pesos.close()
        return pesos
    
    def guardar_tupla(file_path, tupla):
        try:
            archivo_entrenamiento=open(file_path,"a+")
        except IOError: 
            archivo_entrenamiento.close()
            return "Hubo un error al intentar abrir/escribir el archivo"
        for peso in pesos:
            linea_nueva = ""
            for wi in peso:
                linea_nueva += (str(wi) + " ")
            linea_nueva = linea_nueva[:-1]
            archivo_entrenamiento.write(linea_nueva + "\n")
        archivo_entrenamiento.close()
        return pesos

	# Parsea el archvio con los valores de entrenamiento y realiza el ajuste de mínimos cuadrados
    def ajuste_minimos_cuadrados(self, archivo_entrenamiento):
        archivo_entrenamiento = open(archivo_entrenamiento, 'r')
        lista_tuplas_sin_procesar = reversed(list(archivo_entrenamiento))
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
        archivo_pesos_finales = open("pesos_finales.txt", "w+")
        string_pesos = ""
        for peso in self.pesos:
            string_pesos += str(peso) + " "
        archivo_pesos_finales.write(string_pesos + "\r\n")
        archivo_pesos_finales.close()


if __name__ == '__main__':
    jug = AI(Color.Negras, "AI1", None, True, 1)
    jug.ajuste_minimos_cuadrados("entrenamiento.txt")

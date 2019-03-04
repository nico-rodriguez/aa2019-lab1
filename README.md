# AA2019-Lab1

Laboratorio 1 del curso Aprendizaje Automático 2019.
Se implementa un algoritmo de aprendizaje automático para jugar a las damas chinas (dos jugadores).

Función objetivo:
Función que dado un tablero devuelve un valor real de valoración, cuanto más grande sea ese valor, más favorable será el tablero para la AI.

Las blancas comienzan abajo, las negras arriba.
La versión más entrenada del AI siempre juega con las blancas.

Representación:
(x1,x2,x3,x4,x5,x6,x7,x8)

Donde:
1.  x1 es la suma de las distancias verticales de todas las fichas blancas hacia la última fila libre de la punta opuesta
2.  x2 es lo mismo que x1 pero para las fichas negras
3.  x3 es la cantidad de fichas blancas que llegaron a la punta opuesta del tablero
4.  x4 es lo mismo que x3 pero para las fichas negras
5.  x5 es la cantidad de movimientos de blancas que disminuyen la distancia a la punta opuesta
6.  x6 es lo mismo que x5 pero para las fichas negras
7.  x7 es la cantidad de movimientos posibles de las blancas
8.  x8 es lo mismo que x7 pero para las fichas negras

Entonces, la función objetivo se representa como:
F(x1,x2,x3,x4,x5,x6,x7,x8) = w0 + w1*x1 + ... + w8*x8
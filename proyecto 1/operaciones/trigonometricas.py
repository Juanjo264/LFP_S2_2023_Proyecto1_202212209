from operaciones.expresion import *
import math
from Arbol import *

class ExpresionTrigonometrica(Expresion):
    def __init__(self, tipo, valor, linea, columna):
        self.tipo = tipo
        self.valor = valor
        self.linea = linea
        self.columna = columna

    def interpretar(self):
        valor = self.valor

        nodo = None

        if isinstance(self.valor, Expresion):
            valor = self.valor.interpretar()
            nodo = arbol.obtenerUltimoNodo()
        else:
            valor = self.valor
            nodo = arbol.agregarNodo(str(valor))

        print("`" * 20)
        print("tipo: ", self.tipo)
        print("valor: ", valor)
        resultado = None
        if self.tipo == "seno":
            resultado = math.sin(math.radians(valor))  
        elif self.tipo == "coseno":
            resultado = math.cos(math.radians(valor))
        elif self.tipo == "tangente":
            resultado = math.tan(math.radians(valor))
        elif self.tipo == "inverso":
            resultado = 1/valor

        raiz = arbol.agregarNodo(f"{self.tipo}\\n{str(round(resultado, 2))}")
        arbol.agregarArista(raiz, nodo)

        return round(resultado, 2)

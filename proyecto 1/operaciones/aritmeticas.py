from operaciones.expresion import *
from Arbol import *
import math


class ExpresionAritmetica(Expresion):
    def __init__(self, tipo, valor1, valor2, linea, columna):
        self.tipo = tipo
        self.valor1 = valor1
        self.valor2 = valor2
        self.linea = linea
        self.columna = columna

    def interpretar(self):
        global arbol

        valor1 = self.valor1
        valor2 = self.valor2

        nodo1 = None
        nodo2 = None

        if isinstance(self.valor1, Expresion):
            valor1 = self.valor1.interpretar()
            nodo1 = arbol.obtenerUltimoNodo()
            print("RESULTADO: ", valor1)
        else:
            valor1 = self.valor1
            nodo1 = arbol.agregarNodo(str(valor1))
        if isinstance(self.valor2, Expresion):
            valor2 = self.valor2.interpretar()
            nodo2 = arbol.obtenerUltimoNodo()
            print("RESULTADO: ", valor2)
        else:
            valor2 = self.valor2
            nodo2 = arbol.agregarNodo(str(valor2))

        print("OPERACION: ", self.tipo)
        print("NODOS HIJOS: ", nodo1, nodo2)

        print("`" * 20)
        print("tipo: ", self.tipo)
        print("valor1: ", valor1)
        print("valor2: ", valor2)

        resultado = None
        if self.tipo == "suma":
            resultado = valor1 + valor2
        elif self.tipo == "resta":
            resultado = valor1 - valor2
        elif self.tipo == "multiplicacion":
            resultado = valor1 * valor2
        elif self.tipo == "division":
            resultado = valor1 / valor2
        elif self.tipo == "potencia":
            resultado = math.pow(valor1, valor2)
        elif self.tipo == "raiz":
            resultado = math.pow(valor1, 1 / valor2)
        elif self.tipo == "mod":
            resultado = valor1 % valor2

        if arbol == None:
            print("arbol es None")

        raiz = arbol.agregarNodo(f"{self.tipo}\\n{str(round(resultado, 2))}")
        arbol.agregarArista(raiz, nodo1)
        if self.valor2 is not None:
            arbol.agregarArista(raiz, nodo2)

        return round(resultado, 2)

    def __str__(self) -> str:
        return (
            super().__str__()
            + " tipo: "
            + self.tipo
            + " valor1: "
            + str(self.valor1)
            + " valor2: "
            + str(self.valor2)
        )

from collections import namedtuple
from operaciones import *
from operaciones.aritmeticas import ExpresionAritmetica
from operaciones.trigonometricas import ExpresionTrigonometrica
from Arbol import *

Token = namedtuple("Token", ["lexema", "linea", "columna"])

line = 1
col = 1

tokens = []
errores = []


configuracion = {
    "texto": None,
    "fondo": None,
    "fuente": None,
    "forma": None,
}


def tokenize_string(input_str, i):
    token = ""
    for char in input_str:
        if char == '"':
            return [token, i]
        token += char
        i += 1
    print("Error: string no cerrado")


def tokenize_number(input_str, i):
    token = ""
    isDecimal = False
    for char in input_str:
        if char.isdigit():
            token += char
            i += 1
        elif char == "." and not isDecimal:
            token += char
            i += 1
            isDecimal = True
        else:
            break
    if isDecimal:
        return [float(token), i]
    return [int(token), i]


def tokenize_input_analizar(input_str):
    global line, col, tokens
    i = 0
    while i < len(input_str):
        char = input_str[i]
        if char.isspace():
            if char == "\n":
                line += 1
                col = 1
            elif char == "\t":
                col += 4
            else:
                col += 1
            i += 1
        elif char == '"':
            string, pos = tokenize_string(input_str[i + 1 :], i)
            col += len(string) + 1
            i = pos + 2
            token = Token(string, line, col)
            tokens.append(token)
        elif char in ["{", "}", "[", "]", ",", ":"]:
            print({"Lexema": char, "linea": line, "columna": col, "No": i})
            col += 1
            i += 1
            token = Token(char, line, col)
            tokens.append(token)
        elif char.isdigit():
            number, pos = tokenize_number(input_str[i:], i)
            col += pos - i
            i = pos
            token = Token(number, line, col)
            tokens.append(token)
        else:
            error = {
                "mensaje": f"Carácter desconocido: {char}",
                "linea": line + 1,
                "columna": col + 1,
            }
            i += 1
            col += 1


def tokenize_input_error(input_str):
    global line, col, tokens, errores
    i = 0
    while i < len(input_str):
        char = input_str[i]
        if char.isspace():
            if char == "\n":
                line += 1
                col = 1
            elif char == "\t":
                col += 4
            else:
                col += 1
            i += 1
        elif char == '"':
            string, pos = tokenize_string(input_str[i + 1 :], i)
            col += len(string) + 1
            i = pos + 2
            token = Token(string, line, col)
            tokens.append(token)
        elif char in ["{", "}", "[", "]", ",", ":"]:
            col += 1
            i += 1
            token = Token(char, line, col)
            tokens.append(token)
        elif char.isdigit():
            number, pos = tokenize_number(input_str[i:], i)
            col += pos - i
            i = pos
            token = Token(number, line, col)
            tokens.append(token)
        else:
            error = {
            "No": len(errores) + 1,
                "descripcion": {
                    "Caracter desconocido: ": char,
                    "tipo": "Lexico",
                    "linea": line + 1,
                    "columna": col + 1,
                }
            }
            errores.append(error)
            i += 1
            col += 1


def tokenize_input_reporte(input_str):
    global line, col, tokens
    i = 0
    while i < len(input_str):
        char = input_str[i]
        if char.isspace():
            if char == "\n":
                line += 1
                col = 1
            elif char == "\t":
                col += 4
            else:
                col += 1
            i += 1
        elif char == '"':
            string, pos = tokenize_string(input_str[i + 1 :], i)
            col += len(string) + 1
            i = pos + 2
            token = Token(string, line, col)
            tokens.append(token)
        elif char in ["{", "}", "[", "]", ",", ":"]:
            col += 1
            i += 1
            token = Token(char, line, col)
            tokens.append(token)
        elif char.isdigit():
            number, pos = tokenize_number(input_str[i:], i)
            col += pos - i
            i = pos
            token = Token(number, line, col)
            tokens.append(token)
        else:
            error = {
                "mensaje": f"Carácter desconocido: {char}",
                "linea": line + 1,
                "columna": col + 1,
            }
            i += 1
            col += 1


def get_instruccion():
    global tokens
    operacion = None
    value1 = None
    value2 = None
    while tokens:
        token = tokens.pop(0)
        if token.lexema == "operacion":
            tokens.pop(0)
            operacion = tokens.pop(0).lexema
        elif token.lexema == "valor1":
            tokens.pop(0)
            value1 = tokens.pop(0).lexema
            if value1 == "[":
                value1 = get_instruccion()
        elif token.lexema == "valor2":
            tokens.pop(0)
            value2 = tokens.pop(0).lexema
            if value2 == "[":
                value2 = get_instruccion()
        elif token.lexema in ["texto", "fondo", "fuente", "forma"]:
            tokens.pop(0)
            configuracion[token.lexema] = tokens.pop(0).lexema
        else:
            pass
        if operacion and value1 and value2:
            return ExpresionAritmetica(operacion, value1, value2, 0, 0)
        if operacion and operacion in ["seno"] and value1:
            return ExpresionTrigonometrica(operacion, value1, 0, 0)
        if operacion and operacion in ["coseno"] and value1:
            return ExpresionTrigonometrica(operacion, value1, 0, 0)
        if operacion and operacion in ["tangente"] and value1:
            return ExpresionTrigonometrica(operacion, value1, 0, 0)
        if operacion and operacion in ["inverso"] and value1:
            return ExpresionTrigonometrica(operacion, value1, 0, 0)
    return None




def create_instructions():
    global tokens
    global arbol
    instrucciones = []
    while tokens:
        instruccion = get_instruccion()
        if instruccion:
            instrucciones.append(instruccion)
    arbol.agregarConfiguracion(configuracion)
    return instrucciones


def analizar_a(entrada):
    global tokens
    tokens.clear()
    tokenize_input_analizar(entrada)
    return tokens


def error_a(entrada):
    global tokens
    global errores
    errores.clear()
    tokenize_input_error(entrada)
    return errores

def reporte_a(entrada):
    global tokens
    tokenize_input_reporte(entrada)
    arbol.dot.clear()
    arbol.agregarConfiguracion(configuracion)
    instrucciones = create_instructions()
    for i in instrucciones:
        print("RESULTADO INSTRUCCION: ", i.interpretar())
    return arbol
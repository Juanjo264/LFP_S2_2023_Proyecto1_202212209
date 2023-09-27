# MANUAL TECNICO 

## Requisitos del sistema

Para que nuestro programa funcione correctamente tenemos que tener instalados algunos programas:

1. Instalar Visual Studio Code en nuestra computadora.
2. Instalar Python, preferiblemente la version mas reciente o que sea estable.
3. Tener instalado Graphviz, para las graficas.
4. Utilizar extenciones para previsualizar grafos y archivos.

## Archivo main.py
Este archivo contiene nuestra interfaz grafica, contando con botones y los diferentes metoos para que funcione. 

```python
class VentanaPrincipal:
    def __init__(self, root):
        self.root = root
        self.root.title("PROYECTO 1")

        self.crear_interfaz()

    def crear_interfaz(self):
        self.button_frame_top = tk.Frame(self.root, bg="blue")  
        self.button_frame_top.pack(fill="both", expand=True)


        self.file_button = tk.Menubutton(self.button_frame_top, text="ARCHIVO", bg="lavender", padx=10, relief=tk.RAISED)
        self.file_button.configure(bg="White")
        self.file_button.pack(side=tk.LEFT, padx=5) 
        self.file_menu = tk.Menu(self.file_button, tearoff=0)
        self.file_button.config(menu=self.file_menu)
        self.file_menu.add_command(label="Abrir Archivo", command=self.open_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Guardar", command=self.save_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Guardar como", command=self.save_file_as)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Salir", command=quit)

        self.boton1 = tk.Button(self.button_frame_top, text="analizar_texto", command=self.analizar_texto, bg="White", padx=10)
        self.boton2 = tk.Button(self.button_frame_top, text="errores", command=self.errores, bg="White", padx=10)
        self.boton3 = tk.Button(self.button_frame_top, text="reporte", command=self.reporte, bg="White", padx=10)

        self.boton1.pack(side=tk.LEFT, padx=5) 
        self.boton2.pack(side=tk.LEFT, padx=5) 
        self.boton3.pack(side=tk.LEFT, padx=5)  

        self.parte_izquierda = ScrollText(self.root)
        self.parte_izquierda.pack(side="left", fill="both", expand=True)

        self.parte_derecha = TextLineNumbers(self.root)
        self.parte_derecha.pack(side="right", fill="both", expand=True)

        self.parte_izquierda.config(width=200, height=300)
        self.parte_derecha.config(width=400, height=300)

```
La clase  VentanaPrincipal contiene los botones para que funncione nuestro programa que son el boton de Abrir Archivo, Guardar, Guardar como, Salir y los botones de funciones para el texto que seran Analizar, Errores y Reporte. 

```python

    def save_file_as(self):
        filepath = asksaveasfilename(
            defaultextension="json",
            filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")],
        )
        if not filepath:
            return
        with open(filepath, "w") as output_file:
            text = self.parte_izquierda.get(1.0, tk.END)
            output_file.write(text)
```
Este metodo nos guarda nuestro texto como uno nuevo, entonces nos abre una ventana del navegador de archivos, en .json y colocamos el nombre y lo guardamos. 

``` python
  def open_file(self):
        filepath = askopenfilename(
            filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")]
        )
        if not filepath:
            return

        self.current_file = filepath  
        self.parte_izquierda.delete(1.0, tk.END)
        with open(filepath, "r") as input_file:
            text = input_file.read()
            self.parte_izquierda.insert(tk.END, text)
```
Con este metodo abrimos una ventana para seleccionar un archivo .json en modo lectura y que se nos muestre en nuestra ventana para editar el texto.

```python
    def save_file(self):
        if hasattr(self, 'current_file'):
            with open(self.current_file, "w") as output_file:
                text = self.parte_izquierda.get(1.0, tk.END)
                output_file.write(text)
        else:
            messagebox.showwarning( "error.")
```
Este metodo es parecido al anterior, solo que guarda lo que editemos en el mismo archivo, no crea uno aparte, solo guarda los cambios, si no hay archivo abierto mostrara un mensaje de error  

```python
    def analizar_texto(self):
        text = self.parte_izquierda.get(1.0, tk.END)
        tokens = analizar_a(text)

        popup_window = tk.Toplevel(self.root) 
        popup_window.title("Tokens")
        
        tokens_text = tk.Text(popup_window, height=300, width=250, bg="lavender")
        tokens_text.pack()

        for token in tokens:
            tokens_text.insert(tk.END, str(token) + "\n")
```
Esta opcion llama a los tokens, y usa el metodo analizar_a de nuestro archivo analizador que mas adelante se detalla, entonces abre una ventana nueva llamada Tokens y nos muestra los tokens encontrados. 


```python
    def errores(self):
        texte = self.parte_izquierda.get(1.0, tk.END)
        errores = error_a(texte)


        errores_dict = {"errores": errores}

        popup_windowe = tk.Toplevel(self.root)
        popup_windowe.title("errores")
            
        errores_text = tk.Text(popup_windowe, height=300, width=250, bg="lavender")
        errores_text.pack()

        for error in errores:
            errores_text.insert(tk.END, str(error) + "\n")

        with open('RESULTADOS_202212209.json', 'w', encoding='utf-8') as json_file:
            json.dump(errores_dict, json_file, indent=4)
```
Este metodo me muestran los errores usando el metodo error_a de nuestro archivo analizador.py ese archivo nos los almacena en una lista que luego mostramos en uan ventana, pero tambien los guardamos en un archivo .json llamado Resultados_202212209.json. 

```python
    def reporte(self):
        print("Generando reporte")
        text = self.parte_izquierda.get(1.0, tk.END) 
        arbol = reporte_a(text)
        print(arbol.dot.source)
        
        arbol.dot.render("Grafica", view=False)
        
        print("Reporte generado en Grafica.pdf")

```
Y nuestro ultimo metodo llama a la funcion reporte_a de nuestro analizador.py y escribimos en un archivo.dot los nodos para generar nuestra grafica, y muestra un mensaje de Reporte generado en Grafica.pdf, luego solo la buscamos para ver la grafica. 

## Archivo Analizador.py

### tokens

Creamos nuestros tokes que contendran el lexema, linea y columna, tambien sabemos que tendremos lineas y columnas, y al final la configuracion para graficar.

```python
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
```

Ahora veremos la logica que lleva nuestro analizador:

```python
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
```
Recorremos el texto de nuestro archivo de texto.json, entonces cuando encontramos un \n es un salto de linea, entonces vamos incrementado las filas, cuando encontramos un \t es un tabulador, que son 4 espacion osea las columnas, y aumenta 1 cuando haya espacio en blanco. 
Cuando encontremos una comilla doble, significa que viene alguna exprecion, y verificamos si e suno de estos: "{", "}", "[", "]", ",", ":", y lo guardamos como un lexema, y colocamos que fila y columna tiene, esto lo guardamos en la lista token con el metodo append, el lexema puede ser un numero, entonces usamos char.isdigit y lo guardamos de la misma forma, ya si no es ninguno, sera un error, y lo guardamos en una lista. 

```python
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

```

Con el metodo def get_instruccion(), lo utilizamos para las operaciones, primero buscamos el token que diga operacion, y guardamos el siguiente token para saber que operacion es usando el lexema, si viene u "[" es que es una operacion anidada, y ya que termina se almacena la configuracion de ["texto", "fondo", "fuente", "forma"], si es una operacion aritmetica, usamos la clase ExpresionAritmetica, si no es, usamos la clase ExpresionTrigonometrica, y verificamos que operacion es.

Despues tenemos el metodo def create_instructions():
y llamamos a nuestro archivo arbol para agregar las configuraciones, usando la clase arbol

## Archivo Arbol.py

```python
class Arbol:
    def __init__(self):
        timestr = time.strftime("%Y%m%d-%H%M%S")
        self.dot = graphviz.Digraph(comment=f"Graph {timestr}")
        self.counter = 0

    def agregarConfiguracion(self, confg):
        self.dot.attr(
            "node",
            style="filled",
            fillcolor=confg["fondo"],
            fontcolor=confg["fuente"],
            shape=confg["forma"],
        )

    def agregarNodo(self, valor):
        nombre = f"nodo{self.counter}"
        self.dot.node(nombre, valor)
        self.counter += 1
        return nombre

    def agregarArista(self, nodo1: str, nodo2: str):
        self.dot.edge(nodo1, nodo2)

    def generarGrafica(self):
        self.dot.render("Arbol", view=True)
        self.dot.save("Arbol.dot")

    def obtenerUltimoNodo(self):
        return f"nodo{self.counter - 1}"

arbol = Arbol()

```
Primero mostramos la hora, he iniciamos el contador en 0, despues tenemos el metodo de la configuracion, que contendra nuestro archivo de entrada los datos de fondo, color de fuente y figura, despues tenemos el metodo agregar nodo, que a cada nodo le colocamos un nombre, este lo agregamos con el valor, y se suma 1 para que cambie el nombre y lo retornamos, despues tenemos el metodo agregarArista que obtiene los valores 1 y 2 para poner el resultado, el metodo generarGrafica generamos la grafica, y por ultimo el metodo obtenerUltimoNodo y se utiliza para realizar operaciones en el nodo más reciente.


## Operaciones
En esta carpeta tenemos todas nuestras operaciones matematicas que vayamos a usar, usamos la libreria para algunas como seno, coseno o tangente, no es tan complicado de entender esta parte ya que son algo basicas las operaciones, lo que si tenemos que ver es la forma que usamos el arbol aqui para la grafica. 
```python
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
```
Con el metodo interpretar se encarga de evaluar la expresión aritmética y devolver su resultado, comenzamos obteniendo 2 valores, estos seran expreciones y llamamos al metodo interpretar para el resultado, luego agregamos el nodo al grafo dependiendo si es valor 1 o 2, y por ultimo ya hacemos la operacion para obtener el resultado y que nos cree el nodo hacia ese resultado. 


```python
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

```
Las trigonometricas funcionan de la msima manera que las aritmeticas, solo que ahora con un valor, pero sigue la misma secuencia. 

Con esto ya tendriamos la logica de nuestro programa y como funcionan los archivos en conjunto y metodos para lograr nuestro objetivo. 

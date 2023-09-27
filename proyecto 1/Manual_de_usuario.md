# MANUAL TECNICO 

## Requisitos del sistema

Para que nuestro programa funcione correctamente tenemos que tener instalados algunos programas:

1. Instalar Visual Studio Code en nuestra computadora.
2. Instalar Python, preferiblemente la version mas reciente o que sea estable.
3. Tener instalado Graphviz.
4. Instalar un lector de pdf.
  

## Interfaz
Cuando iniciemos nuestro programa nos saldra una ventana donde podemos escribir cualquier texto, y arriba 4 botones con diferentes funciones que seran detalladas mas adelante. 
![Interfaz](imagenes/interfaz1.PNG)

### Boton ARCHIVO

![Alt text](imagenes/boton_archivo.PNG)

Este es un boton con mas funciones adentro, tiene la opcion de Abrir archivo para abrir un archivo .json que tengamos en nuestra computadora como el siguiente ejemplo:

![Alt text](imagenes/opcion_abrir.PNG)

Ya que tenemos nuestro archivo abierto nos tendria que salir el texto en nuestra ventana para editar y seguir usando el programa, ahora el boton Guardar, este boton nos guardara los cambios que realizemos a nuestro texto, siempre y cuando tengas un archivo abierto para editar, porque nos puede salir este error si antes no abrimos un archivo:

![Alt text](imagenes/errorGuardar.PNG)

El boton de guardar como es parecido al anterior, solamente que ahora nos da la opcion de guardar el archivo con otro nombre y en la ubicacion que escojamos, como en el siguiete ejemplo:

![Alt text](imagenes/guardarcomo.PNG)

Por ultimo tenemos el boton de Salir, que finaliza la ejecucion de nuestro programa

### Boton analizar_texto
Este boton escanea nuestro texto y nos muestra los tokens que reconocio en una nueva ventana llamada tokens, y entre mas grande nmuestro texto, mas grande sera la lista, en el ejempolo que usamos, colocamos un ejemplo algo largo para ver que funcionara correctamente.
![Alt text](imagenes/analizar.PNG)


### Boton errores 
Este boton como bien dice, nos mostrara los errores que tiene nuestro texto, como por ejemplo si trae un simbolo que nos es reconocido por nuestro programa, como puede ser el simbolo "$" y automaticamente nos los guarda en un archivo llamado RESULTADOS_202212209.json aqui tendremos los errores que se encontraron, a continuacion hay un ejemplo: 

Ejemplo de ventana errores
![Alt text](imagenes/errores.PNG)

Ejemplo del archivo RESULTADOS_202212209.json
![Alt text](imagenes/archivo_salida.PNG)

### Boton reporte
Este es nuestro ultimo boton, lo que hace es que recorre nuestro texto y realiza las operaciones matematicas, y nos genera una grafica con los valores y resultados en un archivo .pdf y se configura dependiendo nuestro archivo de texto, aqui es donde tenemos que usar el lector de pdf para ver la grafica, aqui hay un ejemplo de una grafica:

![Alt text](imagenes/grafica.PNG)

Todo se guardara en la ruta de nuestro programa, asi que ahi podremos ir a buscar nuestros archivos, y estas serian todas las opciones de nuestro programa.
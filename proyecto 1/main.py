import tkinter as tk
import tkinter as ttk
from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import asksaveasfilename, askopenfilename
from Analizador import analizar_a
from Analizador import reporte_a
from Analizador import error_a
import json


from Arbol import *

class ScrollText(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.text = tk.Text(
            self,
            bg="lavender",  
            foreground="black", 
            insertbackground="black", 
            selectbackground="RoyalBlue2",  
            width=520,
            height=250,
            font=("Arial", 12), 
        )

        self.scrollbar = tk.Scrollbar(self, orient=tk.VERTICAL, command=self.text.yview)
        self.text.configure(yscrollcommand=self.scrollbar.set)

        self.numberLines = TextLineNumbers(self, width=40, bg="azure") 
        self.numberLines.attach(self.text)

        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.numberLines.pack(side=tk.LEFT, fill=tk.Y, padx=(5, 0))
        self.text.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.text.bind("<Key>", self.onPressDelay)
        self.text.bind("<Button-1>", self.numberLines.redraw)
        self.scrollbar.bind("<Button-1>", self.onScrollPress)
        self.text.bind("<MouseWheel>", self.onPressDelay)

    def onScrollPress(self, *args):
        self.scrollbar.bind("<B1-Motion>", self.numberLines.redraw)

    def onScrollRelease(self, *args):
        self.scrollbar.unbind("<B1-Motion>", self.numberLines.redraw)

    def onPressDelay(self, *args):
        self.after(2, self.numberLines.redraw)

    def get(self, *args, **kwargs):
        return self.text.get(*args, **kwargs)

    def insert(self, *args, **kwargs):
        return self.text.insert(*args, **kwargs)

    def delete(self, *args, **kwargs):
        return self.text.delete(*args, **kwargs)

    def index(self, *args, **kwargs):
        return self.text.index(*args, **kwargs)

    def redraw(self):
        self.numberLines.redraw()

class TextLineNumbers(tk.Canvas):
    def __init__(self, *args, **kwargs):
        tk.Canvas.__init__(self, *args, **kwargs, highlightthickness=0)
        self.textwidget = None

    def attach(self, text_widget):
        self.textwidget = text_widget

    def redraw(self, *args):
        self.delete("all")

        i = self.textwidget.index("@0,0")
        while True:
            dline = self.textwidget.dlineinfo(i)
            if dline is None:
                break
            y = dline[1]
            linenum = str(i).split(".")[0]
            self.create_text(
                2,
                y,
                anchor="nw",
                text=linenum,
                fill="black", 
                font=("Arial", 12, "bold"), 
            )
            i = self.textwidget.index("%s+1line" % i)

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


    def save_file(self):
        if hasattr(self, 'current_file'):
            with open(self.current_file, "w") as output_file:
                text = self.parte_izquierda.get(1.0, tk.END)
                output_file.write(text)
        else:
            messagebox.showwarning( "error.")

    def analizar_texto(self):
        text = self.parte_izquierda.get(1.0, tk.END)
        tokens = analizar_a(text)

        popup_window = tk.Toplevel(self.root) 
        popup_window.title("Tokens")
        
        tokens_text = tk.Text(popup_window, height=300, width=250, bg="lavender")
        tokens_text.pack()

        for token in tokens:
            tokens_text.insert(tk.END, str(token) + "\n")


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


    def reporte(self):
        print("Generando reporte")
        text = self.parte_izquierda.get(1.0, tk.END) 
        arbol = reporte_a(text)
        print(arbol.dot.source)
        
        arbol.dot.render("Grafica", view=False)
        
        print("Reporte generado en Grafica.pdf")


if __name__ == "__main__":
    root = tk.Tk()
    app = VentanaPrincipal(root)
    root.mainloop()
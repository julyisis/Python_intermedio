import tkinter as tk
from tkinter import ttk

class FramePrincipal(tk.Frame):
    def __init__(self, master=None, root=None):
        super().__init__(master)
        self.root = root
        self.grid(row=0, column=0, sticky="nsew")
        
        # configuración para que la ventana se expanda
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)  # Fila para el texto
        self.grid_rowconfigure(3, weight=1)  # Fila para el botón "Acerca de"
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)  # Columna para el botón "Acerca de"

        self.labelTitle()
        self.botonesPrincipales()
    
    def labelTitle(self):
        frame_titulo = tk.Frame(self)
        frame_titulo.grid(row=0, column=0, sticky="nsew")  # ocupa toda la primera fila

        # Configura la fila y columna del frame para centrar el contenido
        frame_titulo.grid_rowconfigure(0, weight=1)
        frame_titulo.grid_columnconfigure(0, weight=1)

        # Título centrado
        titulo = ttk.Label(frame_titulo, text='Sistema de Gestión Veterinaria', font=('Arial', 18, 'bold'))
        titulo.grid(row=0, column=0, padx=10, pady=10)

    def botonesPrincipales(self):
        from .vista_mascotas import FrameMascotas
        from .vista_dueños import FrameDueños
        from .vista_visitas import FrameVisitas
        from .vista_base import FrameBase
        
        # Crea un contenedor para los botones
        frame_botones = tk.Frame(self)
        frame_botones.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        # Configura fila y columna del frame para distribución uniforme
        frame_botones.grid_columnconfigure(0, weight=1)
        frame_botones.grid_columnconfigure(1, weight=1)
        frame_botones.grid_columnconfigure(2, weight=1)

        # Botón "Mascotas"
        btn_mascotas = tk.Button(frame_botones, text='Mascotas',
                                command=lambda: FrameBase.mostrarNuevaPantalla(self.master, FrameMascotas, self.master))
        btn_mascotas.config(width=10, font=('Arial', 12, 'bold'), fg='#FFFFFF', bg='#4B92D6', cursor='hand2',
                            activebackground='#6DA8E1', activeforeground='#000000')
        btn_mascotas.grid(row=0, column=0, padx=10, pady=10)

        # Botón "Dueños"
        btn_dueños = tk.Button(frame_botones, text='Dueños',
                            command=lambda: FrameBase.mostrarNuevaPantalla(self.master, FrameDueños, self.master))
        btn_dueños.config(width=10, font=('Arial', 12, 'bold'), fg='#FFFFFF', bg='#F05B2C', cursor='hand2',
                        activebackground='#F78C5D', activeforeground='#000000')
        btn_dueños.grid(row=0, column=1, padx=10, pady=10)

        # Botón "Visitas"
        btn_visitas = tk.Button(frame_botones, text='Visitas', command=lambda: FrameBase.mostrarNuevaPantalla(self.master, FrameVisitas, self.master))
        btn_visitas.config(width=10, font=('Arial', 12, 'bold'), fg='#FFFFFF', bg='#1E8C63', cursor='hand2',
                        activebackground='#4DBB8C', activeforeground='#000000')
        btn_visitas.grid(row=0, column=2, padx=10, pady=10)

        # Texto con derechos de autor
        texto = "C(2024) por Sebastian Puchetti y Julieta Castro para TecnoF - Python Intermedio"
        
        label_texto = tk.Label(self, text=texto, font=("Arial", 7), bg="#F0F0F0", justify="center")
        label_texto.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)
        
        # Botón "Acerca de"
        btn_acerca = tk.Button(self, text='Acerca de', command=self.mostrarAcercaDe)
        btn_acerca.config(width=10, font=('Arial', 8, 'bold'), fg='#FFFFFF', bg='#005E7A', cursor='hand2',
                        activebackground='#38A6C3', activeforeground='#000000')
        btn_acerca.grid(row=3, column=0, padx=20, pady=10, sticky="e")
        
    def mostrarAcercaDe(self):
        acerca_de_ventana = tk.Toplevel(self)
        acerca_de_ventana.title("Acerca de")
        acerca_de_ventana.geometry("400x300")
        acerca_de_ventana.resizable(False, False)

        acerca_de_ventana.config(bg="#F0F0F0")
        
        texto = (
            "Sistema de Gestión Veterinaria\n\n"
            "Versión: 1.0\n"
            "Desarrollado por: Sebastian Puchetti y Julieta Castro \n\n"
            "Este software permite gestionar información sobre mascotas, dueños y visitas "
            "de manera eficiente, con una interfaz sencilla y funcional."
        )

        lbl_acerca = tk.Label(
            acerca_de_ventana, text=texto, font=("Arial", 11), bg="#F0F0F0", justify="center", wraplength=350
        )
        lbl_acerca.pack(expand=True, padx=20, pady=20)

        # Botón para cerrar la ventana
        btn_cerrar = tk.Button(
            acerca_de_ventana, text="Cerrar", command=acerca_de_ventana.destroy,
            font=("Arial", 10, "bold"), bg="#A90A0A", fg="white", cursor="hand2",
            activebackground="#F35B5B", activeforeground="#000000"
        )
        btn_cerrar.pack(pady=10)

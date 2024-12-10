import tkinter as tk
from tkinter import ttk
from abc import ABC, abstractmethod
from bdd.conneciondb import*

class FrameBase(tk.Frame, ABC):
    
    def __init__(self, master=None, root=None):
        super().__init__(master, width=480, height=350)
        self.master = master
        self.root = root  # Guarda la referencia al contenedor raíz
    
    @abstractmethod
    def labelTitle(self):
        pass
    
    @abstractmethod
    def labelForm(self):
        pass

    @abstractmethod
    def inputForm(self):
        pass

    @abstractmethod
    def botonesPrincipales(self):
        pass

    @abstractmethod
    def habilitarCampos(self):
        pass

    @abstractmethod
    def bloquearCampos(self):
        pass
    
    @abstractmethod
    def tableView(self):
        pass
    
    def volver(self):
        from .vista_principal import FramePrincipal
        self.mostrarNuevaPantalla(self.master, FramePrincipal, self.root)
    
    @abstractmethod
    def editarRegistro(self):
        pass
    
    @abstractmethod
    def eliminarRegistro(self):
        pass
    
    @abstractmethod
    def limpiarFormulario(self):
        pass
    
    def cerrarVentana(self):
        try:
            conexion_db.cerrar_conexion()
            print("Conexión a la base de datos cerrada correctamente.")
        except Exception as e:
            print(f"Error al cerrar la conexión: {e}")
        finally:
            self.root.destroy()  # Cierra la ventana principal
            
    @staticmethod
    def barritaMenu(root):
        barra = tk.Menu(root)
        root.config(menu=barra, width=300, height=300)

        menu_inicio = tk.Menu(barra, tearoff=0)
        menu_ayuda = tk.Menu(barra, tearoff=0)

        # Menú principal
        barra.add_cascade(label='Inicio', menu=menu_inicio)
        barra.add_cascade(label='Ayuda', menu=menu_ayuda)

        # Submenú Inicio
        menu_inicio.add_command(label='Conectar DB', command=conexion_db.conectar)
        menu_inicio.add_command(label='Desconectar DB', command=conexion_db.cerrar_conexion)
        menu_inicio.add_command(label='Salir', command=root.destroy)

        # Submenú Ayuda
        menu_ayuda.add_command(label='Contactanos')
        menu_ayuda.add_command(label='Acerca de...')

    @staticmethod
    def mostrarNuevaPantalla(contenedor, tipo: tk.Frame, root):
        if root is None:
            raise ValueError("El valor de 'root' no puede ser None.")
        for widget in contenedor.winfo_children():
            widget.destroy()  # Elimina todos los widgets existentes
        nuevo_frame = tipo(contenedor, root)  # Pasa root al constructor del nuevo frame
        nuevo_frame.pack(fill="both", expand=True)
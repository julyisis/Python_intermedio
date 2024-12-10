import re
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from .vista_base import FrameBase
from bdd.conneciondb import conexion_db

class FrameDueños(FrameBase):
    def __init__(self, master=None, root=None):
        super().__init__(master)
        self.root = root
        self.root.protocol("WM_DELETE_WINDOW", self.cerrarVentana)
        self.pack(fill="both", expand=True)
        
        # Configura filas y columnas en la cuadrícula principal
        self.grid_rowconfigure(0, weight=1)  # Título
        for i in range(1, 6):  # Filas del formulario
            self.grid_rowconfigure(i, weight=0)
        self.grid_rowconfigure(6, weight=1)  # Tabla
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        self.labelTitle()
        self.tableView()
        self.labelForm()
        self.inputForm()
        self.botonesPrincipales()
        self.bloquearCampos()
        self.cargarTablaDueños()
    
    def validarEmail(self, email):
        """Valida que el email tenga un formato válido."""
        patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(patron, email) is not None
    
    def guardarDueños(self):
        """Guarda un nuevo dueño o actualiza uno existente en la base de datos."""
        if not all([self.entry_nombre.get(), self.entry_apellido.get(), self.entry_tel.get(),
                    self.entry_email.get(), self.entry_dir.get()]):
            messagebox.showwarning("Error", "Por favor, complete todos los campos.")
            return

        email = self.entry_email.get()
        if not self.validarEmail(email):
            messagebox.showerror("Error", "Por favor, ingrese un email válido.")
            return

        try:
            # Obtiene los datos del formulario
            nombre = self.entry_nombre.get()
            apellido = self.entry_apellido.get()
            telefono = self.entry_tel.get()
            email = self.entry_email.get()
            direccion = self.entry_dir.get()
            conexion_db.conectar()
            
            # Si id_dueño_editar está definido, actualiza; si no, inserta un nuevo registro
            if hasattr(self, 'id_dueño_editar') and self.id_dueño_editar:
                consulta = """UPDATE dueños
                            SET nombre = ?, apellido = ?, telefono = ?, email = ?, direccion = ?
                            WHERE id = ?"""
                parametros = (nombre, apellido, telefono, email, direccion, self.id_dueño_editar)
                mensaje_exito = "Dueño actualizado correctamente."
            else:
                consulta = """INSERT INTO dueños (nombre, apellido, telefono, email, direccion)
                            VALUES (?, ?, ?, ?, ?)"""
                parametros = (nombre, apellido, telefono, email, direccion)
                mensaje_exito = "Dueño guardado correctamente."

            conexion_db.insertar(consulta, parametros)

            # Muestra un mensaje de éxito y recarga la tabla
            messagebox.showinfo("Éxito", mensaje_exito)
            self.cargarTablaDueños()
            self.limpiarFormulario()

            # Bloquea los campos y resetea el modo de edición
            self.bloquearCampos()
            self.id_dueño_editar = None  # Resetea el ID de edición

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el dueño: {e}")
        
        finally:
            conexion_db.cerrar_conexion()
            
    def cargarTablaDueños(self):
        """Carga los datos de la tabla dueños en el Treeview."""
        try:
            conexion_db.conectar()
            consulta = """SELECT id, nombre, apellido, telefono, email, direccion FROM dueños"""
            datos = conexion_db.leer(consulta)

            # Limpia el Treeview antes de cargar nuevos datos
            for item in self.tree.get_children():
                self.tree.delete(item)

            # Agrega las filas recuperadas de la BDD al Treeview
            for i, fila in enumerate(datos):
                tag = 'even' if i % 2 == 0 else 'odd'  # Alterna entre las etiquetas para filas pares/impares
                self.tree.insert("", "end", values=fila, tags=(tag,))

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar la tabla: {e}")
        
    
    def labelTitle(self):
        # Configura el título en el centro de la ventana
        title_frame = tk.Frame(self)
        title_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")

        btn_volver = tk.Button(title_frame, text='Volver', command=self.volver)
        btn_volver.config(width=12, font=('Arial', 10, 'italic', 'bold'), fg='black', bg='yellow',
                        cursor='hand2', relief='raised', bd=2, activebackground='orange', activeforeground='white')
        btn_volver.pack(side="left", padx=10)

        self.btn_limpiar = tk.Button(title_frame, text='Limpiar', command=self.limpiarFormulario)
        self.btn_limpiar.config(width=10, font=('Arial', 10, 'bold'), fg='#FFFFFF', bg='#808080', cursor='hand2', activebackground= '#808080', activeforeground='#000000')
        self.btn_limpiar.pack(side="right", padx=10)

        # Título de la pantalla
        title = ttk.Label(title_frame, text='Dueños', font=('Arial', 20, 'bold'))
        title.pack(side="left", expand=True, padx=20)

    def labelForm(self):
        labels = ["Nombre:", "Apellido:", "Teléfono:", "Email:", "Dirección:", "Mascota:"]
        for i, text in enumerate(labels):
            label = tk.Label(self, text=text)
            label.config(font=('Arial', 12, 'bold'))
            label.grid(row=i+1, column=0, padx=10, pady=10, sticky="e")

    def inputForm(self):
        self.entry_nombre = tk.Entry(self, width=50)
        self.entry_apellido = tk.Entry(self, width=50)
        self.entry_tel = tk.Entry(self, width=50)
        self.entry_email = tk.Entry(self, width=50)
        self.entry_dir = tk.Entry(self, width=50)
        self.cargarTablaDueños()
        
        entries = [self.entry_nombre, self.entry_apellido, self.entry_tel, self.entry_email, self.entry_dir]
        for i, entry in enumerate(entries):
            entry.grid(row=i + 1, column=1, padx=10, pady=10, sticky="w")
    
    def botonesPrincipales(self):
        btn_frame = tk.Frame(self)  # Contenedor para los botones
        btn_frame.grid(row=6, column=0, columnspan=3, pady=10)

        self.btn_alta = tk.Button(btn_frame, text='Nuevo', command=self.habilitarCampos)
        self.btn_modi = tk.Button(btn_frame, text='Guardar', command=self.guardarDueños)
        self.btn_cance = tk.Button(btn_frame, text='Cancelar', command=self.bloquearCampos)

        botones = [self.btn_alta, self.btn_modi, self.btn_cance]
        colores = ['#1C500B', '#0D2A83', '#A90A0A']
        for i, (btn, color) in enumerate(zip(botones, colores)):
            btn.config(width=20, font=('Arial', 12, 'bold'), fg='#FFFFFF', bg=color, cursor='hand2',
                    activebackground=color, activeforeground='#000000')
            btn.grid(row=0, column=i, padx=10, pady=10)

    def tableView(self):
        # Contenedor para la tabla
        tabla_frame = tk.Frame(self, width=600, height=120)  # Incrementa la altura
        tabla_frame.grid(row=8, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        tabla_frame.grid_propagate(False)
        
        style = ttk.Style()
        style.configure("Treeview", rowheight=20)  # Aumenta altura de cada fila
        
        # Título arriba y alineado a la izquierda
        titulo_tabla = tk.Label(tabla_frame, text="Datos de la tabla", font=("Arial", 10), anchor="w", justify="left")
        titulo_tabla.pack(side="top", anchor="w", padx=15, pady=5)
        
        # Configuración del Treeview
        self.tree = ttk.Treeview(tabla_frame, height=6, columns=("id_dueño", "nombre", "apellido", "telefono", "email", "direccion"), show="headings")
        
        # Configuración de columnas
        self.tree.column("id_dueño", width=50, anchor="center")
        self.tree.column("nombre", width=100, anchor="center")
        self.tree.column("apellido", width=100, anchor="center")
        self.tree.column("telefono", width=100, anchor="center")
        self.tree.column("email", width=100, anchor="center")
        self.tree.column("direccion", width=100, anchor="center")
        
        
        # Encabezados
        self.tree.heading("id_dueño", text="ID")
        self.tree.heading("nombre", text="Nombre")
        self.tree.heading("apellido", text="Apellido")
        self.tree.heading("telefono", text="Teléfono")
        self.tree.heading("email", text="Email")
        self.tree.heading("direccion", text="Dirección")
        
        # Configuración de colores de filas
        self.tree.tag_configure('even', background='#f0f0f0')
        self.tree.tag_configure('odd', background='#ffffff')
        
        # Scrollbar vertical
        scroll_y = ttk.Scrollbar(tabla_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll_y.set)
        
        # Posicionar el Treeview
        self.tree.pack(side="left", fill="both", expand=True, padx=10)
        scroll_y.pack(side="right", fill="y")
    
        # Botones debajo de la tabla
        self.btn_editar = tk.Button(self, text='Editar', command=self.editarRegistro)
        self.btn_editar.config(width=20, font=('Arial', 12, 'bold'), fg='#FFFFFF', bg='#1C500B', cursor='hand2',
                            activebackground='#3FD83F', activeforeground='#000000')
        self.btn_editar.grid(row=9, column=0, padx=10, pady=10)
    
    def editarRegistro(self):
        """Edita el registro seleccionado en la tabla."""
        
        # Obtiene la selección actual del Treeview
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Por favor, seleccione un registro para editar.")
            return
        
        # Obtiene los valores del registro seleccionado
        valores = self.tree.item(selected_item, 'values')
        if not valores:
            messagebox.showwarning("Advertencia", "No se pudo obtener la información del registro.")
            return
    
        # Desbloquea los campos y carga los valores en el formulario
        self.habilitarCampos()
        self.entry_nombre.delete(0, tk.END)
        self.entry_apellido.delete(0, tk.END)
        self.entry_tel.delete(0, tk.END)
        self.entry_email.delete(0, tk.END)
        self.entry_dir.delete(0, tk.END)

        self.entry_nombre.insert(0, valores[1])  # Columna "nombre"
        self.entry_apellido.insert(0, valores[2])  # Columna "apellido"
        self.entry_tel.insert(0, valores[3])  # Columna "telefono"
        self.entry_email.insert(0, valores[4])  # Columna "email"
        self.entry_dir.insert(0, valores[5])  # Columna "direccion"

        # Establece el ID del dueño a editar
        self.id_dueño_editar = valores[0]  # El ID del dueño está en la primera columna
    
    def limpiarFormulario(self):
        
        """Limpia todos los campos del formulario."""
        self.entry_nombre.delete(0, tk.END)
        self.entry_apellido.delete(0, tk.END)
        self.entry_tel.delete(0, tk.END)
        self.entry_email.delete(0, tk.END)
        self.entry_dir.delete(0, tk.END)
        
        self.entry_nombre.focus_set()
    
    def habilitarCampos(self):
        for entry in [self.entry_nombre, self.entry_apellido, self.entry_tel, self.entry_email, self.entry_dir]:
            entry.config(state='normal')
        self.btn_alta.config(state='disabled')
        self.btn_modi.config(state='normal')
        self.btn_cance.config(state='normal')

        self.entry_nombre.focus_set()
        
    def bloquearCampos(self):
        for entry in [self.entry_nombre, self.entry_apellido, self.entry_tel, self.entry_email, self.entry_dir]:
            entry.config(state='disabled')
        self.btn_alta.config(state='normal')
        self.btn_modi.config(state='disabled')
        self.btn_cance.config(state='disabled')
    
     
    def eliminarRegistro(self):
        return super().eliminarRegistro()
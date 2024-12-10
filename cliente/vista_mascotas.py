import re
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from .vista_base import FrameBase
from bdd.conneciondb import conexion_db

class FrameMascotas(FrameBase):
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
        self.labelForm()
        self.inputForm()
        self.botonesPrincipales()
        self.bloquearCampos()
        self.tableView()
        self.cargarTablaMascotas()
        

    
    def cargarDueños(self):
        
        """Carga los datos de dueños en el Combobox."""
        try:
            # Conecta a la base de datos y obtiene los dueños
            conexion_db.conectar()
            consulta = """SELECT id, nombre || ' ' || apellido FROM dueños"""
            dueños = conexion_db.leer(consulta)

            # Limpia el Combobox antes de cargar nuevos datos
            self.entry_dueño['values'] = []  # Resetea las opciones del Combobox
            
            if dueños:
                # Carga los nombres completos de los dueños en el Combobox
                opciones = [f"{fila[0]} - {fila[1]}" for fila in dueños]
                self.entry_dueño['values'] = opciones
                self.entry_dueño.current(0)  # Selecciona la primera opción
                self.entry_dueño.config(state='readonly')  # Habilita el Combobox
            else:
                
                # Si no hay registros, muestra la leyenda
                self.entry_dueño['values'] = ["No hay datos cargados"]
                self.entry_dueño.current(0)  # Selecciona la opción
                self.entry_dueño.config(state='disabled')  # Deshabilita el Combobox
                messagebox.showwarning("Advertencia", "No existen dueños registrados")
        
        except Exception as e:
            messagebox.showerror("Error", f"Hubo un problema al cargar los dueños: {e}")
        
        finally:
            conexion_db.cerrar_conexion()

    def guardarMascotas(self):
        """Guarda una nueva mascota o actualiza una existente en la base de datos."""
        if not all([self.entry_nombre.get(), self.entry_especie.get(), self.entry_raza.get(),
                    self.entry_edad.get(), self.entry_estado.get(), self.entry_dueño.get()]):
            messagebox.showwarning("Error", "Por favor, complete todos los campos.")
            return

        try:
            # Valida la edad
            edad = int(self.entry_edad.get())
            if edad <= 0:
                raise ValueError("La edad debe ser un número mayor a 0.")

            # Obtiene el ID del dueño desde el Combobox
            id_dueño = self.entry_dueño.get().split(" - ")[0]
            conexion_db.conectar()
        # Si `id_mascota_editar` está definido, actualiza; si no, inserta un nuevo registro
            if hasattr(self, 'id_mascota_editar') and self.id_mascota_editar:
                    consulta = """UPDATE mascotas
                                SET nombre = ?, especie = ?, raza = ?, edad = ?, estado = ?, id_dueño = ?
                                WHERE id = ?"""
                    parametros = (
                        self.entry_nombre.get(),
                        self.entry_especie.get(),
                        self.entry_raza.get(),
                        edad,
                        self.entry_estado.get(),
                        id_dueño,
                        self.id_mascota_editar
                    )
                    mensaje_exito = "Mascota actualizada correctamente."
            else:
                consulta = """INSERT INTO mascotas (nombre, especie, raza, edad, estado, id_dueño)
                            VALUES (?, ?, ?, ?, ?, ?)"""
                parametros = (
                    self.entry_nombre.get(),
                    self.entry_especie.get(),
                    self.entry_raza.get(),
                    edad,
                    self.entry_estado.get(),
                    id_dueño
                )
                mensaje_exito = "Mascota guardada correctamente."
                
            conexion_db.insertar(consulta, parametros)

            # Muestra un mensaje de éxito y recarga la tabla
            messagebox.showinfo("Éxito", mensaje_exito)
            self.cargarTablaMascotas()
            self.limpiarFormulario()

            # Bloquea los campos y resetea el modo de edición
            self.bloquearCampos()
            self.id_mascota_editar = None  # Resetea el ID de edición

        except ValueError as ve:
            messagebox.showerror("Error de Validación", str(ve))
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar la mascota: {e}")
        
        finally:
            conexion_db.cerrar_conexion()
    
    def cargarTablaMascotas(self):
        """Carga los datos de la tabla Mascotas en el Treeview."""
        try:
            conexion_db.conectar()
            consulta = """SELECT id, nombre, especie, raza, edad, estado, id_dueño FROM mascotas"""
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
        title = ttk.Label(title_frame, text='Mascotas', font=('Arial', 20, 'bold'))
        title.pack(side="left", expand=True, padx=20)

    def labelForm(self):
        labels = ["Nombre:", "Especie:", "Raza:", "Edad:", "Estado:", "Dueño:"]
        for i, text in enumerate(labels):
            label = tk.Label(self, text=text)
            label.config(font=('Arial', 12, 'bold'))
            label.grid(row=i+1, column=0, padx=10, pady=10, sticky="e")

    def inputForm(self):
        self.entry_nombre = tk.Entry(self, width=50)
        self.entry_especie = tk.Entry(self, width=50)
        self.entry_raza = tk.Entry(self, width=50)
        self.entry_edad = tk.Entry(self, width=50)
        opciones = ['Sano', 'Enfermo', 'En tratamiento', 'Recuperándose']
        self.entry_estado = ttk.Combobox(self, state="readonly", width=47, values=opciones)
        
        self.entry_dueño = ttk.Combobox(self, state="readonly", width=47) # Método para llenar los datos del Combobox
        self.cargarDueños()

        entries = [self.entry_nombre, self.entry_especie, self.entry_raza, self.entry_edad, self.entry_estado, self.entry_dueño]
        for i, entry in enumerate(entries):
            entry.grid(row=i + 1, column=1, padx=10, pady=10, sticky="w")
    
    def botonesPrincipales(self):
        btn_frame = tk.Frame(self)  # Contenedor para los botones
        btn_frame.grid(row=7, column=0, columnspan=3, pady=10)

        self.btn_alta = tk.Button(btn_frame, text='Nuevo', command=self.habilitarCampos)
        self.btn_modi = tk.Button(btn_frame, text='Guardar', command=self.guardarMascotas)
        self.btn_cance = tk.Button(btn_frame, text='Cancelar', command=self.bloquearCampos)
            
        botones = [self.btn_alta, self.btn_modi, self.btn_cance]
        colores = ['#1C500B', '#0D2A83', '#A90A0A']
        for i, (btn, color) in enumerate(zip(botones, colores)):
            btn.config(width=20, font=('Arial', 12, 'bold'), fg='#FFFFFF', bg=color, cursor='hand2',
                    activebackground=color, activeforeground='#000000')
            btn.grid(row=0, column=i, padx=10, pady=10)

    def tableView(self):
        # Contenedor para la tabla
        tabla_frame = tk.Frame(self, width=600, height=120)
        tabla_frame.grid(row=8, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        tabla_frame.grid_propagate(False)

        style = ttk.Style()
        style.configure("Treeview", rowheight=20)  # Aumenta altura de cada fila

        # Título arriba y alineado a la izquierda
        titulo_tabla = tk.Label(tabla_frame, text="Datos de la tabla", font=("Arial", 10), anchor="w", justify="left")
        titulo_tabla.pack(side="top", anchor="w", padx=15, pady=5)

        # Configuración del Treeview
        self.tree = ttk.Treeview(
            tabla_frame, height=6,
            columns=("id_mascota", "nombre", "especie", "raza", "edad", "estado", "id_dueño"),
            show="headings"
        )
        # Configuración de columnas
        self.tree.column("id_mascota", width=50, anchor="center")
        self.tree.column("nombre", width=100, anchor="center")
        self.tree.column("especie", width=100, anchor="center")
        self.tree.column("raza", width=100, anchor="center")
        self.tree.column("edad", width=100, anchor="center")
        self.tree.column("estado", width=100, anchor="center")
        self.tree.column("id_dueño", width=50, anchor="center")

        # Encabezados
        self.tree.heading("id_mascota", text="ID")
        self.tree.heading("nombre", text="Nombre")
        self.tree.heading("especie", text="Especie")
        self.tree.heading("raza", text="Raza")
        self.tree.heading("edad", text="Edad")
        self.tree.heading("estado", text="Estado")
        self.tree.heading("id_dueño", text="Dueño")

        # Configuración de colores de filas
        self.tree.tag_configure('even', background='#f0f0f0')
        self.tree.tag_configure('odd', background='#ffffff')

        # Scrollbar vertical
        scroll_y = ttk.Scrollbar(tabla_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll_y.set)

        # Posicionar Treeview y Scrollbar
        self.tree.pack(side="left", fill="both", expand=True, padx=10)
        scroll_y.pack(side="right", fill="y")

        # Botones debajo de la tabla
        self.btn_editar = tk.Button(self, text='Editar', command=self.editarRegistro)
        self.btn_editar.config(width=15, font=('Arial', 12, 'bold'), fg='#FFFFFF', bg='#1C500B', cursor='hand2',
                            activebackground='#3FD83F', activeforeground='#000000')
        self.btn_editar.grid(row=9, column=0, padx=10, pady=10)

        self.btn_delete = tk.Button(self, text='Eliminar', command=self.eliminarRegistro)
        self.btn_delete.config(width=15, font=('Arial', 12, 'bold'), fg='#FFFFFF', bg='#A90A0A', cursor='hand2',
                                activebackground='#F35B5B', activeforeground='#000000')
        self.btn_delete.grid(row=9, column=1, padx=10, pady=10)

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
        self.entry_especie.delete(0, tk.END)
        self.entry_raza.delete(0, tk.END)
        self.entry_edad.delete(0, tk.END)
        self.entry_estado.set("")
        self.entry_dueño.set("")

        self.entry_nombre.insert(0, valores[1])  # Columna "nombre"
        self.entry_especie.insert(0, valores[2])  # Columna "especie"
        self.entry_raza.insert(0, valores[3])  # Columna "raza"
        self.entry_edad.insert(0, valores[4])  # Columna "edad"
        self.entry_estado.set(valores[5])  # Columna "estado"

        # Cargar el dueño en el Combobox (formatear si necesario)
        id_dueño = valores[6]
        for dueño in self.entry_dueño['values']:
            if dueño.startswith(f"{id_dueño} -"):
                self.entry_dueño.set(dueño)
                break

        # Guarda el ID de la mascota seleccionada para actualizarla después
        self.id_mascota_editar = valores[0]  # ID de la mascota (clave primaria)
    
    def eliminarRegistro(self):
        """Elimina el registro seleccionado de la base de datos y actualiza el ID autoincremental."""
        # Obtiene la selección actual del Treeview
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Por favor, seleccione un registro para eliminar.")
            return

        # Obtiene los valores del registro seleccionado
        valores = self.tree.item(selected_item, 'values')
        if not valores:
            messagebox.showwarning("Advertencia", "No se pudo obtener la información del registro.")
            return

        id_mascota = valores[0]  # El ID de la mascota está en la primera columna

        # Confirmación de eliminación
        respuesta = messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Está seguro de que desea eliminar la mascota con ID {id_mascota} y nombre {valores[1]}?"
        )
        if not respuesta:
            return

        # Realiza la eliminación en la base de datos
        try:
            conexion_db.conectar()
            
            # Eliminar el registro
            consulta_eliminar = "DELETE FROM mascotas WHERE id = ?"
            conexion_db.eliminar(consulta_eliminar, (id_mascota,))

            # Actualizar la secuencia del ID
            consulta_max_id = "SELECT MAX(id) FROM mascotas"
            max_id_resultado = conexion_db.leer(consulta_max_id)
            max_id = max_id_resultado[0][0] if max_id_resultado and max_id_resultado[0][0] else 0

            # Ajustar el valor de la secuencia de la tabla
            consulta_update_sequencia = "UPDATE sqlite_sequence SET seq = ? WHERE name = 'mascotas'"
            conexion_db.insertar(consulta_update_sequencia, (max_id,))

            # Muestra un mensaje de éxito y recarga la tabla
            messagebox.showinfo("Éxito", f"La mascota con ID {id_mascota} fue eliminada exitosamente.")
            self.cargarTablaMascotas()
        
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar el registro: {e}")

        finally:
            conexion_db.cerrar_conexion()
            
    def limpiarFormulario(self):
        """Limpia todos los campos del formulario."""
        self.entry_nombre.delete(0, tk.END)
        self.entry_especie.delete(0, tk.END)
        self.entry_raza.delete(0, tk.END)
        self.entry_edad.delete(0, tk.END)
        self.entry_estado.set("")  # Resetea el Combobox
        self.entry_dueño.set("")  # Resetea el Combobox
        
        self.entry_nombre.focus_set()
        
    def habilitarCampos(self):
        for entry in [self.entry_nombre, self.entry_especie, self.entry_raza, self.entry_edad, self.entry_estado, self.entry_dueño]:
            entry.config(state='normal')
        self.btn_alta.config(state='disabled')
        self.btn_modi.config(state='normal')
        self.btn_cance.config(state='normal')
        
        self.entry_nombre.focus_set()

    def bloquearCampos(self):
        for entry in [self.entry_nombre, self.entry_especie, self.entry_raza, self.entry_edad, self.entry_estado, self.entry_dueño]:
            entry.config(state='disabled')
        self.btn_alta.config(state='normal')
        self.btn_modi.config(state='disabled')
        self.btn_cance.config(state='disabled')
import datetime
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from .vista_base import FrameBase
from bdd.conneciondb import conexion_db

class FrameVisitas(FrameBase):
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
        self.cargarTablaVisitas()

    
    def cargarMascotas(self):
        """Carga las mascotas desde la base de datos en el Combobox."""
        try:
            # Conecta a la base de datos y obtiene las mascotas
            conexion_db.conectar()
            consulta = """SELECT id, nombre FROM mascotas"""
            mascotas = conexion_db.leer(consulta)

            # Limpia el Combobox antes de cargar nuevos datos
            self.entry_mascota['values'] = []  # Resetea las opciones del Combobox
            
            if mascotas:
                # Carga los nombres completos de las mascotas en el Combobox
                opciones = [f"{fila[0]} - {fila[1]}" for fila in mascotas]
                self.entry_mascota['values'] = opciones
                self.entry_mascota.current(0)  # Selecciona la primera opción
                self.entry_mascota.config(state='readonly')  # Habilita el Combobox
            else:
                
                # Si no hay registros, muestra la leyenda
                self.entry_mascota['values'] = ["No hay datos cargados"]
                self.entry_mascota.current(0)  # Selecciona la opción
                self.entry_mascota.config(state='disabled')  # Deshabilita el Combobox
                messagebox.showwarning("Advertencia", "No existen mascotas registradas")
        
        except Exception as e:
            messagebox.showerror("Error", f"Hubo un problema al cargar las mascotas: {e}")
        
        finally:
            conexion_db.cerrar_conexion()

    def guardarMascotas(self):
        """Guarda una nueva visita o actualiza una existente en la base de datos."""
        if not all([self.entry_fecha.get(), self.entry_motivo.get(), self.entry_mascota.get()]):
            messagebox.showwarning("Error", "Por favor, complete todos los campos.")
            return

        try:
            fecha_str = self.entry_fecha.get()
            fecha = datetime.datetime.strptime(fecha_str, '%d/%m/%Y')

            # Validar que la fecha no sea anterior a la fecha actual
            fecha_actual = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

            if fecha < fecha_actual:
                messagebox.showwarning("Error", "La fecha debe ser actual o futura.")
                return
            
            id_mascota = self.entry_mascota.get().split(" - ")[0]
            conexion_db.conectar()

            if hasattr(self, 'id_visita_editar') and self.id_visita_editar:
                consulta = """UPDATE visitas SET fecha = ?, motivo = ?, id_mascota = ? WHERE id = ?"""
                parametros = (fecha.strftime('%d/%m/%Y'), self.entry_motivo.get(), id_mascota, self.id_visita_editar)
            else:
                consulta = """INSERT INTO visitas (fecha, motivo, id_mascota) VALUES (?, ?, ?)"""
                parametros = (fecha.strftime('%Y-%m-%d'), self.entry_motivo.get(), id_mascota)

            conexion_db.insertar(consulta, parametros)
            messagebox.showinfo("Éxito", "Visita guardada correctamente.")
            self.cargarTablaVisitas()
            self.limpiarFormulario()
            self.bloquearCampos()
            self.id_visita_editar = None
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar la visita: {e}")

        finally:
            conexion_db.cerrar_conexion()
    
    def cargarTablaVisitas(self):
        """Carga los datos de la tabla Visitas en el Treeview."""
        try:
            conexion_db.conectar()
            consulta = "SELECT id, fecha, motivo, id_mascota FROM visitas"
            datos = conexion_db.leer(consulta)

            for item in self.tree.get_children():
                self.tree.delete(item)

            for i, fila in enumerate(datos):
                tag = 'even' if i % 2 == 0 else 'odd'
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
        title = ttk.Label(title_frame, text='Visitas', font=('Arial', 20, 'bold'))
        title.pack(side="left", expand=True, padx=20)

    def labelForm(self):
        labels = ["Fecha dd/mm/aaaa:", "Motivo:", "Mascota:"]
        for i, text in enumerate(labels):
            label = tk.Label(self, text=text)
            label.config(font=('Arial', 12, 'bold'))
            label.grid(row=i+1, column=0, padx=10, pady=10, sticky="e")

    def inputForm(self):
        
        self.entry_fecha = tk.Entry(self, width=50)
        opciones = ['Vacunación', 'Chequeo general', 'Desparasitación', 'Castración', 'Control de peso']
        self.entry_motivo = ttk.Combobox(self, state="readonly", width=47, values=opciones)
        
        self.entry_mascota = ttk.Combobox(self, state="readonly", width=47) # Método para llenar los datos del Combobox
        self.cargarMascotas()

        entries = [self.entry_fecha, self.entry_motivo, self.entry_mascota]
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
            columns=("id_visita", "fecha", "motivo", "id_mascota"),
            show="headings"
        )
        # Configuración de columnas
        self.tree.column("id_visita", width=50, anchor="center")
        self.tree.column("fecha", width=100, anchor="center")
        self.tree.column("motivo", width=100, anchor="center")
        self.tree.column("id_mascota", width=100, anchor="center")

        # Encabezados
        self.tree.heading("id_visita", text="ID")
        self.tree.heading("fecha", text="Fecha")
        self.tree.heading("motivo", text="Motivo")
        self.tree.heading("id_mascota", text="Mascota")

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
        self.entry_fecha.delete(0, tk.END)
        self.entry_motivo.set("")
        self.entry_mascota.set("")
        
        # Carga la fecha y formatea como dd/mm/yyyy
        fecha_db = valores[1]
        try:
            # Intentar formatear la fecha de la base de datos (yyyy-mm-dd) a dd/mm/yyyy
            fecha_formateada = datetime.datetime.strptime(fecha_db, '%Y-%m-%d').strftime('%d/%m/%Y')
        except ValueError:
            # Si la fecha no está en el formato esperado, asignar directamente
            fecha_formateada = fecha_db
        
        self.entry_fecha.insert(0, fecha_formateada)  # Coloca la fecha en el formato adecuado
        
        self.entry_motivo.set(valores[2])  # Columna "motivo"

        # Cargar la mascota en el Combobox (formatear si necesario)
        id_mascota = valores[3]
        for mascota in self.entry_mascota['values']:
            if mascota.startswith(f"{id_mascota} -"):
                self.entry_mascota.set(mascota)
                break

        # Guarda el ID de la visita seleccionada para actualizarla después
        self.id_visita_editar = valores[0]  # ID de la visita (clave primaria)
    
    def eliminarRegistro(self):
        """Elimina el registro seleccionado de la base de datos."""
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Por favor, seleccione un registro para eliminar.")
            return

        valores = self.tree.item(selected_item, 'values')
        id_visita = valores[0]

        try:
            conexion_db.conectar()
            consulta = "DELETE FROM visitas WHERE id = ?"
            conexion_db.eliminar(consulta, (id_visita,))
            
            # Actualizar la secuencia del ID
            consulta_max_id = "SELECT MAX(id) FROM visitas"
            max_id_resultado = conexion_db.leer(consulta_max_id)
            max_id = max_id_resultado[0][0] if max_id_resultado and max_id_resultado[0][0] else 0

            # Ajustar el valor de la secuencia de la tabla
            consulta_update_secuencia= "UPDATE sqlite_sequence SET seq = ? WHERE name = 'visitas'"
            conexion_db.insertar(consulta_update_secuencia, (max_id,))
            
            messagebox.showinfo("Éxito", f"La visita con ID {id_visita} fue eliminada exitosamente.")
            self.cargarTablaVisitas()
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar el registro: {e}")
        
        finally:
            conexion_db.cerrar_conexion()
            
    def limpiarFormulario(self):
        """Limpia todos los campos del formulario."""
        self.entry_fecha.delete(0, tk.END)
        self.entry_motivo.set("")  # Resetea el Combobox
        self.entry_mascota.set("")  # Resetea el Combobox
        
        self.entry_fecha.focus_set()
        
    def habilitarCampos(self):
        for entry in [self.entry_fecha, self.entry_motivo, self.entry_mascota]:
            entry.config(state='normal')
        self.btn_alta.config(state='disabled')
        self.btn_modi.config(state='normal')
        self.btn_cance.config(state='normal')
        
        self.entry_fecha.focus_set()

    def bloquearCampos(self):
        for entry in [self.entry_fecha, self.entry_motivo, self.entry_mascota]:
            entry.config(state='disabled')
        self.btn_alta.config(state='normal')
        self.btn_modi.config(state='disabled')
        self.btn_cance.config(state='disabled')
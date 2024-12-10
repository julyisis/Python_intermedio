import sqlite3

class ConnecionDB:
    _instancia = None  # Variable de clase para patrón singleton

    def __new__(cls, *args, **kwargs):
        if not cls._instancia:
            cls._instancia = super(ConnecionDB, cls).__new__(cls, *args, **kwargs)
            cls._instancia.base_datos = 'bdd/veterinaria.db'
            cls._instancia.conexion = None
            cls._instancia.cursor = None
        return cls._instancia

    def conectar(self):
        """Conecta a la base de datos solo si no está conectada."""
        if self.conexion is None:
            self.conexion = sqlite3.connect(self.base_datos)
            self.cursor = self.conexion.cursor()
            print("Base de datos conectada.")
        return self.cursor

    def leer(self, consulta, parametros=()):
        """Lee los datos de la base de datos."""
        if self.cursor is None:
            self.conectar()  # Establece la conexión si no está activa
        try:
            self.cursor.execute(consulta, parametros)
            resultados = self.cursor.fetchall()
            return resultados
        except Exception as e:
            print(f"Error al leer los datos: {e}")
            return None

    def insertar(self, consulta, datos):
        """Inserta datos en la base de datos."""
        try:
            self.cursor.execute(consulta, datos)
            self.conexion.commit()
            print("Datos cargados exitosamente")
        except Exception as e:
            print(f"Error al cargar los datos: {e}")

    def eliminar(self, consulta, parametros=()):
        """Elimina registros en la base de datos."""
        try:
            self.cursor.execute(consulta, parametros)
            self.conexion.commit()  # Confirma los cambios
            print("Registro eliminado exitosamente.")
        except Exception as e:
            print(f"Error al eliminar los datos: {e}")

    def cerrar_conexion(self):
        """Cierra la conexión de la base de datos."""
        if self.conexion:
            self.conexion.close()
            self.conexion = None
            self.cursor = None
            print("Conexión cerrada.")
        else:
            print("No hay conexión activa para cerrar.")

conexion_db = ConnecionDB()
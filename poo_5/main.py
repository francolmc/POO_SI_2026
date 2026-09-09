from database.conexion import obtener_conexion, crear_tablas

crear_tablas()

conexion = obtener_conexion()
cursor = conexion.cursor()
cursor.execute(
    "INSERT INTO libros VALUES ('978-0-1', 'Cien años de soledad', '3')"
)
conexion.commit()

cursor.execute("SELECT * FROM libros")
for fila in cursor.fetchall():
    print(fila)

conexion.close()
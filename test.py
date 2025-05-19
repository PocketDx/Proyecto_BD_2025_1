import csv
import random
from faker import Faker
from datetime import timedelta
from datetime import date

# Inicialización de Faker
fake = Faker()

# Configuración
NUM_USUARIOS = 3000
NUM_LIBROS = 500
MIN_COPIAS_POR_LIBRO = 5
MAX_COPIAS_POR_LIBRO = 10

usuarios = []
libros = []
copias = []
ubicaciones = []
prestamos = []
devoluciones = []
multas = []
reservas = []
pagos = []
auditorias = []
historial_acciones = []
sesion_auditoria = []
empleados = []
reposicion_libros = []


# Metodo para leer usuarios desde archivo CSV

archivo = "c:\\Users\\pocke\\Documents\\usuarios_3000.csv"
def leer_usuarios_csv(archivo):
    with open(archivo, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            usuarios.append({
                'id_usuario': int(row['id_usuario']),
                'nombre': row['nombre'],
                'correo': row['correo'],
                'identificacion': int(row['identificacion']),
                'tipo_usuario': row['tipo_usuario'],
                'fecha_registro': row['fecha_registro'],
                'estado': row['estado'],
                'saldo': float(row['saldo'])
            })
    return usuarios

print("Leyendo usuarios desde CSV...")
leer_usuarios_csv(archivo)
print("Usuarios leídos exitosamente.")
print(f"Total de usuarios: {len(usuarios)}")

# Metodo para leer libros desde archivo CSV separado por punto y coma
# Se asume que el archivo CSV tiene las siguientes columnas: isbn, titulo, autor, editorial, anio_publicacion, id_categoria
archivo_libros = "c:\\Users\\pocke\\Documents\\libros_500.csv"
def leer_libros_csv(archivo):
    with open(archivo, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file, delimiter=';')
        for row in reader:
            libros.append({
                'isbn': row['isbn'],
                'titulo': row['titulo'],
                'autor': row['autor'],
                'editorial': row['editorial'],
                'anio_publicacion': int(row['anio_publicacion']),
                'id_categoria': int(row['id_categoria'])
            })
    return libros

print("Leyendo libros desde CSV...")
leer_libros_csv(archivo_libros)
print("Libros leídos exitosamente.")
print(f"Total de libros: {len(libros)}")

# Metodo para leer copias de libros desde archivo CSV separado por punto y coma
# Se asume que el archivo CSV tiene las siguientes columnas: id_copia, isbn, ubicacion, estado_actual
archivo_copias = "c:\\Users\\pocke\\Documents\\copias_5_10.csv"
def leer_copias_csv(archivo):
    with open(archivo, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file, delimiter=';')
        for row in reader:
            copias.append({
                'id_copia': int(row['id_copia']),
                'isbn': row['isbn'],
                'ubicacion': row['ubicacion'],
                'estado_actual': row['estado_actual']
            })
    return copias

print("Leyendo copias de libros desde CSV...")
leer_copias_csv(archivo_copias)
print("Copias de libros leídas exitosamente.")
print(f"Total de copias: {len(copias)}")

#---------- Reposicion libros ----------

for copia in copias:
    if copia['estado_actual'] == 'Prestado':
        reposicion_libros.append({
            'id_reposicion': len(reposicion_libros) + 1,
            'id_usuario': random.choice(usuarios)['id_usuario'],
            'id_copia': copia['id_copia'],
            'fecha': fake.date_between(start_date='-1M', end_date='today'),
            'monto': random.randint(2000, 50000)
        })

# ---------- Guardado a CSV ----------
def guardar_csv(nombre, lista, campos):
    with open(f"c:\\Users\\pocke\\Documents\\{nombre}.csv", mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=campos, delimiter=';')
        writer.writerows(lista)

guardar_csv("reposicion_libros", reposicion_libros, reposicion_libros[0].keys())

print("Archivos CSV generados exitosamente.")
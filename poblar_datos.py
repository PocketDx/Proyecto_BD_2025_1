# Dairo Javier Rodriguez - 1151358
# Jonathan Guevara - 1152229
# David Torres - 1151717

# -----------------------------------------------------------------------
# Este script genera datos ficticios para poblar la base de datos
# Adicionalmente, se generan archivos CSV para cada tabla
# Tambien cumple con requisitos que solo se cumplen desde la programacion
# como la cantidad de prestamos por usuario, el calculo de multas, etc.
# -----------------------------------------------------------------------

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

'''
# ---------- Usuarios ----------
for i in range(1, NUM_USUARIOS + 1):
    tipo_usuario = random.choices(['estudiante', 'docente'], weights=[0.7, 0.3])[0]
    usuarios.append({
        'id_usuario': i,
        'nombre': fake.unique.name(),
        'correo': fake.unique.email(),
        'identificacion': fake.unique.random_number(digits=8),
        'tipo_usuario': tipo_usuario,
        'fecha_registro': fake.date_between(start_date='-3y', end_date='-1M'),
        'estado': random.choice(['activo', 'bloqueado']),
        'saldo': random.randint(50000, 120000)
    })
    '''

# ---------- Libros y Copias ----------
id_copia = 1
for i in range(1, NUM_LIBROS + 1):
    libros.append({
        'isbn': f"978-3-{id_copia}-{random.randint(0, 99)}",
        'titulo': fake.sentence(nb_words=4),
        'autor': fake.name(),
        'editorial': fake.company(),
        'anio_publicacion': random.randint(1990, 2024),
        'id_categoria': random.randint(1, 10),  # Categorías de 1 a 10
    })
    num_copias = random.randint(MIN_COPIAS_POR_LIBRO, MAX_COPIAS_POR_LIBRO)
    for _ in range(num_copias):
        copias.append({
            'id_copia': id_copia,
            'isbn': libros[-1]['isbn'],
            'ubicacion': random.randint(1, 100),  # Ubicaciones de 1 a 100
            'estado_actual': random.choice(['Disponible', 'Prestado', 'Reservado']),
        })
        id_copia += 1

# ---------- Ubicaciones ----------
for i in range(1, 101): #
    ubicaciones.append({
        'id_ubicacion': i,
        'pasillo': random.randint(1, 4), # Pasillos de 1 a 4
        'estante': random.randint(1, 4), # Estantes de 1 a 4
        'nivel': random.randint(1, 3), # Niveles de 1 a 3
    })

# ---------- Préstamos, Devoluciones y Multas ----------
id_prestamo = 1
id_devolucion = 1
id_multa = 1
prestamos_por_usuario = {u['id_usuario']: 0 for u in usuarios}

for copia in random.sample(copias, int(len(copias) * 0.6)):  # 60% prestadas
    usuario = random.choice(usuarios)
    max_prestamos = 3 if usuario['tipo_usuario'] == 'estudiante' else 5
    if prestamos_por_usuario[usuario['id_usuario']] >= max_prestamos:
        continue
    fecha_prestamo = fake.date_between(start_date='-6M', end_date='-1M')
    duracion = 15 if usuario['tipo_usuario'] == 'estudiante' else 30 
    # Esta es una validación de 15 días para estudiantes y 30 para docentes
    fecha_limite = fecha_prestamo + timedelta(days=duracion)
    estado = random.choices(['devuelto', 'retrasado', 'activo'], [0.5, 0.2, 0.3])[0]

    prestamos.append({
        'id_prestamo': id_prestamo,
        'id_usuario': usuario['id_usuario'],
        'id_copia': copia['id_copia'],
        'fecha_prestamo': fecha_prestamo,
        'fecha_limite': fecha_limite,
        'estado': estado,
        'costo': 5000
    })

    if estado in ['devuelto', 'retrasado']:
        dias_retraso = random.randint(0, 10) if estado == 'retrasado' else 0
        fecha_dev = fecha_limite + timedelta(days=dias_retraso)
        devoluciones.append({
            'id_devolucion': id_devolucion,
            'id_prestamo': id_prestamo,
            'fecha_devolucion': fecha_dev,
            'dias_retraso': dias_retraso,
            'monto_multa': dias_retraso * 2000 if dias_retraso > 0 else 0
        })
        if dias_retraso > 0:
            multa = dias_retraso * 2000
            multas.append({
                'id_multa': id_multa,
                'id_usuario': usuario['id_usuario'],
                'id_tipo_multa': random.choice([1, 3]),  # Tipo de multa
                'fecha': fecha_dev,
                'monto': multa,
            })
            id_multa += 1
        id_devolucion += 1

    prestamos_por_usuario[usuario['id_usuario']] += 1
    copia['estado_actual'] = 'Prestado'
    id_prestamo += 1


# ---------- Reservas ----------
for libro in random.sample(libros, int(NUM_LIBROS * 0.2)):
    reservas.append({
        'id_reserva': len(reservas) + 1,
        'id_usuario': random.choice(usuarios)['id_usuario'],
        'isbn': libro['isbn'],
        'fecha_reserva': fake.date_between(start_date='-3M', end_date='today'),
        'activa': random.choice([0, 1]),  # 0 = No activa, 1 = Activa
    })

# ---------- Pagos ----------
id_pago = 1
for multa in multas:
    fecha_inicio = multa['fecha']
    fecha_hoy = date.today()
    if fecha_inicio > fecha_hoy:
        fecha_pago = fecha_hoy
    else:
        fecha_pago = fake.date_between(start_date=fecha_inicio, end_date=fecha_hoy)
    pagos.append({
        'id_pago': id_pago,
        'id_usuario': multa['id_usuario'],
        'id_tipo_pago': 1,
        'fecha': fecha_pago,
        'monto': multa['monto']
    })
    id_pago += 1

for prestamo in prestamos:
    pagos.append({
        'id_pago': id_pago,
        'id_usuario': prestamo['id_usuario'],
        'id_tipo_pago': 2,
        'fecha': prestamo['fecha_prestamo'],
        'monto': 5000
    })
    id_pago += 1

#----------- Empleados ----------

for i in range(1, 5):
    empleados.append({
        'id_empleado': i,
        'nombre': usuarios[i]['nombre'],
        'usuario': fake.user_name(),
        'contrasena': fake.password(),
        'id_rol': random.choice([1, 2, 3]),  # Rol de empleado
    })

# -------- Sesion auditoria ----------

for _ in range(200):
    sesion_auditoria.append({
        'id_sesion': len(sesion_auditoria) + 1,
        'id_empleado': random.choice(empleados)['id_empleado'],
        'inicio_sesion': fake.date_time_between(start_date='-1y', end_date='now'),
        'fin_sesion': fake.date_time_between(start_date='now', end_date='+23h'),
    })

# ---------- Auditoría ----------
for _ in range(200):
    auditorias.append({
        'id_auditoria': len(auditorias) + 1,
        'id_sesion': random.choice([s['id_sesion'] for s in sesion_auditoria]),
        'tabla_afectada': random.choice(['libros', 'usuarios', 'prestamos', 'devoluciones', 'reservas']),
        'accion': random.choice(['INSERT', 'UPDATE', 'DELETE']),
        'registro_id': random.choice(usuarios)['id_usuario'],
        'fecha': fake.date_between(start_date='-1y', end_date='today')
    })

#----------- Historial de Acciones ----------

for _ in range(200):
    historial_acciones.append({
        'id_historial': len(historial_acciones) + 1,
        'id_usuario': random.choice(usuarios)['id_usuario'],
        'accion': random.choice(['prestamo', 'devolucion', 'multa']),
        'fecha': fake.date_between(start_date='-1y', end_date='today'),
        'detalle': f"Prestamo de libro con ISBN {random.choice(libros)['isbn']}" if 'accion' == 'prestamo' else
                   f"Devolucion de libro con ISBN {random.choice(libros)['isbn']}" if 'accion' == 'devolucion' else
                   f"Multa de {random.randint(1000, 5000)} por retraso en devolucion"
    })

#---------- Informes ----------
informes = []
for _ in range(10):
    informes.append({
        'id_informe': len(informes) + 1,
        'tipo': random.choice([
            'Libros más prestados',
            'Usuarios con más multas',
            'Inventario',
            'Estado reservas',
            'Préstamos retrasados'
        ]),
        'periodo': fake.date_between(start_date='-1y', end_date='today'),
        'generado_por': random.choice(empleados)['id_empleado'],
        'detalles': fake.text(max_nb_chars=200),
    })

#---------- Estado Copias ----------
estado_copias = []
for copia in copias:
    estado_copias.append({
        'id_estado': len(estado_copias) + 1,
        'id_copia': copia['id_copia'],
        'estado': copia['estado_actual'],
        'fecha_estado': fake.date_between(start_date='-1M', end_date='today'),
    })

#---------- Reposicion libros ----------
reposicion_libros = []
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

# Guardar todos
guardar_csv("libros_500", libros, libros[0].keys()) 
guardar_csv("copias_5_10", copias, copias[0].keys()) 
guardar_csv("ubicaciones_100", ubicaciones, ubicaciones[0].keys())
guardar_csv("prestamos", prestamos, prestamos[0].keys())
guardar_csv("devoluciones", devoluciones, devoluciones[0].keys())
guardar_csv("multas", multas, multas[0].keys())
guardar_csv("reservas", reservas, reservas[0].keys())
guardar_csv("pagos", pagos, pagos[0].keys())
guardar_csv("auditorias", auditorias, auditorias[0].keys())
guardar_csv("historial_acciones", historial_acciones, historial_acciones[0].keys())
guardar_csv("empleados", empleados, empleados[0].keys())
guardar_csv("informes", informes, informes[0].keys())
guardar_csv("sesion_auditoria", sesion_auditoria, sesion_auditoria[0].keys())
guardar_csv("estado_copias", estado_copias, estado_copias[0].keys())
guardar_csv("reposicion_libros", reposicion_libros, reposicion_libros[0].keys())

print("Archivos CSV generados exitosamente.")
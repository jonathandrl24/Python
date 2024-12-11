import os  

# leer datos del archivo
def leerArchivo(archivo):
    if os.path.exists(archivo):
        with open(archivo, "r") as archivo:
            contenido = archivo.read()
            return eval(contenido) if contenido else {}
    return {}

# guardar datos en el archivo
def guardarArchivo(archivo, datos):
    with open(archivo, "w") as archivo:
        archivo.write(str(datos))

#registrar estudiantes
def registrarEstudiante(diccionario):
    nombre = input("Nombre del estudiante: ")
    materias = {}
    while True:
        materia = input("Ingrese el nombre de la materia (o 'listo' para terminar): ")
        if materia.lower() == "listo":
            break
        try:
            calificacion = float(input(f"Calificación para {materia}: "))
            materias[materia] = calificacion
        except ValueError:
            print("Por favor, ingresa una calificación válida.")
    diccionario[nombre] = materias
    print(f"Estudiante {nombre} registrado con éxito.")

# mostrar estudiantes y sus calificaciones
def mostrarEstudiantes(diccionario):
    if not diccionario:
        print("No hay estudiantes registrados.")
        return
    for estudiante, materias in diccionario.items():
        print(f"Estudiante: {estudiante}")
        for materia, calificacion in materias.items():
            print(f"  {materia}: {calificacion}")
        promedio = sum(materias.values()) / len(materias)
        print(f"  Promedio: {promedio:.2f}")

# calcular el promedio general
def promedioGeneral(diccionario):
    if not diccionario:
        print("No hay estudiantes registrados.")
        return
    total_calificaciones = 0
    total_materias = 0
    for materias in diccionario.values():
        total_calificaciones += sum(materias.values())
        total_materias += len(materias)
    promedio = total_calificaciones / total_materias
    print(f"Promedio general de todos los estudiantes: {promedio:.2f}")

# Archivo para guardar los datos
archivo = "archivo.txt"
estudiantes = leerArchivo(archivo)
# Ciclo principal
while True:
    print("\nGestión de Estudiantes")
    print("1. Registrar estudiante")
    print("2. Mostrar estudiantes y sus calificaciones")
    print("3. Calcular promedio general")
    print("4. Salir")
    opcion = input("Seleccione una opción: ")

    if opcion == "1":
        registrarEstudiante(estudiantes)
    elif opcion == "2":
        mostrarEstudiantes(estudiantes)
    elif opcion == "3":
        promedioGeneral(estudiantes)
    elif opcion == "4":
        guardarArchivo(archivo, estudiantes)
        print("Datos guardados. Hasta luego.")
        break
    else:
        print("Por favor, selecciona una opción válida.")

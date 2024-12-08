
def guardarArchivo(idx, *datos):
    if idx == 1:
        with open("archivo.txt", "w") as archivo:
            archivo.write(str(datos))

while True:
    print("Elige la opcion que quieras realizar (o escribe 'salir'): ")
    print("1. Registrar un nuevo estudiante")
    print("2. Calcular promedio de calificaciones")
    print("3. Mostrar estudiantes y sus calificaciones")
    print("4. Guardar y leer datos desde el archivo")
    menu = input("Elige el numero de lo que quieres hacer: ")
    
    if menu.lower() == "salir":
        print("Hasta Luego!")
        break
    
    try:
        menu = int(menu)
        datos = [int(data) for data in datos.split(",")]
        numeros = []
        
        if menu == 1:
            numeros.append(data)
        elif menu == 2:
            
        elif menu == 3:
        
        elif menu == 4:
            
        else:
            print("Escribe un valor valido")
        
    except ValueError:
        print("Valor Incorrecto")
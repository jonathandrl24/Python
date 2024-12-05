import datetime
# ciclo while, interesante funcion
while True:
    
    edad = input("¿En qué año naciste? (Escribe 'salir' para terminar): ")
    años = input("¿Ya cumpliste años?")
    # el break es para romper el ciclo
    if edad.lower() == "salir":
        print("Hasta luego!")
        break
    # le decimos que intente mientras que sea cierto que el ciclo no se ha roto y sigue andando
    try:
        edad = int(edad)
        
        if años == "si":
            # desde la libreria importada datetime obtenemos el año actual
            año = datetime.datetime.now().year
            edadActual = año - edad
            print(f"su edad es {edadActual}")
        else:
            edadActualsin = año -1 - edad
            print(f"su edad es {edadActualsin}")
    # excepto si la edad ingresada es invalida
    except ValueError:
        print("Por favor ingresar un año valido")
        
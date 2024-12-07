# se declara la variable diccionario
diccionario = {}

# se abre ciclo while
while True:
    # input de nombre de estudiante o terminar
    estudiante = input("Nombre del estudiante(o escribe 'terminar'): ")
    # si se escribe terminar se pasa al break  
    if estudiante.lower() == "terminar":
        print("Hasta Luego!")
        # se pone este if aqui porque es necesario que al terminar el ciclo while se muestren los datos de los estudiantes 
        # y del promedio, por lo que hay que crear aqui mismo la logica del programa 
        if diccionario:
            suma = sum(diccionario.values()) # suma de calificaciones, values es usado para contar cada valor int del diccionario
            cantidad = len(diccionario) # cantidad de calificaciones con el metodo len para contar contar cada valor guardado
            promedio = suma / cantidad # calcular promedio
            
            print(f"Estudiantes y calificaciones: {diccionario}")
            print(f"Promedio de calificaciones: {promedio:.2f}") # .2f lo cual es para mostrar 2 decimales despues del punto y f de hacer el 
            # promedio tipo float
        else:
            print("No ingresaste ninguna calificacion")
        break
    
    calificacion = input(f"La calificacion de {estudiante} es: ")    
    
    try:
        calificacion = int(calificacion) 
        diccionario[estudiante] = calificacion # esto incluye en el diccionario al estudiante y la calificacion, y hace a la calificacion
        # parte de el estudiante por ejemplo "diccionario[ana] = 95" y como resultado "{'ana': 95}"
        
    # el ValueError para error de datos ingresados
    except ValueError:
        print("por favor, ingresa una calificacion valida")
        
        
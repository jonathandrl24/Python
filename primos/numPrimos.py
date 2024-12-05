# ciclo while debido a la complejidad de este sencillo codigo, tenemos que usar tambien ciclo for e incluso varios if
# se abre el ciclo y antes del try se agrega un if para salir del codigo con break y tambien recolectamos el numero
while True:
    numero = input("Escribe un numero (o escribe 'salir' para salir): ")
    
    if numero.lower() == "salir":
        print("Hasta Luego!")
        break
    #se abre el try
    try:
        # convertimos numero a int
        numero = int(numero)
        # bajo la condicion de ser el numero igual o menor a 1 el numero no seria primo
        if numero <= 1:
            print(f"El numero {numero} no es primo")
            continue
        # la variable primo se crea y es un booleano creo y si es primo sera True 
        primo = True
        # se crea la variable divisor que se traduce a que el divisor estan en el rango entre 2 y el int raiz cuadrada del numero + 1 (porque el rango
        # siempre resta uno en el segundo valor)
        for divisor in range(2, int(numero ** 0.5) + 1):
            # si el residuo del numero dividido en el divisor es igual a 0 entonces el numero no es primo ya que primo retorna False 
            if numero % divisor == 0:
                primo = False
                # por que se hace break? estoy , supongo que es para cerrar el ciclo for e if 
                break 
        # imprimir dependiendo de el resultado anterior si es primo o no    
        if primo:
            print(f"El numero {numero} es primo")
        else:
            print(f"el numero {numero} no es primo")
    # de otro modo a de haber un valor incorrecto en el numero ingresado        
    except ValueError:
        print("Valor incorrecto")
            
        
        
    

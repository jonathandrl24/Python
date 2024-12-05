# escribir las operaciones disponibles
print("Elige una operacion: ")
print("1. suma")
print("2. resta")
print("3. multiplicacion")
print("4. division")

# declarar las variables con los inputs
opcion = input("Ingrese el numero de la operacion: ")
a = input("Escriba un numero: ")
b = input("Escriba otro numero: ")

# convertir las anteriores variables a un tipo de dato en especifico
opcion = int(opcion)
a = float(a)
b = float(b)

# declarar las variables de operaciones
suma = a+b
resta = a-b
division = a/b
multiplicación = a*b 

# funcionamiento algoritmo segun la opcion elegida por usuario
if opcion == 1:
    print("la suma es igual a : ", suma)
elif opcion == 2:
    print("La resta es igual a : ", resta)
elif opcion == 3:
    print("la multiplicacion es igual a : ", multiplicación)
elif opcion == 4:
    print("la division es igual a : ", division)
else:
    print("Opcion no valida")




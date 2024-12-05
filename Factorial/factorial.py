# declarar variables
factorial = input("Escribe un numero: ")

factorial = int(factorial)
# resultado es igual a 1 porque ahi se empieza
resultado = 1

# aqui le decimos que queremos en un rango de 1 a el factorial + 1 (porque siempre se resta un numero si lo dejaramos solo en factorial(si factorial
# fuera = 5 entonces el rango terminaria en 4 asi que hay que sumar 1 por eso)) 
for i in range(1, factorial + 1):
    # esto significa resultado * i, este ejecutando la linea anterior y sera parte de nuestro algoritmo
    # para multiplicar resultado el cual es = resultado * i ,lo cual se hara en bucle una y otra vez 
    # tomando el resultado anterior hasta llegar a factorial + 1 
    resultado *= i

# print el resultado final con print(f"") para agregar variables dentro de las mismas comillas en corchetes {}
print(f"el factorial de {factorial} es {resultado}")
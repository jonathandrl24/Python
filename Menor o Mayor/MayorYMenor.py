numeros = input("Escribe una lista de numeros separados por comas: ").split(",")

# esta linea es como decir por cada numero convertirlo a int en numeros
numeros = [int(num) for num in numeros]

minimo = min(numeros)
maximo = max(numeros)

print(f"el numero mas grande es: {maximo}  ")
print(f"el numero mas pequeño es: {minimo} ")
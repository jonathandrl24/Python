numeros = input("Escribe una lista de numeros separados por comas: ")
# cada valor int en numeros se divide en ","
numeros = [int(num) for num in numeros.split(",")]
# variable pares
pares = []
# por cada numero en numeros hacer la operacion para determinar si es par
for num in numeros:
    if num % 2 == 0:
        pares.append(num) # append es para coger cada numero que cumpla la anterior condicion de ser par y agregar los numeros pares a la lista pares
# imprimir cuales son los pares y promedio
if pares:
    print(f"los numeros pares son: {pares}")
    promedio = sum(pares) / len(pares)
    print(f"el promedio de los numeros es: {promedio}")
else:
    print(f"no hay numeros pares en la lista: {numeros}")    
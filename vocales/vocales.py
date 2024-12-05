palabra = input("Escribe una palabra o frase: ").lower()
vocales = "aeiou"
contador = 0

# se crea variable letra que lee cada elemento por separado de palabra y despues vocales vocales
# y por cada letra en palabras y si esa letra esta en vocales tambien etonces que le sume al contador 1 mas
for letra in palabra:
    if letra in vocales:
        contador += 1
        
print(f"el numero de vocales en {palabra} es: {contador}")


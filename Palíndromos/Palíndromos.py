# el replace literalmente significa remplazar y sirve ppara remplazar los espacios vacios por nada aqui
palabra = input("Ingresa una palabra o frase: ").replace(" ","").lower()
# esto sirve para invertir la palabra o frase, aunque no se si funciona con numeros, supongo que solo funciona con string
palindromo = palabra[::-1]

if palabra == palindromo:
    print(f"La palabra/frase es un palíndromo.")
else:
    print(f"la palabra/frase no es un palindromo.")
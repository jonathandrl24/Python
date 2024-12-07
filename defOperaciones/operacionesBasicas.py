import math

def cuadrado(lado):
    return lado * lado
    
def rectangulo(base, altura):
    return base * altura

def triangulo(base, altura):
    return (base * altura) / 2

def circulo(radio):
    return math.pi * (radio ** 2)

print("Elige una figura para calcular su area: ")
print("1. cuadrado")
print("2. rectangulo")
print("3. triangulo")
print("4. circulo")

figura = input("Escriba el numero de su figura: ")
figura = int(figura)

if figura == 1:
    lado = float(input("Ingresa el lado del cuadrado: "))
    print(f"El area del cuadrado es = {cuadrado(lado)}")
elif figura == 2:
    base = float(input("Ingresa la base del rectangulo: "))
    altura = float(input("Ingresa la altura del rectangulo: "))
    print(f"El area del rectangulo es = {rectangulo(base, altura)}")
elif figura == 3:
    base = float(input("Ingresa la base del triangulo: "))
    altura = float(input("Ingresa la altura del triangulo: "))
    print(f"El area del triangulo es = {triangulo(base, altura)}")
elif figura == 4:
    radio = float(input("Ingresa el radio del circulo: "))
    print(f"El area del circulo es = {circulo(radio)}")
else:
    print("Ingrese una figura valida")
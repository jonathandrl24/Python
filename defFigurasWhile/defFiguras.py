import math

def cuadrado(lado):
    return lado * lado
def rectangulo(base, altura):
    return base * altura
def triangulo(base, altura):
    return (base * altura) / 2
def circulo(radio):
    return math.pi * (radio ** 2)
    
while True:
    print("Ingrese una figura para calcular area: ")
    print("1. cuadrado")
    print("2. rectangulo")
    print("3. triangulo")
    print("4. circulo")
    figura = input("Ingrese el numero de su figura (o escriba 'salir'): ")
    
    if figura.lower() == "salir":
        print("Hasta Luego!")
        break
    
    try:
        figura = int(figura)
        
        if figura == 1:
            lado = float(input("Ingrese el lado del cuadrado: "))
            print(f"El area del cuadrado es = {cuadrado(lado)}")
        elif figura == 2:
            base = float(input("Ingrese la base del rectangulo: "))
            altura = float(input("Ingrese la altura del rectangulo: "))
            print(f"El area del rectangulo es = {rectangulo(base, altura)}")
        elif figura == 3:
            base = float(input("la base del triangulo es: "))
            altura = float(input("La altura del triangulo es: "))
            print(f"El area de triangulo es = {triangulo(base, altura)}")
        elif figura == 4:
            radio = float(input("Ingrese el radio del circulo: "))
            print(F"el area del circulo es = {circulo(radio)}")
        else:
            print("Ingrese una figura valida")
    except ValueError:
        print("valor incorrecto")
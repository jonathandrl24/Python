import math
# funciones de tipo variable args
def area(idx, *lados):
    if idx==1:print("area cuadrado = ", str(lados[0]**2))
    if idx==2:print("area rectangulo = ", str(lados[0]*lados[1]))
    if idx==3:print("area triangulo = ", str((lados[0]*lados[1]) / 2))
    if idx==4:print("area circulo = ", str(math.pi * (lados[0]**2)))

while True:
    print("Ingrese una figura para calcular area: ")
    print("1. cuadrado")
    print("2. rectangulo")
    print("3. triangulo")
    print("4. circulo")
    idx = input("Ingrese el numero de su figura (o escriba 'salir'): ")
    
    if idx.lower() == "salir":
        print("Hasta Luego!")
        break
    
    try:
        idx = int(idx)
        
        if idx == 1:
            area(idx, float(input("Ingrese el lado del cuadrado: ")))
        elif idx == 2:
            a = float(input("Ingrese la base del rectangulo: "))
            b = float(input("Ingrese la altura del rectangulo: "))
            area(idx, a, b)
        elif idx == 3:
            a = float(input("la base del triangulo es: "))
            b = float(input("La altura del triangulo es: "))
            area(idx, a, b)
        elif idx == 4:
            area(idx, float(input("Ingrese el radio del circulo: ")))
        else:
            print("Ingrese una figura valida")
            
    except ValueError:
        print("valor incorrecto")
import time

while True:
    fecha = time.strftime('%D')
    tiempo = time.strftime('%H:%M:%S')
    print(f"\rFecha: {fecha}, Hora Actual: {tiempo}", end='')

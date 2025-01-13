import turtle as l
import colorsys
import time

l.bgcolor("black")
l.tracer(0)  
l.pensize(1)

h = 0.0  
i = 1  
increment = 1  
start_time = time.time()  

while True:  
    if increment == -1:
        l.clear()
        l.bgcolor("black") 
    
    c = colorsys.hsv_to_rgb(h, 1, 1)
    
    l.fillcolor(c)  
    l.begin_fill()
    l.fd(i)
    l.lt(100)
    l.circle(30)
    for j in range(2):
        l.fd(i * j)
        l.rt(109)
    l.end_fill()
    
    h += 0.005 * increment  
    if h > 1:  
        h -= 1
    elif h < 0:  
        h += 1
    
    i += increment  
    
    elapsed_time = time.time() - start_time
    if elapsed_time > 20:  
        increment = -1  
    if i <= 1:  
        start_time = time.time()  
        increment = 1  
 
    l.update()
    
    time.sleep(0.01)

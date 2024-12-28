import turtle as l 
import colorsys

l.bgcolor("black")
l.tracer(100)
l.pensize(1)
h = 0.5
for i in range(450):
    c= colorsys.hsv_to_rgb(h,1,1)
    h= 0.0008
    l.fillcolor(c)
    l.begin_fill()
    l.fd(i)
    l.lt(100)
    l.circle(30)
    for j in range(2):
        l.fd(i*j)
        l.rt(109)
    l.end_fill()
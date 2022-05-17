import random
from glob import glob
from lib2to3.pgen2.grammar import opmap_raw
import time
import turtle
import pygame
import os
import sys
from datetime import datetime, timedelta



actual_hour = datetime.now()

def resolver_ruta(ruta_relativa):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, ruta_relativa)
    return os.path.join(os.path.abspath('.'), ruta_relativa)

first_open = 1
mute = 1
fps = 0.1 #Reduce los FPS

#   CONGIFURACION VENTANA
window = turtle.Screen() #Creamos la ventana
window.title("Tamagotchi") #Titulo de ventana
window.bgcolor("black") #Color de fondo de ventana
window.setup(width = 410, height = 410) #Tamaño de ventana
window.tracer(0) #Animaciones mas suaves

#   POSICIONES
x_text_happy = -100
y_text_happy = 160

x_text_life = 180
y_text_life = 160

x_text_hungry = 55
y_text_hungry = 160

x_tamagotchi = 0
y_tamagotchi = 40

x_apple = 10
y_apple = 0

x_gamepad = 135
y_gamepad = 0


#   BOTONES CONFIGURACION
left_button_obj = turtle.Turtle()
left_button_x = -120
left_button_y = -140
left_button_r = 2.5

middle_button_obj = turtle.Turtle()
middle_button_x = 0
middle_button_y = -140
middle_button_r = 2.5

right_button_obj = turtle.Turtle()
right_button_x = 120
right_button_y = -140
right_button_r = 2.5


#   VARIABLES
life = 1
hungry = 1
happiness = 1
happy = ":("
pixel_life = []
pixel_hung = []
pixel = []
blink = 0
option = 0
eating = 0
playing = False
game_pixel = []
disparar = True
der_apretado = False
izq_apretado = False
destruidos = 0
variables = []
last_hour = 0
time_passed = 0


#   LEER DATOS DE FICHERO
def read_data():
    global first_open
    global hungry
    global life
    global happiness
    global mute
    global last_hour
    global time_passed
    global name

    with open(resolver_ruta('./data.txt'), "r", encoding="utf-8") as data_file:
        total_lines = sum(1 for line in data_file)
        
        data = open(resolver_ruta('./data.txt'), "r", encoding="utf-8")
        for i in range(total_lines):
        
            if(i != (total_lines - 1) and i != (total_lines -2)):
                variables.append(int(data.readline()))
            elif (i == (total_lines -2)):
                variables.append(datetime.strptime(data.readline().rstrip('\n'), '%Y-%m-%d %H:%M:%S.%f'))
            elif (i == (total_lines -1)):
                variables.append(str(data.readline()))



        first_open = variables[0]
        hungry = variables[1]
        life = variables[2]
        happiness = variables[3]
        mute = variables[4]
        last_hour = variables[5]
        name = variables[6]

        time_passed = actual_hour - last_hour  #Tiempo que paso desde la ultima vez que se jugo        
        data_file.close()


#   ESCRIBIR DATOS EN FICHERO
def write_data():
    global first_open
    global hungry
    global life
    global happiness
    global mute
    global name

    with open(resolver_ruta('./data.txt'), "w", encoding="utf-8") as data_file:
        life = int((happiness + hungry)/2)
        data_file.seek(0)
        data_file.write(f"{first_open}\n")
        data_file.write(f"{hungry}\n")
        data_file.write(f"{life}\n")
        data_file.write(f"{happiness}\n")
        if(mute == 1):
            data_file.write("0\n")
        else:
            data_file.write("1\n")
        data_file.write(f"{actual_hour}\n")
        data_file.write(f"{name}")
        data_file.close()

if(os.path.exists(resolver_ruta('./data.txt')) == False):
    name = turtle.textinput("Enter your pet's name", "Pet's name:").rstrip('\n')
    print(name)
    window.title(f"{name}")
    write_data()
    read_data()
    first_open = 0
    write_data()
else:
    read_data()
    if (abs(time_passed) >= timedelta(0.5)) and (abs(time_passed) <= timedelta(1)):  #12hs - 24hs
        hungry -= 3
        happiness -= 2

        if(happiness< 0):
            happiness = 0

        if(hungry< 0):
            hungry = 0
    elif(abs(time_passed) > timedelta(1)) and (abs(time_passed) <= timedelta(1.5)): #24hs a 36hs
        hungry -= 6
        happiness -= 4

        if(happiness< 0):
            happiness = 0

        if(hungry< 0):
            hungry = 0
    elif(abs(time_passed) > timedelta(1.5)) and (abs(time_passed) <= timedelta(2)): #36hs a 48hs
        hungry -= 9
        happiness -= 6

        if(happiness< 0):
            happiness = 0

        if(hungry< 0):
            hungry = 0
    elif(abs(time_passed) > timedelta(2)) and (abs(time_passed) <= timedelta(2.5)): #48hs a 60hs
        hungry -= 10
        happiness -= 8

        if(happiness< 0):
            happiness = 0

        if(hungry< 0):
            hungry = 0
    elif(abs(time_passed) > timedelta(2.5)): #60hs a 72hs
        hungry -= 10
        happiness -= 10

        if(happiness< 0):
            happiness = 0

        if(hungry< 0):
            hungry = 0

    window.title(f"{name}")
    write_data()


def reproducir():
    global mute
    pygame.mixer.init()
    pygame.mixer.music.load(resolver_ruta("./tamagotchi-song.mp3"))

    if(mute == 0):
        pygame.mixer.music.play(-1) #Se reproduce infinitamente
        mute = 1
    else:
        pygame.mixer.music.stop() #Se frena
        mute = 0

    write_data()

reproducir()

game_pixel.append(turtle.Turtle()) # 0 = izq
game_pixel.append(turtle.Turtle()) # 1 = der

for i in range(2):
    game_pixel[i].speed(0)
    game_pixel[i].shape("triangle")
    game_pixel[i].shapesize(1)
    game_pixel[i].color("black")
    game_pixel[i].penup()
    game_pixel[i].direction = "stop"
    
game_pixel[0].goto(-300, 0)
game_pixel[1].goto(300, 0)
game_pixel[1].left(180)

for i in range(10):
    pixel_life.append(turtle.Turtle())
    pixel_hung.append(turtle.Turtle())
    pixel_hung[i].hideturtle()
    pixel_life[i].hideturtle()

for i in range(188):
    pixel.append(turtle.Turtle())
    pixel[i].hideturtle()

#   BOTONES
def left_button(x, y, size,color):
    global left_button_obj
    left_button_obj.speed(0)
    left_button_obj.shape("circle")
    left_button_obj.shapesize(size,size)
    left_button_obj.color(color)
    left_button_obj.penup()
    left_button_obj.goto(x,y)
    left_button_obj.direction = "stop"

left_button(left_button_x, left_button_y, left_button_r, "white")

def middle_button(x, y, size,color):
    global middle_button_obj
    middle_button_obj.speed(0)
    middle_button_obj.shape("circle")
    middle_button_obj.shapesize(size,size)
    middle_button_obj.color(color)
    middle_button_obj.penup()
    middle_button_obj.goto(x,y)
    middle_button_obj.direction = "stop"

middle_button(middle_button_x, middle_button_y, middle_button_r, "white")

def right_button(x, y, size,color):
    global right_button_obj
    right_button_obj.speed(0)
    right_button_obj.shape("circle")
    right_button_obj.shapesize(size,size)
    right_button_obj.color(color)
    right_button_obj.penup()
    right_button_obj.goto(x,y)
    right_button_obj.direction = "stop"

right_button(right_button_x, right_button_y, right_button_r, "white")

#   DIBUJAR PIXELES
def draw(x,y,color,size,i):
    global pixel
    pixel[i].speed(0)
    pixel[i].shape("square")
    pixel[i].shapesize(size,size)
    pixel[i].color(color)
    pixel[i].showturtle()
    pixel[i].penup()
    pixel[i].goto(x,y)
    pixel[i].direction = "stop"

#   BARRA VIDA

def barraLife(x,y,color,size,i):

    global pixel_life
    pixel_life[i].speed(0)
    pixel_life[i].shape("square")
    pixel_life[i].shapesize(size,size)
    pixel_life[i].color(color)
    pixel_life[i].showturtle()
    pixel_life[i].penup()
    pixel_life[i].goto(x,y)
    pixel_life[i].direction = "stop"

def barraLifePrint():

    for i in range(life):
        barraLife(-140 + (i*7), 169,"white",0.25, i)  # X , Y

    for i in range((10-life)):
        i += life
        barraLife(-140 + (i*7), 169,"grey",0.25, i)   # X , Y


#   BARRA HAMBRE
def barraHung(x,y,color,size,i):

    global pixel_hung
    pixel_hung[i].speed(0)
    pixel_hung[i].shape("square")
    pixel_hung[i].shapesize(size,size)
    pixel_hung[i].color(color)
    pixel_hung[i].showturtle()
    pixel_hung[i].penup()
    pixel_hung[i].goto(x,y)
    pixel_hung[i].direction = "stop"

def barraHungPrint():
    global hungry

    if hungry>10:
        hungry = 10

    for i in range(hungry):
        barraHung(((x_text_hungry*(-1))+70) + (i*7), 169,"white",0.25, i)  # X , Y

    for i in range((10-hungry)):
        i += hungry
        barraHung(((x_text_hungry*(-1))+70) + (i*7), 169,"grey",0.25, i)   # X , Y

#   TEXTOS
text = []

for i in range(5):
    text.append(turtle.Turtle())
    text[i].hideturtle()

def textos(texto,x,y,color, i):
    text[i] = turtle.Turtle()
    text[i].color(color)
    text[i].speed(0)
    text[i].penup()
    text[i].hideturtle()
    text[i].left(90)
    text[i].forward(y)
    text[i].left(90)
    text[i].forward(x)
    text[i].write(texto, move=False, align="left", font=("Arial", 13, "normal")) 


#   BARRA VIDA
textos("LIFE : ", x_text_life, y_text_life, "white", 0)
barraLifePrint()

#   BARRA DE HAMBRE
textos("HUNGRY : ", x_text_hungry, y_text_hungry, "white", 1)
barraHungPrint()

#   FELICIDAD
textos("HAPPY : ", x_text_happy, y_text_happy, "white", 3)
if(happiness <= 0 and happiness < 4 ):
    happy = ":("
elif(happiness >= 4 and happiness < 7):
    happy = ":|"
elif(happiness >= 7 and happiness <= 10):
    happy = ":)"

if (happy == ":)"):
    text[4].clear()
    textos(":)", (x_text_happy - 60), (y_text_happy + 2), "green", 4)
elif (happy == ":|"):
    text[4].clear()
    textos(":|", (x_text_happy - 60), (y_text_happy + 2), "yellow", 4)
elif (happy == ":("):
    text[4].clear()
    textos(":(", (x_text_happy - 60), (y_text_happy + 2), "red", 4)


#   ANIMACION TAMAGOTCHI IDDLE
def iddle():
    global blink
    global x_tamagotchi
    global y_tamagotchi

    if (blink >= 0 and blink <= 4):
        draw((20 + x_tamagotchi),(40 + y_tamagotchi),"white",0.5,1)
        draw((10 + x_tamagotchi),(40 + y_tamagotchi),"white",0.5,2)
        draw((0 + x_tamagotchi),(40 + y_tamagotchi),"white",0.5,3)
        draw((-10 + x_tamagotchi),(40 + y_tamagotchi),"white",0.5,4)

        draw((30 + x_tamagotchi),(30 + y_tamagotchi),"white",0.5,5)
        draw((-20 + x_tamagotchi),(30 + y_tamagotchi),"white",0.5,6)

        draw((40 + x_tamagotchi),(20 + y_tamagotchi),"white",0.5,7)
        draw((-30 + x_tamagotchi),(20 + y_tamagotchi),"white",0.5,8)
        draw((40 + x_tamagotchi),(10 + y_tamagotchi),"white",0.5,9)
        draw((-30 + x_tamagotchi),(10 + y_tamagotchi),"white",0.5,10)
        draw((40 + x_tamagotchi),(0 + y_tamagotchi),"white",0.5,11)
        draw((-30 + x_tamagotchi),(0 + y_tamagotchi),"white",0.5,12)
        draw((40 + x_tamagotchi),(-10 + y_tamagotchi),"white",0.5,13)
        draw((-30 + x_tamagotchi),(-10 + y_tamagotchi),"white",0.5,14)
        draw((40 + x_tamagotchi),(-20 + y_tamagotchi),"white",0.5,15)
        draw((-30 + x_tamagotchi),(-20 + y_tamagotchi),"white",0.5,16)
        draw((40 + x_tamagotchi),(-30 + y_tamagotchi),"white",0.5,17)
        draw((-30 + x_tamagotchi),(-30 + y_tamagotchi),"white",0.5,18)

        draw((30 + x_tamagotchi),(-40 + y_tamagotchi),"white",0.5,19)
        draw((20 + x_tamagotchi),(-40 + y_tamagotchi),"white",0.5,20)
        draw((10 + x_tamagotchi),(-40 + y_tamagotchi),"white",0.5,21)
        draw((0 + x_tamagotchi),(-40 + y_tamagotchi),"white",0.5,22)
        draw((-10 + x_tamagotchi),(-40 + y_tamagotchi),"white",0.5,23)
        draw((-20 + x_tamagotchi),(-40 + y_tamagotchi),"white",0.5,24)

        #OJOS
        draw((20 + x_tamagotchi),(10 + y_tamagotchi),"white",0.5,25)
        draw((-10 + x_tamagotchi),(10 + y_tamagotchi),"white",0.5,26)

        #BOCA
        draw((20 + x_tamagotchi),(-10 + y_tamagotchi),"black",0.5,180)
        draw((10 + x_tamagotchi),(-10 + y_tamagotchi),"black",0.5,181)
        draw((0 + x_tamagotchi),(-10 + y_tamagotchi),"black",0.5,182)
        draw((-10 + x_tamagotchi),(-10 + y_tamagotchi),"black",0.5,183)
        draw((20 + x_tamagotchi),(-20 + y_tamagotchi),"black",0.5,184)
        draw((10 + x_tamagotchi),(-20 + y_tamagotchi),"black",0.5,185)
        draw((0 + x_tamagotchi),(-20 + y_tamagotchi),"black",0.5,186)
        draw((-10 + x_tamagotchi),(-20 + y_tamagotchi),"black",0.5,187)
    else:
        draw((20 + x_tamagotchi),(30 + y_tamagotchi),"white",0.5,1)
        draw((10 + x_tamagotchi),(30 + y_tamagotchi),"white",0.5,2)
        draw((0 + x_tamagotchi),(30 + y_tamagotchi),"white",0.5,3)
        draw((-10 + x_tamagotchi),(30 + y_tamagotchi),"white",0.5,4)

        draw((30 + x_tamagotchi),(20 + y_tamagotchi),"white",0.5,5)
        draw((-20 + x_tamagotchi),(20 + y_tamagotchi),"white",0.5,6)

        draw((40 + x_tamagotchi),(20 + y_tamagotchi),"black",0.5,7)
        draw((-30 + x_tamagotchi),(20 + y_tamagotchi),"black",0.5,8)

        #OJOS
        draw((20 + x_tamagotchi),(10 + y_tamagotchi),"black",0.5,25)
        draw((-10 + x_tamagotchi),(10 + y_tamagotchi),"black",0.5,26)

        #BOCA
        draw((20 + x_tamagotchi),(-10 + y_tamagotchi),"black",0.5,180)
        draw((10 + x_tamagotchi),(-10 + y_tamagotchi),"black",0.5,181)
        draw((0 + x_tamagotchi),(-10 + y_tamagotchi),"black",0.5,182)
        draw((-10 + x_tamagotchi),(-10 + y_tamagotchi),"black",0.5,183)
        draw((20 + x_tamagotchi),(-20 + y_tamagotchi),"black",0.5,184)
        draw((10 + x_tamagotchi),(-20 + y_tamagotchi),"black",0.5,185)
        draw((0 + x_tamagotchi),(-20 + y_tamagotchi),"black",0.5,186)
        draw((-10 + x_tamagotchi),(-20 + y_tamagotchi),"black",0.5,187)
    
    blink += 1
    if (blink == 7):
        blink = 0

def eat_anim():
    global blink
    global x_tamagotchi
    global y_tamagotchi
    global eating
    global hungry

    if (blink >= 0 and blink <= 4):
        draw((20 + x_tamagotchi),(40 + y_tamagotchi),"white",0.5,1)
        draw((10 + x_tamagotchi),(40 + y_tamagotchi),"white",0.5,2)
        draw((0 + x_tamagotchi),(40 + y_tamagotchi),"white",0.5,3)
        draw((-10 + x_tamagotchi),(40 + y_tamagotchi),"white",0.5,4)

        draw((30 + x_tamagotchi),(30 + y_tamagotchi),"white",0.5,5)
        draw((-20 + x_tamagotchi),(30 + y_tamagotchi),"white",0.5,6)

        draw((40 + x_tamagotchi),(20 + y_tamagotchi),"white",0.5,7)
        draw((-30 + x_tamagotchi),(20 + y_tamagotchi),"white",0.5,8)
        draw((40 + x_tamagotchi),(10 + y_tamagotchi),"white",0.5,9)
        draw((-30 + x_tamagotchi),(10 + y_tamagotchi),"white",0.5,10)
        draw((40 + x_tamagotchi),(0 + y_tamagotchi),"white",0.5,11)
        draw((-30 + x_tamagotchi),(0 + y_tamagotchi),"white",0.5,12)
        draw((40 + x_tamagotchi),(-10 + y_tamagotchi),"white",0.5,13)
        draw((-30 + x_tamagotchi),(-10 + y_tamagotchi),"white",0.5,14)
        draw((40 + x_tamagotchi),(-20 + y_tamagotchi),"white",0.5,15)
        draw((-30 + x_tamagotchi),(-20 + y_tamagotchi),"white",0.5,16)
        draw((40 + x_tamagotchi),(-30 + y_tamagotchi),"white",0.5,17)
        draw((-30 + x_tamagotchi),(-30 + y_tamagotchi),"white",0.5,18)

        draw((30 + x_tamagotchi),(-40 + y_tamagotchi),"white",0.5,19)
        draw((20 + x_tamagotchi),(-40 + y_tamagotchi),"white",0.5,20)
        draw((10 + x_tamagotchi),(-40 + y_tamagotchi),"white",0.5,21)
        draw((0 + x_tamagotchi),(-40 + y_tamagotchi),"white",0.5,22)
        draw((-10 + x_tamagotchi),(-40 + y_tamagotchi),"white",0.5,23)
        draw((-20 + x_tamagotchi),(-40 + y_tamagotchi),"white",0.5,24)

        #OJOS
        draw((20 + x_tamagotchi),(10 + y_tamagotchi),"white",0.5,25)
        draw((-10 + x_tamagotchi),(10 + y_tamagotchi),"white",0.5,26)

        #BOCA
        draw((20 + x_tamagotchi),(-10 + y_tamagotchi),"white",0.5,180)
        draw((10 + x_tamagotchi),(-10 + y_tamagotchi),"white",0.5,181)
        draw((0 + x_tamagotchi),(-10 + y_tamagotchi),"white",0.5,182)
        draw((-10 + x_tamagotchi),(-10 + y_tamagotchi),"white",0.5,183)
        draw((20 + x_tamagotchi),(-20 + y_tamagotchi),"white",0.5,184)
        draw((10 + x_tamagotchi),(-20 + y_tamagotchi),"white",0.5,185)
        draw((0 + x_tamagotchi),(-20 + y_tamagotchi),"white",0.5,186)
        draw((-10 + x_tamagotchi),(-20 + y_tamagotchi),"white",0.5,187)
    else:
        draw((20 + x_tamagotchi),(30 + y_tamagotchi),"white",0.5,1)
        draw((10 + x_tamagotchi),(30 + y_tamagotchi),"white",0.5,2)
        draw((0 + x_tamagotchi),(30 + y_tamagotchi),"white",0.5,3)
        draw((-10 + x_tamagotchi),(30 + y_tamagotchi),"white",0.5,4)

        draw((30 + x_tamagotchi),(20 + y_tamagotchi),"white",0.5,5)
        draw((-20 + x_tamagotchi),(20 + y_tamagotchi),"white",0.5,6)

        draw((40 + x_tamagotchi),(20 + y_tamagotchi),"black",0.5,7)
        draw((-30 + x_tamagotchi),(20 + y_tamagotchi),"black",0.5,8)

        #OJOS
        draw((20 + x_tamagotchi),(10 + y_tamagotchi),"black",0.5,25)
        draw((-10 + x_tamagotchi),(10 + y_tamagotchi),"black",0.5,26)

        #BOCA
        draw((20 + x_tamagotchi),(-10 + y_tamagotchi),"black",0.5,180)
        draw((10 + x_tamagotchi),(-10 + y_tamagotchi),"black",0.5,181)
        draw((0 + x_tamagotchi),(-10 + y_tamagotchi),"black",0.5,182)
        draw((-10 + x_tamagotchi),(-10 + y_tamagotchi),"black",0.5,183)
        draw((20 + x_tamagotchi),(-20 + y_tamagotchi),"white",0.5,184)
        draw((10 + x_tamagotchi),(-20 + y_tamagotchi),"white",0.5,185)
        draw((0 + x_tamagotchi),(-20 + y_tamagotchi),"white",0.5,186)
        draw((-10 + x_tamagotchi),(-20 + y_tamagotchi),"white",0.5,187)
    
    blink += 1
    if (blink == 7):
        blink = 0
        eating += 1
        if(eating == 3):
            hungry += 2
            eating = 0
            barraHungPrint()
            write_data()
            barraLifePrint()
    
def play():
    global game_pixel
    global playing
    global disparar
    global lado
    global destruidos
    global fps
    global izq_apretado
    global der_apretado

    draw_option(0, -95, "black", 0.5, 27)

    draw((20 + x_tamagotchi),(40 + y_tamagotchi),"white",0.5,1)
    draw((10 + x_tamagotchi),(40 + y_tamagotchi),"white",0.5,2)
    draw((0 + x_tamagotchi),(40 + y_tamagotchi),"white",0.5,3)
    draw((-10 + x_tamagotchi),(40 + y_tamagotchi),"white",0.5,4)

    draw((30 + x_tamagotchi),(30 + y_tamagotchi),"white",0.5,5)
    draw((-20 + x_tamagotchi),(30 + y_tamagotchi),"white",0.5,6)

    draw((40 + x_tamagotchi),(20 + y_tamagotchi),"white",0.5,7)
    draw((-30 + x_tamagotchi),(20 + y_tamagotchi),"white",0.5,8)
    draw((40 + x_tamagotchi),(10 + y_tamagotchi),"white",0.5,9)
    draw((-30 + x_tamagotchi),(10 + y_tamagotchi),"white",0.5,10)
    draw((40 + x_tamagotchi),(0 + y_tamagotchi),"white",0.5,11)
    draw((-30 + x_tamagotchi),(0 + y_tamagotchi),"white",0.5,12)
    draw((40 + x_tamagotchi),(-10 + y_tamagotchi),"white",0.5,13)
    draw((-30 + x_tamagotchi),(-10 + y_tamagotchi),"white",0.5,14)
    draw((40 + x_tamagotchi),(-20 + y_tamagotchi),"white",0.5,15)
    draw((-30 + x_tamagotchi),(-20 + y_tamagotchi),"white",0.5,16)
    draw((40 + x_tamagotchi),(-30 + y_tamagotchi),"white",0.5,17)
    draw((-30 + x_tamagotchi),(-30 + y_tamagotchi),"white",0.5,18)

    draw((30 + x_tamagotchi),(-40 + y_tamagotchi),"white",0.5,19)
    draw((20 + x_tamagotchi),(-40 + y_tamagotchi),"white",0.5,20)
    draw((10 + x_tamagotchi),(-40 + y_tamagotchi),"white",0.5,21)
    draw((0 + x_tamagotchi),(-40 + y_tamagotchi),"white",0.5,22)
    draw((-10 + x_tamagotchi),(-40 + y_tamagotchi),"white",0.5,23)
    draw((-20 + x_tamagotchi),(-40 + y_tamagotchi),"white",0.5,24)

    #OJOS
    draw((20 + x_tamagotchi),(10 + y_tamagotchi),"white",0.5,25)
    draw((-10 + x_tamagotchi),(10 + y_tamagotchi),"white",0.5,26)

    #BOCA
    draw((20 + x_tamagotchi),(-10 + y_tamagotchi),"white",0.5,180)
    draw((10 + x_tamagotchi),(-10 + y_tamagotchi),"white",0.5,181)
    draw((0 + x_tamagotchi),(-10 + y_tamagotchi),"white",0.5,182)
    draw((-10 + x_tamagotchi),(-10 + y_tamagotchi),"white",0.5,183)
    draw((20 + x_tamagotchi),(-20 + y_tamagotchi),"white",0.5,184)
    draw((10 + x_tamagotchi),(-20 + y_tamagotchi),"white",0.5,185)
    draw((0 + x_tamagotchi),(-20 + y_tamagotchi),"white",0.5,186)
    draw((-10 + x_tamagotchi),(-20 + y_tamagotchi),"white",0.5,187)

    speed = 2

    fps = 0
    if(disparar == True):
        izq_apretado = False
        der_apretado = False
        lado = random.randint(0, 1)
        game_pixel[0].goto(-270, 40)
        game_pixel[1].goto(270, 40)
        disparar = False

    game_pixel[lado].color("white")
    game_pixel[lado].forward(speed + destruidos)
    
    if(lado == 0):

        game_pixel[lado].direction = "right"

        if(game_pixel[lado].xcor() >= -50):
            game_pixel[lado].color("black")
            game_pixel[lado].forward(0)
            playing = False
            disparar = True
        if(izq_apretado == True):
            game_pixel[lado].color("black")
            game_pixel[lado].forward(0)
            disparar = True
            destruidos += 0.5
        elif(der_apretado == True):
            game_pixel[lado].color("black")
            game_pixel[lado].forward(0)
            playing = False
            disparar = True
    elif(lado == 1):

        game_pixel[lado].direction = "left"

        if(game_pixel[lado].xcor() <= 60):
            game_pixel[lado].color("black")
            game_pixel[lado].forward(0)
            playing = False
            disparar = True
        if(izq_apretado == True):
            game_pixel[lado].color("black")
            game_pixel[lado].forward(0)
            playing = False
            disparar = True
        elif(der_apretado == True):
            game_pixel[lado].color("black")
            game_pixel[lado].forward(0)
            disparar = True
            destruidos += 0.5
    
    if(playing == False):
        apple("white")
        gamepad("#D8D8D8")
        draw_option(0, -95, "white", 0.5, 27)
        

def apple(color_apple):
    draw((-130 + x_apple),(-43 + y_apple),"black",0.15,28)
    draw((-127 + x_apple),(-43 + y_apple),color_apple,0.15,29)
    draw((-130 + x_apple),(-47 + y_apple),color_apple,0.15,30)
    draw((-133 + x_apple),(-47 + y_apple),color_apple,0.15,31)

    draw((-142 + x_apple),(-51 + y_apple),color_apple,0.15,32)
    draw((-139 + x_apple),(-51 + y_apple),color_apple,0.15,33)
    draw((-136 + x_apple),(-51 + y_apple),color_apple,0.15,34)
    draw((-133 + x_apple),(-51 + y_apple),color_apple,0.15,35)
    draw((-130 + x_apple),(-51 + y_apple),color_apple,0.15,36)
    draw((-127 + x_apple),(-51 + y_apple),color_apple,0.15,37)
    draw((-124 + x_apple),(-51 + y_apple),color_apple,0.15,38)
    draw((-121 + x_apple),(-51 + y_apple),color_apple,0.15,39)

    draw((-145 + x_apple),(-55 + y_apple),color_apple,0.15,40)
    draw((-142 + x_apple),(-55 + y_apple),color_apple,0.15,41)
    draw((-139 + x_apple),(-55 + y_apple),color_apple,0.15,42)
    draw((-136 + x_apple),(-55 + y_apple),color_apple,0.15,43)
    draw((-133 + x_apple),(-55 + y_apple),color_apple,0.15,44)
    draw((-130 + x_apple),(-55 + y_apple),color_apple,0.15,45)
    draw((-127 + x_apple),(-55 + y_apple),color_apple,0.15,46)
    draw((-124 + x_apple),(-55 + y_apple),color_apple,0.15,47)
    draw((-121 + x_apple),(-55 + y_apple),color_apple,0.15,48)
    draw((-118 + x_apple),(-55 + y_apple),color_apple,0.15,49)

    draw((-148 + x_apple),(-59 + y_apple),color_apple,0.15,50)
    draw((-145 + x_apple),(-59 + y_apple),color_apple,0.15,51)
    draw((-142 + x_apple),(-59 + y_apple),"black",0.15,52)
    draw((-139 + x_apple),(-59 + y_apple),color_apple,0.15,53)
    draw((-136 + x_apple),(-59 + y_apple),color_apple,0.15,54)
    draw((-133 + x_apple),(-59 + y_apple),color_apple,0.15,55)
    draw((-130 + x_apple),(-59 + y_apple),color_apple,0.15,56)
    draw((-127 + x_apple),(-59 + y_apple),color_apple,0.15,57)
    draw((-124 + x_apple),(-59 + y_apple),color_apple,0.15,58)
    draw((-121 + x_apple),(-59 + y_apple),color_apple,0.15,59)
    draw((-118 + x_apple),(-59 + y_apple),color_apple,0.15,60)
    draw((-115 + x_apple),(-59 + y_apple),color_apple,0.15,61)

    draw((-148 + x_apple),(-63 + y_apple),color_apple,0.15,62)
    draw((-145 + x_apple),(-63 + y_apple),color_apple,0.15,63)
    draw((-142 + x_apple),(-63 + y_apple),"black",0.15,64)
    draw((-139 + x_apple),(-63 + y_apple),color_apple,0.15,65)
    draw((-136 + x_apple),(-63 + y_apple),color_apple,0.15,66)
    draw((-133 + x_apple),(-63 + y_apple),color_apple,0.15,67)
    draw((-130 + x_apple),(-63 + y_apple),color_apple,0.15,68)
    draw((-127 + x_apple),(-63 + y_apple),color_apple,0.15,69)
    draw((-124 + x_apple),(-63 + y_apple),color_apple,0.15,70)
    draw((-121 + x_apple),(-63 + y_apple),color_apple,0.15,71)
    draw((-118 + x_apple),(-63 + y_apple),color_apple,0.15,72)
    draw((-115 + x_apple),(-63 + y_apple),color_apple,0.15,73)

    draw((-148 + x_apple),(-67 + y_apple),color_apple,0.15,74)
    draw((-145 + x_apple),(-67 + y_apple),color_apple,0.15,75)
    draw((-142 + x_apple),(-67 + y_apple),color_apple,0.15,76)
    draw((-139 + x_apple),(-67 + y_apple),color_apple,0.15,77)
    draw((-136 + x_apple),(-67 + y_apple),color_apple,0.15,78)
    draw((-133 + x_apple),(-67 + y_apple),color_apple,0.15,79)
    draw((-130 + x_apple),(-67 + y_apple),color_apple,0.15,80)
    draw((-127 + x_apple),(-67 + y_apple),color_apple,0.15,81)
    draw((-124 + x_apple),(-67 + y_apple),color_apple,0.15,82)
    draw((-121 + x_apple),(-67 + y_apple),color_apple,0.15,83)
    draw((-118 + x_apple),(-67 + y_apple),color_apple,0.15,84)
    draw((-115 + x_apple),(-67 + y_apple),color_apple,0.15,85)

    draw((-148 + x_apple),(-71 + y_apple),color_apple,0.15,86)
    draw((-145 + x_apple),(-71 + y_apple),color_apple,0.15,87)
    draw((-142 + x_apple),(-71 + y_apple),color_apple,0.15,88)
    draw((-139 + x_apple),(-71 + y_apple),"black",0.15,89)
    draw((-136 + x_apple),(-71 + y_apple),color_apple,0.15,90)
    draw((-133 + x_apple),(-71 + y_apple),color_apple,0.15,91)
    draw((-130 + x_apple),(-71 + y_apple),color_apple,0.15,92)
    draw((-127 + x_apple),(-71 + y_apple),color_apple,0.15,93)
    draw((-124 + x_apple),(-71 + y_apple),color_apple,0.15,94)
    draw((-121 + x_apple),(-71 + y_apple),color_apple,0.15,95)
    draw((-118 + x_apple),(-71 + y_apple),color_apple,0.15,96)
    draw((-115 + x_apple),(-71 + y_apple),color_apple,0.15,97)

    draw((-145 + x_apple),(-75 + y_apple),color_apple,0.15,98)
    draw((-142 + x_apple),(-75 + y_apple),color_apple,0.15,99)
    draw((-139 + x_apple),(-75 + y_apple),color_apple,0.15,100)
    draw((-136 + x_apple),(-75 + y_apple),color_apple,0.15,101)
    draw((-133 + x_apple),(-75 + y_apple),color_apple,0.15,102)
    draw((-130 + x_apple),(-75 + y_apple),color_apple,0.15,103)
    draw((-127 + x_apple),(-75 + y_apple),color_apple,0.15,104)
    draw((-124 + x_apple),(-75 + y_apple),color_apple,0.15,105)
    draw((-121 + x_apple),(-75 + y_apple),color_apple,0.15,106)
    draw((-118 + x_apple),(-75 + y_apple),color_apple,0.15,107)

    draw((-142 + x_apple),(-79 + y_apple),color_apple,0.15,108)
    draw((-139 + x_apple),(-79 + y_apple),color_apple,0.15,109)
    draw((-136 + x_apple),(-79 + y_apple),color_apple,0.15,110)
    draw((-133 + x_apple),(-79 + y_apple),"black",0.15,111)
    draw((-130 + x_apple),(-79 + y_apple),"black",0.15,112)
    draw((-127 + x_apple),(-79 + y_apple),color_apple,0.15,113)
    draw((-124 + x_apple),(-79 + y_apple),color_apple,0.15,114)
    draw((-121 + x_apple),(-79 + y_apple),color_apple,0.15,115)


apple("white")

def gamepad (color):
    draw((-148 + x_gamepad),(-63 + y_gamepad),color,0.15,116)
    draw((-145 + x_gamepad),(-63 + y_gamepad),color,0.15,117)
    draw((-142 + x_gamepad),(-63 + y_gamepad),color,0.15,118)
    draw((-139 + x_gamepad),(-63 + y_gamepad),color,0.15,119)
    draw((-136 + x_gamepad),(-63 + y_gamepad),color,0.15,120)
    draw((-133 + x_gamepad),(-63 + y_gamepad),color,0.15,121)
    draw((-130 + x_gamepad),(-63 + y_gamepad),color,0.15,122)
    draw((-127 + x_gamepad),(-63 + y_gamepad),color,0.15,123)
    draw((-124 + x_gamepad),(-63 + y_gamepad),color,0.15,124)
    draw((-121 + x_gamepad),(-63 + y_gamepad),color,0.15,125)

    draw((-151 + x_gamepad),(-67 + y_gamepad),color,0.15,126)
    draw((-148 + x_gamepad),(-67 + y_gamepad),color,0.15,127)
    draw((-145 + x_gamepad),(-67 + y_gamepad),"black",0.15,128)
    draw((-142 + x_gamepad),(-67 + y_gamepad),color,0.15,129)
    draw((-139 + x_gamepad),(-67 + y_gamepad),color,0.15,130)
    draw((-136 + x_gamepad),(-67 + y_gamepad),color,0.15,131)
    draw((-133 + x_gamepad),(-67 + y_gamepad),color,0.15,132)
    draw((-130 + x_gamepad),(-67 + y_gamepad),color,0.15,133)
    draw((-127 + x_gamepad),(-67 + y_gamepad),"black",0.15,134)
    draw((-124 + x_gamepad),(-67 + y_gamepad),color,0.15,135)
    draw((-121 + x_gamepad),(-67 + y_gamepad),color,0.15,136)
    draw((-118 + x_gamepad),(-67 + y_gamepad),color,0.15,137)

    draw((-151 + x_gamepad),(-71 + y_gamepad),color,0.15,138)
    draw((-148 + x_gamepad),(-71 + y_gamepad),"black",0.15,139)
    draw((-145 + x_gamepad),(-71 + y_gamepad),color,0.15,140)
    draw((-142 + x_gamepad),(-71 + y_gamepad),"black",0.15,141)
    draw((-139 + x_gamepad),(-71 + y_gamepad),color,0.15,142)
    draw((-136 + x_gamepad),(-71 + y_gamepad),color,0.15,143)
    draw((-133 + x_gamepad),(-71 + y_gamepad),color,0.15,144)
    draw((-130 + x_gamepad),(-71 + y_gamepad),color,0.15,145)
    draw((-127 + x_gamepad),(-71 + y_gamepad),color,0.15,146)
    draw((-124 + x_gamepad),(-71 + y_gamepad),color,0.15,147)
    draw((-121 + x_gamepad),(-71 + y_gamepad),color,0.15,148)
    draw((-118 + x_gamepad),(-71 + y_gamepad),color,0.15,149)

    draw((-151 + x_gamepad),(-74 + y_gamepad),color,0.15,150)
    draw((-148 + x_gamepad),(-74 + y_gamepad),color,0.15,151)
    draw((-145 + x_gamepad),(-74 + y_gamepad),"black",0.15,152)
    draw((-142 + x_gamepad),(-74 + y_gamepad),color,0.15,153)
    draw((-139 + x_gamepad),(-74 + y_gamepad),color,0.15,154)
    draw((-136 + x_gamepad),(-74 + y_gamepad),color,0.15,155)
    draw((-133 + x_gamepad),(-74 + y_gamepad),color,0.15,156)
    draw((-130 + x_gamepad),(-74 + y_gamepad),color,0.15,157)
    draw((-127 + x_gamepad),(-74 + y_gamepad),color,0.15,158)
    draw((-124 + x_gamepad),(-74 + y_gamepad),color,0.15,159)
    draw((-121 + x_gamepad),(-74 + y_gamepad),"black",0.15,160)
    draw((-118 + x_gamepad),(-74 + y_gamepad),color,0.15,161)

    draw((-151 + x_gamepad),(-78 + y_gamepad),color,0.15,162)
    draw((-148 + x_gamepad),(-78 + y_gamepad),color,0.15,163)
    draw((-145 + x_gamepad),(-78 + y_gamepad),color,0.15,164)
    draw((-142 + x_gamepad),(-78 + y_gamepad),color,0.15,165)
    draw((-139 + x_gamepad),(-78 + y_gamepad),color,0.15,166)
    draw((-136 + x_gamepad),(-78 + y_gamepad),color,0.15,167)
    draw((-133 + x_gamepad),(-78 + y_gamepad),color,0.15,168)
    draw((-130 + x_gamepad),(-78 + y_gamepad),color,0.15,169)
    draw((-127 + x_gamepad),(-78 + y_gamepad),color,0.15,170)
    draw((-124 + x_gamepad),(-78 + y_gamepad),color,0.15,171)
    draw((-121 + x_gamepad),(-78 + y_gamepad),color,0.15,172)
    draw((-118 + x_gamepad),(-78 + y_gamepad),color,0.15,173)

    draw((-148 + x_gamepad),(-82 + y_gamepad),color,0.15,174)
    draw((-145 + x_gamepad),(-82 + y_gamepad),color,0.15,175)
    draw((-142 + x_gamepad),(-82 + y_gamepad),color,0.15,176)
    draw((-127 + x_gamepad),(-82 + y_gamepad),color,0.15,177)
    draw((-124 + x_gamepad),(-82 + y_gamepad),color,0.15,178)
    draw((-121 + x_gamepad),(-82 + y_gamepad),color,0.15,179)

gamepad("white")

#def bath():



def option_change(option_state):
    if option_state == 0:
        x_option = -120
        apple("#D8D8D8")
        gamepad("white")
    elif option_state == 1:
        x_option = 0
        apple("white")
        gamepad("#D8D8D8")
    elif option_state == 2:
        x_option = 120
        apple("white")
        gamepad("white")

    draw_option(x_option, -95, "white", 0.5, 27)

pixel[27].left(90)

def draw_option(x,y,color,size,i):
    global pixel
    pixel[i].speed(0)
    pixel[i].shape("triangle")
    pixel[i].shapesize(size,size)
    pixel[i].color(color)
    pixel[i].showturtle()
    pixel[i].penup()
    pixel[i].goto(x,y)
    pixel[i].direction = "stop"

def left_press():
    global option
    global izq_apretado
    left_button_obj.color("grey")
    if(playing == False):
        option -= 1
    else:
        izq_apretado = True

    if option > 2:
        option = 0
    elif option < 0:
        option = 2

    option_change(option)


def right_press():
    global option
    global der_apretado

    right_button_obj.color("grey")
    if(playing == False):
        option += 1
    else:
        der_apretado = True

    if option > 2:
        option = 0
    elif option < 0:
        option = 2
    
    option_change(option)

def middle_press():
    middle_button_obj.color("grey")
    global option
    global eating
    global hungry
    global playing

    if(playing == False):
        if option == 0:
            eating = 1
        elif option == 1:
            playing = True


def left_rel():
    global izq_apretado
    left_button_obj.color("white")
    izq_apretado = False

def right_rel():
    global der_apretado
    right_button_obj.color("white")
    der_apretado = False

def middle_rel():
    middle_button_obj.color("white")

window.listen()
window.onkeypress(middle_press, "Up")
window.onkeypress(left_press, "Left") 
window.onkeypress(right_press, "Right")
window.onkeypress(reproducir, "m")

window.onkeyrelease(middle_rel, "Up")
window.onkeyrelease(left_rel, "Left") 
window.onkeyrelease(right_rel, "Right")

option_change(option)

#   MAIN LOOP
while(True):
    window.update()
    if(eating > 0):
        eat_anim()
    elif(playing == True):
        apple("black")
        gamepad("black")
        play()
    else:
        iddle()
        if(destruidos >= 4):
            happiness += 4
            if(happiness > 10):
                happiness = 10
            write_data()
            barraLifePrint()
            if(happiness <= 0 and happiness < 4 ):
                happy = ":("
            elif(happiness >= 4 and happiness < 7):
                happy = ":|"
            elif(happiness >= 7 and happiness <= 10):
                happy = ":)"

            if (happy == ":)"):
                text[4].clear()
                textos(":)", (x_text_happy - 60), (y_text_happy + 2), "green", 4)
            elif (happy == ":|"):
                text[4].clear()
                textos(":|", (x_text_happy - 60), (y_text_happy + 2), "yellow", 4)
            elif (happy == ":("):
                text[4].clear()
                textos(":(", (x_text_happy - 60), (y_text_happy + 2), "red", 4)
            destruidos = 0
        fps = 0.1


    time.sleep(fps)





    
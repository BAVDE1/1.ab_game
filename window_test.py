import turtle
import random
import time

# Window screen
window = turtle.Screen()
window.title("help")
window.bgcolor("grey")
window.setup(width=500, height=500)

# Object
obj = turtle.Turtle()
obj.penup()
obj.shape("square")
obj.color("black")
obj.speed(1)
obj.direction = "Stop"

# Ground
ground = turtle.Turtle()
ground.penup()
ground.shape("square")
ground.color("black")
ground.setposition(0, -40)
ground.tilt(45)


# Controls
jump = False
key_binds = ["left", "right", "up", "down"]


def left():
    global jump
    coord_x = obj.xcor()
    i = 20
    if jump:
        i = 60
        obj.color("black")
    obj.setx(coord_x - i)
    jump = False
    print(obj.pos())


def right():
    global jump
    coord_x = obj.xcor()
    i = 20
    if jump:
        i = 60
        obj.color("black")
    obj.setx(coord_x + i)
    jump = False
    print(obj.pos())


def up():
    global jump
    coord_y = obj.ycor()
    i = 20
    if jump:
        i = 60
        obj.color("black")
    obj.sety(coord_y + i)
    jump = False
    print(obj.pos())


def down():
    global jump
    coord_y = obj.ycor()
    i = 20
    if jump:
        i = 60
        obj.color("black")
    obj.sety(coord_y - i)
    jump = False
    print(obj.pos())


def e():
    obj.tilt(45)


def q():
    obj.tilt(-45)


def space():
    global jump
    jump = True
    obj.color("red")


window.listen()
window.onkeypress(left, 'Left')
window.onkeypress(right, 'Right')
window.onkeypress(up, 'Up')
window.onkeypress(down, 'Down')
window.onkeypress(e, "e")
window.onkeypress(q, "q")
window.onkeypress(space, "space")

# Keeps window open
turtle.mainloop()

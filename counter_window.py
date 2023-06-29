import turtle

num = 0

# Window screen
window = turtle.Screen()
window.title("help")
window.bgcolor("grey")
window.setup(width=500, height=500)


def cover():
    cover_block = turtle.Turtle()
    cover_block.color("grey")
    cover_block.shape("square")
    cover_block.shapesize(40)


def write_num(increase):
    cover()
    
    global num
    if increase:
        num += 1
    else:
        num -= 1
    turtle.write(num, align="center", font=("Lora", 25, "bold"))


# Controls
def up():
    write_num(True)


def down():
    write_num(False)


window.listen()
window.onkeypress(up, 'Up')
window.onkeypress(down, 'Down')

cover()
turtle.write("Press arrow up or down", align="center", font=("Lora", 15, "bold"))

# Keeps window open
turtle.mainloop()


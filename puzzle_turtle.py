import turtle

###################
# ----Defaults----#
###################
width = 30
height = 40

ground_char = "#"
ground_block = turtle.Turtle()
ground_block.shape("square")
ground_block.penup()
ground_block.speed(0)
ground_block.color("white")
ground_block.setposition(500, 500)

player_char = "@"
player = turtle.Turtle()
player.shape("circle")
player.penup()
player.speed(1)
player.color("yellow")

lines = []
all_block_pos = []  # [0]=xcor, [1]=ycor
"""[0]=xcor, [1]=ycor"""
drawing = False

wind = turtle.Screen()
wind.bgcolor("black")
wind.setup(width=(width + 2) * 20, height=(height + 2) * 20)
wind.title("idk")
wind.delay(0)


####################
# ----Rendering----#
####################
def read_level():
    with open("levels/level_1.txt") as file:
        global lines
        global drawing
        lines = [line.rstrip() for line in file]

        # draw level
        drawing = True
        wind.delay(0)
        draw_level()
        wind.delay(1)
        drawing = False

        # init check for ground
        check_for_ground()


def draw_ground_cube(pos_x, pos_y):
    ground_block.clone().setposition(pos_x, pos_y)
    all_block_pos.append([pos_x, pos_y])


def draw_player(pos_w, pos_h):
    player.setposition(pos_w, pos_h)


def draw_level():
    if lines:
        line_num = 0
        for line in lines:
            line_num += 1
            chars = list(line)
            char_num = 0
            for char in chars:
                char_num += 1
                if char == ground_char:
                    draw_ground_cube((width / 2 * -20) + (20 * char_num), (height / 2 * 20) - (20 * line_num))
                elif char == player_char:
                    draw_player((width / 2 * -20) + (20 * char_num), (height / 2 * 20) - (20 * line_num))


##############################
# ----Collision & Gravity----#
##############################
# https://python-forum.io/thread-30979.html
# Collision
def check_for_ground():
    needs_to_fall = True
    for block_pos in all_block_pos:
        if block_pos[0] == player.xcor():
            if block_pos[1] + 20 == player.ycor():
                needs_to_fall = False
    if needs_to_fall:
        fall()


def fall():
    player.sety(player.ycor() - 20)
    check_for_ground()


###################
# ----Controls----#
###################
def left():
    print("left")


def right():
    print("right")


def space():
    print("space")


wind.listen()
wind.onkeypress(left, 'Left')
wind.onkeypress(right, 'Right')
wind.onkeypress(space, "space")

###############
# ----Init----#
###############
if __name__ == '__main__':
    print("Initialising")
    read_level()

wind.mainloop()

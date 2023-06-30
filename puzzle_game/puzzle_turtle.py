import sys
import turtle
import os

###################
# ----Defaults----#
###################
width = 30
height = 40

load_wind_delay = 0
run_wind_delay = 4

# Screen setup
wind = turtle.Screen()
wind.bgcolor("black")
margin = 2
wind.setup(width=(width + margin) * 20, height=(height + margin) * 20)
wind.title("idk")
wind.delay(load_wind_delay)

# Base blocks
base_block = turtle.Turtle()
base_block.shape("square")
base_block.penup()
base_block.speed(0)

base_triangle = base_block.clone()
base_triangle.shape("triangle")

base_circle = base_block.clone()
base_circle.shape("circle")

# Fancy blocks
dark_grey_char = "."
dark_grey_block = base_block.clone()
dark_grey_block.color("grey10")
dark_grey_block.setposition(540, 500)

grey_char = ":"
grey_block = base_block.clone()
grey_block.color("grey20")
grey_block.setposition(520, 500)

fancy_ground_char = "*"
fancy_block = base_block.clone()
fancy_block.shapesize(.5)
fancy_block.color("black")
fancy_block.setposition(500, 500)

# Ground
ground_char = "#"
ground_block = base_block.clone()
ground_block.color("white")
ground_block.setposition(500, 500)

# Intractable
switch_char = "^"
switch_block = base_triangle.clone()
switch_block.color("cyan")
switch_block.tilt(90)
switch_block.setposition(500, 470)

tp_block_blue = base_circle.clone()
tp_block_blue.color("cyan")
tp_block_blue.setposition(500, 450)

tp_block_dull_blue = base_circle.clone()
tp_block_dull_blue.color("cyan4")
tp_block_dull_blue.setposition(520, 450)

tp_base_char = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]

tp_first_char = ["a", "c", "e", "g", "i", "k", "m", "o", "q"]

tp_second_char = ["b", "d", "f", "h", "j", "l", "n", "p", "r"]

hover_interact = switch_block.clone()
hover_interact.shapesize(0.5)
hover_interact.tilt(180)

# Player
player_char = "@"
player = turtle.Turtle()
player.shape("circle")
player.penup()
player.speed(1)
player.color("yellow")
player_falling = False
player_moving = False

# Other
lines = []
all_block_pos = []  # [0]=xcor, [1]=ycor
all_switch_pos = []
tp_1 = []
tp_2 = []
tp_3 = []
tp_4 = []
tp_5 = []
tp_6 = []
tp_7 = []
tp_8 = []
tp_9 = []
all_tp = [tp_1, tp_2, tp_3, tp_4, tp_5, tp_6, tp_7, tp_8, tp_9]
drawing = False


####################
# ----Rendering----#
####################
def read_level():
    level_file = "puzzle_game/levels/level_1.txt"
    if str(sys.platform) == "linux":
        level_file = "levels/level_1.txt"

    with open(level_file) as file:
        global lines
        global drawing
        lines = [line.rstrip() for line in file]

        # draw level
        drawing = True
        wind.delay(load_wind_delay)
        draw_level()
        draw_teleporters()
        wind.delay(run_wind_delay)
        drawing = False


def draw_ground_cube(pos_x, pos_y, fancy):
    ground_block.clone().setposition(pos_x, pos_y)
    if fancy:
        fancy_block.clone().setposition(pos_x, pos_y)
    all_block_pos.append([pos_x, pos_y])


def draw_grey_cube(pos_x, pos_y, dark):
    if dark:
        dark_grey_block.clone().setposition(pos_x, pos_y - 1)
    else:
        grey_block.clone().setposition(pos_x, pos_y - 1)


def draw_switch_cube(pos_x, pos_y):
    switch_block.clone().setposition(pos_x, pos_y - 5)
    s_fancy = switch_block.clone()
    s_fancy.setposition(pos_x, pos_y - 5)
    s_fancy.shapesize(.5)
    s_fancy.color("cyan4")
    all_switch_pos.append([pos_x, pos_y])


def draw_tp_base(pos_x, pos_y, index):
    tp_block_blue.clone().setposition(pos_x, pos_y)
    f = tp_block_dull_blue.clone()
    f.shapesize(.5)
    f.setposition(pos_x, pos_y)
    all_tp[index].insert(0, [pos_x, pos_y])


def draw_tp_first(pos_x, pos_y, index):
    b = tp_block_blue.clone()
    all_tp[index].insert(1, [pos_x, pos_y])


def draw_tp_second(pos_x, pos_y, index):
    b = tp_block_dull_blue.clone()
    all_tp[index].insert(2, [pos_x, pos_y])


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
                pos_x = (width / 2 * -20) + (20 * char_num)
                pos_y = (height / 2 * 20) - (20 * line_num)
                if char == dark_grey_char:
                    draw_grey_cube(pos_x, pos_y, True)
                elif char == grey_char:
                    draw_grey_cube(pos_x, pos_y, False)
                elif char == ground_char:
                    draw_ground_cube(pos_x, pos_y, False)
                elif char == fancy_ground_char:
                    draw_ground_cube(pos_x, pos_y, True)
                elif char == switch_char:
                    draw_switch_cube(pos_x, pos_y)
                elif char == player_char:
                    draw_player(pos_x, pos_y)

                # Teleporters
                for base_tp_char in tp_base_char:
                    if char == base_tp_char:
                        draw_tp_base(pos_x, pos_y, int(char) - 1)

                for first_tp_char in tp_first_char:
                    if char == first_tp_char:
                        # add to list, render after level has been drawn
                        all_tp[tp_first_char.index(char)].insert(1, [pos_x, pos_y])

                for second_tp_char in tp_second_char:
                    if char == second_tp_char:
                        # add to list, render after level has been drawn
                        all_tp[tp_second_char.index(char)].insert(2, [pos_x, pos_y])


def draw_teleporters():
    for tp_list in all_tp:
        if tp_list:
            if len(tp_list) == 3:
                return None
            else:
                raise ValueError("Incorrect amount of values in list: ", tp_list, " (Must be exactly 3 entries)")


##############################
# ----Collision & Gravity----#
##############################
def check_for_ground():
    needs_to_fall = True
    for block_pos in all_block_pos:
        if block_pos[0] - 19 < player.xcor() < block_pos[0] + 19:
            if block_pos[1] + 20 == player.ycor():
                needs_to_fall = False
    if needs_to_fall:
        fall()


def fall():
    global player_falling
    player_falling = True
    player.sety(player.ycor() - 20)
    check_for_ground()
    player_falling = False


def check_for_wall(is_going_right):
    can_move = True
    for block_pos in all_block_pos:
        if block_pos[1] == player.ycor():
            if is_going_right and block_pos[0] - 20 == player.xcor():
                can_move = False
            elif not is_going_right and block_pos[0] + 20 == player.xcor():
                can_move = False
    return can_move


######################
# ----Interaction----#
######################
def interact():
    for switch_pos in all_switch_pos:
        if player.xcor() == switch_pos[0] and player.ycor() == switch_pos[1]:
            print("switch")


def check_for_switch():
    for switch_pos in all_switch_pos:
        if player.xcor() == switch_pos[0] and player.ycor() == switch_pos[1]:
            hover_interact.setposition(switch_pos[0], switch_pos[1] + 30)
            return None
        hover_interact.setposition(switch_block.xcor(), switch_block.ycor())


###################
# ----Controls----#
###################
left_keys = ["Left", "a"]
right_keys = ["Right", "d"]
interact_key = ["space"]


def left():
    global player_moving
    if not player_falling and not player_moving and check_for_wall(False):
        player_moving = True
        player.setx(player.xcor() - 20)
        player_moving = False
        check_for_ground()
        check_for_switch()


def right():
    global player_moving
    if not player_falling and not player_moving and check_for_wall(True):
        player_moving = True
        player.setx(player.xcor() + 20)
        player_moving = False
        check_for_ground()
        check_for_switch()


def space():
    interact()


wind.listen()
wind.onkeypress(left, left_keys[0])
wind.onkeypress(left, left_keys[1])
wind.onkeypress(right, right_keys[0])
wind.onkeypress(right, right_keys[1])
wind.onkeypress(space, interact_key[0])

###############
# ----Init----#
###############
if __name__ == '__main__':
    print("Initialising")

    # draw level
    print("Drawing level")
    read_level()

    # init check for ground
    print("Checking for ground")
    check_for_ground()

    print("Initialisation complete")

wind.mainloop()

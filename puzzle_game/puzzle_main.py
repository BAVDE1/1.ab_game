import sys
import turtle
import time
import threading

###################
# ----Defaults----#
###################
turtle.ht()

width = 30
height = 40

load_wind_delay = 0
run_wind_delay = 1

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
if str(sys.platform) == "win32":
    dark_grey_block.color("grey2")
dark_grey_block.setposition(540, 500)

grey_char = ":"
grey_block = base_block.clone()
grey_block.color("grey20")
if str(sys.platform) == "win32":
    grey_block.color("grey5")
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

timer_switch_char = '"'
timer_switch_block = switch_block.clone()
timer_progress_block = base_block.clone()
timer_progress_block.color("cyan")
timer_progress_block.setposition(600, 600)

tp_block_blue = base_circle.clone()
tp_block_blue.color("cyan")
tp_block_blue.setposition(500, 450)

tp_block_dull_blue = base_circle.clone()
tp_block_dull_blue.color("cyan4")
tp_block_dull_blue.setposition(520, 450)

tp_base_char = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]

tp_first_char = ["a", "c", "e", "g", "i", "k", "m", "o", "q"]

tp_second_char = ["b", "d", "f", "h", "j", "l", "n", "p", "r"]

interact_indicator = switch_block.clone()
interact_indicator.shapesize(0.5)
interact_indicator.tilt(180)

winpad_char = "!"
winpad_block = base_block.clone()
winpad_block.color("lime")

# Player
player_char = "@"
player = turtle.Turtle()
player.shape("circle")
player.penup()
player.speed(1)
player.color("yellow")
player_falling = False
player_moving = False
player_teleporting = False
switching_teleporters = False
timer_enabled = False

# Other
lines = []
all_block_pos = []  # [0]=xcor, [1]=ycor
all_switch_pos = []
all_timer_switch_pos = []
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
timer_switch = []  # Only one entry allowed
drawing = False


####################
# ----Rendering----#
####################
def read_level():
    level_file = "levels/level_1.txt"

    with open(level_file) as file:
        global lines
        global drawing
        lines = [line.rstrip() for line in file]

        # draw level
        drawing = True
        wind.delay(load_wind_delay)
        draw_level()
        wind.delay(run_wind_delay)
        drawing = False


def draw_ground_cube(pos_x, pos_y, fancy):
    ground_block.clone().setposition(pos_x, pos_y)
    if fancy:
        fancy_block.clone().setposition(pos_x, pos_y)
    all_block_pos.append([pos_x, pos_y])


def draw_winpad(pos_x, pos_y):
    winpad_block.clone().setposition(pos_x, pos_y)


def draw_grey_cube(pos_x, pos_y, dark):
    if dark:
        dark_grey_block.clone().setposition(pos_x + 1, pos_y - 1)
    else:
        grey_block.clone().setposition(pos_x + 1, pos_y - 1)


def draw_switch(pos_x, pos_y):
    switch_block.clone().setposition(pos_x, pos_y - 5)
    s_fancy = switch_block.clone()
    s_fancy.setposition(pos_x, pos_y - 5)
    s_fancy.shapesize(.5)
    s_fancy.color("cyan4")
    all_switch_pos.append([pos_x, pos_y])


def draw_timer_switch():
    pos_x = timer_switch[0]
    pos_y = timer_switch[1]
    timer_switch_block.clone().setposition(pos_x, pos_y - 5)

    ts_b = timer_switch_block.clone()
    ts_b.setposition(pos_x, pos_y - 5)
    ts_b.shapesize(.5)
    ts_b.color("cyan4")

    draw_timer_switch_deco_1()
    draw_timer_switch_deco_2()


def draw_timer_switch_deco_1():
    pos_x = timer_switch[0]
    pos_y = timer_switch[1]

    ts_a = timer_switch_block.clone()
    ts_a.setposition(pos_x, pos_y - 20)
    ts_a.color("cyan", "white")
    ts_a.shape("square")


def draw_timer_switch_deco_2():
    pos_x = timer_switch[0]
    pos_y = timer_switch[1]

    ts_b = timer_switch_block.clone()
    ts_b.shapesize(.5)
    ts_b.color("cyan4")
    ts_b.tilt(180)
    ts_b.setposition(pos_x, pos_y - 12)


def draw_timer_switch_progress(percent):
    c = timer_progress_block.clone()
    c.shapesize(percent / 100)
    c.setposition(timer_switch[0], timer_switch[1] - 20)


def draw_tp_base(pos_x, pos_y):
    tp_block_blue.clone().setposition(pos_x, pos_y)
    f = tp_block_dull_blue.clone()
    f.shapesize(.5)
    f.setposition(pos_x, pos_y)


def draw_tp_first(base_x, base_y, pos_x, pos_y, active):
    b = tp_block_dull_blue.clone()
    if active:
        b = tp_block_blue.clone()
    b.setposition(base_x, base_y)
    b.pendown()
    b.pensize(2)
    b.shapesize(0.8)
    b.setposition(pos_x, pos_y)
    b.penup()


def draw_tp_second(base_x, base_y, pos_x, pos_y, active):
    b = tp_block_dull_blue.clone()
    if active:
        b = tp_block_blue.clone()
    b.setposition(base_x, base_y)
    b.pendown()
    b.pensize(2)
    b.shapesize(0.8)
    b.setposition(pos_x, pos_y)
    b.penup()


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
                    draw_switch(pos_x, pos_y)
                elif char == timer_switch_char:
                    all_timer_switch_pos.append([pos_x, pos_y])
                elif char == winpad_char:
                    draw_winpad(pos_x, pos_y)
                elif char == player_char:
                    draw_player(pos_x, pos_y)

                # Teleporters
                for base_tp_char in tp_base_char:
                    if char == base_tp_char:
                        # add to list, render after level has been drawn
                        all_tp[int(char) - 1].insert(0, [pos_x, pos_y])

                for first_tp_char in tp_first_char:
                    if char == first_tp_char:
                        # add to list, render after level has been drawn
                        all_tp[tp_first_char.index(char)].insert(1, [pos_x, pos_y])

                for second_tp_char in tp_second_char:
                    if char == second_tp_char:
                        # add to list, render after level has been drawn
                        all_tp[tp_second_char.index(char)].insert(2, [pos_x, pos_y])

        # To be done after base level is drawn
        draw_timer_switches()
        draw_teleporters()


def draw_timer_switches():
    for ts in all_timer_switch_pos:
        if len(timer_switch) == 0:
            timer_switch.append(ts[0])
            timer_switch.append(ts[1])
            draw_timer_switch()
        else:
            raise ValueError("Only one timer switch is allowed!")


def draw_teleporters():
    for tp_list in all_tp:
        if tp_list:
            all_tp[all_tp.index(tp_list)].append(False)  # adds 'switched' value to end

            if len(tp_list) == 4:
                base_pos = tp_list[0]
                first_pos = tp_list[1]
                second_pos = tp_list[2]

                draw_tp_first(base_pos[0], base_pos[1], first_pos[0], first_pos[1], True)
                draw_tp_second(base_pos[0], base_pos[1], second_pos[0], second_pos[1], False)
                draw_tp_base(base_pos[0], base_pos[1])
            else:
                raise ValueError("Incorrect amount of values in list: ", tp_list,
                                 " (Must be exactly 3 entries - base, tp point 1, tp point 2, False)")


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
            switch_interact()

    for timer_switch_pos in all_timer_switch_pos:
        if player.xcor() == timer_switch_pos[0] and player.ycor() == timer_switch_pos[1] and not timer_enabled:
            threading.Thread(target=timer_switch_interact).start()

    for tp_list in all_tp:
        if tp_list:
            teleporter_interact(tp_list)


def switch_interact():
    global switching_teleporters
    switching_teleporters = True
    for tp_list in all_tp:
        wind.delay(load_wind_delay)
        if tp_list:
            base_pos = tp_list[0]
            first_pos = tp_list[1]
            second_pos = tp_list[2]
            current_switch = tp_list[3]

            draw_tp_first(base_pos[0], base_pos[1], first_pos[0], first_pos[1], current_switch)
            draw_tp_second(base_pos[0], base_pos[1], second_pos[0], second_pos[1], not current_switch)
            draw_tp_base(base_pos[0], base_pos[1])

            tp_list[3] = not current_switch
        wind.delay(run_wind_delay)
    switching_teleporters = False


def timer_switch_interact():
    global timer_enabled
    timer_enabled = True
    time_pressed = time.time()
    timer_sec = 8
    while time.time() - time_pressed < timer_sec:
        time.sleep(0.2)
        timer_percent = ((time.time() - time_pressed) / timer_sec) * 100
        draw_timer_switch_progress(timer_percent)
    switch_interact()
    timer_enabled = False
    draw_timer_switch_deco_1()
    draw_timer_switch_deco_2()
    check_for_interact_able()


def teleporter_interact(tp_list):
    base_pos = tp_list[0]
    first_pos = tp_list[1]
    second_pos = tp_list[2]
    switched = tp_list[3]

    if player.xcor() == base_pos[0] and player.ycor() == base_pos[1]:
        # Base > pos
        if not switched:
            tp_player_to(first_pos[0], first_pos[1])
        else:
            tp_player_to(second_pos[0], second_pos[1])
    elif (player.xcor() == first_pos[0] and player.ycor() == first_pos[1] and not switched) or \
            (player.xcor() == second_pos[0] and player.ycor() == second_pos[1] and switched):
        # Pos > base
        tp_player_to(base_pos[0], base_pos[1])

    check_for_ground()
    check_for_interact_able()


def tp_player_to(tp_to_x, tp_to_y):
    global player_teleporting
    if str(sys.platform) == "win32":
        player.speed(2)
    player_teleporting = True
    player.setposition(tp_to_x, tp_to_y)
    player_teleporting = False
    if str(sys.platform) == "win32":
        player.speed(1)


def check_for_interact_able():
    # Switch
    for switch_pos in all_switch_pos:
        if player.xcor() == switch_pos[0] and player.ycor() == switch_pos[1]:
            interact_indicator.setposition(switch_pos[0], switch_pos[1] + 30)
            return None

    # Timer switch
    for timer_switch_pos in all_timer_switch_pos:
        if player.xcor() == timer_switch_pos[0] and player.ycor() == timer_switch_pos[1] and not timer_enabled:
            interact_indicator.setposition(timer_switch_pos[0], timer_switch_pos[1] + 30)
            return None

    # Teleporter
    for tp_list in all_tp:
        if tp_list:
            base_pos = tp_list[0]
            first_pos = tp_list[1]
            second_pos = tp_list[2]
            switched = tp_list[3]

            if player.xcor() == base_pos[0] and player.ycor() == base_pos[1]:
                interact_indicator.setposition(base_pos[0], base_pos[1] + 30)
                return None
            elif player.xcor() == first_pos[0] and player.ycor() == first_pos[1] and not switched:
                interact_indicator.setposition(first_pos[0], first_pos[1] + 30)
                return None
            elif player.xcor() == second_pos[0] and player.ycor() == second_pos[1] and switched:
                interact_indicator.setposition(second_pos[0], second_pos[1] + 30)
                return None

    # Removes indicator
    interact_indicator.setposition(switch_block.xcor(), switch_block.ycor())


###################
# ----Controls----#
###################
left_keys = ["Left", "a"]
right_keys = ["Right", "d"]
interact_key = ["space", "z", "m"]


def left():
    global player_moving
    if not player_falling and not player_moving and not player_teleporting and not switching_teleporters and check_for_wall(False):
        player_moving = True
        player.setx(player.xcor() - 20)
        player_moving = False
        check_for_ground()
        check_for_interact_able()


def right():
    global player_moving
    if not player_falling and not player_moving and not player_teleporting and not switching_teleporters and check_for_wall(True):
        player_moving = True
        player.setx(player.xcor() + 20)
        player_moving = False
        check_for_ground()
        check_for_interact_able()


wind.listen()
wind.onkeypress(left, left_keys[0])
wind.onkeypress(left, left_keys[1])
wind.onkeypress(right, right_keys[0])
wind.onkeypress(right, right_keys[1])
wind.onkeypress(interact, interact_key[0])
wind.onkeypress(interact, interact_key[1])
wind.onkeypress(interact, interact_key[2])

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

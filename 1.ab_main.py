from textures import *
import turtle
import time
import threading

###################
# ----Defaults----#
###################
width = 30
height = 40

load_wind_delay = 0
run_wind_delay = 1

wind = turtle.Screen()

# One time textures
player = turtle.Turtle()
active_lift = platform_block.clone()
interact_indicator = interact_indicator_base.clone()


def reset_textures():
    global player
    global active_lift
    global interact_indicator

    player = player_base.clone()
    active_lift = platform_block.clone()
    interact_indicator = interact_indicator_base.clone()


# Screen setup
def screen_setup():
    global wind
    wind.bgcolor("black")
    margin = 2
    wind.setup(width=(width + margin) * 20, height=(height + margin) * 20)
    wind.title("1.ab")
    wind.delay(load_wind_delay)
    wind.register_shape("rectangle", rectangle_cors)


screen_setup()
current_file = ""
drawing = False

# Player values
player_falling = False
player_moving = False
player_teleporting = False
switching_teleporters = False
timer_enabled = False

# Lists
lines = []
all_block_pos = []  # [0]=xcor, [1]=ycor
all_platform_pos = []
all_lift_pos = []
all_switch_pos = []
all_timer_switch_pos = []

# Tp lists
tp_base_char = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
tp_first_char = ["a", "c", "e", "g", "i", "k", "m", "o", "q"]
tp_second_char = ["b", "d", "f", "h", "j", "l", "n", "p", "r"]
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


####################
# ----Rendering----#
####################
def read_level(level_to_load):
    print("Drawing Level")
    level_file = "levels/" + level_to_load + ".txt"

    with open(level_file) as file:
        global lines
        global drawing
        lines = [line.rstrip() for line in file]

        # draw level
        drawing = True
        wind.delay(load_wind_delay)
        for i in range(3):
            draw_level(i)
        wind.delay(run_wind_delay)
        drawing = False

        print("Read level complete")


# Times=0: base level drawn, times=1: first tp points drawn, times=2: second tp points drawn and timers and switches drawn
def draw_level(times):
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
                if times == 0:
                    if char == dark_grey_char:
                        draw_grey_cube(pos_x, pos_y, True)
                    elif char == grey_char:
                        draw_grey_cube(pos_x, pos_y, False)
                    elif char == ground_char:
                        draw_ground_cube(pos_x, pos_y, False)
                    elif char == fancy_ground_char:
                        draw_ground_cube(pos_x, pos_y, True)
                    elif char == level_sel_char:
                        draw_green_door(pos_x, pos_y)
                    elif char == platform_char:
                        draw_platform(pos_x, pos_y)
                    elif char == lift_char:
                        draw_lift(pos_x, pos_y)
                    elif char == switch_char:
                        draw_switch(pos_x, pos_y)
                    elif char == timer_switch_char:
                        all_timer_switch_pos.append([pos_x, pos_y])
                    elif char == winpad_char:
                        draw_green_door(pos_x, pos_y)
                    elif char == player_char:
                        draw_player(pos_x, pos_y)

                # Teleporters
                for base_tp_char in tp_base_char:
                    if char == base_tp_char and times == 0:
                        # add to list, render after level has been drawn
                        all_tp[int(char) - 1].insert(0, [pos_x, pos_y])

                for first_tp_char in tp_first_char:
                    if char == first_tp_char and times == 1:
                        # add to list, render after level has been drawn
                        all_tp[tp_first_char.index(char)].insert(1, [pos_x, pos_y])

                for second_tp_char in tp_second_char:
                    if char == second_tp_char and times == 2:
                        # add to list, render after level has been drawn
                        all_tp[tp_second_char.index(char)].insert(2, [pos_x, pos_y])

        # To be done after base level is drawn
        if times == 2:
            draw_timer_switches()
            draw_teleporters()

            print("Draw level complete")


def draw_ground_cube(pos_x, pos_y, fancy):
    ground_block.clone().setposition(pos_x, pos_y)
    if fancy:
        fancy_block.clone().setposition(pos_x, pos_y)
    all_block_pos.append([pos_x, pos_y])


def draw_grey_cube(pos_x, pos_y, dark):
    if dark:
        dark_grey_block.clone().setposition(pos_x + 1, pos_y - 1)
    else:
        grey_block.clone().setposition(pos_x + 1, pos_y - 1)


def draw_green_door(pos_x, pos_y):
    green_door_block.clone().setposition(pos_x, pos_y - 5)
    green_door_block_a.clone().setposition(pos_x, pos_y - 7)
    green_door_block_b.clone().setposition(pos_x, pos_y + 20)
    green_door_block_c.clone().setposition(pos_x, pos_y + 20)


def draw_grey_door(pos_x, pos_y):
    grey_door_block.clone().setposition(pos_x, pos_y - 5)
    grey_door_block_a.clone().setposition(pos_x, pos_y - 7)
    grey_door_block_b.clone().setposition(pos_x, pos_y + 20)
    grey_door_block_c.clone().setposition(pos_x, pos_y + 20)


def draw_platform(pos_x, pos_y):
    r = platform_block.clone()
    r.setposition(pos_x, pos_y + 5)
    r.shape("rectangle")
    all_block_pos.append([pos_x, pos_y])
    all_platform_pos.append([pos_x, pos_y])


def draw_lift(pos_x, pos_y):
    r = platform_block.clone()
    r.setposition(pos_x, pos_y + 5)
    r.shape("rectangle")
    lr = lift_block_a.clone()
    lr.setposition(pos_x, pos_y + 5)
    lr.shape("rectangle")
    all_block_pos.append([pos_x, pos_y])
    all_platform_pos.append([pos_x, pos_y])
    all_lift_pos.append([pos_x, pos_y])


def draw_switch(pos_x, pos_y):
    switch_block.clone().setposition(pos_x, pos_y - 5)
    switch_block_fancy.clone().setposition(pos_x, pos_y - 7)
    all_switch_pos.append([pos_x, pos_y])


def draw_timer_switch():
    timer_switch_block.clone().setposition(timer_switch[0], timer_switch[1] - 5)
    timer_switch_block_fancy_a.clone().setposition(timer_switch[0], timer_switch[1] - 7)
    draw_timer_switch_deco_1()
    draw_timer_switch_deco_2()


def draw_timer_switch_deco_1():
    timer_switch_block_fancy_b.clone().setposition(timer_switch[0], timer_switch[1] - 20)


def draw_timer_switch_deco_2():
    timer_switch_block_fancy_c.clone().setposition(timer_switch[0], timer_switch[1] - 12)


def draw_timer_switch_progress(percent):
    c = timer_progress_block.clone()
    c.shapesize(percent / 100)
    c.setposition(timer_switch[0], timer_switch[1] - 20)


def draw_tp_base(pos_x, pos_y):
    tp_block_blue.clone().setposition(pos_x, pos_y)
    f = tp_block_dull_blue.clone()
    f.shapesize(.5)
    f.setposition(pos_x, pos_y)


def draw_tp_point(base_x, base_y, pos_x, pos_y, active):
    b = tp_block_dull_blue.clone()
    if active:
        b = tp_block_blue.clone()
    b.setposition(base_x, base_y)
    b.pendown()
    b.pensize(2)
    b.shapesize(0.8)
    b.setposition(pos_x, pos_y)
    b.penup()


def draw_player(pos_x, pos_y):
    reset_textures()
    player.setposition(pos_x, pos_y)


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

                draw_tp_point(base_pos[0], base_pos[1], first_pos[0], first_pos[1], True)
                draw_tp_point(base_pos[0], base_pos[1], second_pos[0], second_pos[1], False)
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
    print(player.pos())
    global player_falling
    player_falling = True
    player.sety(player.ycor() - 20)
    check_for_ground()
    player_falling = False
    print(player.pos())


def check_for_platform():
    needs_to_lift = True
    for platform_pos in all_platform_pos:
        if platform_pos[0] == player.xcor() and platform_pos[1] + 20 == player.ycor():
            needs_to_lift = False
    if needs_to_lift:
        lift_interact()


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
    if not player_falling and not player_moving and not player_teleporting and not drawing:
        for lift_pos in all_lift_pos:
            if player.xcor() == lift_pos[0] and player.ycor() == lift_pos[1] + 20:
                active_lift.setposition(player.xcor(), player.ycor() - 16)
                active_lift.shape("rectangle")
                active_lift.speed(1)
                lift_interact()

        for switch_pos in all_switch_pos:
            if player.xcor() == switch_pos[0] and player.ycor() == switch_pos[1] and not switching_teleporters:
                switch_interact()

        for timer_switch_pos in all_timer_switch_pos:
            if player.xcor() == timer_switch_pos[0] and player.ycor() == timer_switch_pos[1] and not timer_enabled:
                threading.Thread(target=timer_switch_interact).start()

        for tp_list in all_tp:
            if tp_list:
                teleporter_interact(tp_list)

        if player.xcor() == winpad.xcor() and player.ycor() == winpad.ycor():
            print("YOU WIN!")


def lift_interact():
    global player_teleporting
    player_teleporting = True

    threading.Thread(target=lift_thread_a).start()
    player.setposition(player.xcor(), player.ycor() + 20)
    check_for_platform()
    active_lift.speed(0)
    active_lift.setposition(500, 570)

    player_teleporting = False
    check_for_interact_able()


def lift_thread_a():
    active_lift.setposition(player.xcor(), player.ycor() + 4)


def switch_interact():
    global switching_teleporters
    switching_teleporters = True
    wind.delay(load_wind_delay)
    for tp_list in all_tp:
        if tp_list:
            base_pos = tp_list[0]
            first_pos = tp_list[1]
            second_pos = tp_list[2]
            current_switch = tp_list[3]

            draw_tp_point(base_pos[0], base_pos[1], first_pos[0], first_pos[1], current_switch)
            draw_tp_point(base_pos[0], base_pos[1], second_pos[0], second_pos[1], not current_switch)
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
    # Lift
    for lift_pos in all_lift_pos:
        if player.xcor() == lift_pos[0] and player.ycor() == lift_pos[1] + 20:
            interact_indicator.setposition(lift_pos[0], lift_pos[1] + 50)
            return None

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

    if player.xcor() == winpad.xcor() and player.ycor() == winpad.ycor():
        interact_indicator.color("lime")
        interact_indicator.setposition(winpad.xcor(), winpad.ycor() + 30)
        return None

    # Removes indicator
    interact_indicator.setposition(switch_block.xcor(), switch_block.ycor())
    interact_indicator.color("cyan")


###################
# ----Controls----#
###################
left_keys = ["Left", "a"]
right_keys = ["Right", "d"]
interact_key = ["space", "z", "m"]
escape_key = ["Escape", "Delete"]


def left():
    global player_moving
    if not player_falling and not player_moving and not player_teleporting and not switching_teleporters and not drawing and check_for_wall(False):
        player_moving = True
        player.setx(player.xcor() - 20)
        player_moving = False
        check_for_ground()
        check_for_interact_able()


def right():
    global player_moving
    if not player_falling and not player_moving and not player_teleporting and not switching_teleporters and not drawing and check_for_wall(True):
        player_moving = True
        player.setx(player.xcor() + 20)
        player_moving = False
        check_for_ground()
        check_for_interact_able()


def escape():
    if not current_file == "main_menu" and not drawing and not player_falling and not player_moving and not player_teleporting and not switching_teleporters:
        unload_level()
        print("Unloaded level")
        screen_setup()
        load_level("main_menu")


def setup_listeners():
    wind.listen()
    wind.onkeypress(left, left_keys[0])
    wind.onkeypress(left, left_keys[1])
    wind.onkeypress(right, right_keys[0])
    wind.onkeypress(right, right_keys[1])
    wind.onkeypress(interact, interact_key[0])
    wind.onkeypress(interact, interact_key[1])
    wind.onkeypress(interact, interact_key[2])
    wind.onkeypress(escape, escape_key[0])
    wind.onkeypress(escape, escape_key[1])


###############
# ----Init----#
###############
def load_level(level_to_load):
    global current_file
    print("Initialising")

    setup_listeners()

    # draw level
    print("Reading level")
    read_level(level_to_load)
    current_file = level_to_load

    # init check for ground
    print("Checking for ground")
    check_for_ground()

    print("Initialisation complete")


def unload_level():
    print("Unloading level")
    wind.delay(load_wind_delay)
    wind.clearscreen()

    global lines
    global all_block_pos
    global all_platform_pos
    global all_lift_pos
    global all_switch_pos
    global all_timer_switch_pos
    lines = []
    all_block_pos = []  # [0]=xcor, [1]=ycor
    all_platform_pos = []
    all_lift_pos = []
    all_switch_pos = []
    all_timer_switch_pos = []

    global tp_1
    global tp_2
    global tp_3
    global tp_4
    global tp_5
    global tp_6
    global tp_7
    global tp_8
    global tp_9
    tp_1 = []
    tp_2 = []
    tp_3 = []
    tp_4 = []
    tp_5 = []
    tp_6 = []
    tp_7 = []
    tp_8 = []
    tp_9 = []

    global all_tp
    all_tp = [tp_1, tp_2, tp_3, tp_4, tp_5, tp_6, tp_7, tp_8, tp_9]

    global current_file
    current_file = ""

    global timer_switch
    timer_switch = []


if __name__ == '__main__':
    load_level("1")


wind.mainloop()

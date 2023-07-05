from draw_handler import *
from save_handler import *
import turtle
import time
import threading
import sys

###################
# ----Defaults----#
###################
width = 30
height = 40

load_wind_delay = 0
run_wind_delay = 1
if str(sys.platform) == "linux":
    run_wind_delay = 10

wind = turtle.Screen()

# One time textures (must be in main)
player = turtle.Turtle()
active_lift = lift_block_a.clone()
interact_indicator = interact_indicator_base.clone()
green_interaction_indicator = green_interaction_indicator_base.clone()
red_interaction_indicator = red_interaction_indicator_base.clone()


# reset one time textures
def reset_ot_textures():
    global player
    global active_lift
    global interact_indicator
    global green_interaction_indicator
    global red_interaction_indicator

    player = player_base.clone()
    active_lift = lift_block_a.clone()
    interact_indicator = interact_indicator_base.clone()
    green_interaction_indicator = green_interaction_indicator_base.clone()
    red_interaction_indicator = red_interaction_indicator_base.clone()


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
blue_timer_enabled = False
red_timer_enabled = False

# Lists
lines = []
all_block_pos = []  # [0]=xcor, [1]=ycor
all_platform_pos = []
all_lift_pos = []
all_blue_switch_pos = []
all_red_switch_pos = []
blue_timer_switch = []  # Only one pair of pos entry allowed
red_timer_switch = []  # Only one pair of pos entry allowed
winpad_pos = []

# Tp lists
blue_tp_base_char = ["1", "2", "3", "4", "5"]
red_tp_base_char = ["6", "7", "8", "9"]
blue_tp_first_char = ["a", "c", "e", "g", "i"]
red_tp_first_char = ["k", "m", "o", "q"]
blue_tp_second_char = ["b", "d", "f", "h", "j"]
red_tp_second_char = ["l", "n", "p", "r"]
blue_tp_1 = []
blue_tp_2 = []
blue_tp_3 = []
blue_tp_4 = []
blue_tp_5 = []
red_tp_6 = []
red_tp_7 = []
red_tp_8 = []
red_tp_9 = []
all_blue_tp = [blue_tp_1, blue_tp_2, blue_tp_3, blue_tp_4, blue_tp_5]
all_red_tp = [red_tp_6, red_tp_7, red_tp_8, red_tp_9]

# Level select pos (only in lobby), Order: [xcor, ycor, level number]
all_base_lvl_sel_pos = [[-100, -240, 1], [0.0, -240, 2], [100, -240, 3], [100, -360, 4], [0.0, -360, 5], [-100, -360, 6]]


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


# Times=0: base level drawn and base tp points saved, times=1: first tp points saved, times=2: second tp points saved, teleporters drawn and timers drawn
def draw_level(times):
    global blue_timer_switch
    global red_timer_switch

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
                        all_block_pos.append([pos_x, pos_y])
                    elif char == fancy_ground_char:
                        draw_ground_cube(pos_x, pos_y, True)
                        all_block_pos.append([pos_x, pos_y])
                    elif char == platform_char:
                        draw_platform(pos_x, pos_y)
                        all_block_pos.append([pos_x, pos_y])
                        all_platform_pos.append([pos_x, pos_y])
                    elif char == lift_char:
                        draw_lift(pos_x, pos_y)
                        all_block_pos.append([pos_x, pos_y])
                        all_platform_pos.append([pos_x, pos_y])
                        all_lift_pos.append([pos_x, pos_y])
                    elif char == blue_switch_char:
                        draw_blue_switch(pos_x, pos_y)
                        all_blue_switch_pos.append([pos_x, pos_y])
                    elif char == red_switch_char:
                        draw_red_switch(pos_x, pos_y)
                        all_red_switch_pos.append([pos_x, pos_y])
                    elif char == blue_timer_switch_char:
                        blue_timer_switch = [pos_x, pos_y]
                    elif char == red_timer_switch_char:
                        red_timer_switch = [pos_x, pos_y]
                    elif char == winpad_char:
                        draw_green_door(pos_x, pos_y)
                        draw_green_door_star(pos_x, pos_y)
                        if not len(winpad_pos) > 2:
                            winpad_pos.append([pos_x, pos_y])
                        else:
                            raise ValueError("Too many win-pads in level")
                    elif char == player_char:
                        draw_player(pos_x, pos_y)

                # Blue teleporters
                for base_tp_char in blue_tp_base_char:
                    if char == base_tp_char and times == 0:
                        # add to list, render after level has been drawn
                        all_blue_tp[int(char) - 1].insert(0, [pos_x, pos_y])

                for first_tp_char in blue_tp_first_char:
                    if char == first_tp_char and times == 1:
                        all_blue_tp[blue_tp_first_char.index(char)].insert(1, [pos_x, pos_y])

                for second_tp_char in blue_tp_second_char:
                    if char == second_tp_char and times == 2:
                        all_blue_tp[blue_tp_second_char.index(char)].insert(2, [pos_x, pos_y])

                # Red teleporters
                for base_tp_char in red_tp_base_char:
                    if char == base_tp_char and times == 0:
                        all_red_tp[int(char) - 6].insert(0, [pos_x, pos_y])

                for first_tp_char in red_tp_first_char:
                    if char == first_tp_char and times == 1:
                        all_red_tp[red_tp_first_char.index(char)].insert(1, [pos_x, pos_y])

                for second_tp_char in red_tp_second_char:
                    if char == second_tp_char and times == 2:
                        all_red_tp[red_tp_second_char.index(char)].insert(2, [pos_x, pos_y])

        # To be done after base level is drawn
        if times == 2:

            # Timer switches
            if len(blue_timer_switch) > 2:
                raise ValueError("Only one blue timer switch is allowed!")
            elif len(blue_timer_switch) == 2:
                draw_blue_timer_switch(blue_timer_switch)

            if len(red_timer_switch) > 2:
                raise ValueError("Only one red timer switch is allowed!")
            elif len(red_timer_switch) == 2:
                draw_red_timer_switch(red_timer_switch)

            # Level selectors
            if current_file == "lobby":
                draw_level_selectors(all_base_lvl_sel_pos)

            # Teleporters
            draw_blue_teleporters()
            draw_red_teleporters()

            print("Draw level complete")


def draw_player(pos_x, pos_y):
    reset_ot_textures()
    player.setposition(pos_x, pos_y)


def draw_blue_teleporters():
    for tp_list in all_blue_tp:
        if tp_list:
            all_blue_tp[all_blue_tp.index(tp_list)].append(False)  # adds 'switched' value to end

            if len(tp_list) == 4:
                base_pos = tp_list[0]
                first_pos = tp_list[1]
                second_pos = tp_list[2]

                draw_blue_tp_point(base_pos[0], base_pos[1], first_pos[0], first_pos[1], True)
                draw_blue_tp_point(base_pos[0], base_pos[1], second_pos[0], second_pos[1], False)
                draw_blue_tp_base(base_pos[0], base_pos[1])
            else:
                raise ValueError("Incorrect amount of values in list: ", tp_list,
                                 " (Must be exactly 3 entries - base, tp point 1, tp point 2, False)")


def draw_red_teleporters():
    for tp_list in all_red_tp:
        if tp_list:
            all_red_tp[all_red_tp.index(tp_list)].append(False)  # adds 'switched' value to end

            if len(tp_list) == 4:
                base_pos = tp_list[0]
                first_pos = tp_list[1]
                second_pos = tp_list[2]

                draw_red_tp_point(base_pos[0], base_pos[1], first_pos[0], first_pos[1], True)
                draw_red_tp_point(base_pos[0], base_pos[1], second_pos[0], second_pos[1], False)
                draw_red_tp_base(base_pos[0], base_pos[1])
            else:
                raise ValueError("Incorrect amount of values in list: ", tp_list,
                                 " (Must be exactly 3 entries - base, tp point 1, tp point 2, False)")


##############################
# ----Collision & Gravity----#
##############################
def is_not_on_ground():
    for block_pos in all_block_pos:
        if block_pos[0] - 19 < player.xcor() < block_pos[0] + 19:
            if block_pos[1] + 20 == player.ycor():
                return False
    return True


def can_fall():
    global player_falling
    while is_not_on_ground():
        player_falling = True
        player.sety(player.ycor() - 20)
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
def interact(x=0, y=0):
    if not player_falling and not player_moving and not player_teleporting and not drawing:
        # Lift
        for lift_pos in all_lift_pos:
            if player.xcor() == lift_pos[0] and player.ycor() == lift_pos[1] + 20:
                active_lift.setposition(player.xcor(), player.ycor() - 16)
                active_lift.shape("rectangle")
                lift_interact()

        # Blue switch
        for switch_pos in all_blue_switch_pos:
            if player.xcor() == switch_pos[0] and player.ycor() == switch_pos[1] and not switching_teleporters:
                switch_interact(True)

        # Red switch
        for switch_pos in all_red_switch_pos:
            if player.xcor() == switch_pos[0] and player.ycor() == switch_pos[1] and not switching_teleporters:
                switch_interact(False)

        # Blue timer switch
        if len(blue_timer_switch) == 2 and player.xcor() == blue_timer_switch[0] and player.ycor() == blue_timer_switch[1] and not blue_timer_enabled:
            threading.Thread(target=blue_timer_switch_interact).start()

        # Red timer switch
        if len(red_timer_switch) == 2 and player.xcor() == red_timer_switch[0] and player.ycor() == red_timer_switch[1] and not red_timer_enabled:
            threading.Thread(target=red_timer_switch_interact).start()

        # Blue teleporter
        for tp_list in all_blue_tp:
            if tp_list:
                teleporter_interact(tp_list)

        # Red teleporter
        for tp_list in all_red_tp:
            if tp_list:
                teleporter_interact(tp_list)

        # Winpad
        for winpad_p in winpad_pos:
            if player.xcor() == winpad_p[0] and player.ycor() == winpad_p[1]:
                complete_level(int(current_file))
                go_to_level("lobby")

        # Level select
        for base_lvl_sel_pos in all_base_lvl_sel_pos:
            if player.xcor() == base_lvl_sel_pos[0] and player.ycor() == base_lvl_sel_pos[1] and is_level_unlocked(base_lvl_sel_pos[2]) and current_file == "lobby":
                go_to_level(str(base_lvl_sel_pos[2]))


def lift_interact():
    global player_teleporting
    player_teleporting = True

    # Save y positions of all platforms directly above lift
    platforms_above = []
    for platform_pos in all_platform_pos:
        if platform_pos[0] == player.xcor() and platform_pos[1] > player.ycor():
            platforms_above.append(platform_pos[1])

    # Save the y pos of the nearest platform above lift
    go_up_to = platforms_above[len(platforms_above) - 1]

    active_lift.setposition(player.xcor(), go_up_to + 4)
    player.setposition(player.xcor(), go_up_to + 20)

    # After lift use
    active_lift.setposition(500, 570)

    player_teleporting = False
    check_for_interact_able()


def switch_interact(is_blue):
    global switching_teleporters
    switching_teleporters = True
    wind.delay(load_wind_delay)

    if is_blue:
        all_tp_list = all_blue_tp
    else:
        all_tp_list = all_red_tp

    for tp_list in all_tp_list:
        if tp_list:
            base_pos = tp_list[0]
            first_pos = tp_list[1]
            second_pos = tp_list[2]
            current_switch = tp_list[3]

            if is_blue:
                draw_blue_tp_point(base_pos[0], base_pos[1], first_pos[0], first_pos[1], current_switch)
                draw_blue_tp_point(base_pos[0], base_pos[1], second_pos[0], second_pos[1], not current_switch)
                draw_blue_tp_base(base_pos[0], base_pos[1])
            else:
                draw_red_tp_point(base_pos[0], base_pos[1], first_pos[0], first_pos[1], current_switch)
                draw_red_tp_point(base_pos[0], base_pos[1], second_pos[0], second_pos[1], not current_switch)
                draw_red_tp_base(base_pos[0], base_pos[1])

            tp_list[3] = not current_switch
    wind.delay(run_wind_delay)
    switching_teleporters = False


def blue_timer_switch_interact():
    global blue_timer_enabled

    blue_timer_enabled = True
    time_pressed = time.time()
    timer_sec = 10

    while time.time() - time_pressed < timer_sec:
        time.sleep(0.5)
        timer_percent = ((time.time() - time_pressed) / timer_sec) * 100
        draw_blue_timer_switch_progress(timer_percent, blue_timer_switch)

    switch_interact(True)
    blue_timer_enabled = False

    draw_blue_timer_switch_deco_1(blue_timer_switch)
    draw_blue_timer_switch_deco_2(blue_timer_switch)
    check_for_interact_able()


def red_timer_switch_interact():
    global red_timer_enabled

    red_timer_enabled = True
    time_pressed = time.time()
    timer_sec = 10

    while time.time() - time_pressed < timer_sec:
        time.sleep(0.5)
        timer_percent = ((time.time() - time_pressed) / timer_sec) * 100
        draw_red_timer_switch_progress(timer_percent, red_timer_switch)

    switch_interact(False)
    red_timer_enabled = False

    draw_red_timer_switch_deco_1(red_timer_switch)
    draw_red_timer_switch_deco_2(red_timer_switch)
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

    can_fall()
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

    # Blue switch
    for switch_pos in all_blue_switch_pos:
        if player.xcor() == switch_pos[0] and player.ycor() == switch_pos[1]:
            interact_indicator.setposition(switch_pos[0], switch_pos[1] + 30)
            return None

    # Red switch
    for switch_pos in all_red_switch_pos:
        if player.xcor() == switch_pos[0] and player.ycor() == switch_pos[1]:
            red_interaction_indicator.setposition(switch_pos[0], switch_pos[1] + 30)
            return None

    # Blue timer switch
    if len(blue_timer_switch) == 2 and player.xcor() == blue_timer_switch[0] and player.ycor() == blue_timer_switch[1] and not blue_timer_enabled:
        interact_indicator.setposition(blue_timer_switch[0], blue_timer_switch[1] + 30)
        return None

    # Red timer switch
    if len(red_timer_switch) == 2 and player.xcor() == red_timer_switch[0] and player.ycor() == red_timer_switch[1] and not red_timer_enabled:
        red_interaction_indicator.setposition(red_timer_switch[0], red_timer_switch[1] + 30)
        return None

    # blue teleporter
    for tp_list in all_blue_tp:
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

    # Red teleporter
    for tp_list in all_red_tp:
        if tp_list:
            base_pos = tp_list[0]
            first_pos = tp_list[1]
            second_pos = tp_list[2]
            switched = tp_list[3]

            if player.xcor() == base_pos[0] and player.ycor() == base_pos[1]:
                red_interaction_indicator.setposition(base_pos[0], base_pos[1] + 30)
                return None
            elif player.xcor() == first_pos[0] and player.ycor() == first_pos[1] and not switched:
                red_interaction_indicator.setposition(first_pos[0], first_pos[1] + 30)
                return None
            elif player.xcor() == second_pos[0] and player.ycor() == second_pos[1] and switched:
                red_interaction_indicator.setposition(second_pos[0], second_pos[1] + 30)
                return None

    # Winpad
    for winpad_p in winpad_pos:
        if player.xcor() == winpad_p[0] and player.ycor() == winpad_p[1]:
            green_interaction_indicator.setposition(winpad_p[0], winpad_p[1] + 40)
            return None

    # Level select
    for base_lvl_sel_pos in all_base_lvl_sel_pos:
        if player.xcor() == base_lvl_sel_pos[0] and player.ycor() == base_lvl_sel_pos[1] and is_level_unlocked(base_lvl_sel_pos[2]) and current_file == "lobby":
            green_interaction_indicator.setposition(base_lvl_sel_pos[0], base_lvl_sel_pos[1] + 40)
            return None

    # Moves indicator off-screen
    interact_indicator.setposition(500, 500)
    green_interaction_indicator.setposition(500, 500)
    red_interaction_indicator.setposition(500, 500)


###################
# ----Controls----#
###################
left_keys = ["Left", "a", "A"]
right_keys = ["Right", "d", "D"]
interact_key = ["space", "z", "m", "Z", "M"]
escape_key = ["Escape", "Delete"]


def left():
    global player_moving
    if not player_falling and not player_moving and not player_teleporting and not switching_teleporters and not drawing and check_for_wall(
            False):
        player_moving = True
        player.setx(player.xcor() - 20)
        can_fall()
        check_for_interact_able()
        player_moving = False


def right():
    global player_moving
    if not player_falling and not player_moving and not player_teleporting and not switching_teleporters and not drawing and check_for_wall(
            True):
        player_moving = True
        player.setx(player.xcor() + 20)
        can_fall()
        check_for_interact_able()
        player_moving = False


def escape():
    if not current_file == "lobby" and not drawing and not player_falling and not player_moving and not player_teleporting and not switching_teleporters:
        go_to_level("lobby")
    elif current_file == "lobby":
        print("Exiting game")
        wind.bye()


def setup_listeners():
    wind.listen()
    wind.onkeypress(left, left_keys[0])
    wind.onkeypress(left, left_keys[1])
    wind.onkeypress(left, left_keys[2])
    wind.onkeypress(right, right_keys[0])
    wind.onkeypress(right, right_keys[1])
    wind.onkeypress(right, right_keys[2])
    wind.onkeypress(interact, interact_key[0])
    wind.onkeypress(interact, interact_key[1])
    wind.onkeypress(interact, interact_key[2])
    wind.onkeypress(interact, interact_key[3])
    wind.onkeypress(interact, interact_key[4])
    wind.onclick(interact)
    wind.onkeypress(escape, escape_key[0])
    wind.onkeypress(escape, escape_key[1])


###############
# ----Init----#
###############
def go_to_level(level_to_load):
    unload_level()
    print("Unloaded level")
    screen_setup()
    load_level(level_to_load)


# Use go_to_level to load levels, not this
def load_level(level_to_load):
    global current_file
    current_file = level_to_load

    setup_listeners()

    # draw level
    print("Reading level")
    read_level(level_to_load)

    # init check for ground
    print("Checking for ground")
    can_fall()

    print("Initialisation complete")


def unload_level():
    print("Unloading level")
    wind.delay(load_wind_delay)
    wind.clearscreen()

    global lines
    global all_block_pos
    global all_platform_pos
    global all_lift_pos
    global all_blue_switch_pos
    global all_red_switch_pos
    global blue_timer_switch
    global red_timer_switch
    global winpad_pos
    lines = []
    all_block_pos = []  # [0]=xcor, [1]=ycor
    all_platform_pos = []
    all_lift_pos = []
    all_blue_switch_pos = []
    all_red_switch_pos = []
    blue_timer_switch = []
    red_timer_switch = []
    winpad_pos = []

    global blue_tp_1
    global blue_tp_2
    global blue_tp_3
    global blue_tp_4
    global blue_tp_5
    global red_tp_6
    global red_tp_7
    global red_tp_8
    global red_tp_9
    blue_tp_1 = []
    blue_tp_2 = []
    blue_tp_3 = []
    blue_tp_4 = []
    blue_tp_5 = []
    red_tp_6 = []
    red_tp_7 = []
    red_tp_8 = []
    red_tp_9 = []

    global all_blue_tp
    global all_red_tp
    all_blue_tp = [blue_tp_1, blue_tp_2, blue_tp_3, blue_tp_4, blue_tp_5]
    all_red_tp = [red_tp_6, red_tp_7, red_tp_8, red_tp_9]

    global current_file
    current_file = ""


if __name__ == '__main__':
    print("Initialising")
    read_save_file()
    load_level("5")

wind.mainloop()

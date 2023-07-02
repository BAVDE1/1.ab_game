from draw_handler import *
from save_handler import *
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

# One time textures (must be in main)
player = turtle.Turtle()
active_lift = platform_block.clone()
interact_indicator = interact_indicator_base.clone()
green_interaction_indicator = green_interaction_indicator_base.clone()


def reset_ot_textures():
    global player
    global active_lift
    global interact_indicator
    global green_interaction_indicator

    player = player_base.clone()
    active_lift = platform_block.clone()
    interact_indicator = interact_indicator_base.clone()
    green_interaction_indicator = green_interaction_indicator_base.clone()


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
winpad_pos = []

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

# [xcor, ycor, level number]
all_base_lvl_sel_pos = [[-100, -240, 1], [0.0, -240, 2], [100, -240, 3], [100, -360, 4], [0.0, -360, 5], [-100, -360, 6]]

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


# Times=0: base level drawn and base tp points saved, times=1: first tp points saved, times=2: second tp points saved, teleporters drawn and timers drawn
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
                    elif char == switch_char:
                        draw_switch(pos_x, pos_y)
                        all_switch_pos.append([pos_x, pos_y])
                    elif char == timer_switch_char:
                        all_timer_switch_pos.append([pos_x, pos_y])
                    elif char == winpad_char:
                        draw_green_door(pos_x, pos_y)
                        draw_green_door_star(pos_x, pos_y)
                        if not len(winpad_pos) > 2:
                            winpad_pos.append([pos_x, pos_y])
                        else:
                            raise ValueError("Too many win-pads in level")
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
            draw_timer_switches(all_timer_switch_pos, timer_switch)
            if current_file == "lobby":
                draw_level_selectors(all_base_lvl_sel_pos)
            draw_teleporters()

            print("Draw level complete")


def draw_player(pos_x, pos_y):
    reset_ot_textures()
    player.setposition(pos_x, pos_y)


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
    global player_falling
    player_falling = True
    player.sety(player.ycor() - 20)
    check_for_ground()
    player_falling = False


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
        # Lift
        for lift_pos in all_lift_pos:
            if player.xcor() == lift_pos[0] and player.ycor() == lift_pos[1] + 20:
                active_lift.setposition(player.xcor(), player.ycor() - 16)
                active_lift.shape("rectangle")
                active_lift.speed(1)
                lift_interact()

        # Switch
        for switch_pos in all_switch_pos:
            if player.xcor() == switch_pos[0] and player.ycor() == switch_pos[1] and not switching_teleporters:
                switch_interact()

        # Timer switch
        for timer_switch_pos in all_timer_switch_pos:
            if player.xcor() == timer_switch_pos[0] and player.ycor() == timer_switch_pos[1] and not timer_enabled:
                threading.Thread(target=timer_switch_interact).start()

        # teleporter
        for tp_list in all_tp:
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
    timer_sec = 10
    while time.time() - time_pressed < timer_sec:
        time.sleep(0.2)
        timer_percent = ((time.time() - time_pressed) / timer_sec) * 100
        draw_timer_switch_progress(timer_percent, timer_switch)
    switch_interact()
    timer_enabled = False
    draw_timer_switch_deco_1(timer_switch)
    draw_timer_switch_deco_2(timer_switch)
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

    # Removes indicator
    interact_indicator.setposition(switch_block.xcor(), switch_block.ycor())
    green_interaction_indicator.setposition(switch_block.xcor(), switch_block.ycor())


###################
# ----Controls----#
###################
left_keys = ["Left", "a"]
right_keys = ["Right", "d"]
interact_key = ["space", "z", "m"]
escape_key = ["Escape", "Delete"]


def left():
    global player_moving
    if not player_falling and not player_moving and not player_teleporting and not switching_teleporters and not drawing and check_for_wall(
            False):
        player_moving = True
        player.setx(player.xcor() - 20)
        check_for_ground()
        check_for_interact_able()
        player_moving = False


def right():
    global player_moving
    if not player_falling and not player_moving and not player_teleporting and not switching_teleporters and not drawing and check_for_wall(
            True):
        player_moving = True
        player.setx(player.xcor() + 20)
        check_for_ground()
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
    global winpad_pos
    lines = []
    all_block_pos = []  # [0]=xcor, [1]=ycor
    all_platform_pos = []
    all_lift_pos = []
    all_switch_pos = []
    all_timer_switch_pos = []
    winpad_pos = []

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
    print("Initialising")
    read_save_file()
    load_level("3")

wind.mainloop()

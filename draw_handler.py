from textures import *


def draw_ground_cube(pos_x, pos_y, fancy):
    ground_block.clone().setposition(pos_x, pos_y)
    if fancy:
        fancy_block.clone().setposition(pos_x, pos_y)


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
    r = platform_block.clone()  # Must be done in main
    r.setposition(pos_x, pos_y + 5)
    r.shape("rectangle")


def draw_lift(pos_x, pos_y):
    r = platform_block.clone()  # Must be done in main
    r.setposition(pos_x, pos_y + 5)
    r.shape("rectangle")
    lr = lift_block_a.clone()
    lr.setposition(pos_x, pos_y + 5)
    lr.shape("rectangle")


def draw_timer_switches(all_timer_switch_pos, timer_switch):
    for ts in all_timer_switch_pos:
        if len(timer_switch) == 0:
            timer_switch.append(ts[0])
            timer_switch.append(ts[1])
            draw_timer_switch(timer_switch)
        else:
            raise ValueError("Only one timer switch is allowed!")


def draw_timer_switch(timer_switch):
    timer_switch_block.clone().setposition(timer_switch[0], timer_switch[1] - 5)
    timer_switch_block_fancy_a.clone().setposition(timer_switch[0], timer_switch[1] - 7)
    draw_timer_switch_deco_1(timer_switch)
    draw_timer_switch_deco_2(timer_switch)


def draw_timer_switch_deco_1(timer_switch):
    timer_switch_block_fancy_b.clone().setposition(timer_switch[0], timer_switch[1] - 20)


def draw_timer_switch_deco_2(timer_switch):
    timer_switch_block_fancy_c.clone().setposition(timer_switch[0], timer_switch[1] - 12)


def draw_timer_switch_progress(percent, timer_switch):
    c = timer_progress_block.clone()  # Must be done in main
    c.shapesize(percent / 100)
    c.setposition(timer_switch[0], timer_switch[1] - 20)


def draw_switch(pos_x, pos_y):
    switch_block.clone().setposition(pos_x, pos_y - 5)
    switch_block_fancy.clone().setposition(pos_x, pos_y - 7)


def draw_tp_base(pos_x, pos_y):
    tp_block_blue.clone().setposition(pos_x, pos_y)  # Must be done in main
    f = tp_block_dull_blue.clone()
    f.shapesize(.5)
    f.setposition(pos_x, pos_y)


def draw_tp_point(base_x, base_y, pos_x, pos_y, active):
    b = tp_block_dull_blue.clone()  # Must be done in main
    if active:
        b = tp_block_blue.clone()
    b.setposition(base_x, base_y)
    b.pendown()
    b.pensize(2)
    b.shapesize(0.8)
    b.setposition(pos_x, pos_y)
    b.penup()

from textures import *
from save_handler import is_level_complete


def draw_level_selectors(all_base_lvl_sel_pos):
    on_level = 0

    for base_lvl_sel_pos in all_base_lvl_sel_pos:
        on_level += 1

        # Level select
        if on_level == 1 or is_level_complete(on_level - 1):
            draw_green_door(base_lvl_sel_pos[0], base_lvl_sel_pos[1])
        else:
            draw_grey_door(base_lvl_sel_pos[0], base_lvl_sel_pos[1])

        # Completion star
        if is_level_complete(on_level):
            draw_green_door_star(base_lvl_sel_pos[0], base_lvl_sel_pos[1])
        else:
            draw_grey_door_star(base_lvl_sel_pos[0], base_lvl_sel_pos[1])


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
    green_door_block.clone().setposition(pos_x, pos_y - 3)
    green_door_block_a.clone().setposition(pos_x, pos_y - 6)


def draw_green_door_star(pos_x, pos_y):
    green_door_block_b.clone().setposition(pos_x, pos_y + 20)
    green_door_block_c.clone().setposition(pos_x, pos_y + 20)


def draw_grey_door(pos_x, pos_y):
    grey_door_block.clone().setposition(pos_x, pos_y - 3)
    grey_door_block_a.clone().setposition(pos_x, pos_y - 6)


def draw_grey_door_star(pos_x, pos_y):
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
    lift_block_b.clone().setposition(pos_x, pos_y - 1)


def draw_blue_timer_switch(timer_switch):
    blue_timer_switch_block.clone().setposition(timer_switch[0], timer_switch[1] - 5)
    blue_timer_switch_block_fancy_a.clone().setposition(timer_switch[0], timer_switch[1] - 7)
    draw_blue_timer_switch_deco_1(timer_switch)
    draw_blue_timer_switch_deco_2(timer_switch)


def draw_blue_timer_switch_deco_1(timer_switch):
    blue_timer_switch_block_fancy_b.clone().setposition(timer_switch[0], timer_switch[1] - 20)


def draw_blue_timer_switch_deco_2(timer_switch):
    blue_timer_switch_block_fancy_c.clone().setposition(timer_switch[0], timer_switch[1] - 12)


def draw_blue_timer_switch_progress(percent, timer_switch):
    c = blue_timer_progress_block.clone()  # Must be done in main
    c.shapesize(percent / 100)
    c.setposition(timer_switch[0], timer_switch[1] - 20)


def draw_red_timer_switch(timer_switch):
    red_timer_switch_block.clone().setposition(timer_switch[0], timer_switch[1] - 5)
    red_timer_switch_block_fancy_a.clone().setposition(timer_switch[0], timer_switch[1] - 7)
    draw_red_timer_switch_deco_1(timer_switch)
    draw_red_timer_switch_deco_2(timer_switch)


def draw_red_timer_switch_deco_1(timer_switch):
    red_timer_switch_block_fancy_b.clone().setposition(timer_switch[0], timer_switch[1] - 20)


def draw_red_timer_switch_deco_2(timer_switch):
    red_timer_switch_block_fancy_c.clone().setposition(timer_switch[0], timer_switch[1] - 12)


def draw_red_timer_switch_progress(percent, timer_switch):
    c = red_timer_progress_block.clone()  # Must be done in main
    c.shapesize(percent / 100)
    c.setposition(timer_switch[0], timer_switch[1] - 20)


def draw_blue_switch(pos_x, pos_y):
    blue_switch_block.clone().setposition(pos_x, pos_y - 5)
    blue_switch_block_fancy.clone().setposition(pos_x, pos_y - 7)


def draw_red_switch(pos_x, pos_y):
    red_switch_block.clone().setposition(pos_x, pos_y - 5)
    red_switch_block_fancy.clone().setposition(pos_x, pos_y - 7)


def draw_blue_tp_base(pos_x, pos_y):
    tp_block_blue.clone().setposition(pos_x, pos_y)  # Must be done in main
    f = tp_block_dull_blue.clone()
    f.shapesize(.5)
    f.setposition(pos_x, pos_y)


def draw_red_tp_base(pos_x, pos_y):
    tp_block_red.clone().setposition(pos_x, pos_y)  # Must be done in main
    f = tp_block_dull_red.clone()
    f.shapesize(.5)
    f.setposition(pos_x, pos_y)


def draw_blue_tp_point(base_x, base_y, pos_x, pos_y, active):
    b = tp_block_dull_blue.clone()  # Must be done in main
    if active:
        b = tp_block_blue.clone()
    b.setposition(base_x, base_y)
    b.pendown()
    b.pensize(2)
    b.shapesize(0.8)
    b.setposition(pos_x, pos_y)
    b.penup()


def draw_red_tp_point(base_x, base_y, pos_x, pos_y, active):
    b = tp_block_dull_red.clone()  # Must be done in main
    if active:
        b = tp_block_red.clone()
    b.setposition(base_x, base_y)
    b.pendown()
    b.pensize(2)
    b.shapesize(0.8)
    b.setposition(pos_x, pos_y)
    b.penup()

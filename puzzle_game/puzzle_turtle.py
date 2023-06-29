import turtle

###################
# ----Defaults----#
###################
width = 30
height = 40

dark_grey_char = "."
dark_grey_block = turtle.Turtle()
dark_grey_block.shape("square")
dark_grey_block.penup()
dark_grey_block.speed(0)
dark_grey_block.color("grey5")
dark_grey_block.setposition(540, 500)

grey_char = ":"
grey_block = turtle.Turtle()
grey_block.shape("square")
grey_block.penup()
grey_block.speed(0)
grey_block.color("grey10")
grey_block.setposition(520, 500)

ground_char = "#"
ground_block = turtle.Turtle()
ground_block.shape("square")
ground_block.penup()
ground_block.speed(0)
ground_block.color("white")
ground_block.setposition(500, 500)

fancy_ground_char = "*"
fancy_block = turtle.Turtle()
fancy_block.shape("square")
fancy_block.penup()
fancy_block.speed(0)
fancy_block.shapesize(.5)
fancy_block.color("black")
fancy_block.setposition(500, 500)

switch_char = "^"
switch_block = turtle.Turtle()
switch_block.shape("triangle")
switch_block.penup()
switch_block.speed(0)
switch_block.color("cyan")
switch_block.tilt(90)
switch_block.setposition(500, 470)

hover_switch = switch_block.clone()
hover_switch.shapesize(0.5)
hover_switch.tilt(180)

player_char = "@"
player = turtle.Turtle()
player.shape("circle")
player.penup()
player.speed(1)
player.color("yellow")
player_falling = False
player_moving = False

lines = []
all_block_pos = []  # [0]=xcor, [1]=ycor
all_switch_pos = []
drawing = False

# Screen setup
wind = turtle.Screen()
wind.bgcolor("black")
margin = 2
wind.setup(width=(width + margin) * 20, height=(height + margin) * 20)
wind.title("idk")
wind.delay(0)


####################
# ----Rendering----#
####################
def read_level():
    with open("puzzle_game/levels/level_1.txt") as file:
        global lines
        global drawing
        lines = [line.rstrip() for line in file]

        # draw level
        drawing = True
        wind.delay(0)
        draw_level()
        wind.delay(1)
        drawing = False


def draw_ground_cube(pos_x, pos_y, fancy):
    ground_block.clone().setposition(pos_x, pos_y)
    if fancy:
        fancy_block.clone().setposition(pos_x, pos_y)
    all_block_pos.append([pos_x, pos_y])


def draw_grey_cube(pos_x, pos_y, dark):
    if dark:
        dark_grey_block.clone().setposition(pos_x, pos_y)
    else:
        grey_block.clone().setposition(pos_x, pos_y)


def draw_switch_cube(pos_x, pos_y):
    switch_block.clone().setposition(pos_x, pos_y - 5)
    s_fancy = switch_block.clone()
    s_fancy.setposition(pos_x, pos_y - 5)
    s_fancy.shapesize(.5)
    s_fancy.color("cyan4")
    all_switch_pos.append([pos_x, pos_y])


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
                if char == dark_grey_char:
                    draw_grey_cube((width / 2 * -20) + (20 * char_num), (height / 2 * 20) - (20 * line_num), True)
                elif char == grey_char:
                    draw_grey_cube((width / 2 * -20) + (20 * char_num), (height / 2 * 20) - (20 * line_num), False)
                elif char == ground_char:
                    draw_ground_cube((width / 2 * -20) + (20 * char_num), (height / 2 * 20) - (20 * line_num), False)
                elif char == fancy_ground_char:
                    draw_ground_cube((width / 2 * -20) + (20 * char_num), (height / 2 * 20) - (20 * line_num), True)
                elif char == switch_char:
                    draw_switch_cube((width / 2 * -20) + (20 * char_num), (height / 2 * 20) - (20 * line_num))
                elif char == player_char:
                    draw_player((width / 2 * -20) + (20 * char_num), (height / 2 * 20) - (20 * line_num))


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
            hover_switch.setposition(switch_pos[0], switch_pos[1] + 30)
            return None
        hover_switch.setposition(switch_block.xcor(), switch_block.ycor())


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

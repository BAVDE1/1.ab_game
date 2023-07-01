import sys
import turtle

# Custom shape
rectangle_cors = ((-20, 10), (20, 10), (20, -10), (-20, -10))

# Loading
turtle.ht()
turtle.write("loading...", font=("Lora", 10, "bold"))

# Player
player_char = "@"
player_base = turtle.Turtle()
player_base.penup()
player_base.speed(0)
player_base.setposition(500, 500)
player_base.speed(1)
player_base.shape("circle")
player_base.color("yellow")

# Base blocks
base_block = turtle.Turtle()
base_block.penup()
base_block.speed(0)
base_block.setposition(500, 500)
base_block.shape("square")

base_triangle = base_block.clone()
base_triangle.shape("triangle")

base_circle = base_block.clone()
base_circle.shape("circle")

# Ground
ground_char = "#"
ground_block = base_block.clone()
ground_block.setposition(500, 500)
ground_block.color("white")

# Fancy blocks
dark_grey_char = "."
dark_grey_block = base_block.clone()
dark_grey_block.setposition(540, 500)
dark_grey_block.color("grey10")
if str(sys.platform) == "win32":
    dark_grey_block.color("grey2")

grey_char = ":"
grey_block = base_block.clone()
grey_block.setposition(520, 500)
grey_block.color("grey20")
if str(sys.platform) == "win32":
    grey_block.color("grey5")

fancy_ground_char = "*"
fancy_block = base_block.clone()
fancy_block.setposition(500, 500)
fancy_block.shapesize(.5)
fancy_block.color("black")

# Interact-able
# Green door
level_sel_char = "|"
green_door_block = base_triangle.clone()
green_door_block.setposition(600, 500)
green_door_block.color("lawn green")
green_door_block.tilt(90)

green_door_block_a = green_door_block.clone()
green_door_block_a.shapesize(0.5)
green_door_block_a.color("lime")

green_door_block_b = green_door_block_a.clone()
green_door_block_b.tilt(180)
green_door_block_b.color("lawn green")

green_door_block_c = green_door_block_a.clone()
green_door_block_c.color("lawn green")

# Grey door
grey_door_block = green_door_block.clone()
grey_door_block.color("grey")

grey_door_block_a = green_door_block_a.clone()
grey_door_block_a.color("grey25")

grey_door_block_b = green_door_block_b.clone()
grey_door_block_b.color("grey")

grey_door_block_c = green_door_block_c.clone()
grey_door_block_c.color("grey")

# Other interact-able
platform_char = "-"
platform_block = base_block.clone()
platform_block.tilt(90)
platform_block.shapesize(0.5)
platform_block.color("white")

lift_char = "="
lift_block_a = platform_block.clone()
lift_block_a.shapesize(0.3)
lift_block_a.color("cyan")

switch_char = "^"
switch_block = base_triangle.clone()
switch_block.setposition(500, 470)
switch_block.color("cyan")
switch_block.tilt(90)

switch_block_fancy = switch_block.clone()
switch_block_fancy.shapesize(.5)
switch_block_fancy.color("cyan4")

# Timer switch
timer_switch_char = '"'
timer_switch_block = switch_block.clone()
timer_progress_block = base_block.clone()
timer_progress_block.setposition(600, 600)
timer_progress_block.color("cyan")

timer_switch_block_fancy_a = timer_switch_block.clone()
timer_switch_block_fancy_a.shapesize(.5)
timer_switch_block_fancy_a.color("cyan4")

timer_switch_block_fancy_b = timer_switch_block.clone()
timer_switch_block_fancy_b.color("cyan", "white")
timer_switch_block_fancy_b.shape("square")

timer_switch_block_fancy_c = timer_switch_block.clone()
timer_switch_block_fancy_c.shapesize(.5)
timer_switch_block_fancy_c.color("cyan4")
timer_switch_block_fancy_c.tilt(180)

# Teleporter
tp_block_blue = base_circle.clone()
tp_block_blue.setposition(500, 450)
tp_block_blue.color("cyan")

tp_block_dull_blue = base_circle.clone()
tp_block_dull_blue.setposition(520, 450)
tp_block_dull_blue.color("cyan4")

interact_indicator_base = switch_block.clone()
interact_indicator_base.shapesize(0.5)
interact_indicator_base.tilt(180)

green_interaction_indicator_base = interact_indicator_base.clone()
green_interaction_indicator_base.color("lawn green")

# Winpad
winpad_char = "!"
winpad = base_block.clone()
winpad.color("green yellow")

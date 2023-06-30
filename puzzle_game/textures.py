import sys
import turtle

# Player
player_char = "@"
player = turtle.Turtle()
player.shape("circle")
player.penup()
player.speed(1)
player.color("yellow")

# Base blocks
base_block = turtle.Turtle()
base_block.shape("square")
base_block.penup()
base_block.speed(0)

base_triangle = base_block.clone()
base_triangle.shape("triangle")

base_circle = base_block.clone()
base_circle.shape("circle")

# Ground
ground_char = "#"
ground_block = base_block.clone()
ground_block.color("white")
ground_block.setposition(500, 500)

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

# Interact-able
platform_char = "~"
platform_block = base_block.clone()
platform_block.shapesize(0.5)
platform_block.color("white")

lift_char = "="
lift_block_a = platform_block.clone()
lift_block_a.shapesize(0.3)
lift_block_a.color("cyan")

switch_char = "^"
switch_block = base_triangle.clone()
switch_block.color("cyan")
switch_block.tilt(90)
switch_block.setposition(500, 470)

switch_block_fancy = switch_block.clone()

switch_block_fancy.shapesize(.5)
switch_block_fancy.color("cyan4")

timer_switch_char = '"'
timer_switch_block = switch_block.clone()
timer_progress_block = base_block.clone()
timer_progress_block.color("cyan")
timer_progress_block.setposition(600, 600)

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

tp_block_blue = base_circle.clone()
tp_block_blue.color("cyan")
tp_block_blue.setposition(500, 450)

tp_block_dull_blue = base_circle.clone()
tp_block_dull_blue.color("cyan4")
tp_block_dull_blue.setposition(520, 450)

interact_indicator = switch_block.clone()
interact_indicator.shapesize(0.5)
interact_indicator.tilt(180)

# Winpad
winpad_char = "!"
winpad_block = base_block.clone()
winpad_block.color("lime")

winpad_interact_indicator = interact_indicator.clone()
winpad_interact_indicator.color("lime")

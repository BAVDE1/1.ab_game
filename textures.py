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
dark_grey_block.color("grey5")

grey_char = ":"
grey_block = base_block.clone()
grey_block.setposition(520, 500)
grey_block.color("grey10")

fancy_ground_char = "*"
fancy_block = base_block.clone()
fancy_block.setposition(500, 500)
fancy_block.shapesize(.5)
fancy_block.color("black")

# Interact-able
# Green door
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

# Red door
red_door_block = green_door_block.clone()
red_door_block.color("red")

red_door_block_a = green_door_block_a.clone()
red_door_block_a.color("dark red")

red_door_block_b = green_door_block_b.clone()
red_door_block_b.color("red")

red_door_block_c = green_door_block_c.clone()
red_door_block_c.color("red")

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

lift_block_b = base_triangle.clone()
lift_block_b.shapesize(0.6)
lift_block_b.tilt(-90)
lift_block_b.color("cyan")

blue_switch_char = "^"
blue_switch_block = base_triangle.clone()
blue_switch_block.setposition(500, 470)
blue_switch_block.color("cyan")
blue_switch_block.tilt(90)

blue_switch_block_fancy = blue_switch_block.clone()
blue_switch_block_fancy.shapesize(.5)
blue_switch_block_fancy.color("cyan4")

red_switch_char = "~"
red_switch_block = blue_switch_block.clone()
red_switch_block.color("red")

red_switch_block_fancy = blue_switch_block_fancy.clone()
red_switch_block_fancy.color("dark red")

# Timer switch
blue_timer_switch_char = '"'
blue_timer_switch_block = blue_switch_block.clone()
blue_timer_progress_block = base_block.clone()
blue_timer_progress_block.setposition(600, 600)
blue_timer_progress_block.color("cyan")

blue_timer_switch_block_fancy_a = blue_timer_switch_block.clone()
blue_timer_switch_block_fancy_a.shapesize(.5)
blue_timer_switch_block_fancy_a.color("cyan4")

blue_timer_switch_block_fancy_b = blue_timer_switch_block.clone()
blue_timer_switch_block_fancy_b.color("cyan", "white")
blue_timer_switch_block_fancy_b.shape("square")

blue_timer_switch_block_fancy_c = blue_timer_switch_block.clone()
blue_timer_switch_block_fancy_c.shapesize(.5)
blue_timer_switch_block_fancy_c.color("cyan4")
blue_timer_switch_block_fancy_c.tilt(180)

red_timer_switch_char = "'"
red_timer_switch_block = red_switch_block.clone()
red_timer_progress_block = blue_timer_progress_block.clone()
red_timer_progress_block.color("red")

red_timer_switch_block_fancy_a = blue_timer_switch_block_fancy_a.clone()
red_timer_switch_block_fancy_a.color("dark red")

red_timer_switch_block_fancy_b = blue_timer_switch_block_fancy_b.clone()
red_timer_switch_block_fancy_b.color("red", "white")

red_timer_switch_block_fancy_c = blue_timer_switch_block_fancy_c.clone()
red_timer_switch_block_fancy_c.color("dark red")

# Teleporter
tp_block_blue = base_circle.clone()
tp_block_blue.setposition(500, 450)
tp_block_blue.color("cyan")

tp_block_dull_blue = base_circle.clone()
tp_block_dull_blue.setposition(520, 450)
tp_block_dull_blue.color("cyan4")

tp_block_red = tp_block_blue.clone()
tp_block_red.color("red")

tp_block_dull_red = tp_block_dull_blue.clone()
tp_block_dull_red.color("dark red")

interact_indicator_base = blue_switch_block.clone()
interact_indicator_base.shapesize(0.5)
interact_indicator_base.tilt(180)

green_interaction_indicator_base = interact_indicator_base.clone()
green_interaction_indicator_base.color("lawn green")

red_interaction_indicator_base = interact_indicator_base.clone()
red_interaction_indicator_base.color("red")

# Winpad
winpad_char = "!"
winpad = base_block.clone()
winpad.color("green yellow")

import turtle

width = 30
height = 40

ground_char = "#"
player_char = "@"
player = None

lines = []
drawing = False

wind = turtle.Screen()
wind.bgcolor("black")
wind.setup(width=width * 20, height=height * 20)
wind.title("idk")


def draw_ground_cube(pos_w, pos_h):
    obj = turtle.Turtle()
    obj.shape("square")
    obj.penup()
    obj.speed(0)
    obj.setposition(pos_w, pos_h)
    obj.color("white")


def draw_player(pos_w, pos_h):
    global player
    player = turtle.Turtle()
    player.shape("circle")
    player.penup()
    player.speed(0)
    player.setposition(pos_w, pos_h)
    player.color("yellow")


def draw_level():
    if lines:
        line_num = 0
        for line in lines:
            line_num += 1
            chars = list(line)
            char_num = 0
            for char in chars:
                char_num += 1
                if char == ground_char:
                    draw_ground_cube((width / 2 * -20) + (20 * char_num), (height / 2 * 20) - (20 * line_num))
                elif char == player_char:
                    draw_player((width / 2 * -20) + (20 * char_num), (height / 2 * 20) - (20 * line_num))


def read_level():
    with open("levels/level_dat.txt") as file:
        global lines
        global drawing
        lines = [line.rstrip() for line in file]
        drawing = True
        draw_level()
        drawing = False


# Controls
wind.listen()
wind.onkeypress(left, 'Left')
wind.onkeypress(right, 'Right')
wind.onkeypress(space, "space")


# Init
if __name__ == '__main__':
    print("Initialising")
    read_level()

wind.mainloop()

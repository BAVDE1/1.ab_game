import math
import tkinter as tk
from tkinter import simpledialog


# Testing .py file


def print_loop(r):
    # var a starts at 0
    print("--loop--")
    c = ""
    for count in range(r):
        c += str(count)
    print(c)


def border(s, border_char):
    border_string = ""
    for count in range(len(s)):
        border_string += border_char
    print(border_string)


def print_bordered_str(s):
    border(s, "+")
    print(s)
    border(s, "+")


def print_list(li):
    for i in li:
        print(i)


def iterate_through(li):
    print_list(li)
    border(li, "=")
    print_list([len(word) for word in li])

    # Dict
    print("--Dict--")
    di = {'a': 'one', 'b': 'two', 'c': 'three'}
    print_list(di.items())


def zip_and_average(li_a, li_b, li_c):
    print("Zipped:")
    for i in zip(li_a, li_b, li_c):
        print(i)
    print("Averages (of one and two):")
    for a, b in zip(li_a, li_b):
        print("average = ", (a + b) / 2)


# default window values
root = tk.Tk()
root.title("Math operations")
root.geometry('400x400')


def user_math_select():
    if input("Do you want to run calculation operations? [y/n]: ") == "y":
        # var to store the option
        value_ins = tk.StringVar(root)
        value_ins.set("Select an option")

        # options that can be selected
        op_list = ["Addition", "Square", "Cube"]

        choose_op = tk.OptionMenu(root, value_ins, *op_list)
        choose_op.pack()

        def submit():
            if value_ins.get() == op_list[0]:
                root.destroy()
                user_addition()
            elif value_ins.get() == op_list[1]:
                root.destroy()
                user_squared()
            elif value_ins.get() == op_list[2]:
                root.destroy()
                user_cubed()
            else:
                print("Please select an option!")
            return None

        sub_button = tk.Button(root, text="Submit", command=submit)
        sub_button.pack()

        root.mainloop()


def user_addition():
    try:
        a = int(input("First number: "))
        b = int(input("Second number: "))

        print("Product: ", a + b)
    except ValueError:
        print("ERROR: input is not a number!")
        return


def user_squared():
    try:
        a = int(input("Number to square: "))
        print(a, " squared is: ", math.pow(a, 2))
    except ValueError:
        print("ERROR: input is not a number!")
        return


def user_cubed():
    try:
        a = int(input("Number to cube: "))
        print(a, " cubed is: ", math.pow(a, 3))
    except ValueError:
        print("ERROR: input is not a number!")
        return


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # Strings
    print_loop(10)
    print_bordered_str("hello")

    # Lists
    print("--LISTS--")
    words = "hi hello hulo"
    iterate_through(words.split())

    # Zip
    print("--ZIP--")
    one = [10, 15, 12]
    two = [8, 13, 9]
    three = [11, 16, 12]
    zip_and_average(one, two, three)

    # User math
    print("--User Math--")
    user_math_select()

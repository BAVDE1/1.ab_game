import distutils.util
import os

save_file = "save.txt"
sv_lines = []

num_of_levels = len(os.listdir("levels")) - 4


def read_save_file():
    global sv_lines

    with open(save_file) as sv:
        for line in sv:
            line = line.rstrip()
            line = line.replace(" ", "")
            line = line.replace("[", "")
            line = line.replace("]", "")
            sp = line.split(",")
            sv_lines.append([int(sp[0]), distutils.util.strtobool(sp[1])])
    check_integrity()


def is_level_complete(level_num):
    is_complete = False
    for level in sv_lines:
        if level[0] == level_num and level[1]:
            is_complete = True
    return is_complete


def is_level_unlocked(level_num):
    is_unlocked = False
    if level_num == 1 or is_level_complete(level_num - 1):
        is_unlocked = True
    return is_unlocked


def complete_level(level_num):
    for line in sv_lines:
        if line[0] == level_num:
            line[1] = 1

    with open(save_file, "w") as sv:
        for line in sv_lines:
            sv.write("%s\n" % line)


def check_integrity():
    # Check level number, and append
    should_be_num = 0
    for line in sv_lines:
        should_be_num += 1
        if not line[0] == should_be_num:
            line[0] = should_be_num
            print("ERROR appended: changed to: ", should_be_num)

    # Check amount of levels in list, and append
    if not len(sv_lines) == num_of_levels:
        needs = num_of_levels - len(sv_lines)
        for i in range(needs):
            needs = num_of_levels - len(sv_lines)
            sv_lines.append([num_of_levels - (needs - 1), 0])
            print("ERROR appended: added ", needs, " lines")

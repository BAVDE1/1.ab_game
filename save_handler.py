import distutils.util

save_file = "save.txt"
sv_lines = []
amount_of_levels = 6


def read_sv():
    global sv_lines

    with open(save_file) as sv:
        for line in sv:
            line = line.rstrip()
            line = line.replace(" ", "")
            line = line.replace("[", "")
            line = line.replace("]", "")
            num = line.split(",")
            sv_lines.append([int(num[0]), distutils.util.strtobool(num[1])])
    check_integrity()


def is_level_complete(level_num):
    is_complete = False
    for level in sv_lines:
        if level[0] == level_num and level[1]:
            is_complete = True
    return is_complete


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
    if not len(sv_lines) == amount_of_levels:
        needs = amount_of_levels - len(sv_lines)
        for i in range(needs):
            needs = amount_of_levels - len(sv_lines)
            sv_lines.append([amount_of_levels - (needs - 1), 0])
            print("ERROR appended: added ", needs, " lines")

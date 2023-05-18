# exports configurations to tikz code

def export(configs):
    print("\\begin{tikzpicture}")

    current_x = 0
    current_y = 0

    for config in configs:
        draw_single_config(config, current_x, current_y)
        if (current_x < 11):
            current_x += 3
        else:
            current_x = 0
            print("\\end{tikzpicture}")
            print("\\begin{tikzpicture}")

    print("\\end{tikzpicture}")


def draw_single_config(config, x, y):
    print("\\draw (" + str(x) + ", " + str(y) +
          ") rectangle (" + str(x + 2) + ", " + str(y + 2) + ");")
    for line in config.lines:
        print("\\draw (" + str(line.start.x * 2 + x) + ", " + str(line.start.y * 2 + y) +
              ") -- (" + str(line.end.x * 2 + x) + ", " + str(line.end.y * 2 + y) + ");")

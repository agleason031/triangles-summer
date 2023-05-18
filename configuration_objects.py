'''
objects used for creating and storing configurations

c points are labeled 0 to 3 starting at bottom left and moving counterclockwise
sides are labeleed 1 to 4 started at the bottom and moving counterclockwise

point types:
1 = a point
2 = b point
3 = s point
4 = c point
'''
import random


class configuration():
    def __init__(self, n):
        self.n = n
        self.s_points = []
        self.a_points = []
        self.b_points = []
        self.c_points = []
        self.points_on_sides = [[], [], [], []]
        for i in range(4):  # creates 4 corner points for every configuration
            self.c_points.append(c_point(i))
        self.lines = []

    def add_a_point(self, line):
        self.a_points.append(a_point(line))

    def add_b_point(self):
        self.b_points.append(b_point())

    def add_s_point(self, side):
        # pass value 1-4 to indicate which side of the triangle the point lies on
        new_point = s_point(side)
        self.s_points.append(new_point)
        self.points_on_sides[side - 1].append(new_point)

    def add_line(self, start_point, end_point):
        self.lines.append(line(start_point, end_point))

    def duplicate(self):
        dupe = configuration(self.n)
        for s_point in self.s_points:
            dupe.add_s_point(s_point.side)
            dupe.s_points[len(dupe.s_points) - 1].x = s_point.x
            dupe.s_points[len(dupe.s_points) - 1].y = s_point.y
        for b_point in self.b_points:
            dupe.add_b_point()
            dupe.b_points[len(dupe.b_points) - 1].x = b_point.x
            dupe.b_points[len(dupe.b_points) - 1].y = b_point.y
        for a_point in self.a_points:
            dupe.add_a_point(a_point.line)
            dupe.a_points[len(dupe.a_points) - 1].x = a_point.x
            dupe.a_points[len(dupe.a_points) - 1].y = a_point.y
        for line in self.lines:
            dupe.add_line(dupe.find_point_at_coord(line.start.x, line.start.y),
                          dupe.find_point_at_coord(line.end.x, line.end.y))

        # reassigns lines in a points for lines in config
        for a_point in dupe.a_points:
            a_point.line = dupe.lines[find_same_line(dupe, a_point.line)]
            dupe.lines[find_same_line(
                dupe, a_point.line)].a_points.append(a_point)

        return dupe

    # evenly spaces s points for visual clarity
    def adjust_s_points(self):
        for points_on_side in self.points_on_sides:
            for i in range(len(points_on_side)):
                if (points_on_side[0].side == 1 or points_on_side[0].side == 3):  # top or bottom
                    points_on_side[i].x = (i+1)/(len(points_on_side) + 1)
                if (points_on_side[0].side == 2 or points_on_side[0].side == 4):  # left or right
                    points_on_side[i].y = (i+1)/(len(points_on_side) + 1)

        return None

    def adjust_a_points(self):
        points_on_lines = []
        for line in self.lines:
            points_on_lines.append([])
        for a_point in self.a_points:
            points_on_lines[self.lines.index(a_point.line)].append(a_point)
        temps = []
        for j in range(len(self.a_points) + 1):
            temps.append([])
        for i in range(len(points_on_lines)):
            k = find_a_dependency(self.lines[i], 0)
            temps[k].append(points_on_lines[i])
        for temp in temps:
            for line in temp:
                points_on_lines.append(line)

        for points_on_line in points_on_lines:
            points_on_line.sort(key=get_x)
            for i in range(len(points_on_line)):
                points_on_line[i].place_coordinates(
                    (i+1)/(len(points_on_line) + 1))

        return None

    # deletes points and lines depending on a line as well as the lines
    def delete_line(self, line):  # line is passed as index
        objects_to_delete = [
            [], []]  # first list is a points, second is lines; lines are indexs, points are objects
        objects_to_delete = delete_dependant_points(
            self, line, objects_to_delete)

        objects_to_delete[0].append(line)
        objects_to_delete[0].sort(reverse=True)

        for line in objects_to_delete[0]:
            self.lines.pop(line)
        for a_point in objects_to_delete[1]:
            self.a_points.remove(a_point)

    def find_point_at_coord(self, x, y):
        if (x == 0 or y == 0 or x == 1 or y == 1):
            for corner in self.c_points:
                if (corner.x == x and corner.y == y):
                    return corner
            for s_point in self.s_points:
                if (s_point.x == x and s_point.y == y):
                    return s_point

        for a_point in self.a_points:
            if (a_point.x == x and a_point.y == y):
                return a_point

        for b_point in self.b_points:
            if (b_point.x == x and b_point.y == y):
                return b_point


class c_point():
    def __init__(self, corner):
        self.corner = corner
        self.type = 4
        # defines x and y coords of corner
        if (corner == 0):
            self.x = 0
            self.y = 1
        elif(corner == 1):
            self.x = 1
            self.y = 1
        elif (corner == 2):
            self.x = 1
            self.y = 0
        elif (corner == 3):
            self.x = 0
            self.y = 0

    def __eq__(self, point2):
        if (isinstance(point2, c_point)):
            if (point2.x == self.x and point2.y == self.y):
                return True
        return False


class s_point():
    def __init__(self, side):
        self.side = side
        self.type = 3
        if (side == 1 or side == 3):  # generates random coordinates along side for line, coords are given from 0 to 1 starting from top left
            self.x = random.random()
            if (side == 3):
                self.y = 0
            else:
                self.y = 1
        if (side == 2 or side == 4):
            self.y = random.random()
            if (side == 4):
                self.x = 0
            else:
                self.x = 1

    def __eq__(self, point2):
        if (isinstance(point2, s_point)):
            if (point2.x == self.x and point2.y == self.y):
                return True
        return False


# can probably clean this up at some point
class a_point():
    def __init__(self, line):
        self.line = line
        line.a_points.append(self)
        self.type = 1

        self.place_coordinates(random.random())

    def place_coordinates(self, param):
        if (min(self.line.start.x, self.line.end.x) == self.line.start.x):
            left_point = self.line.start
            right_point = self.line.end
        else:
            left_point = self.line.end
            right_point = self.line.start
        x_length = right_point.x - left_point.x
        y_length = right_point.y - left_point.y

        self.x = (param * x_length) + left_point.x
        if (x_length != 0):
            slope = y_length / x_length
            temp = (self.x - min(self.line.start.x, self.line.end.x)) * slope
            if (slope < 0):
                self.y = max(self.line.start.y, self.line.end.y) - abs(temp)
            else:
                self.y = min(self.line.start.y, self.line.end.y) + abs(temp)
        else:  # vertical line
            self.y = abs((y_length / 2)) + \
                min(left_point.y, right_point.y)

    def __eq__(self, point2):
        if (isinstance(point2, a_point)):
            if (point2.x == self.x and point2.y == self.y):
                return True
        return False


class b_point():
    def __init__(self):
        self.type = 2
        self.x = random.random()
        self.y = random.random()

    def __eq__(self, point2):
        if (isinstance(point2, b_point)):
            if (point2.x == self.x and point2.y == self.y):
                return True
        return False


class line():
    def __init__(self, start_point, end_point):
        self.start = start_point
        self.end = end_point
        self.a_points = []

    def __eq__(self, line2):
        if isinstance(line2, line):
            A = self.start
            B = self.end
            C = line2.start
            D = line2.end
            if (((A == C) and (B == D)) or ((B == C) and (A == D))):
                return True

        return False


# object for storing num of s points on each side
class s_point_case():
    def __init__(self, side1, side2, side3, side4):
        self.side1 = side1
        self.side2 = side2
        self.side3 = side3
        self.side4 = side4


def delete_dependant_points(config, line, objects_to_delete):
    if (len(config.a_points) != 0):
        points_on_line = []
        for a_point in config.a_points:
            if (a_point.line == config.lines[line]):
                points_on_line.append(a_point)

        for i in range(len(config.lines)):
            if (config.lines[i].start.type == 1):
                if (points_on_line.count(config.lines[i].start) > 0):
                    delete_dependant_points(config, i, objects_to_delete)
                    objects_to_delete[0].append(i)
            if (config.lines[i].end.type == 1):
                if (points_on_line.count(config.lines[i].end) > 0):
                    delete_dependant_points(config, i, objects_to_delete)
                    objects_to_delete[0].append(i)

        for a_point in points_on_line:
            objects_to_delete[1].append(a_point)

    return objects_to_delete


# looks for existing like in configuration, if it finds it it returns index of line in config's line list
def find_same_line(config, line):
    for config_line in config.lines:
        if (config_line == line):
            return config.lines.index(config_line)
    return -1


def get_x(e):
    return e.x


def find_a_dependency(line, k):
    if (line.start.type == 1):  # is a point
        return find_a_dependency(line.start.line, k + 1)
    if (line.end.type == 1):
        return find_a_dependency(line.end, k + 1)

    return k

# adjustment of a points is still broken

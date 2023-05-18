import configuration_objects as obj
import math
from itertools import combinations
import display as disp


def create_configs(case):
    current_configs = [obj.configuration(case.n)]
    if (case.s > 0):
        current_configs = place_s_points(case.s, current_configs[0])
    # s lines also does diagonals
    current_configs = place_s_lines(current_configs)
    new_configs = []
    for config in current_configs:
        new_configs.extend(remove_intersection_v2(config, case.s))
    current_configs = remove_duplicate_configs(new_configs)
    # end s point manipulation

    # placing a points
    if (case.a > 0):
        new_configs = []
        for config in current_configs:
            temp_configs = (place_a_points(case.a, config))
            for temp in temp_configs:
                new_configs.append(temp)
        current_configs = new_configs

        new_configs = []
        for config in current_configs:
            temp_configs = (remove_intersection(config, case.s + case.a))
            for temp in temp_configs:
                new_configs.append(temp)
        current_configs = remove_duplicate_configs(new_configs)

    if (case.b > 0):
        current_configs = place_b_points(case.b, current_configs, case.n, case)
        current_configs = remove_duplicate_configs(current_configs)

    return current_configs


def place_s_points(s_num, config):
    new_configs = []

    cases = s_point_case_solver(s_num)

    # 1 side
    new_configs.append(config.duplicate())
    for i in range(cases[0][0].side1):
        new_configs[0].add_s_point(1)

    # 2 sides
    two_sides = cases[1]
    for case in two_sides:
        # two configs, one when points are on adjacent sides, one on opposing sides
        new_configs.append(config.duplicate())
        new_configs.append(config.duplicate())
        for i in range(case.side1):
            new_configs[len(new_configs) - 1].add_s_point(1)
            new_configs[len(new_configs) - 2].add_s_point(1)

        for i in range(case.side2):
            new_configs[len(new_configs) - 1].add_s_point(2)
            new_configs[len(new_configs) - 2].add_s_point(3)

    # 3 sides
    three_sides = cases[2]
    for case in three_sides:
        if (case.side2 != case.side3):  # order can be switched
            new_configs.append(config.duplicate())
            new_configs.append(config.duplicate())
            for i in range(case.side1):
                new_configs[len(new_configs) - 1].add_s_point(1)
                new_configs[len(new_configs) - 2].add_s_point(1)

            for i in range(case.side2):
                new_configs[len(new_configs) - 1].add_s_point(2)
                new_configs[len(new_configs) - 2].add_s_point(3)

            for i in range(case.side3):
                new_configs[len(new_configs) - 1].add_s_point(3)
                new_configs[len(new_configs) - 2].add_s_point(2)

        else:  # 2 and 3 are same so order doesn't matter
            new_configs.append(config.duplicate())
            for i in range(case.side1):
                new_configs[len(new_configs) - 1].add_s_point(1)

            for i in range(case.side2):
                new_configs[len(new_configs) - 1].add_s_point(2)

            for i in range(case.side3):
                new_configs[len(new_configs) - 1].add_s_point(3)

        # all sides don't have the same num, greater num can be placed in middle of arrangement
        if (case.side1 != case.side2):
            new_configs.append(config.duplicate())
            for i in range(case.side1):
                new_configs[len(new_configs) - 1].add_s_point(1)

            for i in range(case.side2):
                new_configs[len(new_configs) - 1].add_s_point(2)

            for i in range(case.side3):
                new_configs[len(new_configs) - 1].add_s_point(4)

    # 4 sides
    four_sides = cases[3]
    for case in four_sides:
        if (case.side3 != case.side4):  # order can be switched
            new_configs.append(config.duplicate())
            new_configs.append(config.duplicate())
            for i in range(case.side1):
                new_configs[len(new_configs) - 1].add_s_point(1)
                new_configs[len(new_configs) - 2].add_s_point(1)

            for i in range(case.side2):
                new_configs[len(new_configs) - 1].add_s_point(2)
                new_configs[len(new_configs) - 2].add_s_point(2)

            for i in range(case.side3):
                new_configs[len(new_configs) - 1].add_s_point(3)
                new_configs[len(new_configs) - 2].add_s_point(4)

            for i in range(case.side4):
                new_configs[len(new_configs) - 1].add_s_point(4)
                new_configs[len(new_configs) - 2].add_s_point(3)

        else:  # order can't be switched
            new_configs.append(config.duplicate())
            for i in range(case.side1):
                new_configs[len(new_configs) - 1].add_s_point(1)

            for i in range(case.side2):
                new_configs[len(new_configs) - 1].add_s_point(2)

            for i in range(case.side3):
                new_configs[len(new_configs) - 1].add_s_point(3)

            for i in range(case.side4):
                new_configs[len(new_configs) - 1].add_s_point(4)

        if (case.side2 != case.side3):  # can have side 2 opposing side 1
            new_configs.append(config.duplicate())
            for i in range(case.side1):
                new_configs[len(new_configs) - 1].add_s_point(1)

            for i in range(case.side2):
                new_configs[len(new_configs) - 1].add_s_point(3)

            for i in range(case.side3):
                new_configs[len(new_configs) - 1].add_s_point(2)

            for i in range(case.side4):
                new_configs[len(new_configs) - 1].add_s_point(4)

    for config in new_configs:
        config.adjust_s_points()

    return new_configs


def place_a_points(a_num, config):
    point_configs = []
    for i in range(len(config.lines)):
        point_configs.append(config.duplicate())
        point_configs[i].add_a_point(point_configs[i].lines[i])

    new_configs = []
    for config in point_configs:
        a_point = config.a_points[len(config.a_points) - 1]
        # a points to corners
        possible_end_points = []
        for corner in config.c_points:  # possible c points are corners where line the a point is on does not end
            if (is_same_point(a_point.line.start, corner) == False and is_same_point(a_point.line.end, corner) == False):
                possible_end_points.append(corner)
        for s_point in config.s_points:
            if (is_same_point(a_point.line.start, s_point) == False and is_same_point(a_point.line.end, s_point) == False):
                possible_end_points.append(s_point)

        # separates possible points based on which side of the line they are on
        same_side = []
        opposide_side = []
        same_side.append(possible_end_points[0])
        for i in range(len(possible_end_points) - 1):
            if (ccw(a_point.line.start, a_point.line.end, same_side[0]) == ccw(a_point.line.start, a_point.line.end, possible_end_points[i + 1])):
                same_side.append(possible_end_points[i + 1])
            else:
                opposide_side.append(possible_end_points[i + 1])

        # makes two configs, one each with all possible lines on that side
        new_configs.append(config.duplicate())
        for point in same_side:
            new_configs[len(new_configs) - 1].add_line(a_point, point)
        new_configs.append(config.duplicate())
        for point in opposide_side:
            new_configs[len(new_configs) - 1].add_line(a_point, point)

    # recursion
    if (len(new_configs[0].a_points) != a_num):
        even_newer_configs = []
        for config in new_configs:
            temp_configs = place_a_points(a_num, config)
            for temp in temp_configs:
                even_newer_configs.append(temp)
        new_configs = even_newer_configs

    return new_configs


def place_b_points(b_num, configs, n, case):
    new_configs = []

    # first other points configs
    for config in configs:
        triangles = get_triangles(config, n - (2 * b_num))
        for triangle in triangles:
            temp = config.duplicate()
            centroid_x = (triangle[0].x + triangle[1].x + triangle[2].x) / 3
            centroid_y = (triangle[0].y + triangle[1].y + triangle[2].y) / 3

            temp.add_b_point()
            temp.b_points[len(temp.b_points) - 1].x = centroid_x
            temp.b_points[len(temp.b_points) - 1].y = centroid_y
            temp.add_line(temp.b_points[len(temp.b_points) - 1], triangle[0])
            temp.add_line(temp.b_points[len(temp.b_points) - 1], triangle[1])
            temp.add_line(temp.b_points[len(temp.b_points) - 1], triangle[2])

            # adds lines to unused corners and then removes intersection
            for corner in config.c_points:
                if (not(corner in triangle)):
                    temp.add_line(
                        temp.b_points[len(temp.b_points) - 1], corner)
            temp_configs = remove_intersection_v2(temp, n - b_num)
            new_configs.extend(temp_configs)

    # first b points configs
    # tailored for n=5
    if (case.a > 0):
        temp = obj.configuration(n)
        centroid_x = 2/3
        centroid_y = 2/3

        temp.add_line(temp.c_points[0], temp.c_points[2])
        temp.add_b_point()
        temp.b_points[len(temp.b_points) - 1].x = centroid_x
        temp.b_points[len(temp.b_points) - 1].y = centroid_y
        temp.add_line(temp.b_points[len(temp.b_points) - 1], temp.c_points[0])
        temp.add_line(temp.b_points[len(temp.b_points) - 1], temp.c_points[1])
        temp.add_line(temp.b_points[len(temp.b_points) - 1], temp.c_points[2])

        temp1 = obj.configuration(n)
        temp1.add_b_point()
        temp1.b_points[len(temp1.b_points) - 1].x = 0.5
        temp1.b_points[len(temp1.b_points) - 1].y = 0.5
        temp1.add_line(
            temp1.b_points[len(temp1.b_points) - 1], temp1.c_points[0])
        temp1.add_line(
            temp1.b_points[len(temp1.b_points) - 1], temp1.c_points[1])
        temp1.add_line(
            temp1.b_points[len(temp1.b_points) - 1], temp1.c_points[2])
        temp1.add_line(
            temp1.b_points[len(temp1.b_points) - 1], temp1.c_points[3])

        base_configs = [temp, temp1]
        current_configs = []
        for config in base_configs:
            current_configs.extend(place_a_points(case.a, config))
        output_configs = []
        for config in current_configs:
            temp_configs = (remove_intersection(config, n - 1))
            output_configs.extend(temp_configs)
        new_configs.extend(remove_duplicate_configs(output_configs))

    return new_configs


def get_triangles(config, n):
    triangles = []

    new_triangle, temp_point = walk_edge(config.c_points[0], config)
    triangles.append(new_triangle)

    while len(triangles) < n:
        new_triangle, temp_point = walk_edge(temp_point, config)
        triangles.append(new_triangle)

    return triangles


# walks around edge to generate triangles, keep in mind wraparound issues for later
'''
doesn't work for triangles that don't lie on the edge
'''


def walk_edge(start_point, config):
    triangle = []
    last_side_point = None
    start_line = None

    # find side to walk on
    triangle.append(start_point)
    if (start_point.type == 3):  # is s_point
        start_line = start_point.side

        # removes starting line value to prevent confusion
        points_on_start = config.points_on_sides[start_line - 1]
        points_on_start.remove(start_point)
    if (start_point.type == 4):  # is c point
        start_line = start_point.corner + 1
        points_on_start = config.points_on_sides[start_line - 1]

    # if there are points on starting side find the first one
    if (len(points_on_start) > 0):
        least_x = 1
        least_y = 0
        first_point = None
        if (start_line == 1 or start_line == 3):  # defined by x coordinate
            for point in points_on_start:
                if (point.x < least_x):
                    least_x = point.x  # point is closer to the start point
                    first_point = point
        else:
            # defined by y coordinate
            for point in points_on_start:
                if (point.y > least_y):
                    least_y = point.y  # point is closer to the start point
                    first_point = point
        # next point is the first point along side
        triangle.append(first_point)
        last_side_point = first_point

        triangle = find_finishing_line(config, triangle, start_line)
    else:  # no points on starting side
        # ending corner is next point
        triangle.append(config.c_points[start_line % 4])

        triangle = find_finishing_line(config, triangle, start_line)
        if (len(triangle) < 3):
            # if side has lines
            if (len(config.points_on_sides[start_line]) > 0):
                least_x = 1
                least_y = 0
                first_point = None
                if (start_line == 1 or start_line == 3):  # defined by x coordinate
                    for point in config.points_on_sides[start_line]:
                        if (point.x < least_x):
                            least_x = point.x  # point is closer to the start point
                            first_point = point
                else:
                    # defined by y coordinate
                    for point in config.points_on_sides[start_line]:
                        if (point.y > least_y):
                            least_y = point.y  # point is closer to the start point
                            first_point = point
                # last point is the first point along side
                triangle.append(first_point)
                last_side_point = first_point
            else:
                # last point is next corner
                triangle.append(config.c_points[(start_line + 1) % 4])
                last_side_point = triangle[2]
        else:
            last_side_point = triangle[1]

    return triangle, last_side_point


def find_finishing_line(config, triangle, start_line):
    # find 3rd point by finding connecting lines
    for line in config.lines:
        # line starts on second point in triangle
        if (line.start == triangle[1]):
            temp_line = obj.line(line.end, triangle[0])
            if (same_line_exists(config, temp_line)):  # lines completing the triangle exist
                triangle.append(line.end)
                break
            if (temp_line.start.type == 4 and temp_line.end.type == 4):  # both are corners
                for point in line.a_points:  # doesn't check for first point
                    possible_line = obj.line(point, triangle[0])
                    if (same_line_exists(config, possible_line)):
                        triangle.append(point)
                        break
                if (((temp_line.start.corner + 1) % 4 == temp_line.end.corner) or ((temp_line.end.corner + 1) % 4 == temp_line.start.corner)):  # adjacent corners
                    # no points on line between corners
                    if (len(config.points_on_sides[(start_line - 2) % 4]) == 0):
                        triangle.append(line.end)
                        break
            if (line.end.type == 1):  # line ends on a point
                # line the a point is on connects to start
                if (line.end.line.start == triangle[0] or line.end.line.end == triangle[0]):
                    triangle.append(line.end)
                    break

            '''
            need to add for when there is an s point on side
            '''
        # line ends on second point in triangle
        elif (line.end == triangle[1]):
            temp_line = obj.line(line.start, triangle[0])
            if (same_line_exists(config, temp_line)):  # lines completing the triangle exist
                triangle.append(line.start)
                break
            if (temp_line.start.type == 4 and temp_line.end.type == 4):  # both are corners
                for point in line.a_points:
                    possible_line = obj.line(point, triangle[0])
                    if (same_line_exists(config, possible_line)):
                        triangle.append(point)
                        break
                if (((temp_line.start.corner + 1) % 4 == temp_line.end.corner) or ((temp_line.end.corner + 1) % 4 == temp_line.start.corner)):  # adjacent corners
                    # no points on line between corners
                    if (len(config.points_on_sides[(start_line - 2) % 4]) == 0):
                        triangle.append(line.start)
                        break
            if (line.start.type == 1):  # line ends on a point
                # line the a point is on connects to start
                if (line.start.line.start == triangle[0] or line.start.line.end == triangle[0]):
                    triangle.append(line.start)
                    break

    return triangle


def place_s_lines(current_configs):
    for config in current_configs:
        # drawing all lines to corners
        for corner in config.c_points:
            for i in range(len(config.s_points)):
                # stops generating lines along edge of square
                if (corner.x != config.s_points[i].x and corner.y != config.s_points[i].y):
                    config.add_line(corner, config.s_points[i])

        # always drawns one diagonal
        config.add_line(config.c_points[0], config.c_points[2])

        # only drawns second diagonal if there is no reflectional symmetry over vertical line
        side2 = 0
        side4 = 0
        for s_point in config.s_points:
            if (s_point.side == 2):
                side2 += 1
            if (s_point.side == 4):
                side4 += 1
        if (side2 != side4):
            config.add_line(config.c_points[1], config.c_points[3])

        # drawing s point to s point lines
        s_pairs = list(combinations(config.s_points, 2))

        for pair in s_pairs:
            # makes sure they aren't on the same side so line is drawn through edge
            if (pair[0].side != pair[1].side):
                config.add_line(pair[0], pair[1])

    return current_configs


def remove_intersection(config, s):
    new_configs = []

    line_pairs = list(combinations(config.lines, 2))

    intersections = []
    for line_pair in line_pairs:  # check for each pair of lines if they intersect
        if (intersect(line_pair[0], line_pair[1])):
            intersections.append(line_pair)

    for intersection in intersections:
        # creates dupe configuration and then removes one line from original and other from dupe
        temp_config1 = config.duplicate()
        temp_config2 = config.duplicate()
        line1 = find_same_line(temp_config1, intersection[0])
        line2 = find_same_line(temp_config2, intersection[1])
        temp_config1.delete_line(line1)
        temp_config2.delete_line(line2)
        new_configs.append(temp_config1)
        new_configs.append(temp_config2)

    if (len(intersections) == 0):
        new_configs.append(config)
    else:
        new_configs = delete_simple_cases(new_configs, s)
        # possibly remove duplicates

        even_newer_configs = []
        for config in new_configs:
            temp_configs = remove_intersection(config, s)
            for temp in temp_configs:
                even_newer_configs.append(temp)
        new_configs = even_newer_configs

    return new_configs


# second version of formula
def remove_intersection_v2(config, s):
    new_configs = []

    line_pairs = list(combinations(config.lines, 2))

    intersections = []
    for line_pair in line_pairs:  # check for each pair of lines if they intersect
        if (intersect(line_pair[0], line_pair[1])):
            intersections.append(line_pair)

    # generates a list of possible variations of intersections to remove
    n = len(intersections)
    base_case = [None] * n
    config_cases = []
    gen_binary_strings(n, base_case, 0, config_cases)

    # creates new config for each case in above list
    for config_case in config_cases:
        temp_config = config.duplicate()
        for i in range(n):
            line = find_same_line(
                temp_config, intersections[i][config_case[i]])
            if (line != -1):  # line hasn't already been deleted
                temp_config.delete_line(line)
        new_configs.append(temp_config)

    new_configs = delete_simple_cases(new_configs, s)

    return new_configs


# returns all cases for where to place s points
def s_point_case_solver(s_num):
    one_side_cases = []
    two_side_cases = []
    three_side_cases = []
    four_side_cases = []

    # all on one side
    one_side_cases.append(obj.s_point_case(s_num, 0, 0, 0))

    # two sides
    if (s_num > 1):
        for i in range(math.floor(s_num / 2)):
            two_side_cases.append(obj.s_point_case(s_num - i - 1, i + 1, 0, 0))

    # three sides
    if (s_num > 2):
        for i in range(math.ceil(s_num / 3), s_num - 1):
            for j in range(math.floor((s_num - i) / 2)):
                if (s_num - i - j - 1 <= i):
                    three_side_cases.append(obj.s_point_case(
                        i, s_num - i - j - 1, j + 1, 0))

    # four sides
    if (s_num > 4):
        for i in range(math.ceil(s_num / 4), s_num - 2):
            for j in range(math.floor((s_num - i) / 3), s_num - i - 1):
                for k in range(math.floor((s_num - i - j) / 2)):
                    if (s_num - i - j - k - 1 <= j and j <= i):
                        four_side_cases.append(obj.s_point_case(
                            i, j, s_num - i - j - k - 1, k + 1))

    cases = [one_side_cases, two_side_cases, three_side_cases, four_side_cases]

    return cases


# removes cases where too many lines were removed
def delete_simple_cases(current_configs, s):
    new_configs = []
    for config in current_configs:
        if (len(config.lines) >= (s + 1)):
            new_configs.append(config)

    return new_configs


# removes configurations that are the exact same as others
def remove_duplicate_configs(current_configs):
    unique_configs = []

    for config in current_configs:
        if (len(unique_configs) == 0):  # first configuration is always unique
            unique_configs.append(config)
        else:
            config_is_unique = False
            for unique in unique_configs:  # otherwise compare to each unique config and if it is different from each one add to unique
                if (compare(config, unique) == True):
                    config_is_unique = True

            if (config_is_unique == False):
                unique_configs.append(config)

    return unique_configs


# checks if two configs are identical, if they are then returns true, otherwise returns false
def compare(config1, config2):
    # if they don't have the same number of elements then they are not equal, probably useless but might eliminate simple differences without adding computational complexity of line comparison
    if (len(config1.lines) != len(config2.lines)):
        return False
    if (len(config1.a_points) != len(config2.a_points)):
        return False
    if (len(config1.b_points) != len(config2.b_points)):
        return False
    if (len(config1.s_points) != len(config2.s_points)):
        return False

    # if all lines don't have a match then they are not equal
    for line1 in config1.lines:
        line_match = same_line_exists(config2, line1)
        if (line_match == False):
            return False

    return True


# looks for existing like in configuration, if it finds it it returns index of line in config's line list
def find_same_line(config, line):
    for i in range(len(config.lines)):
        if ((is_same_point(config.lines[i].start, line.start) and is_same_point(config.lines[i].end, line.end)) or (is_same_point(config.lines[i].end, line.start) and is_same_point(config.lines[i].start, line.end))):
            return i
    return -1


# same as find_same_line but returns bool of whether such a line exists or not
def same_line_exists(config, line):
    for i in range(len(config.lines)):
        A = config.lines[i].start
        B = config.lines[i].end
        C = line.start
        D = line.end
        if ((is_same_point(A, C) and is_same_point(B, D)) or (is_same_point(B, C) and is_same_point(A, D))):
            return True
    return False


def ccw(A, B, C):
    return (C.y-A.y) * (B.x-A.x) > (B.y-A.y) * (C.x-A.x)


def intersect(line1, line2):  # not sure how this deals with colineararity
    A = line1.start
    B = line1.end
    C = line2.start
    D = line2.end

    temp = ccw(A, C, D) != ccw(B, C, D) and ccw(A, B, C) != ccw(A, B, D)
    if (temp == True):  # checks if the intersection is the start or end of lines, note: this may break with internal points
        if (is_same_point(A, C) or is_same_point(A, D) or is_same_point(B, C) or is_same_point(B, D)):
            temp = False

        # they don't intersect because one line ends on an a point on the other line
        if (A.type == 1):
            if (A.line == line2):
                temp = False
        if (B.type == 1):
            if (B.line == line2):
                temp = False

        if (C.type == 1):
            if (C.line == line1):
                temp = False
        if (D.type == 1):
            if (D.line == line1):
                temp = False

    return temp


def is_same_point(A, B):
    return (A.x == B.x and A.y == B.y)


def gen_binary_strings(n, arr, i, config_cases):
    if (i == n):                    # depth reached
        new_entry = []
        for j in range(0, n):
            new_entry.append(arr[j])
        config_cases.append(new_entry)
        return

    arr[i] = 0
    gen_binary_strings(n, arr, i+1, config_cases)

    arr[i] = 1
    gen_binary_strings(n, arr, i+1, config_cases)


'''
def check_reflectional_symmetry(config1, config2):
    # add vertical and horizontal symmtry later, this is just structural right now
    return diagonal_symmetry(config1, config2)
'''


'''
def diagonal_symmetry(config1, config2):
    # config reflected over bottom left top right diagonal
    diagonal1 = obj.configuration(config1.n)
    diagonal1_points = {}
    # config reflected over top left bottom right diagonal
    diagonal2 = obj.configuration(config1.n)
    diagonal2_points = {}
    for s_point in config1.s_points:
        match (s_point.side):
            case 1:
                diagonal1.add_s_point(4)
                diagonal1.s_points[len(
                    diagonal1.s_points) - 1].y = 1 - s_point.x
                diagonal2.add_s_point(2)
                diagonal2.s_points[len(
                    diagonal2.s_points) - 1].y = s_point.x
            case 2:
                diagonal1.add_s_point(3)
                diagonal1.s_points[len(
                    diagonal1.s_points) - 1].x = 1 - s_point.y
                diagonal2.add_s_point(1)
                diagonal2.s_points[len(
                    diagonal2.s_points) - 1].x = s_point.y
            case 3:
                diagonal1.add_s_point(2)
                diagonal1.s_points[len(
                    diagonal1.s_points) - 1].y = 1 - s_point.x
                diagonal2.add_s_point(4)
                diagonal2.s_points[len(
                    diagonal2.s_points) - 1].y = s_point.x
            case 4:
                diagonal1.add_s_point(1)
                diagonal1.s_points[len(
                    diagonal1.s_points) - 1].x = 1 - s_point.y
                diagonal2.add_s_point(3)
                diagonal2.s_points[len(
                    diagonal2.s_points) - 1].y = s_point.x

        diagonal1_points[s_point] = diagonal1.s_points[len(
            diagonal1.s_points) - 1]
        diagonal2_points[s_point] = diagonal1.s_points[len(
            diagonal2.s_points) - 1]

    for corner in config1.c_points:  # add corners to dicts
        match (corner.corner):
            case 0:
                diagonal1_points[corner] = diagonal1.c_points[0]
                diagonal2_points[corner] = diagonal2.c_points[2]
            case 1:
                diagonal1_points[corner] = diagonal1.c_points[3]
                diagonal2_points[corner] = diagonal2.c_points[1]
            case 2:
                diagonal1_points[corner] = diagonal1.c_points[2]
                diagonal2_points[corner] = diagonal2.c_points[0]
            case 3:
                diagonal1_points[corner] = diagonal1.c_points[1]
                diagonal2_points[corner] = diagonal2.c_points[3]

    for a_point in config1.a_points:
        diagonal1.add_a_point(a_point.line)
        diagonal1.a_points[len(diagonal1.a_points) - 1].x = a_point.x
        diagonal1.a_points[len(diagonal1.a_points) - 1].y = a_point.y
        diagonal1_points[a_point] = diagonal1.a_points[len(
            diagonal1.a_points) - 1]

        diagonal2.add_a_point(a_point.line)
        diagonal2.a_points[len(diagonal2.a_points) - 1].x = a_point.x
        diagonal2.a_points[len(diagonal2.a_points) - 1].y = a_point.y
        diagonal1_points[a_point] = diagonal2.a_points[len(
            diagonal2.a_points) - 1]

    for line in config1.lines:
        diagonal1.add_line(
            diagonal1_points[line.start], diagonal1_points[line.end])
        diagonal2.add_line(
            diagonal2_points[line.start], diagonal2_points[line.start])

    if (compare(config2, diagonal1) or compare(config2, diagonal2)):
        return True
    else:
        return False
'''

# write function for each possible transformation that keeps identical
# fix a_point cheat in diagonal reflections

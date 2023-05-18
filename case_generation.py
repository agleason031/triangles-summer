import math


class solution:
    def __init__(self, n, a, b, s):
        self.n = n
        self.a = a
        self.b = b
        self.s = s


def case_solver(n):
    solution_set = []
    for a in range(n):
        for s in range(n - a):
            b = b_solver(n, a, s)
            if (b >= 0 and check_working_solution(n, a, b, s)):
                solution_set.append(solution(n, a, b, s))

    return solution_set


def print_solutions(solution_set):
    print("Listed in form (a, b, s)")
    for i in solution_set:
        string = "(" + str(i.a) + ", " + str(i.b) + ", " + str(i.s) + ")"
        print(string)


def check_working_solution(n, a, b, s):
    if (n == (a + (2 * b) + s) + 2):
        return True
    else:
        return False


def a_solver(n, b, s):
    return(n - s - (2 * b) - 2)


def s_solver(n, a, b):
    return(n - a - (2 * b) - 2)


def b_solver(n, a, s):
    return(math.floor((n - s - a - 2)/2))

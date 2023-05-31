import case_generation as gen
import configuration_objects as obj
import config_generation as conf
import display
import export

# full functionality
'''
configs = []
cases = gen.case_solver(4)
for case in cases:
    configs.append(conf.create_configs(case))

for i in configs:
    for config in i:
        display.show_config(config)
'''

# independent case testing
case1 = gen.solution(5, 3, 0, 0)

configs = conf.create_configs(case1)

print(len(configs))
for config in configs:
    config.adjust_a_points()
    display.show_config(config)
export.export(configs)

'''
arrange1 = obj.configuration(4)
arrange1.add_line(arrange1.c_points[0], arrange1.c_points[2])
arrange1.add_a_point(arrange1.lines[0])
arrange1.add_line(arrange1.a_points[0], arrange1.c_points[0])
arrange1.add_line(arrange1.a_points[0], arrange1.c_points[1])

print(len(arrange1.lines))
configs = conf.remove_intersection(arrange1, 1)
print(len(arrange1.lines))

print(len(configs))
for config in configs:
    display.show_config(config)
'''

"""
four_combos = gen.case_solver(4)
gen.print_solutions(four_combos)
"""

'''
current state:
all nums of s points
nums of a points < 3, would mostly work for >= 3 but don't have a point loops
b points work for 1 b and 1 of either s or a
'''

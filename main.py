
import math
import numpy as np
import pygame as pg

link1_length = 400
link2_length = 400

origin = [0, 0]

steps = 1000
theta_1 = np.linspace(math.radians(0), math.radians(180), steps)
theta_2 = np.linspace(math.radians(0), math.radians(180), steps)


def end_effector_x(angle1, angle2):
    return int(link1_length * math.cos(angle1) + link2_length * math.cos(angle1 + angle2))


def end_effector_y(angle1, angle2):
    return int(link1_length * math.sin(angle1) + link2_length * math.sin(angle1 + angle2))


# Returns a list of every single combination of angles.
# Amount of possible angles is dictated by the angle limit and step size
def append_angles_to_list(angle1, angle2):
    _angle_list = []
    for x in range(0, len(angle1)):
        _temp_angle_list = []
        for y in range(0, len(angle2)):
            _temp_angle_list.append([math.degrees(angle1[x]), math.degrees(angle2[y])])
        _angle_list.append(_temp_angle_list)
    return _angle_list


angle_list = append_angles_to_list(theta_1, theta_2)


def solve_analytical_ik():
    _pos_list = []
    for x in range(0, steps):
        _temp_pos_list = []
        for y in range(0, steps):
            x_pos = end_effector_x(theta_1[x], theta_2[y])
            y_pos = end_effector_y(theta_1[x], theta_2[y])
            _temp_pos_list.append((x_pos, y_pos))
        _pos_list.append(_temp_pos_list)
    return _pos_list


pos_list = solve_analytical_ik()


def match_point_with_angle(end_eff_x, end_eff_y):
    for x in range(0, len(pos_list)):
        for y in range(0, len(pos_list[x])):
            if pos_list[x][y][0] == end_eff_x and pos_list[x][y][1] == end_eff_y:
                # print(x,y)
                # print("I FOUND A MATCH")
                return [x, y]


def rotate_vector(length, angle):
    rad_angle = math.radians(angle)
    return [length * math.cos(rad_angle), length * math.sin(rad_angle)]


pg.init()
size = width, height = pg.display.Info().current_w, pg.display.Info().current_h
screen = pg.display.set_mode(size)

white = 255, 255, 255
black = 0, 0, 0
blue = 0, 0, 255

running = True
while running:

    screen.fill(white)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False

    mouse_pos = pg.mouse.get_pos()

    pg.draw.circle(screen, black, mouse_pos, 5)
    pg.draw.circle(screen, black, origin, link1_length + link2_length, 5)
    try:
        solution = match_point_with_angle(mouse_pos[0], mouse_pos[1])
        angles = angle_list[solution[0]][solution[1]]

        vec_1 = rotate_vector(link1_length, angles[0])
        vec_2 = pos_list[solution[0]][solution[1]]
        pg.draw.circle(screen, blue, vec_1, 5)
        pg.draw.circle(screen, blue, vec_2, 5)
        pg.draw.aaline(screen, black, origin, vec_1)
        pg.draw.aaline(screen, black, vec_1, vec_2)

    except:
        pass

    pg.display.flip()

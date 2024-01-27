from math import sin, cos, radians
import numpy as np


def rotate(point, center, degrees):
    deg_in_rad = radians(degrees)
    rotation_matrix = np.array([
        [cos(deg_in_rad), -sin(deg_in_rad)],
        [sin(deg_in_rad), cos(deg_in_rad)]
    ])
    norm_point = np.subtract(point, center)
    rotated_point = np.add(np.matmul(rotation_matrix, norm_point), center)
    return tuple(map(round, rotated_point))


def move(point, vector):
    return tuple(map(sum, zip(point, vector)))

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


def pg_rect_to_points(rect):
    return [
        (rect.left, rect.top),
        (rect.right, rect.top),
        (rect.right, rect.bottom),
        (rect.left, rect.bottom)
    ]


def rect_center(rect):
    x = sum([p[0] for p in rect]) // len(rect)
    y = sum([p[1] for p in rect]) // len(rect)
    return x, y

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


def rotate_3d(point, center, axis, degrees):
    deg_in_rad = radians(degrees)
    rotation_matrix = None
    if axis == "x":
        rotation_matrix = np.array([
            [1, 0, 0],
            [0, cos(deg_in_rad), -sin(deg_in_rad)],
            [0, sin(deg_in_rad), cos(deg_in_rad)]
        ])
        center = 0, center[1], center[2]
    elif axis == "y":
        rotation_matrix = np.array([
            [cos(deg_in_rad), 0, sin(deg_in_rad)],
            [0, 1, 0],
            [-sin(deg_in_rad), 0, cos(deg_in_rad)]
        ])
        center = center[0], 0, center[2]
    elif axis == "z":
        rotation_matrix = np.array([
            [cos(deg_in_rad), -sin(deg_in_rad), 0],
            [sin(deg_in_rad), cos(deg_in_rad), 0],
            [0, 0, 1]
        ])
        center = center[0], center[1], 0
    if rotation_matrix is None:
        raise Exception("Invalid axis")
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


def rect_center_3d(rect):
    x = sum([p[0] for p in rect]) // len(rect)
    y = sum([p[1] for p in rect]) // len(rect)
    z = sum([p[2] for p in rect]) // len(rect)
    return x, y, z


def build_cube_lines(points):
    a, b, c, d, e, f, g, h = points
    return [
        (a, b), (b, c), (c, d), (d, a),
        (e, f), (f, g), (g, h), (h, e),
        (a, e), (b, f), (c, g), (d, h)
    ]

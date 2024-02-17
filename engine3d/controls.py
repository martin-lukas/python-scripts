import pygame as pg


def on_key_down_update_movement(pressed_keys, cube_points, move_step):
    def update_coordinates(xyz_coords, delta):
        return tuple(map(sum, zip(xyz_coords, delta)))

    def update_cube_points(points, delta):
        return [update_coordinates(p, delta) for p in points]

    new_points = cube_points
    if pressed_keys[pg.K_w]:
        new_points = update_cube_points(new_points, (0, -move_step, 0))
    if pressed_keys[pg.K_s]:
        new_points = update_cube_points(new_points, (0, move_step, 0))
    if pressed_keys[pg.K_a]:
        new_points = update_cube_points(new_points, (-move_step, 0, 0))
    if pressed_keys[pg.K_d]:
        new_points = update_cube_points(new_points, (move_step, 0, 0))
    return new_points


def on_key_down_update_rotations(pressed_keys, cur_rots, rot_step):
    def update_rotations(rots, delta):
        return tuple(map(sum, zip(rots, delta)))

    new_rots = cur_rots
    if pressed_keys[pg.K_RIGHT]:
        new_rots = update_rotations(cur_rots, (0, rot_step, 0))
    if pressed_keys[pg.K_LEFT]:
        new_rots = update_rotations(cur_rots, (0, -rot_step, 0))
    if pressed_keys[pg.K_UP]:
        new_rots = update_rotations(cur_rots, (rot_step, 0, 0))
    if pressed_keys[pg.K_DOWN]:
        new_rots = update_rotations(cur_rots, (-rot_step, 0, 0))
    if pressed_keys[pg.K_q]:
        new_rots = update_rotations(cur_rots, (0, 0, rot_step))
    if pressed_keys[pg.K_e]:
        new_rots = update_rotations(cur_rots, (0, 0, -rot_step))
    return new_rots

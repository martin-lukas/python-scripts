import pygame as pg

from transformations import rotate_3d, pg_rect_to_points, \
    rect_center_3d, build_cube_lines
from colors import BLACK

WIDTH, HEIGHT = 800, 800
H_WIDTH, H_HEIGHT = WIDTH // 2, HEIGHT // 2
FPS = 60
ROTATION_STEP = 0.5
MOVE_STEP = 3

pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()

front_square = pg_rect_to_points(pg.Rect(400, 400, 100, 100))
[a, b, c, d] = [(x, y, 100) for x, y in front_square]
back_square = front_square.copy()
[e, f, g, h] = [(x, y, 200) for x, y in back_square]
cube_points = [a, b, c, d, e, f, g, h]

rot_x = 0.0
rot_y = 0.0
rot_z = 0.0


def draw():
    global cube_points
    screen.fill((96, 35, 32))

    # Find cube center
    diagonal_square = [
        cube_points[0],
        cube_points[5],
        cube_points[6],
        cube_points[3],
    ]
    cube_center = rect_center_3d(diagonal_square)

    # Rotate cube points by all axes
    axes = [("y", rot_y), ("x", rot_x), ("z", rot_z)]
    for axis in axes:
        for i in range(len(cube_points)):
            cube_points[i] = rotate_3d(
                point=cube_points[i],
                center=cube_center,
                axis=axis[0],
                degrees=axis[1]
            )

    # Draw cube lines
    cube_lines = build_cube_lines(cube_points)
    for line in cube_lines:
        pg.draw.line(screen, BLACK, line[0][:2], line[1][:2])


while True:
    draw()
    [exit() for ev in pg.event.get() if ev.type == pg.QUIT]

    # Rotation controls
    if pg.key.get_pressed()[pg.K_RIGHT]:
        rot_y += ROTATION_STEP
    if pg.key.get_pressed()[pg.K_LEFT]:
        rot_y -= ROTATION_STEP
    if pg.key.get_pressed()[pg.K_UP]:
        rot_x += ROTATION_STEP
    if pg.key.get_pressed()[pg.K_DOWN]:
        rot_x -= ROTATION_STEP
    if pg.key.get_pressed()[pg.K_q]:
        rot_z += ROTATION_STEP
    if pg.key.get_pressed()[pg.K_e]:
        rot_z -= ROTATION_STEP

    # Movement controls
    if pg.key.get_pressed()[pg.K_w]:
        new_cube_points = [list(p) for p in cube_points]
        for p in new_cube_points:
            p[1] -= MOVE_STEP
        cube_points = [tuple(p) for p in new_cube_points]
    if pg.key.get_pressed()[pg.K_s]:
        new_cube_points = [list(p) for p in cube_points]
        for p in new_cube_points:
            p[1] += MOVE_STEP
        cube_points = [tuple(p) for p in new_cube_points]
    if pg.key.get_pressed()[pg.K_a]:
        new_cube_points = [list(p) for p in cube_points]
        for p in new_cube_points:
            p[0] -= MOVE_STEP
        cube_points = [tuple(p) for p in new_cube_points]
    if pg.key.get_pressed()[pg.K_d]:
        new_cube_points = [list(p) for p in cube_points]
        for p in new_cube_points:
            p[0] += MOVE_STEP
        cube_points = [tuple(p) for p in new_cube_points]

    pg.display.set_caption(str(int(clock.get_fps())))
    pg.display.flip()
    clock.tick(FPS)

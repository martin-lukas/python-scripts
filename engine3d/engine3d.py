import pygame as pg
from controls import \
    on_key_down_update_rotations, on_key_down_update_movement
from transformations import \
    pg_rect_to_points, rect_center_3d, build_cube_lines, rotate_points
from colors import BLACK, WHITE

# Constants
WIDTH, HEIGHT = 800, 800
H_WIDTH, H_HEIGHT = WIDTH // 2, HEIGHT // 2
FPS = 60
ROTATION_STEP = 0.5
MOVE_STEP = 3

# Pygame setup
pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()

# Initial cube points setup
front_square = pg_rect_to_points(pg.Rect(400, 400, 100, 100))
[a, b, c, d] = [(x, y, 100) for x, y in front_square]
back_square = front_square.copy()
[e, f, g, h] = [(x, y, 200) for x, y in back_square]

# App state
cube_points = [a, b, c, d, e, f, g, h]
rot_x = 0.0
rot_y = 0.0
rot_z = 0.0


def draw(points):
    screen.fill(WHITE)

    # Draw lines
    cube_lines = build_cube_lines(points)
    for line in cube_lines:
        pg.draw.line(
            screen,
            color=BLACK,
            start_pos=line[0][:2],
            end_pos=line[1][:2],
            width=3
        )


while True:
    [exit() for ev in pg.event.get() if ev.type == pg.QUIT]

    # Update rotations based on key presses
    (new_rot_x, new_rot_y, new_rot_z) = on_key_down_update_rotations(
        pg.key.get_pressed(),
        (rot_x, rot_y, rot_z),
        ROTATION_STEP
    )
    rot_x, rot_y, rot_z = new_rot_x, new_rot_y, new_rot_z

    cube_center = rect_center_3d([
        cube_points[0],
        cube_points[5],
        cube_points[6],
        cube_points[3],
    ])
    cube_points = rotate_points(
        cube_points,
        cube_center,
        (rot_x, rot_y, rot_z)
    )

    # Update movement based on key presses
    cube_points = on_key_down_update_movement(
        pg.key.get_pressed(),
        cube_points,
        MOVE_STEP
    )

    draw(cube_points)

    pg.display.set_caption(str(int(clock.get_fps())))
    pg.display.flip()
    clock.tick(FPS)

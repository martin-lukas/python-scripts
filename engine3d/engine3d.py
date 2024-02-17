import pygame as pg
from transformations import pg_rect_to_points, build_cube_lines
from colors import BLACK, WHITE

# Constants
WIDTH, HEIGHT = 800, 800
H_WIDTH, H_HEIGHT = WIDTH // 2, HEIGHT // 2
FPS = 60

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
    # Monitor exit events
    [exit() for ev in pg.event.get() if ev.type == pg.QUIT]

    # Draw
    draw(cube_points)

    # FPS setup
    pg.display.set_caption(str(int(clock.get_fps())))
    pg.display.flip()
    clock.tick(FPS)

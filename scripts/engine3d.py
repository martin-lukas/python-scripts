import pygame as pg

from transformations import rotate, move, rect_center, pg_rect_to_points
from colors import BLACK

WIDTH, HEIGHT = 800, 800
H_WIDTH, H_HEIGHT = WIDTH // 2, HEIGHT // 2
FPS = 60
ROTATION_STEP = 4
MOVE_STEP = 3

pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()

rect_1 = pg_rect_to_points(pg.Rect(300, 300, 300, 50))
rect_2 = pg_rect_to_points(pg.Rect(300, 560, 300, 50))
rect_3 = pg_rect_to_points(pg.Rect(20, 400, 300, 50))
rect_1_center = rect_center(rect_1)
rect_2_center = rect_center(rect_2)
rect_3_center = rect_center(rect_3)
rect_1 = [rotate(p, rect_1_center, 45) for p in rect_1]
rect_2 = [rotate(p, rect_2_center, 45) for p in rect_2]
rect_3 = [rotate(p, rect_3_center, 90) for p in rect_3]

square = pg_rect_to_points(pg.Rect(600, 500, 100, 100))

cur_rot = 0


def draw():
    screen.fill((96, 35, 32))

    # Draw the rectangles as obstacles
    for rect in [rect_1, rect_2, rect_3]:
        pg.draw.polygon(screen, BLACK, rect, 2)

    # Draw the square
    square_center = rect_center(square)
    rotated_square = [
        rotate(p, square_center, cur_rot)
        for p in square
    ]
    pg.draw.polygon(screen, BLACK, rotated_square, 2)


while True:
    draw()
    [exit() for ev in pg.event.get() if ev.type == pg.QUIT]

    # Rotation controls
    if pg.key.get_pressed()[pg.K_RIGHT]:
        cur_rot += ROTATION_STEP
    if pg.key.get_pressed()[pg.K_LEFT]:
        cur_rot -= ROTATION_STEP

    # Movement controls
    if pg.key.get_pressed()[pg.K_w]:
        square = [move(p, (0, -MOVE_STEP)) for p in square]
    if pg.key.get_pressed()[pg.K_s]:
        square = [move(p, (0, MOVE_STEP)) for p in square]
    if pg.key.get_pressed()[pg.K_a]:
        square = [move(p, (-MOVE_STEP, 0)) for p in square]
    if pg.key.get_pressed()[pg.K_d]:
        square = [move(p, (MOVE_STEP, 0)) for p in square]

    pg.display.set_caption(str(int(clock.get_fps())))
    pg.display.flip()
    clock.tick(FPS)

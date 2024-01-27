import pygame as pg

from transformations import rotate, move
from colors import BLACK

WIDTH, HEIGHT = 800, 800
H_WIDTH, H_HEIGHT = WIDTH // 2, HEIGHT // 2
FPS = 60
ROTATION_STEP = 4
MOVE_STEP = 3

pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()

square = pg.Rect(600, 500, 100, 100)
square_points = [
    (square.left, square.top),
    (square.right, square.top),
    (square.right, square.bottom),
    (square.left, square.bottom)
]

cur_rot = 0


def draw():
    screen.fill((96, 35, 32))
    # Draw rectangles
    rect_1 = pg.Rect(300, 300, 300, 50)
    rect_2 = pg.Rect(300, 560, 300, 50)
    rect_3 = pg.Rect(20, 400, 300, 50)
    # Get points of rectangle as a list of tuples
    rect_1_points = [
        (rect_1.left, rect_1.top),
        (rect_1.right, rect_1.top),
        (rect_1.right, rect_1.bottom),
        (rect_1.left, rect_1.bottom)
    ]
    rect_2_points = [
        (rect_2.left, rect_2.top),
        (rect_2.right, rect_2.top),
        (rect_2.right, rect_2.bottom),
        (rect_2.left, rect_2.bottom)
    ]
    rect_3_points = [
        (rect_3.left, rect_3.top),
        (rect_3.right, rect_3.top),
        (rect_3.right, rect_3.bottom),
        (rect_3.left, rect_3.bottom)
    ]
    # Rotate these points by 315 degrees, around the center of the rectangle
    rect_1_points = [rotate(p, rect_1.center, 45) for p in rect_1_points]
    rect_2_points = [rotate(p, rect_2.center, 45) for p in rect_2_points]
    rect_3_points = [rotate(p, rect_3.center, 90) for p in rect_3_points]
    # Draw the rotated rectangle using the rotated points
    pg.draw.polygon(screen, BLACK, rect_1_points, 2)
    pg.draw.polygon(screen, BLACK, rect_2_points, 2)
    pg.draw.polygon(screen, BLACK, rect_3_points, 2)

    square_center = (
        (square_points[1][0] - square_points[0][0]) // 2 + square_points[0][0],
        (square_points[2][1] - square_points[0][1]) // 2 + square_points[0][1]
    )
    rotated_square_points = [
        rotate(p, square_center, cur_rot)
        for p in square_points
    ]
    pg.draw.polygon(screen, BLACK, rotated_square_points, 2)


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
        square_points = [move(p, (0, -MOVE_STEP)) for p in square_points]
    if pg.key.get_pressed()[pg.K_s]:
        square_points = [move(p, (0, MOVE_STEP)) for p in square_points]
    if pg.key.get_pressed()[pg.K_a]:
        square_points = [move(p, (-MOVE_STEP, 0)) for p in square_points]
    if pg.key.get_pressed()[pg.K_d]:
        square_points = [move(p, (MOVE_STEP, 0)) for p in square_points]

    pg.display.set_caption(str(int(clock.get_fps())))
    pg.display.flip()
    clock.tick(FPS)

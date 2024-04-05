from math import sin, cos, radians
import pygame as pg
from colors import BLACK, WHITE, ELECTRIC_BLUE

# Constants
WIDTH, HEIGHT = 800, 800
H_WIDTH, H_HEIGHT = WIDTH // 2, HEIGHT // 2
FPS = 60

# Pygame setup
pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()


def scale_point(coords, scale):
    return tuple(coord * scale for coord in coords)


def scale_points(points, scale):
    return [scale_point(point, scale) for point in points]


def translate_points(points, delta):
    dx, dy, dz = delta
    return [(x + dx, y + dy, z + dz) for x, y, z in points]


# Data setup
a = scale_point((0, 0, 0), 100)
b = scale_point((1, 0, 0), 100)
c = scale_point((1, 1, 0), 100)
d = scale_point((0, 1, 0), 100)
e = scale_point((0, 0, 1), 100)
f = scale_point((1, 0, 1), 100)
g = scale_point((1, 1, 1), 100)
h = scale_point((0, 1, 1), 100)
triangles = [
    (a, b, c), (a, c, d),
    (a, b, e), (b, e, f),
    (b, c, f), (c, f, g),
    (a, d, e), (d, e, h),
    (e, f, h), (f, g, h),
    (c, d, h), (c, h, g),
]
edges = [
    (a, b), (b, c), (c, d), (d, a),
    (e, f), (f, g), (g, h), (h, e),
    (a, e), (b, f), (c, g), (d, h),
]
triangles = [translate_points(t, (400, 400, 0)) for t in triangles]
edges = [translate_points(e, (400, 400, 0)) for e in edges]

camera_position = (0, 0, -300)
camera_yaw = 0
camera_pitch = 0


def project_points(points):
    global camera_position, camera_yaw, camera_pitch, WIDTH, HEIGHT
    
    projected_points = []
    for x, y, z in points:
        x -= camera_position[0]
        y -= camera_position[1]
        z -= camera_position[2]
        
        # Apply pitch and yaw transformations
        x, y, z = (
            x * cos(radians(camera_yaw)) - y * sin(radians(camera_yaw)),
            x * sin(radians(camera_yaw)) + y * cos(radians(camera_yaw)),
            z * cos(radians(camera_pitch)),
        )
        
        # Perspective projection
        if z != 0:
            scale = 300 / z  # Adjust the scale factor for proper perspective
            x, y = x * scale, y * scale
        
        # Translate to screen coordinates
        x += H_WIDTH
        y = HEIGHT - (y + H_HEIGHT)  # Flip y-coordinate for pygame
        
        projected_points.append((int(x), int(y)))
    
    return projected_points


def draw():
    screen.fill(WHITE)
    
    projected_triangles = []
    for triangle in triangles:
        projected_triangle = project_points(triangle)
        projected_triangles.append(projected_triangle)
    
    for triangle in projected_triangles:
        pg.draw.polygon(screen, ELECTRIC_BLUE, triangle)
    
    projected_edges = []
    for edge in edges:
        projected_edge = project_points(edge)
        projected_edges.append(projected_edge)
    
    for edge in projected_edges:
        start, end = edge
        pg.draw.line(screen, BLACK, start, end, 2)


while True:
    # Monitor exit events
    [exit() for ev in pg.event.get() if ev.type == pg.QUIT]
    
    # camera_controls(pg.key.get_pressed())
    
    # Draw
    draw()
    
    # FPS setup
    pg.display.set_caption(str(int(clock.get_fps())))
    pg.display.flip()
    clock.tick(FPS)

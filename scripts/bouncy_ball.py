from math import pi, sin, cos, sqrt

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# Initial parameters
window_width = 800
window_height = 600
aspect_ratio = window_width / window_height
ball_radius = 0.1

# Ball 1
ball1_x, ball1_y = -0.5, 0.0
ball1_speed_x, ball1_speed_y = 0.02, 0.02
mass_ball1 = 1.0  # Mass of ball1

# Ball 2
ball2_x, ball2_y = 0.5, 0.0
ball2_speed_x, ball2_speed_y = -0.02, -0.02
mass_ball2 = 2.0 / 3.0  # Mass of ball2 (2/3 of mass_ball1)

gravity = -0.001
elasticity = 0.93
collision_radius = ball_radius * 2.0  # Radius for collision detection

# Keyboard input state
keys = {'a': False, 'd': False, 'w': False, 's': False}


def draw_ball(x, y, color):
    glColor3f(*color)
    glBegin(GL_TRIANGLE_FAN)
    glVertex2f(x, y)  # Center of the circle
    num_segments = 100
    for i in range(num_segments + 1):
        angle = 2.0 * pi * i / num_segments
        bx = x + ball_radius * cos(angle)
        by = y + ball_radius * sin(angle)
        glVertex2f(bx, by)
    glEnd()


def draw_scene():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    gluOrtho2D(-aspect_ratio, aspect_ratio, -1.0, 1.0)

    draw_ball(ball1_x, ball1_y, (1.0, 0.0, 0.0))
    draw_ball(ball2_x, ball2_y, (0.0, 0.0, 1.0))

    glutSwapBuffers()


def update_ball_position():
    global ball1_x, ball1_y, ball1_speed_x, ball1_speed_y, mass_ball1
    global ball2_x, ball2_y, ball2_speed_x, ball2_speed_y, mass_ball2
    global gravity, aspect_ratio, elasticity

    # Apply gravity
    ball1_speed_y += gravity
    ball2_speed_y += gravity

    # Update ball positions based on arrow key input
    if keys['a']:
        ball1_speed_x = max(ball1_speed_x - 0.001, -0.1)
    if keys['d']:
        ball1_speed_x = min(ball1_speed_x + 0.001, 0.1)
    if keys['w']:
        ball1_speed_y = min(ball1_speed_y + 0.001, 0.1)
    if keys['s']:
        ball1_speed_y = max(ball1_speed_y - 0.001, -0.1)

    ball1_x += ball1_speed_x
    ball1_y += ball1_speed_y

    # Bounce off the walls for ball1
    if ball1_x + ball_radius > aspect_ratio:
        ball1_speed_x = -abs(ball1_speed_x) * elasticity
        ball1_x = aspect_ratio - ball_radius

    if ball1_x - ball_radius < -aspect_ratio:
        ball1_speed_x = abs(ball1_speed_x) * elasticity
        ball1_x = -aspect_ratio + ball_radius

    # Bounce off the floor for ball1
    if ball1_y - ball_radius < -1.0:
        ball1_speed_y = abs(ball1_speed_y) * elasticity
        ball1_y = -1.0 + ball_radius

    # Reset vertical speed when hitting the ceiling for ball1
    if ball1_y + ball_radius > 1.0:
        ball1_speed_y *= -1
        ball1_y = 1.0 - ball_radius

    # Update ball2 positions
    ball2_x += ball2_speed_x
    ball2_y += ball2_speed_y

    # Bounce off the walls for ball2
    if ball2_x + ball_radius > aspect_ratio:
        ball2_speed_x = -abs(ball2_speed_x) * elasticity
        ball2_x = aspect_ratio - ball_radius

    if ball2_x - ball_radius < -aspect_ratio:
        ball2_speed_x = abs(ball2_speed_x) * elasticity
        ball2_x = -aspect_ratio + ball_radius

    # Bounce off the floor for ball2
    if ball2_y - ball_radius < -1.0:
        ball2_speed_y = abs(ball2_speed_y) * elasticity
        ball2_y = -1.0 + ball_radius

    # Reset vertical speed when hitting the ceiling for ball2
    if ball2_y + ball_radius > 1.0:
        ball2_speed_y *= -1
        ball2_y = 1.0 - ball_radius

    # Check for collision between balls
    if check_collision(ball1_x, ball1_y, ball2_x, ball2_y, collision_radius):
        handle_collision(ball1_x, ball1_y, ball1_speed_x, ball1_speed_y,
                         mass_ball1,
                         ball2_x, ball2_y, ball2_speed_x, ball2_speed_y,
                         mass_ball2)


def check_collision(x1, y1, x2, y2, radius):
    distance = sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return distance < radius


def handle_collision(x1, y1, vx1, vy1, mass1, x2, y2, vx2, vy2, mass2):
    # Calculate the collision normal
    collision_normal_x = x2 - x1
    collision_normal_y = y2 - y1
    length = sqrt(collision_normal_x ** 2 + collision_normal_y ** 2)
    collision_normal_x /= length
    collision_normal_y /= length

    # Calculate relative velocity
    relative_velocity_x = vx2 - vx1
    relative_velocity_y = vy2 - vy1

    # Calculate dot product of relative velocity and collision normal
    dot_product = relative_velocity_x * collision_normal_x + relative_velocity_y * collision_normal_y

    # Apply impulse to both balls with adjusted masses
    impulse = 2 * dot_product / (mass1 + mass2)
    vx1 += impulse * collision_normal_x * mass2
    vy1 += impulse * collision_normal_y * mass2
    vx2 -= impulse * collision_normal_x * mass1
    vy2 -= impulse * collision_normal_y * mass1

    # Update ball velocities
    global ball1_speed_x, ball1_speed_y, ball2_speed_x, ball2_speed_y
    ball1_speed_x, ball1_speed_y = vx1, vy1
    ball2_speed_x, ball2_speed_y = vx2, vy2


def special_key_pressed(key, x, y):
    global keys
    if key == ord('a'):
        keys['a'] = True
    elif key == ord('d'):
        keys['d'] = True
    elif key == ord('w'):
        keys['w'] = True
    elif key == ord('s'):
        keys['s'] = True


def special_key_released(key, x, y):
    global keys
    if key == ord('a'):
        keys['a'] = False
    elif key == ord('d'):
        keys['d'] = False
    elif key == ord('w'):
        keys['w'] = False
    elif key == ord('s'):
        keys['s'] = False


def update_scene(value):
    update_ball_position()
    glutTimerFunc(16, update_scene, 0)
    glutPostRedisplay()


def main():
    global window_width, window_height

    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(window_width, window_height)
    glutCreateWindow("Two Bouncing Balls with Collision and Weight Difference")

    glutDisplayFunc(draw_scene)
    glutSpecialFunc(special_key_pressed)
    glutSpecialUpFunc(special_key_released)
    glutTimerFunc(16, update_scene, 0)

    glClearColor(1.0, 1.0, 1.0, 1.0)  # White background

    gluOrtho2D(-aspect_ratio, aspect_ratio, -1.0, 1.0)

    glutMainLoop()


if __name__ == "__main__":
    main()

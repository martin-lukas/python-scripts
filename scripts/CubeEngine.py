import pygame
import sys

black = (0, 0, 0)
white = (255, 255, 255)


class CubeEngine:
    def __init__(self, screen_width, screen_height, unit_px, dist_factor, size):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.center_x = screen_width // 2
        self.center_y = screen_height // 2
        self.unit_px = unit_px
        self.dist_factor = dist_factor
        self.size = size

        self.lines = [
            ((0, 0), (0, 1))
        ]

        pygame.init()
        pygame.display.set_caption("Cube")
        self.screen = pygame.display.set_mode((screen_width, screen_height))

    def draw_perspective_square(self, cur_x, cur_y):
        a = (self.x(cur_x), self.y(cur_y))
        b = (self.x(cur_x + self.size), self.y(cur_y))
        c = (self.x(cur_x), self.y(cur_y + self.size))
        d = (self.x(cur_x + self.size), self.y(cur_y + self.size))
        pygame.draw.line(self.screen, black, a, b)
        pygame.draw.line(self.screen, black, a, c)
        pygame.draw.line(self.screen, black, b, d)
        pygame.draw.line(self.screen, black, c, d)

    def x(self, units):
        total_delta = 0
        cur_delta = self.unit_px
        for _ in range(abs(units)):
            cur_delta = round(cur_delta * self.dist_factor)
            if units < 0:
                total_delta -= cur_delta
            else:
                total_delta += cur_delta
        return self.center_x + total_delta

    def y(self, units):
        total_delta = 0
        cur_delta = self.unit_px
        for _ in range(abs(units)):
            cur_delta = round(cur_delta * self.dist_factor)
            if units < 0:
                total_delta -= cur_delta
            else:
                total_delta += cur_delta
        return self.center_y + total_delta

    def game_loop(self):
        cur_x = 0
        cur_y = 0
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        cur_y += 1
                    elif event.key == pygame.K_DOWN:
                        cur_y -= 1
                    if event.key == pygame.K_LEFT:
                        cur_x -= 1
                    elif event.key == pygame.K_RIGHT:
                        cur_x += 1

            self.screen.fill(white)

            self.draw_perspective_square(cur_x, cur_y)

            pygame.display.flip()
            pygame.time.Clock().tick(60)

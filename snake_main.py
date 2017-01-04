#coding: utf8
import random
import pygame
import pygame.gfxdraw

random.seed()
pygame.init()


class GameController(object):
    def __init__(self):
        if not GameController.is_joystick_present():
            print(u'Джойстик не найден. Для управления используйте курсор клавиатуры.')
        else:
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()
            self.joystick_hat = self.joystick.get_hat(0)
            self.joystick_button = self.joystick.get_button(0)

    @staticmethod
    def is_joystick_present():
        return pygame.joystick.get_count() > 0

    def run_event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Game.quit()
            if GameController.is_joystick_present():
                if event.type == pygame.JOYHATMOTION:
                    hat_state = self.joystick.get_hat(0)
                    if hat_state == (0, 1):
                        return Snake.DIRECTION_UP
                    elif hat_state == (1, 0):
                        return Snake.DIRECTION_RIGHT
                    elif hat_state == (0, -1):
                        return Snake.DIRECTION_DOWN
                    elif hat_state == (-1, 0):
                        return Snake.DIRECTION_LEFT
            if event.type == pygame.KEYDOWN:
                key = pygame.key.get_pressed()
                if key[pygame.K_LEFT]:
                    return Snake.DIRECTION_LEFT
                elif key[pygame.K_RIGHT]:
                    return Snake.DIRECTION_RIGHT
                elif key[pygame.K_UP]:
                    return Snake.DIRECTION_UP
                elif key[pygame.K_DOWN]:
                    return Snake.DIRECTION_DOWN


class Game(object):
    SCREEN_BOUNDARY_TOP = 0
    SCREEN_BOUNDARY_RIGHT = 1
    SCREEN_BOUNDARY_BOTTOM = 2
    SCREEN_BOUNDARY_LEFT = 3

    def __init__(self, display_size_x=800, display_size_y=600, full_screen=False, field_color=(0, 0, 0),
                 max_fpx=60, initial_snake_speed=1, snake_speed_add=0.3, snake_length=100, snake_length_add=50,
                 snake_width=3, apple_size=30):
        self.display_size_x = display_size_x
        self.display_size_y = display_size_y
        self.field_color = field_color
        self.max_fps = max_fpx
        self.snake_speed = initial_snake_speed
        self.snake_speed_add = snake_speed_add
        self.snake_length = snake_length
        self.snake_length_add = snake_length_add
        self.snake_width = snake_width
        self.apple_size = apple_size
        self.clock = pygame.time.Clock()
        self.game_controller = GameController()
        self.screen = (pygame.display.set_mode() if full_screen
                       else pygame.display.set_mode((self.display_size_x, self.display_size_y)))
        self.snake = Snake(self.screen, self.snake_speed, length=self.snake_length, width=self.snake_width)
        self.apple = Apple(self.screen, self.apple_size)
        pygame.display.set_caption(u'Змейка для Ивана и Петра')

    def screen_boundary_hit(self, x, y):
        max_x, max_y = self.screen.get_size()
        if x < 0:
            return self.SCREEN_BOUNDARY_LEFT
        elif x > max_x:
            return self.SCREEN_BOUNDARY_RIGHT
        elif y < 0:
            return self.SCREEN_BOUNDARY_TOP
        elif y > max_y:
            return self.SCREEN_BOUNDARY_BOTTOM

    def check_snake_hit_screen_edge(self):
        edge_hit = self.screen_boundary_hit(*self.snake.head_x_y)
        if edge_hit is None:
            return
        elif edge_hit == self.SCREEN_BOUNDARY_TOP:
            self.snake.head_x_y[1] = self.display_size_y
        elif edge_hit == self.SCREEN_BOUNDARY_BOTTOM:
            self.snake.head_x_y[1] = 0
        elif edge_hit == self.SCREEN_BOUNDARY_LEFT:
            self.snake.head_x_y[0] = self.display_size_x
        elif edge_hit == self.SCREEN_BOUNDARY_RIGHT:
            self.snake.head_x_y[0] = 0

    def check_snake_bites_apple(self):
        snake_head_x = self.snake.head_x_y[0]
        snake_head_y = self.snake.head_x_y[1]
        apple_x = self.apple.coordinates[0]
        apple_y = self.apple.coordinates[1]
        apple_radius = self.apple.radius
        snake_head_radius = self.snake.width
        if (apple_x - snake_head_x) ** 2 + (apple_y - snake_head_y) ** 2 < (apple_radius + snake_head_radius) ** 2:
            self.snake.length += self.snake_length_add
            self.snake.speed += self.snake_speed_add
            self.apple.relocate()

    def run(self):
        while True:
            direction = self.game_controller.run_event_loop()
            if direction is not None:
                self.snake.change_direction(direction)

            self.screen.fill(self.field_color)
            self.apple.update()
            self.snake.update()

            self.check_snake_bites_apple()
            self.check_snake_hit_screen_edge()

            pygame.display.update()
            self.clock.tick(self.max_fps)

    @staticmethod
    def quit():
        pygame.quit()
        exit()


class Snake(object):
    DIRECTION_UP = 0
    DIRECTION_RIGHT = 1
    DIRECTION_DOWN = 2
    DIRECTION_LEFT = 3
    DIRECTIONS = {
        DIRECTION_UP: [0, -1],
        DIRECTION_RIGHT: [1, 0],
        DIRECTION_DOWN: [0, 1],
        DIRECTION_LEFT: [-1, 0]
    }

    def __init__(self, screen, speed, length, width, color=pygame.Color('Green')):
        self.screen = screen
        self.speed = speed
        self.current_direction = random.choice(self.DIRECTIONS.keys())
        self.color = color
        self.length = length
        self.width = width
        max_x, max_y = self.screen.get_size()
        self.head_x_y = [random.randrange(0, max_y), random.randrange(0, max_y)]
        self.pixels = []

    def move_head(self):
        unit_vector = self.DIRECTIONS[self.current_direction]
        self.head_x_y = [j + k for j, k in zip(self.head_x_y, unit_vector)]

    def grow(self, length=1):
        if length < 0:
            self.shrink(length=-length)
        while length > 0:
            self.pixels.insert(0, self.head_x_y)
            self.move_head()
            length -= 1

    def shrink(self, length=1):
        if length < 0:
            self.grow(length=-length)
        if len(self.pixels) < self.length:
            return
        while length > 0:
            self.pixels.pop()
            length -= 1

    def render(self):
        head_size = 2
        for pixel in self.pixels:
            pygame.draw.circle(self.screen, self.color, pixel, self.width + head_size, 0)
            head_size = 0

    def update(self):
        for _ in range(int(self.speed)):
            self.grow()
            self.shrink()
        self.render()

    def change_direction(self, direction):
        self.current_direction = direction


class Apple(object):
    def __init__(self, screen, radius):
        self.screen = screen
        self.color = pygame.Color("Red")
        self.radius = radius
        self.coordinates = self.relocate()

    def render(self):
        pygame.draw.circle(self.screen, self.color, self.coordinates, self.radius, 0)

    def relocate(self):
        max_x, max_y = self.screen.get_size()
        self.coordinates = (
            random.randrange(self.radius, max_x - self.radius),
            random.randrange(self.radius, max_y - self.radius)
        )
        return self.coordinates

    def update(self):
        self.render()


if __name__ == '__main__':
    snake_game = Game()
    snake_game.run()

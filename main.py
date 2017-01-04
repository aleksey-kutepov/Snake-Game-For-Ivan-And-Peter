# coding: utf8
import random
import pygame as pg
random.seed()

pg.init()
pg.display.set_caption('Змейка для Ивана и Петра')

DISPLAY_SIZE_X = 300
DISPLAY_SIZE_Y = 300
DISPLAY_CENTER_X = DISPLAY_SIZE_X // 2
DISPLAY_CENTER_Y = DISPLAY_SIZE_Y // 2

MOVING_RECTANGLE_SIZE = 30
SPEED_X = MOVING_RECTANGLE_SIZE
SPEED_Y = -MOVING_RECTANGLE_SIZE

# surface = pg.display.set_mode((DISPLAY_SIZE_X, DISPLAY_SIZE_Y))
surface = pg.display.set_mode()
DISPLAY_SIZE_X, DISPLAY_SIZE_Y = surface.get_size()
DISPLAY_CENTER_X = DISPLAY_SIZE_X // 2
DISPLAY_CENTER_Y = DISPLAY_SIZE_Y // 2

backgroud_color = pg.Color("Black")

moving_rectangle = pg.Rect(
    DISPLAY_CENTER_X - MOVING_RECTANGLE_SIZE // 2,
    DISPLAY_CENTER_Y - MOVING_RECTANGLE_SIZE // 2,
    MOVING_RECTANGLE_SIZE,
    MOVING_RECTANGLE_SIZE
)
moving_rectangle_color = pg.Color("White")

apple_rectangle = pg.Rect(
    DISPLAY_CENTER_X - MOVING_RECTANGLE_SIZE // 2 + 10 * MOVING_RECTANGLE_SIZE,
    DISPLAY_CENTER_Y - MOVING_RECTANGLE_SIZE // 2 - 10 * MOVING_RECTANGLE_SIZE,
    MOVING_RECTANGLE_SIZE,
    MOVING_RECTANGLE_SIZE
)
apple_color = pg.Color("Red")


def exit_game():
    pg.quit()
    exit()

if pg.joystick.get_count() == 0:
    print(u'Джойстик не найден. Подключите джойстик и перезапустите игру.')
    exit_game()

joystick = pg.joystick.Joystick(0)
joystick.init()
joystick_hat = joystick.get_hat(0)
joystick_button = joystick.get_button(0)


def reallocate_apple():
    global apple_rectangle
    while apple_rectangle.colliderect(moving_rectangle):
        random_x = random.randrange(0, DISPLAY_SIZE_X, MOVING_RECTANGLE_SIZE)
        random_y = random.randrange(0, DISPLAY_SIZE_Y, MOVING_RECTANGLE_SIZE)
        apple_rectangle.x = random_x
        apple_rectangle.y = random_y


while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit_game()
        elif event.type == pg.JOYHATMOTION:
            dx, dy = joystick.get_hat(0)
            moving_rectangle.move_ip(dx * SPEED_X, dy * SPEED_Y)
        elif event.type == pg.JOYBUTTONDOWN:
            if joystick.get_button(0) == 1:
                moving_rectangle_color = pg.Color('Yellow')
            elif joystick.get_button(1) == 1:
                moving_rectangle_color = pg.Color('Green')
            elif joystick.get_button(8) == 1:
                backgroud_color = pg.Color('Orange')
            elif joystick.get_button(9) == 1:
                backgroud_color = pg.Color('Purple')
            elif joystick.get_button(2) == 1:
                moving_rectangle_color = pg.Color('Magenta')
    if apple_rectangle.colliderect(moving_rectangle):
        moving_rectangle.inflate_ip(MOVING_RECTANGLE_SIZE, MOVING_RECTANGLE_SIZE)
        reallocate_apple()
    surface.fill(backgroud_color)
    surface.fill(apple_color, apple_rectangle)
    surface.fill(moving_rectangle_color, moving_rectangle)
    pg.display.update()


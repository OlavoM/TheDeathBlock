import pygame, sys, time, random
from pygame.locals import *
from enum import Enum
from fighter import Fighter

pygame.init()

pygame.display.set_caption("The Death Block")


class Direction(Enum):
    UP = "up"
    DOWN = "down"
    RIGHT = "right"
    LEFT = "left"


def set_play_surface_config():
    global SCREEN_HEIGHT, SCREEN_WIDTH, play_surface
    SCREEN_HEIGHT = 600
    SCREEN_WIDTH = 1000
    play_surface = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))


def set_config():
    fps_clock = pygame.time.Clock()
    direction = ""
    change_direction = direction
    return fps_clock, direction, change_direction


def set_background_music():
    # Audio mixer for bg music
    pygame.mixer.init()
    pygame.mixer.music.load("bg_music/Blue Danube Strauss (No Copyright Music).mp3")
    pygame.mixer.music.set_volume(1.0)
    pygame.mixer.music.play(-1) # Continuos replay


def set_colours():
    global redColour, blackColour, whiteColour, greyColour, greenColour
    redColour = pygame.Color(255, 0, 0)    
    blackColour = pygame.Color(0, 0, 0)
    whiteColour = pygame.Color(255, 255, 255)
    greyColour = pygame.Color(150, 150, 150)
    greenColour = pygame.Color(0,200,0)


def draw_background(bg_image):
    bg_resized = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    play_surface.blit(bg_resized, (0,0))


def game_over():
    gameOverFont = pygame.font.Font("freesansbold.ttf", 72)
    gameOverSurf = gameOverFont.render("Game Over", True, greyColour)
    gameOverRect = gameOverSurf.get_rect()
    gameOverRect.midtop = (320, 10)
    play_surface.blit(gameOverSurf, gameOverRect)
    pygame.display.flip()
    time.sleep(1)
    pygame.quit()
    sys.exit()


def print_text(text):
    textFont = pygame.font.Font("freesansbold.ttf", 72)
    textSurf = textFont.render(text, True, greyColour)
    textRect = textSurf.get_rect()
    textRect.midtop = (320, 10)
    play_surface.blit(textSurf, textRect)
    pygame.display.flip()


def get_dPad_direction():
    d_pad = (joystick.get_hat(0)[0], joystick.get_hat(0)[1])
    if d_pad == (1, 0):
        return Direction.RIGHT
    elif d_pad == (-1, 0):
        return Direction.LEFT
    elif d_pad == (0, 1):
        return Direction.UP
    elif d_pad == (0, -1):
        return Direction.DOWN


def get_key_direction(event):
    if event.key==K_RIGHT or event.key==ord("d"):
        return Direction.RIGHT
    if event.key==K_LEFT or event.key==ord("a"):
        return Direction.LEFT
    if event.key==K_UP or event.key==ord("w"):
        return Direction.UP
    if event.key==K_DOWN or event.key==ord("s"):
        return Direction.DOWN
    if event.key==K_ESCAPE:
        pygame.event.post(pygame.event.Event(QUIT))


def get_analog_stick_direction():
    x_axis = joystick.get_axis(0)
    y_axis = joystick.get_axis(1)

    # Threshold for avoid direction detection mistakes (analogic dead zone)
    threshold = 0.3

    # Diagonal threshold
    dThreshold = 0.5

    if x_axis > threshold and y_axis < dThreshold and y_axis > -dThreshold:
        return Direction.RIGHT
    elif x_axis < -threshold and y_axis < dThreshold and y_axis > -dThreshold:
        return Direction.LEFT
    elif y_axis > threshold and x_axis < dThreshold and x_axis > -dThreshold:
        return Direction.DOWN
    elif y_axis < -threshold and x_axis < dThreshold and x_axis > -dThreshold:
        return Direction.UP


def joystick_connected():
    # Xbox Controller
    global joystick
    pygame.joystick.init()
    joystick_count = pygame.joystick.get_count()
    if joystick_count == 0:
        return False
    else:
        joystick = pygame.joystick.Joystick(0)
        joystick.init()
        return True


def main(config, joystickConnected):
    fps_clock, direction, change_direction = config
    play_surface.fill(whiteColour)
    pygame.display.flip()

    fighter_one = Fighter(200, 320)
    fighter_two = Fighter(700, 320)

    while True:
        draw_background(background_image)

        fighter_one.draw(play_surface)
        fighter_two.draw(play_surface)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                change_direction = get_key_direction(event)
            elif joystickConnected and (event.type == pygame.JOYHATMOTION):
                change_direction = get_dPad_direction()
            elif joystickConnected and event.type == pygame.JOYAXISMOTION:
                change_direction = get_analog_stick_direction()
            
        if change_direction==Direction.RIGHT:
                print_text("Right")
        if change_direction==Direction.LEFT:
                print_text("Left")
        if change_direction==Direction.UP:
                print_text("Up")
        if change_direction==Direction.DOWN:
                print_text("Down")
        
        pygame.display.update()
        
        fps_clock.tick(18)


#setBackgroundMusic()
set_colours()
set_play_surface_config()
config_values = set_config()
has_joystick = joystick_connected()
background_image = pygame.image.load("resources/images/background/white_bg.png")

main(config_values, has_joystick)
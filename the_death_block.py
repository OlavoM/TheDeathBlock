import pygame, sys, time, random
from fighter import Fighter
from controls_util import *

pygame.init()
pygame.display.set_caption("The Death Block")


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


def main(config, joystick_player_one):
    joystickConnected = (not (joystick_player_one == None))
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
                change_direction = get_dPad_direction(joystick_player_one)
            elif joystickConnected and event.type == pygame.JOYAXISMOTION:
                change_direction = get_analog_stick_direction(joystick_player_one)
            
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
joystick_player_one = get_joystick_connected()
background_image = pygame.image.load("resources/images/background/white_bg.png")

main(config_values, joystick_player_one)
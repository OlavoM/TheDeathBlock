import pygame, sys, time, random
from pygame.locals import *
from enum import Enum

pygame.init()
playSurface = pygame.display.set_mode((640,480))
pygame.display.set_caption("The Death Block")


class Direction(Enum):
    UP = "up"
    DOWN = "down"
    RIGHT = "right"
    LEFT = "left"


def setConfig():
    playSurface = pygame.display.set_mode((640,480))
    fpsClock = pygame.time.Clock()
    direction = ""
    changeDirection = direction

    return playSurface, fpsClock, direction, changeDirection


def joystickConnected():
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


def setBackgroundMusic():
    # Audio mixer for bg music
    pygame.mixer.init()
    pygame.mixer.music.load("bg_music/Blue Danube Strauss (No Copyright Music).mp3")
    pygame.mixer.music.set_volume(1.0)
    pygame.mixer.music.play(-1) # Continuos replay


def setColours():
    global redColour, blackColour, whiteColour, greyColour, greenColour
    redColour = pygame.Color(255, 0, 0)    
    blackColour = pygame.Color(0, 0, 0)
    whiteColour = pygame.Color(255, 255, 255)
    greyColour = pygame.Color(150, 150, 150)
    greenColour = pygame.Color(0,200,0)


def gameOver():
    gameOverFont = pygame.font.Font("freesansbold.ttf", 72)
    gameOverSurf = gameOverFont.render("Game Over", True, greyColour)
    gameOverRect = gameOverSurf.get_rect()
    gameOverRect.midtop = (320, 10)
    playSurface.blit(gameOverSurf, gameOverRect)
    pygame.display.flip()
    time.sleep(1)
    pygame.quit()
    sys.exit()

def printText(text):
    textFont = pygame.font.Font("freesansbold.ttf", 72)
    textSurf = textFont.render(text, True, greyColour)
    textRect = textSurf.get_rect()
    textRect.midtop = (320, 10)
    playSurface.blit(textSurf, textRect)
    pygame.display.flip()


def getDPadDirection():
    d_pad = (joystick.get_hat(0)[0], joystick.get_hat(0)[1])
    if d_pad == (1, 0):
        return Direction.RIGHT
    elif d_pad == (-1, 0):
        return Direction.LEFT
    elif d_pad == (0, 1):
        return Direction.UP
    elif d_pad == (0, -1):
        return Direction.DOWN


def getKeyDirection(event):
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


def getAnalogStickDirection():
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


def main(config, joystickConnected):
    playSurface, fpsClock, direction, changeDirection = config

    playSurface.fill(whiteColour)
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                changeDirection = getKeyDirection(event)
            elif joystickConnected and (event.type == pygame.JOYHATMOTION):
                changeDirection = getDPadDirection()
            elif joystickConnected and event.type == pygame.JOYAXISMOTION:
                changeDirection = getAnalogStickDirection()
            
        if changeDirection==Direction.RIGHT:
                printText("Right")
        if changeDirection==Direction.LEFT:
                printText("Left")
        if changeDirection==Direction.UP:
                printText("Up")
        if changeDirection==Direction.DOWN:
                printText("Down")
        
        playSurface.fill(whiteColour)
        
        fpsClock.tick(18)


#setBackgroundMusic()
setColours()
configValues = setConfig()
hasJoystick = joystickConnected()
main(configValues, hasJoystick)
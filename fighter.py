import pygame

class Fighter():
    def __init__(self, x, y):
        self.rect = pygame.Rect((x, y, 80, 180))
    
    def move(self):
        SPEED = 10
        delta_x = 0
        delta_y = 0
    
    def draw(self, surface):
        pygame.draw.rect(surface, (255,0,0), self.rect)
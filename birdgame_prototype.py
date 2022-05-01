from calendar import c
import pygame, sys, random, time

pygame.init()

FPS = 60
FramePerSec = pygame.time.Clock()

White = (255, 255, 255)
Black = (0, 0, 0)

Screen_Width = 1920
Screen_Height = 1080
Gamespeed = 1

Birdlife = pygame.display.set_mode((Screen_Width, Screen_Height))
Birdlife.fill(White)
pygame.display.set_caption("Birds")

class Bird():

    def to_rect(self):

        return pygame.Rect(self.x, self.y, self.image.get_width() , self.image.get_height())

    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("BirdM1.png")
        self.x = Screen_Width / 2 + random.randint(-200, 200)
        self.y = Screen_Height / 2 + random.randint(-200, 200)
    
    def set_position(self, x, y):
        self.x = x
        self.y = y

    def rdirec(self):
        
        self.x = self.x + random.randint(-5, 5)
        self.y = self.y + random.randint(-5, 5)
    
    def move(self):
        
        self.rdirec()

    def render(self):
        Birdlife.blit(self.image, self.to_rect())

birds = []
birds.append(Bird())

movecounter = 0

while True:
    
    Birdlife.fill(White)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

            Earl = Bird()
            birds.append(Earl)

            Earl.set_position(*pygame.mouse.get_pos())

    for entity in birds:

        entity.render()
        entity.move()
    
        for bird in birds:
            if bird is not entity and bird.to_rect().colliderect(entity.to_rect()):
                print("bruh")
                birds.remove(bird)
                birds.remove(entity)

    movecounter = movecounter + random.randint(0, 10)

    movecounter = 0
    
    pygame.display.update()
    FramePerSec.tick(FPS)
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
pygame.display.set_caption("Birds: ")

print(Birdlife.get_rect())

def get_ms():
    return int(time.time_ns() / 1000000)
class Bird():

    def to_rect(self):

        return pygame.Rect(self.x, self.y, self.image.get_width() , self.image.get_height())

    def __init__(self):
        super().__init__()
        self.birthtime = get_ms()
        self.cooldown = get_ms()
        self.image = pygame.image.load("BirdM1.png")
        self.x = Screen_Width / 2 + random.randint(-200, 200)
        self.y = Screen_Height / 2 + random.randint(-200, 200)
        self.direction = pygame.Rect(0,0,0,0)
        self.LastDirectionChange = get_ms() - random.randint(0, 10)
        self.MSNextChange = 0
    
    def set_position(self, x, y):
        self.x = x
        self.y = y

    def rdirec(self):
        
        self.x += self.direction.x
        self.y += self.direction.y
        if not Birdlife.get_rect().colliderect(self.to_rect()):
            birds.remove(self)

        if get_ms() - self.LastDirectionChange > self.MSNextChange:

            self.direction.x = random.randint(-2, 2)
            self.direction.y = random.randint(-2, 2)
            self.LastDirectionChange = get_ms()
            self.MSNextChange = random.randint(0, 3000)
    def move(self):
        
        if self.get_age() < 100000:
            self.rdirec()
        elif self.get_age() < 110000:
            self.y+=20

    def render(self):
        Birdlife.blit(self.image, self.to_rect())

    def get_age(self):
        return get_ms() - self.birthtime
    
    def collide(self, other):
        if self.get_age() > 100000:
            return
        
        if self.get_age() >= 0000 and get_ms() - self.cooldown > 10000:

            self.cooldown = get_ms()

            if(random.randint(0,3) == 1):
                Earl = Bird()
                birds.append(Earl)
                Earl.set_position(self.x, self.y)
        
birds = []

for i in range(50):
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
                bird.collide(entity)
    
    pygame.display.set_caption("Birds: " + str(len(birds)))


    movecounter = movecounter + random.randint(0, 10)

    movecounter = 0
    
    pygame.display.update()
    FramePerSec.tick(FPS)
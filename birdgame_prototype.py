from calendar import c
from locale import locale_encoding_alias
from re import X
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
birdsprite = pygame.image.load("BirdM1.png")
female = pygame.image.load("BirdF1.png")
boomsprite = pygame.image.load("boom.png")
rip = pygame.image.load("mrsanders.png")
boomer = []
gcd = 0

print(Birdlife.get_rect())

def get_ms():
    return int(time.time_ns() / 1000000)

def set_gender():
    return random.randint(0,1)

class Boom():
    def __init__(self, x, y):

        self.x = x
        self.y = y
        self.boomtime = get_ms()
    
    def render(self):

        Birdlife.blit(boomsprite, (self.x, self.y,0, 0))

    def boomremoval(self):
        if get_ms() - self.boomtime > 1500:
            boomer.remove(self)


class Bird():

    def to_rect(self):

        return pygame.Rect(self.x, self.y, self.image.get_width() , self.image.get_height())

    def __init__(self):

        super().__init__()
        self.birthtime = get_ms()
        self.cooldown = get_ms()
        self.image = birdsprite.copy()
        self.x = Screen_Width / 2 + random.randint(-200, 200)
        self.y = Screen_Height / 2 + random.randint(-200, 200)
        self.direction = pygame.Rect(0,0,0,0)
        self.LastDirectionChange = get_ms() - random.randint(0, 10)
        self.MSNextChange = 0
        self.gender = set_gender()
    
    def set_position(self, x, y):
        self.x = x
        self.y = y

    def rdirec(self):
        
        self.x += self.direction.x
        self.y += self.direction.y
        if not Birdlife.get_rect().contains(self.to_rect()):
            
            self.LastDirectionChange = get_ms()
            self.MSNextChange = random.randint(500, 3500)

            if(self.get_age() > 100000):
                birds.remove(self)
                return

            if self.x < Screen_Width / 2:
                self.direction.x = random.randint(5, 25)
            else:
                self.direction.x = -random.randint(5, 25)
            
            if self.y < Screen_Height / 2:
                self.direction.y = random.randint(5, 25)
            else:
                self.direction.y = -random.randint(5, 25)

        elif get_ms() - self.LastDirectionChange > self.MSNextChange:

            self.direction.x = random.randint(-2, 2)
            self.direction.y = random.randint(-2, 2)
            self.LastDirectionChange = get_ms()
            self.MSNextChange = random.randint(0, 3000)
            self.image = pygame.transform.rotate(birdsprite, random.randint(0,90) -25)

    def move(self):
        
        if self.get_age() > 100000:
            self.direction.y = 10
            self.direction.x = 0
        self.rdirec()

    def render(self):

        if(self.get_age() < 100000):
            if(self.gender == 1):
                Birdlife.blit(female, self.to_rect())
            else:
                Birdlife.blit(self.image, self.to_rect())
        else:
            Birdlife.blit(rip, self.to_rect())
        

    def get_age(self):
        return get_ms() - self.birthtime
    
    def collide(self, other):
        if self.get_age() > 100000:
            return
        
        if self.get_age() >= 0 and get_ms() - self.cooldown > 10000:

            self.cooldown = get_ms()
        
            if len(birds) < 15:

                if(random.randint(0,1) == 1):
                    if self.gender != other.gender:
                        Earl = Bird()
                        birds.append(Earl)
                        Earl.set_position(self.x, self.y)
                elif self.get_age() > other.get_age():
                    if other.get_age() > 100000:
                        pass
                    elif self.gender == other.gender:
                        other.birthtime = get_ms() - 100000
                        if abs(self.direction.x) > 10 or abs(self.direction.y) > 10:
                            boomer.append(Boom(other.x, other.y))
            
            else:

                if(random.randint(0,2) == 1):
                    if self.gender != other.gender:
                        Earl = Bird()
                        birds.append(Earl)
                        Earl.set_position(self.x, self.y)
                elif self.get_age() > other.get_age():
                    if other.get_age() > 100000:
                        pass
                    elif self.gender == other.gender:
                        other.birthtime = get_ms() - 100000
                        if abs(self.direction.x) > 10 or abs(self.direction.y) > 10:
                            boomer.append(Boom(other.x, other.y))
                        
birds = []

for i in range(10):
    birds.append(Bird())

movecounter = 0
Running = True
Jumpscare = False

while Running:
    
    Birdlife.fill(White)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Running = False
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
    
    for entity in boomer:

        entity.render()
        entity.boomremoval()

    pygame.display.set_caption("Birds: " + str(len(birds)))


    movecounter = movecounter + random.randint(0, 10)

    movecounter = 0
    
    pygame.display.update()
    FramePerSec.tick(FPS)

    if len(birds) == 0:
        Jumpscare = True
        time.sleep(10)
    
    if Jumpscare == True:
        birds.append(Bird())
        if len(birds) > 250:
            Running = False
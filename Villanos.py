import pygame, random
from typing import Any

class Villano(pygame.sprite.Sprite):
    def __init__(self, link, ancho: int, alto: int) -> None:
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(link), (ancho, alto))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(50, 950)
        self.rect.y = random.randrange(-3000, -100)
        self.velocidad_y = random.randrange(3, 4)
        self.velocidad_x = random.randrange(-4, 4)

    def update(self) -> None:
        
        if(self.rect.y < 0):
            
            self.rect.y += self.velocidad_y
        elif(self.rect.y >= 0 and self.rect.y < 850):

            self.rect.y += self.velocidad_y
            self.rect.x += self.velocidad_x

            if(self.rect.left < 0): self.velocidad_x += 1
            elif(self.rect.right > 1020): self.velocidad_x -= 1
            
            if(self.rect.y >= 850):
                self.rect.x = random.randrange(50, 950)
                self.rect.y = random.randrange(-1000, -40)
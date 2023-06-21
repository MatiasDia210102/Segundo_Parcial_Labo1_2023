import pygame, random
from typing import Any
class Estrella(pygame.sprite.Sprite):
    #Metodo
    def __init__(self, link, ancho: int, alto: int) -> None:
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(link), (ancho, alto))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(50, 1000)
        self.rect.y = random.randrange(-500, 0)
        self.velocidad_y = 3

    def update(self) -> None:
        self.rect.y += self.velocidad_y

        if(self.rect.y > 850):
            self.rect.x = random.randrange(50, 950)
            self.rect.y = random.randrange(-500, 0)
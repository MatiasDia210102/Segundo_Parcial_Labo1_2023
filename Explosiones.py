import pygame
from typing import Any

def obtener_imagenes_explosion(ancho: int, alto: int):
    lista_imagenes = []
    for i in range(8):

        lista_imagenes.append(pygame.transform.scale(pygame.image.load(f"Explosion{i}.png"), (ancho, alto)))
    return lista_imagenes

class Explosion(pygame.sprite.Sprite):
    #Metodo
    def __init__(self, center) -> None:
        super().__init__()
        #Atributos
        self.explosion = obtener_imagenes_explosion(150, 150)
        self.fotograma = 0
        self.image = self.explosion[self.fotograma]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.contador = 0
        self.velocidad = 4
        
    def update(self):
        self.contador += 1
        if(self.fotograma < len(self.explosion)-1):
            if(self.contador >= self.velocidad):
                self.contador = 0
                self.fotograma += 1
                self.image = self.explosion[self.fotograma]
        elif(self.fotograma == len(self.explosion)-1):
            self.kill()
            self.fotograma = 0
            
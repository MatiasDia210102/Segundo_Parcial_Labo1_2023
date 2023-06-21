import pygame
from typing import Any

def obtener_imagenes(ancho: int, alto: int):
    lista = [pygame.transform.scale(pygame.image.load("Heroe.png"), (ancho, alto)), 
             pygame.transform.scale(pygame.image.load("Heroe_Izquierda.png"),(ancho, alto)),
             pygame.transform.scale(pygame.image.load("Heroe_Derecha.png"),(ancho, alto)),
             pygame.transform.scale(pygame.image.load("Heroe_Abajo.png"),(ancho, alto))]
    return lista

class Heroe(pygame.sprite.Sprite):
    def __init__(self, ancho: int, alto: int, x: int, y: int, nombre: str) -> None:
        super().__init__()

        self.personaje = obtener_imagenes(ancho, alto)
        self.movimiento = 0
        self.image = self.personaje[self.movimiento]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vidas = 3
        self.nombre = nombre
        self.puntaje = 0
        self.velocidad_x = 0
        self.velocidad_y = 0

    def update(self):
        lista_teclas = pygame.key.get_pressed()

        if True in lista_teclas:

            if(lista_teclas[pygame.K_LEFT]):
                self.velocidad_x = -11
                self.movimiento = 1
            if(lista_teclas[pygame.K_RIGHT]):
                self.velocidad_x = 11
                self.movimiento = 2
            if(lista_teclas[pygame.K_UP]):
                self.velocidad_y = -11
                self.movimiento = 0
            if(lista_teclas[pygame.K_DOWN]):
                self.velocidad_y = 11
                self.movimiento = 3

            self.rect.x += self.velocidad_x
            self.rect.y += self.velocidad_y

            if(self.rect.right > 1020): self.rect.right = 1020
            if(self.rect.left < 0): self.rect.left = 0
            if(self.rect.y > 775): self.rect.y = 775
            if(self.rect.y < 510): self.rect.y = 510

    def dibujar(self, pantalla):
        self.image = self.personaje[self.movimiento]
        pantalla.blit(self.image, self.rect) #(superficie, posicion)
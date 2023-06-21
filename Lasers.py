import pygame, random
from typing import Any
from Heroe import Heroe
from Villanos import Villano

class Laser(pygame.sprite.Sprite):
    def __init__(self, link, ancho, alto: int, clase, x, y, direccion) -> None:
        super().__init__()
        self.image = pygame.image.load(link)
        self.image = pygame.transform.scale(self.image, (ancho, alto))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clase = clase
        self.direccion = direccion

    def update(self) -> None:

        if(self.clase == Heroe): 

            if(self.direccion == 0):
                self.rect.y -= 8
            if(self.direccion == 1):
                self.rect.x -= 8
            if(self.direccion == 2):
                self.rect.x += 8
            if(self.direccion == 3):
                self.rect.y += 8
        elif(self.clase == Villano): 
            self.rect.y += 8

        if(self.rect.y > 850 or self.rect.y < 0 or self.rect.x > 1020 or self.rect.x < 0): 
            self.kill()

def crear_laser(link, clase, ancho, alto, x, y, lista_sprites, lista_lasers, laser_sonido, direccion):
    """
    Que hace: Crea un tipo de laser segun el tipo de personaje recibido
    Que Recibe: Recibe los datos del laser (direccion de imagen, dimensiones, ubicacion, sonido, direccion) y las listas en las que estara el laser
    """
    if(len(link) > 0 and ancho > 0 and alto > 0 and x >= 0 and y >= 0):
        laser = Laser(link, ancho ,alto, clase, x, y, direccion)
        lista_lasers.add(laser)
        lista_sprites.add(laser)
        laser_sonido.play()

def generar_disparo_heroe(heroe, lista_lasers, lista_sprites, laser_sonido):
    """
    Que hace: Crea un laser cada vez que se presiona el mouse
    Que Recibe: Recibe la nave principal, las listas en las que estara el laser y el sonido del laser 
    Que Retorna: Retorna True si no se intento cerrar la ventana y False en caso opuesto
    """
    recorrer = True
    lista_eventos = pygame.event.get()
    for evento in lista_eventos:
        if(evento.type == pygame.QUIT):
            
            recorrer = False
        if(evento.type == pygame.MOUSEBUTTONDOWN):

            crear_laser("Laser.png", Heroe, 8,9, heroe.rect.centerx, heroe.rect.centery, lista_lasers, lista_sprites, laser_sonido, heroe.movimiento)
    return recorrer

def generar_disparo_villanos(lista_villanos, lista_estrellas, lista_lasers, lista_sprites, laser_sonido, tiempo):
    """
    Que hace: Crea un disparo cada vez que un villano colisiona con una estrella en un tiempo determinado
    Que Recibe: Recibe la lista de villanos, de estrellas, las listas en las que estara el laser y los datos de este (direccion de imagen, sonido, direccion)
    """
    lista_villanos_impactados = pygame.sprite.groupcollide(lista_villanos, lista_estrellas, False, False)
    for villano_impactado in lista_villanos_impactados:

        tiempo_entre_disparos = random.randrange(1, 10000)
            
        if(tiempo_entre_disparos <= tiempo*5):
            if(villano_impactado.rect.y > 0):
                crear_laser("Laser_Enemigo.png", Villano, 50, 50, villano_impactado.rect.x+20, villano_impactado.rect.y+30, lista_lasers, lista_sprites, laser_sonido, 0)
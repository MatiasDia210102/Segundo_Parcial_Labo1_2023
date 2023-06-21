import pygame
from typing import Any

def escribir_texto(tipo_de_letra, tamaño: int, texto: str, pantalla, posicion: tuple):
    """
    Que hace:
    Que Recibe: 
    """
    fuente = pygame.font.SysFont(tipo_de_letra, tamaño)
    puntaje_texto = fuente.render(texto, True, (255,255,255)) #(texto, bool, color)
    pantalla.blit(puntaje_texto, posicion)

def leer_imagen(nombre: str, tamaño: tuple):
    """
    Que hace:
    Que Recibe: 
    Que Retorna:
    """
    imagen = pygame.image.load(nombre)
    imagen = pygame.transform.scale(imagen, tamaño) #modifico el tamaño de la imagen 
    return imagen

def definir_sonido(path, volumen_mixer: float, volumen_sonido: float):
    """
    Que hace:
    Que Recibe: 
    Que Retorna:
    """
    pygame.mixer.music.set_volume(volumen_mixer)
    sonido = pygame.mixer.Sound(path)
    sonido.set_volume(volumen_sonido)
    return sonido

def crear_temporizador(tiempo: int, segundos: int)-> int:
    """
    Que hace:
    Que Recibe: 
    Que Retorna:
    """
    tiempo += 1
    if(tiempo == 40):
        tiempo = 0
        segundos += 1
    return segundos, tiempo

def mostrar_pantalla_jugable(pantalla, lista_sprites, heroe, tiempo):
    """
    Que hace:
    Que Recibe: 
    """
    heroe.dibujar(pantalla)
    lista_sprites.update() #Ejecuto cada update de cada clase
    lista_sprites.draw(pantalla)

    escribir_texto("Arial", 30, f"Puntaje: {heroe.puntaje}", pantalla, (0,0))
    escribir_texto("Arial", 30, f"Vidas: {heroe.vidas}", pantalla, (925,0))
    escribir_texto("Arial", 30, f"Tiempo: {tiempo}", pantalla, (425,0))
    
def mostrar_pantalla_inicial(pantalla, fondo_inicio, titulo):

    pantalla.blit(fondo_inicio, (0,0)) #fondo
    pantalla.blit(titulo, (300, 200))
    escribir_texto("Impact", 30, "Presione Enter Para Jugar", pantalla, (370, 400))
    escribir_texto("Impact", 30, "Presione Espacio Para Ver Puntajes", pantalla, (330, 445))
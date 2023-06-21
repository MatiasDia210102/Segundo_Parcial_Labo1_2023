import pygame
from typing import Any
from Estrellas import Estrella
from Villanos import Villano
from Heroe import Heroe
from Explosiones import Explosion
from Lasers import generar_disparo_heroe, generar_disparo_villanos
from Puntajes import escribir_texto, ingresar_usuario, salir_opcion_puntuaciones, terminar_juego

def leer_imagen(nombre: str, tamaño: tuple):
    """
    Que hace: Obtiene una imagen y modifica su tamaño
    Que Recibe: Recibe la direccion de la imagen y el tamaño que tendra
    Que Retorna: Retorna la imagen
    """
    if(len(nombre) > 0 and len(tamaño) > 0):
        imagen = pygame.image.load(nombre)
        imagen = pygame.transform.scale(imagen, tamaño)
    return imagen

def definir_sonido(path, volumen_mixer: float, volumen_sonido: float):
    """
    Que hace: Obtiene un sonido y le asigna un volumen
    Que Recibe: Recibe la direccion del sonido y los volumenes
    Que Retorna: Retorna el sonido
    """
    if(len(path) > 0):
        pygame.mixer.music.set_volume(volumen_mixer)
        sonido = pygame.mixer.Sound(path)
        sonido.set_volume(volumen_sonido)
    return sonido

def crear_temporizador(tiempo: int, tiempo_de_juego: int):
    """
    Que hace: Crea un temporizador para el juego
    Que Recibe: Recibe el tiempo de ejecucion y el tiempo de juego
    Que Retorna: Retorna ambos tiempos
    """
    tiempo += 1
    if(tiempo == 40):
        tiempo = 0
        tiempo_de_juego += 1
    return tiempo_de_juego, tiempo

def mostrar_pantalla_jugable(pantalla, lista_sprites, heroe, tiempo):
    """
    Que hace: Muestra en la pantalla los textos y los personajes del juego
    Que Recibe: Recibe la pantalla de juego, la lista de sprites, la nave principal y el tiempo de juego
    """
    heroe.dibujar(pantalla)
    lista_sprites.draw(pantalla)
    lista_sprites.update()

    escribir_texto("Arial", 30, f"Puntaje: {heroe.puntaje}", pantalla, (0,0))
    escribir_texto("Arial", 30, f"Vidas: {heroe.vidas}", pantalla, (925,0))
    escribir_texto("Arial", 30, f"Tiempo: {tiempo}", pantalla, (425,0))
    pygame.display.flip()
    
def mostrar_pantalla_inicial(pantalla, fondo_inicio, titulo):
    """
    Que hace: Crea la pantalla de inicio
    Que Recibe: Recibe la pantalla, fondo y titulo del juego
    """
    pantalla.blit(fondo_inicio, (0,0)) #fondo
    pantalla.blit(titulo, (300, 200))
    escribir_texto("Impact", 30, "Presione Enter Para Jugar", pantalla, (370, 400))
    escribir_texto("Impact", 30, "Presione Espacio Para Ver Puntajes", pantalla, (330, 445))

def añadir_heroe(ancho, alto, x, y, nombre_heroe, lista_sprites):
    """
    Que hace: Crea y ubica a la nave principal
    Que Recibe: Recibe los datos de la nave principal (dimensiones, ubicacion), nombre del jugador y la lista de sprites
    Que Retorna: Retorna la nave principal
    """
    if(ancho > 0 and alto > 0 and len(nombre_heroe) > 0):
        heroe = Heroe(ancho, alto, x, y, nombre_heroe)
        lista_sprites.add(heroe)
    else:
        heroe = None
    return heroe

def añadir_personajes(clase, path, ancho, alto, cantidad: int, lista_objeto, lista_sprites):
    """
    Que hace: Crea una cantidad de personajes segun la clase y cantidad recibidas
    Que Recibe: Recibe una clase, los datos del personaje (direccion de la imagen, dimensiones), la cantidad de personajes y las listas en la que estara
    """
    if(cantidad > 0 and len(path) > 0):
        for i in range(cantidad):
            objeto = clase(path, ancho, alto)
            lista_objeto.add(objeto)
            lista_sprites.add(objeto)

def generar_primeros_personajes(lista_villanos, lista_estrellas, lista_sprites, nombre_heroe):
    """
    Que hace: Genera a los personajes del juego
    Que Recibe: Recibe las listas personajes, la lista de sprites y el nombre del jugador 
    Que Retorna: Retorna la nave principal
    """
    if(len(nombre_heroe) > 0):
        añadir_personajes(Estrella, "Estrella.png", 5, 4, 150, lista_estrellas, lista_sprites)
        añadir_personajes(Villano, "Enemigo2.png", 65, 65, 10, lista_villanos, lista_sprites)
        heroe = añadir_heroe(80, 80, 550, 700, nombre_heroe, lista_sprites)
    else:
        heroe = None
    return heroe

def generar_villanos_por_tiempo(cantidad: int, lista_villanos, lista_sprites, tiempo):
    """
    Que hace: Crea un numero de personajes cada vez que el jugador elimina a todas las naves enemigas
    Que Recibe: Recibe una clase, la cantidad de enemigos, las listas en la que estaran y el tiempo de juego
    """
    if(len(lista_villanos) == 0 and tiempo < 90):

        añadir_personajes(Villano, "Enemigo.png", 65, 65, cantidad, lista_villanos, lista_sprites)
        añadir_personajes(Villano, "Enemigo2.png", 65, 65, cantidad, lista_villanos, lista_sprites)

def detectar_colisiones(heroe, lista_enemigos, vidas: int, puntaje: int, valor: int, lista_sprites):
    """
    Que hace: Crea una explosion cada vez que el heroe choca con un enemigo, se resta una vida y suma un valor al puntaje
    Que Recibe: Recibe la nave principal con sus datos(vidas, puntaje), el valor a sumar, la lista de enemigos y sprites
    Que Retorna: Retorna las vidas y puntaje
    """
    if(type(heroe) == Heroe and len(lista_enemigos) > 0):
        lista_impactos = pygame.sprite.spritecollide(heroe, lista_enemigos, True)
        
        for impacto in lista_impactos:
            puntaje += valor
            explosion_animada = Explosion(impacto.rect.center)
            explosion_heroe = Explosion(heroe.rect.center)
            explosion = definir_sonido("Explosion.mp3", 0.7, 0.4)
            explosion.play()
            lista_sprites.add(explosion_animada)
            lista_sprites.add(explosion_heroe)
            vidas -= 1
    return vidas, puntaje

def explotar_villanos(lista_lasers, lista_villanos, lista_sprites, laser_sonido, puntaje: int):
    """
    Que hace: Crea una explosion cada vez que un disparo choca con un enemigo y suma 100 al puntaje
    Que Recibe: Recibe la lista de cada grupo (lasers, villanos), la lista de sprites, el sonido del disparo y el puntaje del heroe
    Que Retorna: Retorna el puntaje del jugador
    """
    if(len(lista_lasers) > 0):
        
        lista_naves_impactadas = pygame.sprite.groupcollide(lista_lasers, lista_villanos, True, True)
            
        for nave in lista_naves_impactadas:
            
            laser_sonido.stop()
            explosion = definir_sonido("Explosion.mp3", 0.7, 0.4)
            explosion.play()
                
            explosion_animada = Explosion(nave.rect.center)
            lista_sprites.add(explosion_animada)
            puntaje += 100
    return puntaje

def disparar_a_personajes(heroe, lista_villanos, lista_lasers, lista_lasers_enemigos, lista_sprites, laser_sonido, lista_estrellas, tiempo):
    """
    Que hace: Genera los disparos que realizara cada personaje
    Que Recibe: Recibe la nave principal, todos los grupos de sprites, el sonido de los laseres y el tiempo de juego
    Que Retorna: Retorna el estado de juego
    """
    if(type(heroe) == Heroe and len(lista_villanos) > 0 and len(lista_estrellas) > 0):
        recorrer = generar_disparo_heroe(heroe, lista_lasers, lista_sprites, laser_sonido)
        heroe.puntaje = explotar_villanos(lista_lasers, lista_villanos, lista_sprites, laser_sonido, heroe.puntaje)
        generar_disparo_villanos(lista_villanos, lista_estrellas, lista_lasers_enemigos, lista_sprites, laser_sonido, tiempo)
    return recorrer

def detectar_colisiones_sprites(heroe, lista_villanos, lista_lasers_enemigos, lista_sprites):
    """
    Que hace: Cambia el valor de las vidas y puntajes segun con que choque el jugador
    Que Recibe: Recibe la nave principal, la lista de cada grupo (villanos, lasers_enemigos) y la lista de sprites
    """
    heroe.vidas, heroe.puntaje = detectar_colisiones(heroe, lista_villanos, heroe.vidas, heroe.puntaje, 50, lista_sprites)
    heroe.vidas, heroe.puntaje = detectar_colisiones(heroe, lista_lasers_enemigos, heroe.vidas, heroe.puntaje, 0, lista_sprites)

def iniciar_juego(heroe, lista_villanos, lista_sprites, pantalla, segundos):
    """
    Que hace: 
    Que Recibe: 
    """
    if(type(heroe) == Heroe):
        mostrar_pantalla_jugable(pantalla, lista_sprites, heroe, segundos)
        generar_villanos_por_tiempo(5, lista_villanos, lista_sprites, segundos)

def generar_ataques(heroe, lista_villanos, lista_lasers, lista_lasers_enemigos, lista_estrellas, lista_sprites, laser_sonido, segundos):
    """
    Que hace: Valida que los datos sean recidos correctamente
    Que Recibe: Recibe la nave principal, los grupos de sprites, el sonido del laser y el tiempo de juego
    Que Retorna: Retorna el estado de juego
    """
    if(type(heroe) == Heroe and len(lista_villanos) > 0 and len(lista_estrellas) > 0):
        recorrer = disparar_a_personajes(heroe, lista_villanos, lista_lasers, lista_lasers_enemigos, lista_sprites, laser_sonido, lista_estrellas, segundos)
        detectar_colisiones_sprites(heroe, lista_villanos, lista_lasers_enemigos, lista_sprites)
    else:
        recorrer = False
    return recorrer

def main(pantalla, fondo_inicio, fondo_juego, titulo, sonido_fondo, laser_sonido, lista_puntajes, tiempo_de_juego, tiempo):
    """
    Que hace: Crea todas las listas de sprites y ejecuta el juego
    Que Recibe: Recibe los datos del juego y la lista de puntajes
    """
    pygame.init()
    pygame.mixer.init()
    recorrer = True
    jugando = 0
    while recorrer:
        reloj = pygame.time.Clock()

        if(jugando == 0):
            mostrar_pantalla_inicial(pantalla, fondo_inicio, titulo)
            
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    recorrer = False
                if(evento.type == pygame.KEYDOWN):
                    if(evento.key == pygame.K_RETURN):
                        nombre = ingresar_usuario(pantalla, fondo_inicio)
                        tiempo_de_juego = 0
                        lista_estrellas = pygame.sprite.Group()
                        lista_villanos = pygame.sprite.Group()
                        lista_lasers = pygame.sprite.Group()
                        lista_lasers_enemigos = pygame.sprite.Group()
                        lista_sprites = pygame.sprite.Group()
                        heroe = generar_primeros_personajes(lista_villanos, lista_estrellas, lista_sprites, nombre)
                        sonido_fondo.play(-1)
                        jugando = 1
                    if(evento.key == pygame.K_SPACE):
                        jugando = 2
            pygame.display.flip()
        elif(jugando == 1):
            pantalla.blit(fondo_juego, (0,0))
            reloj.tick(80)
            tiempo_de_juego, tiempo = crear_temporizador(tiempo, tiempo_de_juego)
            iniciar_juego(heroe, lista_villanos, lista_sprites, pantalla, tiempo_de_juego)
            recorrer = generar_ataques(heroe, lista_villanos, lista_lasers, lista_lasers_enemigos, lista_estrellas, lista_sprites, laser_sonido, tiempo_de_juego)
            jugando = terminar_juego(tiempo_de_juego, heroe, jugando, sonido_fondo, lista_puntajes)
        elif(jugando == 2):
            pantalla.blit(fondo_juego, (0,0))
            jugando = salir_opcion_puntuaciones(pantalla, jugando)
    pygame.quit()
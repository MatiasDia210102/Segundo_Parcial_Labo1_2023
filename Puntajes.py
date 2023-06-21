import pygame, re, json
from typing import Any

def escribir_texto(tipo_de_letra, tamaño: int, texto: str, pantalla, posicion: tuple):
    """
    Que hace: Escribe el texto recibido en la pantalla
    Que Recibe: Recibe el tipo de letra, tamaño del texto recibido, la pantalla y posicion donde estara el texto
    """
    if(len(tipo_de_letra) > 0 and tamaño > 0 and len(texto) > 0):
        fuente = pygame.font.SysFont(tipo_de_letra, tamaño)
        puntaje_texto = fuente.render(texto, True, (255,255,255)) #(texto, bool, color)
        pantalla.blit(puntaje_texto, posicion)

def ingresar_usuario(pantalla, fondo):
    """
    Que hace: Pide al jugador que ingrese su nombre de usuario
    Que Recibe: Recibe la pantalla y el fondo del juego
    Que Retorna: Retorna el nombre de usuario
    """
    pygame.init()
    nombre_usuario = ""
    rectangulo_ingreso = pygame.Rect(400, 450, 200, 60)
    recorrer = True

    while recorrer:
        pantalla.blit(fondo, (0,0))
        escribir_texto("Impact", 30, "Ingrese su usuario", pantalla, (390, 400))

        for evento in pygame.event.get():
            if(evento.type == pygame.QUIT):
                pygame.quit() 
            if(evento.type == pygame.KEYDOWN):
                
                if(evento.key == pygame.K_BACKSPACE):

                    nombre_usuario = nombre_usuario[0:-1]
                elif(evento.key == pygame.K_RETURN and len(nombre_usuario) >= 3):

                    recorrer = False
                else:

                    if(len(nombre_usuario) < 13):
                        nombre_usuario += evento.unicode
                
        pygame.draw.rect(pantalla, (255, 255, 0), rectangulo_ingreso, 2)
        escribir_texto("Arial", 30, nombre_usuario, pantalla, (rectangulo_ingreso.x+5, rectangulo_ingreso.y+5))
        pygame.display.flip()
    return nombre_usuario

def guardar_archivo(nombre: str, nombre_usuario: str, puntos: int, jugadores: dict):
    """
    Que hace: Abre o crea un archivo en escritura y guarda el contenido 
    Que Recibe: Recibe el nombre que tiene o tendra el archivo, el contendo a escribir y un diccionario
    """
    if(len(nombre) > 0 and len(nombre_usuario) > 0):

        jugadores['jugador'].append({"nombre": nombre_usuario})
        jugadores['jugador'].append({"puntos": puntos})

        with open(nombre, 'w') as archivo:
            json.dump(jugadores, archivo, indent=4)

def leer_archivo(archivo: str)-> list:
    """
    Que hace: Abre un archivo json en lectura, se accede a los datos y se los guarda en a lista de diccionarios
    Que Recibe: Recibe el nombre que tiene el archivo
    Que Retorna: Retorna la lista de jugadores ordenada
    """
    if(len(archivo) > 0):
  
        with open(archivo, "r")as archivo:
            lista_puntos = []
            todo = archivo.read()
            nombre = re.findall(r'"nombre": "([a-zA-Z0-9 ]+)', todo)
            puntos = re.findall(r'"puntos": ([0-9]+)', todo)

            for i in range(len(nombre)):
                puntajes = {}
                puntajes["nombre"] = nombre[i]
                puntajes["puntos"] = int(puntos[i])
                lista_puntos.append(puntajes)
        lista_puntos.sort(key= lambda diccionario: diccionario["puntos"], reverse= True)  
    return lista_puntos

def generar_rankin_puntuaciones(pantalla):
    """
    Que hace: Escribe en la pantalla los datos del jugador (nombre de usuario y puntaje)
    Que Recibe: Recibe la pantalla en la que se escribira
    """
    pygame.init()
    lista_puntajes = leer_archivo("jugadores.json") 
    escribir_texto("Calibri", 30, "Presione espacio para volver", pantalla, (350, 370))

    if(len(lista_puntajes) > 0):
        for i in range(len(lista_puntajes)):
            escribir_texto("Calibri", 24, lista_puntajes[i]["nombre"], pantalla, (450, 410+(i*25)))
            escribir_texto("Calibri", 24, str(lista_puntajes[i]["puntos"]), pantalla, (350, 410+(i*25)))

def salir_opcion_puntuaciones(pantalla, jugando):
    """
    Que hace: Muestra el ranking de puntuaciones
    Que Recibe: Recibe la pantalla de juego y el estado de juego
    Que Retorna: Retorna el estado de juego
    """
    pygame.init()
    generar_rankin_puntuaciones(pantalla)

    for evento in pygame.event.get():

        if(evento.type == pygame.QUIT):
            pygame.quit() # Cierra la ventana de pygame

        if(evento.type == pygame.KEYDOWN):
            if(evento.key == pygame.K_SPACE):
                jugando = 0
    pygame.display.flip()
    return jugando

def terminar_juego(tiempo, heroe, jugando, sonido_fondo, lista_puntajes):
    """
    Que hace: Termina el juego cuando el jugador pierda todas las vidas o cuando termine el tiempo
    Que Recibe: Recibe el tiempo, la nave principal, el estado de juego y la lista de puntajes
    Que Retorna:
    """
    if(tiempo == 90 or heroe.vidas <= 0):
        jugando = 0
        sonido_fondo.stop()
        guardar_archivo("jugadores.json", heroe.nombre, heroe.puntaje, lista_puntajes)
    return jugando
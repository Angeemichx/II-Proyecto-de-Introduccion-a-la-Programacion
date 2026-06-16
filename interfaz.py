import pygame

#Se utiliza init para que las funciones dentro de pygame puedan funcionar 
pygame.init()

#Se desarrollan ciertas variables que se utilizaran constantemente con el fin de facilitar su modificación de ser necesario
ANCHO = 1280
ALTO = 720
ROJO = (255, 0, 0)
NEGRO = (0,0,0)
VERDE = (0, 255, 0)

#variables para chef 1
chef1_pos_x = 10
chef1_pos_y = 10
chef1_velocidad_x = 0
chef1_velocidad_y = 0

#variables para el chef 2
chef2_pos_x = 10
chef2_pos_y = 10
chef2_velocidad_x = 0
chef2_velocidad_y = 0

#Con esto, se crea la ventana principal 
ventana = pygame.display.set_mode((ANCHO, ALTO), pygame.FULLSCREEN) 
reloj = pygame.time.Clock()

#imágenes 
menu = pygame.image.load("menu.png")
mapa_1 = pygame.image.load("mapa_1.png").convert()
mapa_2 = pygame.image.load("mapa_2.png").convert()
mapa_3 = pygame.image.load("mapa_3.png").convert()
chef1_a = pygame.image.load("chef1_a.png").convert()
chef1_b = pygame.image.load("chef1_b.png").convert()
chef1_c = pygame.image.load("chef1_c.png").convert()
chef1_d = pygame.image.load("chef1_d.png").convert()
chef2_a = pygame.image.load("chef2_a.png").convert()
chef2_b = pygame.image.load("chef2_b.png").convert()
chef2_c = pygame.image.load("chef2_c.png").convert()
chef2_d = pygame.image.load("chef2_d.png").convert()


#Esta función permite que la pantalla no se cierre mientras se está jugando, además se añade la x superior derecha y la tecla esc para cerrar la ventana (salir del bucle)
jugando = True 

while jugando:

    reloj.tick(60)

    for event in pygame.event.get():
        print(event)
        if event.type == pygame.QUIT:
            jugando = False 

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                jugando = False 

            #Controles cuando se presiona una tecla
            if event.key == pygame.K_d:
                chef1_velocidad_x = 10

            if event.key == pygame.K_a:
                chef1_velocidad_x = -10

            if event.key == pygame.K_s:
                chef1_velocidad_y = 10

            if event.key == pygame.K_w:
                chef1_velocidad_y = -10
        
        #Controles cuando se suelta una tecla 
        if event.type == pygame.KEYUP:
        
            if event.key == pygame.K_d:
                chef1_velocidad_x = 0

            if event.key == pygame.K_a:
                chef1_velocidad_x = 0

            if event.key == pygame.K_s:
                chef1_velocidad_y = 0

            if event.key == pygame.K_w:
                chef1_velocidad_y = 0

#Lógica 
    chef1_pos_x += chef1_velocidad_x
    chef1_pos_y += chef1_velocidad_y
    chef2_pos_x += chef2_velocidad_x
    chef2_pos_y += chef2_velocidad_y

#Se configurarán los dibujos de la pantalla
    ventana.blit(mapa_1, (0,0))
    ventana.blit(chef1_a, (chef1_pos_x, chef1_pos_y))
    ventana.blit(chef1_b, (chef1_pos_x, chef1_pos_y))
    ventana.blit(chef1_c, (chef1_pos_x, chef1_pos_y))
    ventana.blit(chef1_d, (chef1_pos_x, chef1_pos_y))
    ventana.blit(chef2_a, (chef2_pos_x, chef2_pos_y))
    ventana.blit(chef2_b, (chef2_pos_x, chef2_pos_y))
    ventana.blit(chef2_c, (chef2_pos_x, chef2_pos_y))
    ventana.blit(chef2_d, (chef2_pos_x, chef2_pos_y))

#Actualizar (se produce lo guardado en memoria)
    pygame.display.update()

#Permitir que el juego tenga un final y no se ejecuten las funciones para siempre en el bucle
pygame.quit()

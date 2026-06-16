import pygame

#Se utiliza init para que las funciones dentro de pygame puedan funcionar 
pygame.init()

#Se desarrollan ciertas variables que se utilizaran constantemente con el fin de facilitar su modificación de ser necesario
ANCHO = 1280
ALTO = 720
ROJO = (255, 0, 0)
NEGRO = (0,0,0)
VERDE = (0, 255, 0)
personaje_pos_x = 10
personaje_pos_y = 10
personaje_velocidad_x = 0
personaje_velocidad_y = 0

#Con esto, se crea la ventana principal 
ventana = pygame.display.set_mode((ANCHO, ALTO), pygame.FULLSCREEN) 
reloj = pygame.time.Clock()

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
                personaje_velocidad_x = 10

            if event.key == pygame.K_a:
                personaje_velocidad_x = -10

            if event.key == pygame.K_s:
                personaje_velocidad_y = 10

            if event.key == pygame.K_w:
                personaje_velocidad_y = -10
        
        #Controles cuando se suelta una tecla 
        if event.type == pygame.KEYUP:
        
            if event.key == pygame.K_d:
                personaje_velocidad_x = 0

            if event.key == pygame.K_a:
                personaje_velocidad_x = 0

            if event.key == pygame.K_s:
                personaje_velocidad_y = 0

            if event.key == pygame.K_w:
                personaje_velocidad_y = 0

#Lógica 
    personaje_pos_x += personaje_velocidad_x
    personaje_pos_y += personaje_velocidad_y

#Se configurarán los dibujos de la pantalla
    ventana.fill(ROJO)
    pygame.draw.rect(ventana, VERDE, (personaje_pos_x, personaje_pos_y ,100,100))

#Actualizar (se produce lo guardado en memoria)
    pygame.display.update()

#Permitir que el juego tenga un final y no se ejecuten las funciones para siempre en el bucle
pygame.quit()

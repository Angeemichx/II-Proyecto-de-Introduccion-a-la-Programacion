import pygame
from logica import Chef, VegetalesYFrutas, PanesYBases, Proteina, Papas

# ChefControlado
# Extiende la clase Chef con todo lo necesario para moverse en pantalla, colisionar con estaciones y dibujarse en la ventana de Pygame
class ChefControlado(Chef):
    def __init__(self, nombre, imagenes, pos_x, pos_y):
        super().__init__(nombre)

        self.imagenes = imagenes         # Diccionario con imágenes por dirección: arriba,abajo,izquierda,derecha
        self.pos_x = pos_x               # Posición horizontal en píxeles
        self.pos_y = pos_y               # Posición vertical en píxeles
        self.direccion = "abajo"         # Última dirección en que miró el chef
        self.velocidad_x = 0             # (Reservado) velocidad horizontal
        self.velocidad_y = 0             # (Reservado) velocidad vertical
        self.activo = False              # True si este chef es el que controla el jugador ahora
        self.velocidad_movimiento = 5    # Píxeles que avanza por frame
        self.ancho = 200                 # Ancho de la hitbox visual del chef
        self.alto = 200                  # Alto de la hitbox visual del chef
        self.plato_sostenido = None      # Nombre de la mesa a la que el chef "asignó" ingredientes (Mesa A o Mesa B)

    def mover(self, teclas, limites, estaciones_colision):
        #Mueve al chef según las teclas WASD presionadas, limites: tupla (x_min, y_min, x_max, y_max) para no salir de pantalla.
        #estaciones_colision: lista de pygame.Rect que el chef no puede atravesar
        
        dx, dy = 0, 0

        if teclas[pygame.K_w]:
            dy = -self.velocidad_movimiento
            self.direccion = "arriba"
        elif teclas[pygame.K_s]:
            dy = self.velocidad_movimiento
            self.direccion = "abajo"
        elif teclas[pygame.K_a]:
            dx = -self.velocidad_movimiento
            self.direccion = "izquierda"
        elif teclas[pygame.K_d]:
            dx = self.velocidad_movimiento
            self.direccion = "derecha"

        # ── Movimiento horizontal ──
        nueva_x = self.pos_x + dx
        # Clampear dentro de los límites de pantalla
        nueva_x = max(limites[0], min(nueva_x, limites[2] - self.ancho))
        # Solo mover si no colisiona con ninguna estación
        if not self._colisiona_con_estaciones(nueva_x, self.pos_y, estaciones_colision):
            self.pos_x = nueva_x

        # ── Movimiento vertical ──
        nueva_y = self.pos_y + dy
        nueva_y = max(limites[1], min(nueva_y, limites[3] - self.alto))
        if not self._colisiona_con_estaciones(self.pos_x, nueva_y, estaciones_colision):
            self.pos_y = nueva_y

    def _colisiona_con_estaciones(self, x, y, estaciones):
        """
        Devuelve True si la hitbox del chef en la posición (x, y)
        se superpone con algún rect de estación.
        La hitbox del chef es más pequeña que su imagen (offsets de 60 y 80 px).
        """
        rect = pygame.Rect(x + 60, y + 80, 80, 100)
        return any(rect.colliderect(e) for e in estaciones)

    def dibujar(self, ventana, resaltar=False):
        """
        Dibuja al chef en la ventana:
        - Su imagen según la dirección que mira.
        - Un borde amarillo si está activo (resaltar=True).
        - El ingrediente que lleva en la mano (texto sobre la cabeza).
        - El plato que está ensamblando, si tiene uno asignado.
        """
        # Dibujar la imagen del chef
        ventana.blit(self.imagenes[self.direccion], (self.pos_x, self.pos_y))

        # Borde de resalte para indicar cuál chef controla el jugador
        if resaltar:
            rect_resalte = pygame.Rect(self.pos_x + 55, self.pos_y + 75, 90, 110)
            pygame.draw.rect(ventana, (255, 255, 0), rect_resalte, 3)

        # Mostrar ingrediente en la mano encima del chef
        if self.ingrediente:
            fuente = pygame.font.SysFont("Arial", 18)
            txt = f"{self.ingrediente.nombre} [{self.ingrediente.estado}]"
            color = (255, 220, 0)
            texto = fuente.render(txt, True, color)
            ventana.blit(texto, (self.pos_x + 50, self.pos_y - 20))

        # Mostrar qué plato está ensamblando (Mesa A o Mesa B)
        if self.plato_sostenido:
            fuente = pygame.font.SysFont("Arial", 16)
            txt = f"Sosteniendo: {self.plato_sostenido}"
            color = (255, 165, 0)
            texto = fuente.render(txt, True, color)
            ventana.blit(texto, (self.pos_x + 20, self.pos_y - 40))

    def obtener_rect_interaccion(self):
        """
        Devuelve el rect que se usa para detectar si el chef
        está lo suficientemente cerca de una estación para interactuar.
        Es un poco más grande que la hitbox de colisión.
        """
        return pygame.Rect(self.pos_x + 40, self.pos_y, 120, 250)
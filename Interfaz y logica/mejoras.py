import pygame
from logica import Chef, VegetalesYFrutas, PanesYBases, Proteina, Papas

class ChefControlado(Chef):
    def __init__(self, nombre, imagenes, pos_x, pos_y):
        super().__init__(nombre)
        self.imagenes = imagenes
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.direccion = "abajo"
        self.velocidad_x = 0
        self.velocidad_y = 0
        self.activo = False
        self.velocidad_movimiento = 5
        self.ancho = 200
        self.alto = 200
        self.plato_sostenido = None
        
    def mover(self, teclas, limites, estaciones_colision):
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
            
        nueva_x = self.pos_x + dx
        nueva_x = max(limites[0], min(nueva_x, limites[2] - self.ancho))
        if not self._colisiona_con_estaciones(nueva_x, self.pos_y, estaciones_colision):
            self.pos_x = nueva_x
            
        nueva_y = self.pos_y + dy
        nueva_y = max(limites[1], min(nueva_y, limites[3] - self.alto))
        if not self._colisiona_con_estaciones(self.pos_x, nueva_y, estaciones_colision):
            self.pos_y = nueva_y

    def _colisiona_con_estaciones(self, x, y, estaciones):
        rect = pygame.Rect(x + 60, y + 80, 80, 100)
        return any(rect.colliderect(e) for e in estaciones)
    
    def dibujar(self, ventana, resaltar=False):
        ventana.blit(self.imagenes[self.direccion], (self.pos_x, self.pos_y))
        
        if resaltar:
            s = pygame.Surface((self.ancho - 20, self.alto - 20), pygame.SRCALPHA)
            s.fill((255, 255, 0, 50))
            ventana.blit(s, (self.pos_x + 10, self.pos_y + 10))
            
        if self.ingrediente:
            fuente = pygame.font.SysFont("Arial", 18)
            txt = f"{self.ingrediente.nombre} [{self.ingrediente.estado}]"
            color = (255, 220, 0)
            texto = fuente.render(txt, True, color)
            ventana.blit(texto, (self.pos_x + 50, self.pos_y - 20))
        
        if self.plato_sostenido:
            fuente = pygame.font.SysFont("Arial", 16)
            txt = f"Sosteniendo: {self.plato_sostenido}"
            color = (255, 165, 0)
            texto = fuente.render(txt, True, color)
            ventana.blit(texto, (self.pos_x + 20, self.pos_y - 40))
            
    def obtener_rect_interaccion(self):
        return pygame.Rect(self.pos_x + 40, self.pos_y, 120, 250)
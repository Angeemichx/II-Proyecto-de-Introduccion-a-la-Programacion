import random
from collections import Counter

class Ingrediente:
    def __init__(self, nombre, estado="crudo"):
        self.nombre = nombre
        self.estado = estado

    def __str__(self):
        return f"{self.nombre} ({self.estado})"


class VegetalesYFrutas(Ingrediente):
    def __init__(self, nombre):
        super().__init__(nombre, estado="crudo")

    def cortar(self):
        self.estado = "preparado"


class PanesYBases(Ingrediente):
    def __init__(self, nombre):
        super().__init__(nombre, estado="listo")


class Proteina(Ingrediente):
    def __init__(self, nombre):
        super().__init__(nombre, estado="crudo")
        self.tiempo_coccion = 0
        self.tiempo_minimo = 3
        self.tiempo_maximo = 8

    def cocinar(self, delta):
        self.tiempo_coccion += delta
        if self.tiempo_coccion >= self.tiempo_maximo:
            self.estado = "quemado"
        elif self.tiempo_coccion >= self.tiempo_minimo:
            self.estado = "preparado"


class Papas(Ingrediente):
    def __init__(self):
        super().__init__("Papas", estado="crudo")
        self.tiempo_fritura = 0
        self.tiempo_minimo = 3

    def freir(self, delta):
        self.tiempo_fritura += delta
        if self.tiempo_fritura >= self.tiempo_minimo:
            self.estado = "preparado"


class Estacion:
    def __init__(self, nombre, ingredientes_aceptados, tipo):
        self.nombre = nombre
        self.ingredientes_aceptados = ingredientes_aceptados
        self.tipo = tipo

    def __str__(self):
        return self.nombre


class Chef:
    def __init__(self, nombre):
        self.nombre = nombre
        self.puntos = 0
        self.ingrediente = None

    def recoger(self, ingrediente):
        if self.ingrediente is None:
            self.ingrediente = ingrediente
            return True
        return False

    def soltar(self):
        ing = self.ingrediente
        self.ingrediente = None
        return ing

    def sumar_puntos(self, puntos):
        self.puntos = max(0, self.puntos + puntos)

    def __str__(self):
        return f"{self.nombre} - Puntos: {self.puntos}"


class Receta:
    def __init__(self, nombre, ListaIngredientes, PuntosReceta, MaxTimeReceta):
        self.nombre = nombre
        self.ListaIngredientes = ListaIngredientes
        self.PuntosReceta = PuntosReceta
        self.MaxTimeReceta = MaxTimeReceta
        self.tiempo_transcurrido = 0
        self.puntos_actuales = PuntosReceta

    def actualizar_tiempo(self, delta):
        self.tiempo_transcurrido += delta
        if self.tiempo_transcurrido >= self.MaxTimeReceta:
            self.puntos_actuales = max(0, self.puntos_actuales // 2)
            self.tiempo_transcurrido = 0

    def CompararReceta(self, ingredientes_entregados):
        requeridos = Counter()
        for req in self.ListaIngredientes:
            requeridos[(req["nombre"], req["estado"])] += 1
        
        entregados = Counter()
        for ing in ingredientes_entregados:
            entregados[(ing.nombre, ing.estado)] += 1

        print("REQUERIDOS: ", requeridos)
        print("ENTREGADOS: ", entregados)
        
        return requeridos == entregados

    def __str__(self):
        return f"{self.nombre} - {self.puntos_actuales} pts"


class Cocina:
    def __init__(self, tiempo, chefs, recetas_posibles):
        self.tiempo = tiempo
        self.tiempo_restante = tiempo
        self.chefs = chefs
        self.ordenes = []
        self.recetas_posibles = recetas_posibles
        self.max_ordenes = 3
        self.intervalo_generacion = 25
        self.tiempo_desde_ultima = 0

    def GenerarReceta(self):
        if len(self.ordenes) < self.max_ordenes:
            receta = random.choice(self.recetas_posibles)
            nueva = Receta(
                receta.nombre,
                receta.ListaIngredientes,
                receta.PuntosReceta,
                receta.MaxTimeReceta
            )
            self.ordenes.append(nueva)

    def actualizar(self, delta):
        self.tiempo_restante -= delta
        self.tiempo_desde_ultima += delta

        if self.tiempo_desde_ultima >= self.intervalo_generacion:
            self.GenerarReceta()
            self.tiempo_desde_ultima = 0

        for orden in self.ordenes[:]:
            orden.actualizar_tiempo(delta)
            if orden.puntos_actuales <= 0:
                self.chefs[0].sumar_puntos(-orden.PuntosReceta)
                self.ordenes.remove(orden)

    def entregar(self, ingredientes_entregados):
        ordenes_coincidentes = []
        for orden in self.ordenes:
            if orden.CompararReceta(ingredientes_entregados):
                ordenes_coincidentes.append(orden)
        
        if ordenes_coincidentes:
            orden = min(ordenes_coincidentes, key=lambda o: o.MaxTimeReceta - o.tiempo_transcurrido)
            self.chefs[0].sumar_puntos(orden.puntos_actuales)
            self.ordenes.remove(orden)
            return orden.nombre
        else:
            self.chefs[0].sumar_puntos(-10)
        return None

    def juego_terminado(self):
        return self.tiempo_restante <= 0


recetas_nivel1 = [
    Receta("Ensalada de Frutas", [
        {"nombre": "Banano",  "estado": "preparado"},
        {"nombre": "Fresa",   "estado": "preparado"},
        {"nombre": "Mango",   "estado": "preparado"},
    ], PuntosReceta=30, MaxTimeReceta=60),

    Receta("Ensalada de Pollo", [
        {"nombre": "Pollo",   "estado": "preparado"},
        {"nombre": "Lechuga", "estado": "preparado"},
    ], PuntosReceta=40, MaxTimeReceta=90),
]

recetas_nivel2 = [
    Receta("Perro Caliente", [
        {"nombre": "Pan",      "estado": "listo"},
        {"nombre": "Salchicha","estado": "preparado"},
    ], PuntosReceta=30, MaxTimeReceta=60),

    Receta("Perro con Repollo", [
        {"nombre": "Pan",      "estado": "listo"},
        {"nombre": "Salchicha","estado": "preparado"},
        {"nombre": "Repollo",  "estado": "preparado"},
    ], PuntosReceta=40, MaxTimeReceta=75),

    Receta("Perro con Papas", [
        {"nombre": "Pan",      "estado": "listo"},
        {"nombre": "Salchicha","estado": "preparado"},
        {"nombre": "Papas",    "estado": "preparado"},
    ], PuntosReceta=40, MaxTimeReceta=75),

    Receta("Perro Completo", [
        {"nombre": "Pan",      "estado": "listo"},
        {"nombre": "Salchicha","estado": "preparado"},
        {"nombre": "Repollo",  "estado": "preparado"},
        {"nombre": "Papas",    "estado": "preparado"},
    ], PuntosReceta=60, MaxTimeReceta=90),
]

recetas_nivel3 = [
    Receta("Empanada de Pollo", [
        {"nombre": "Empanada", "estado": "listo"},
        {"nombre": "Pollo",    "estado": "preparado"},
    ], PuntosReceta=40, MaxTimeReceta=90),

    Receta("Empanada Arreglada", [
        {"nombre": "Empanada", "estado": "listo"},
        {"nombre": "Pollo",    "estado": "preparado"},
        {"nombre": "Repollo",  "estado": "preparado"},
    ], PuntosReceta=50, MaxTimeReceta=100),

    Receta("Empanada de Queso", [
        {"nombre": "Empanada", "estado": "listo"},
        {"nombre": "Queso",    "estado": "listo"},
    ], PuntosReceta=30, MaxTimeReceta=60),

    Receta("Salchipapas", [
        {"nombre": "Salchicha","estado": "preparado"},
        {"nombre": "Papas",    "estado": "preparado"},
    ], PuntosReceta=35, MaxTimeReceta=70),
]
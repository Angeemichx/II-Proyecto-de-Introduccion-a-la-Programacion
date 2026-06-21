class Ingrediente:
    def __init__(self, nombre):
        self.nombre = nombre
        self.cortado = False
        self.cocinado = False
        self.frito = False

    def cortar(self):
        self.cortado = True

    def cocinar(self):
        self.cocinado = True

    def freir(self):
        self.frito = True

    def __str__(self):
        return self.nombre


class Receta:
    def __init__(self, nombre, requisitos):
        """
        requisitos = {
            "Ingrediente": {
                "cortado": True/False,
                "cocinado": True/False,
                "frito": True/False
            }
        }
        """
        self.nombre = nombre
        self.requisitos = requisitos

    def plato_terminado(self, ingredientes):

        for nombre_requerido, estados_requeridos in self.requisitos.items():

            ingrediente = None

            for ing in ingredientes:
                if ing.nombre == nombre_requerido:
                    ingrediente = ing
                    break

            if ingrediente is None:
                return False

            if ingrediente.cortado != estados_requeridos["cortado"]:
                return False

            if ingrediente.cocinado != estados_requeridos["cocinado"]:
                return False

            if ingrediente.frito != estados_requeridos["frito"]:
                return False

        return True


# ======================
# INGREDIENTES
# ======================

banano = Ingrediente("Banano")
fresa = Ingrediente("Fresa")
mango = Ingrediente("Mango")

pollo = Ingrediente("Pollo")
lechuga = Ingrediente("Lechuga")

pan = Ingrediente("Pan")
salchicha = Ingrediente("Salchicha")
repollo = Ingrediente("Repollo")
papas = Ingrediente("Papas")

empanada = Ingrediente("Empanada")
queso = Ingrediente("Queso")


# ======================
# RECETAS NIVEL 1
# ======================

ensalada_frutas = Receta(
    "Ensalada de Frutas",
    {
        "Banano": {"cortado": True, "cocinado": False, "frito": False},
        "Fresa": {"cortado": True, "cocinado": False, "frito": False},
        "Mango": {"cortado": True, "cocinado": False, "frito": False}
    }
)

ensalada_pollo = Receta(
    "Ensalada de Pollo",
    {
        "Pollo": {"cortado": True, "cocinado": True, "frito": False},
        "Lechuga": {"cortado": True, "cocinado": False, "frito": False}
    }
)


# ======================
# RECETAS NIVEL 2
# ======================

perro_caliente = Receta(
    "Perro Caliente",
    {
        "Pan": {"cortado": False, "cocinado": False, "frito": False},
        "Salchicha": {"cortado": False, "cocinado": True, "frito": False}
    }
)

perro_repollo = Receta(
    "Perro con Repollo",
    {
        "Pan": {"cortado": False, "cocinado": False, "frito": False},
        "Salchicha": {"cortado": False, "cocinado": True, "frito": False},
        "Repollo": {"cortado": True, "cocinado": False, "frito": False}
    }
)

perro_papas = Receta(
    "Perro con Papas",
    {
        "Pan": {"cortado": False, "cocinado": False, "frito": False},
        "Salchicha": {"cortado": False, "cocinado": True, "frito": False},
        "Papas": {"cortado": False, "cocinado": False, "frito": True}
    }
)

perro_completo = Receta(
    "Perro Completo",
    {
        "Pan": {"cortado": False, "cocinado": False, "frito": False},
        "Salchicha": {"cortado": False, "cocinado": True, "frito": False},
        "Repollo": {"cortado": True, "cocinado": False, "frito": False},
        "Papas": {"cortado": False, "cocinado": False, "frito": True}
    }
)


# ======================
# RECETAS NIVEL 3
# ======================

empanada_pollo = Receta(
    "Empanada de Pollo",
    {
        "Empanada": {"cortado": False, "cocinado": False, "frito": True},
        "Pollo": {"cortado": True, "cocinado": True, "frito": False}
    }
)

empanada_arreglada = Receta(
    "Empanada Arreglada",
    {
        "Empanada": {"cortado": False, "cocinado": False, "frito": True},
        "Pollo": {"cortado": True, "cocinado": True, "frito": False},
        "Repollo": {"cortado": True, "cocinado": False, "frito": False}
    }
)

empanada_queso = Receta(
    "Empanada de Queso",
    {
        "Empanada": {"cortado": False, "cocinado": False, "frito": True},
        "Queso": {"cortado": False, "cocinado": False, "frito": False}
    }
)

salchipapas = Receta(
    "Salchipapas",
    {
        "Salchicha": {"cortado": True, "cocinado": True, "frito": False},
        "Papas": {"cortado": False, "cocinado": False, "frito": True}
    }
)


# ======================
# EJEMPLO DE USO
# ======================

banano.cortar()
fresa.cortar()
mango.cortar()

ingredientes_plato = [banano, fresa, mango]

if ensalada_frutas.plato_terminado(ingredientes_plato):
    print("Plato terminado")
else:
    print("Plato incorrecto")
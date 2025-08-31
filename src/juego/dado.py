from src.servicios.generador_aleatorio import GeneradorAleatorio

class Dado:
    denominaciones = {
        1: "As",
        2: "Tonto",
        3: "Tren",
        4: "Cuadra",
        5: "Quina",
        6: "Sexto"
    }

    plurales = {
        1: "Ases",
        2: "Tontos",
        3: "Trenes",
        4: "Cuadras",
        5: "Quinas",
        6: "Sextos"
    }

    def __init__(self):
       self.valor_actual = None

    def lanzar(self):
        self.valor_actual = GeneradorAleatorio.generar_valor_aleatorio()

    @staticmethod
    def get_nombre_pinta(num_pinta: int, cantidad: int = 1):
        if cantidad == 1:
            return Dado.denominaciones[num_pinta]
        else:
            return Dado.plurales[num_pinta]




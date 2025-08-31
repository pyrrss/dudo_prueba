from src.juego.cacho import Cacho
from src.juego.contador_pintas import ContadorPintas

class ArbitroRonda:
    def __init__(self):
        self.contador_pintas = ContadorPintas()

    # NOTE: se puede evaluar si es que es útil que este método devuelva el cacho perdedor
    def manejar_duda(self, lista_cachos: list[Cacho], apuesta: tuple[int, int], apostador: Cacho, dudador: Cacho, ronda_especial: bool = False) -> Cacho:
        # TODO: ver cómo manejar luego rondas especiales donde no se cuenten los ases acá
        cantidad_total = self._contar_total(lista_cachos, apuesta[1])

        # NOTE: se devuelve cacho que perdió un dado
        # (puede ser útil para decir quién perdió un dado en GestorPartida)
        if cantidad_total >= apuesta[0]:
            dudador.quitar_dado()
            return dudador
        else:
            apostador.quitar_dado()
            return apostador

    # NOTE: apostador no está siendo usado 
    def manejar_calzar(self, lista_cachos: list[Cacho], apuesta: tuple[int, int], apostador: Cacho, calzador: Cacho, ronda_especial: bool = False) -> bool:
        cantidad_total = self._contar_total(lista_cachos, apuesta[1])

        if cantidad_total == apuesta[0]:
            calzador.agregar_dado()
            return True
        else:
            calzador.quitar_dado()
            return False

    def _contar_total(self, lista_cachos: list[Cacho], pinta: int, ronda_especial: bool = False) -> int:
        lista_valores = []
        for cacho in lista_cachos:
            for dado in cacho.dados:
                lista_valores.append(dado.valor_actual)
        
        # -> si ronda_especial es True, luego ases_comodines = False, y viceversa
        cantidad_total = self.contador_pintas.contar_apariciones(lista_valores, pinta, not ronda_especial)
        return cantidad_total

    def puede_calzar(self, lista_cachos: list[Cacho], calzador: Cacho) -> bool:
        if calzador.get_cantidad_dados() == 1:
            return True

        # NOTE: se asume que cada jugador siempre parte con 5 dados
        cantidad_inicial_dados = len(lista_cachos) * 5

        dados_en_juego = 0
        for cacho in lista_cachos:
            dados_en_juego += cacho.get_cantidad_dados()

        # TODO: corroborar si se puede con mitad de dados o menos,
        # o debe ser exactamente la mitad, o más de la mitad?
        return dados_en_juego <= cantidad_inicial_dados // 2

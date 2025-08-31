from src.juego.arbitro_ronda import ArbitroRonda
from src.juego.contador_pintas import ContadorPintas
from src.juego.cacho import Cacho

import pytest

class TestArbitroRonda:

    @pytest.mark.parametrize("lista_valores",[
            [1, 4, 3, 6, 2, 4, 4, 6, 5, 5],
            [5, 5, 1, 2, 4, 3, 6, 2, 4, 4],
            [6, 6, 1, 4, 3, 2, 5, 3, 4, 6]
        ])
    def test_jugador_duda_incorrectamente_y_pierde_dado(self, lista_valores):
        """
        se verifica que cuando un jugador duda sobre una apuesta
        y esta sí se cumple, el que duda pierde un dado
        """
        cacho_a = Cacho()
        cacho_b = Cacho()
        cacho_a.set_valores_dados(lista_valores[:5])
        cacho_b.set_valores_dados(lista_valores[5:])

        # DEBUG
        print(f"Cantidad dados cacho_a: {cacho_a.get_cantidad_dados()}")
        print(f"Valores dados cacho_a: {cacho_a.get_valores()}")
        print(f"Cantidad dados cacho_b: {cacho_b.get_cantidad_dados()}")
        print(f"Valores dados cacho_b: {cacho_b.get_valores()}")

        lista_cachos = [cacho_a, cacho_b]

        apuesta = (3, 4) # -> 3 cuadras (contando comodines, se cumple en todos los casos)

        arbitro_ronda = ArbitroRonda()
        arbitro_ronda.manejar_duda(lista_cachos, apuesta, apostador=cacho_a, dudador=cacho_b)

        assert cacho_b.get_cantidad_dados() == 4 # -> pierde un dado
        assert cacho_a.get_cantidad_dados() == 5 # -> queda igual

    @pytest.mark.parametrize("lista_valores",[
            [1, 4, 3, 6, 2, 4, 4, 6, 5, 5],
            [5, 5, 1, 2, 4, 3, 6, 2, 6, 4],
            [6, 6, 1, 4, 3, 2, 5, 3, 4, 6]
        ])
    def test_jugador_duda_correctamente_y_apostador_pierde_dado(self, lista_valores):
        """
        se verifica que cuando un jugador duda sobre una apuesta
        y tiene razón (apuesta no se cumple), quien hizo la apuesta
        pierde un dado
        """
        cacho_a = Cacho()
        cacho_b = Cacho()
        cacho_a.set_valores_dados(lista_valores[:5])
        cacho_b.set_valores_dados(lista_valores[5:])
        lista_cachos = [cacho_a, cacho_b]

        apuesta = (5, 4) # -> 5 cuadras (contando ases como comodines, no se cumple en ningún caso)
        arbitro_ronda = ArbitroRonda()
        arbitro_ronda.manejar_duda(lista_cachos, apuesta, apostador=cacho_a, dudador=cacho_b)

        assert cacho_a.get_cantidad_dados() == 4 # -> apostador pierde dado
        assert cacho_b.get_cantidad_dados() == 5 # -> queda igual

    @pytest.mark.parametrize("lista_valores",[
            [1, 4, 3, 6, 2, 4, 4, 6, 5, 5],
            [5, 5, 1, 2, 4, 3, 6, 4, 6, 4],
            [6, 6, 1, 4, 3, 2, 4, 3, 4, 6]
        ])
    def test_jugador_calza_correctamente_y_gana_dado(self, lista_valores):
        """
        se verifica que cuando un jugador calza correctamente
        (exactamente en cantidad), gana un dado (si ya tiene 5, queda en espera)
        """
        cacho_a = Cacho()
        cacho_b = Cacho()
        cacho_a.set_valores_dados(lista_valores[:5])
        cacho_b.set_valores_dados(lista_valores[5:])
        lista_cachos = [cacho_a, cacho_b]

        cantidad_inicial = cacho_b.get_cantidad_dados()

        apuesta = (4, 4) # -> 4 cuadras (contando ases como comodines, se cumple exactamente en todos los casos)
        arbitro_ronda = ArbitroRonda()
        arbitro_ronda.manejar_calzar(lista_cachos, apuesta, apostador=cacho_a, calzador=cacho_b)

        assert cacho_b.get_cantidad_dados() == min(cantidad_inicial + 1, 5) # -> gana un dado (queda igual si ya tenía 5)
        assert cacho_b.dados_en_espera == 1 # -> queda con un dado en espera
        assert cacho_a.get_cantidad_dados() == 5 # -> queda igual

    @pytest.mark.parametrize("lista_valores",[
            [1, 4, 3, 6, 2, 4, 4, 6, 5, 5],
            [5, 5, 1, 2, 4, 3, 6, 4, 6, 4],
            [6, 6, 1, 4, 3, 2, 4, 3, 4, 6]
        ])
    def test_jugador_calza_incorrectamente_y_pierde_dado(self, lista_valores):
        """
        se verifica que si un jugador calza incorrectamente,
        (no cumple exactamente en cantidad), pierde un dado
        """
        cacho_a = Cacho()
        cacho_b = Cacho()
        cacho_a.set_valores_dados(lista_valores[:5])
        cacho_b.set_valores_dados(lista_valores[5:])
        lista_cachos = [cacho_a, cacho_b]

        cantidad_inicial = cacho_b.get_cantidad_dados()

        apuesta = (1, 4) # -> 1 cuadra (no cumple exactamente en ningún caso)
        arbitro_ronda = ArbitroRonda()
        arbitro_ronda.manejar_calzar(lista_cachos, apuesta, apostador=cacho_a, calzador=cacho_b)

        assert cacho_b.get_cantidad_dados() == cantidad_inicial - 1 # -> pierde un dado
        assert cacho_a.get_cantidad_dados() == 5 # -> queda igual

    def test_calzar_posible_con_jugador_con_un_dado(self):
        """
        se verifica que si calzador tiene solo un dado, puede calzar
        """
        cacho_a = Cacho()
        cacho_b = Cacho()
        lista_cachos = [cacho_a, cacho_b]
        cacho_b.dados = [cacho_b.dados[0]] # -> solo tiene un dado

        arbitro_ronda = ArbitroRonda()

        assert arbitro_ronda.puede_calzar(lista_cachos, cacho_b) is True
    
    def test_calzar_posible_con_mitad_dados_en_juego(self):
        """
        se verifica que si queda la mitad (o menos?) de dados en juego,
        se puede calzar
        """
        cacho_a = Cacho()
        cacho_b = Cacho()
        lista_cachos = [cacho_a, cacho_b]
        
        # -> se dejan 5 dados en total (mitad en juego)
        cacho_a.dados = cacho_a.dados[:2]
        cacho_b.dados = cacho_b.dados[:3]

        arbitro_ronda = ArbitroRonda()
        assert arbitro_ronda.puede_calzar(lista_cachos, cacho_b) is True
    
    def test_calzar_no_posible_por_cantidad_de_dados(self):
        """
        se verifica que si hay más de la mitad de dados en juego,
        no se puede calzar
        """
        cacho_a = Cacho()
        cacho_b = Cacho()
        lista_cachos = [cacho_a, cacho_b]

        arbitro_ronda = ArbitroRonda()
        assert arbitro_ronda.puede_calzar(lista_cachos, cacho_b) is False

    # TODO: falta testear casos borde:
    # 1. jugador con 1 dado calza mal, queda con 0 (eliminado) y bien, queda con 1 dado
    # 2. jugador calza 2 veces, queda con 2 dados en espera
    # 3. verificar condiciones para poder calzar

from src.juego.validador_apuesta import ValidadorApuesta

import pytest

class TestValidadorApuesta:

    def test_cantidad_superior_misma_pinta_valida(self):
        """
        se verifica subir cantidad y mantener pinta sea válido
        """
        validador = ValidadorApuesta()
       
        assert validador.validar_nueva_apuesta((2, 2), (3, 2)) is True
        assert validador.validar_nueva_apuesta((5, 4), (6, 4)) is True

    def test_cantidad_inferior_misma_pinta_invalida(self):
        """
        se verifica que bajar cantidad y mantener pinta sea inválido
        """
        validador = ValidadorApuesta()

        assert validador.validar_nueva_apuesta((4, 3), (3, 3)) is False
        assert validador.validar_nueva_apuesta((6, 5), (4, 5)) is False

    def test_misma_cantidad_pinta_superior_valida(self):
        """
        se verifica que mantener cantidad y subir pinta sea válido
        """
        validador = ValidadorApuesta()

        assert validador.validar_nueva_apuesta((2, 2), (2, 3)) is True
        assert validador.validar_nueva_apuesta((5, 4), (5, 5)) is True

    def test_misma_cantidad_pinta_inferior_invalida(self):
        """
        se verifica que mantener cantidad y bajar pinta sea inválido
        """
        validador = ValidadorApuesta()

        assert validador.validar_nueva_apuesta((4, 3), (4, 2)) is False
        assert validador.validar_nueva_apuesta((6, 5), (6, 3)) is False

    def test_cantidad_y_pinta_superior_valida(self):
        """
        se verifica que subir cantidad y pinta sea válido
        """
        validador = ValidadorApuesta()

        assert validador.validar_nueva_apuesta((2, 2), (3, 3)) is True
        assert validador.validar_nueva_apuesta((5, 4), (6, 5)) is True

    def test_cantidad_y_pinta_inferior_invalida(self):
        """
        se verifica que bajar cantidad y pinta sea inválido
        """
        validador = ValidadorApuesta()

        assert validador.validar_nueva_apuesta((4, 3), (3, 3)) is False
        assert validador.validar_nueva_apuesta((6, 5), (7, 4)) is False

    def test_pinta_fuera_de_dominio_invalida(self):
        """
        se verifica que la pinta de la nueva apuesta esté en dominio 1-6
        """
        validador = ValidadorApuesta()

        assert validador.validar_nueva_apuesta((2, 2), (3, 7)) is False
        assert validador.validar_nueva_apuesta((4, 3), (5, 0)) is False

    def test_cantidad_fuera_de_dominio_invalida(self):
        """
        se verifica que la cantidad de la nueva apuesta esté en dominio (>0)
        """
        validador = ValidadorApuesta()

        assert validador.validar_nueva_apuesta((2, 2), (0, 3)) is False
        assert validador.validar_nueva_apuesta((2, 2), (-1, 3)) is False

    @pytest.mark.parametrize("apuesta_actual, apuesta_nueva", [
        ((2, 3), (2, 1)),  # 2/2 -> 1 + 1 → 2
        ((5, 4), (3, 1)),  # 5/2 -> ceil(2.5) = 3
        ((6, 5), (4, 1)),  # 6/2 + 1 = 4
        ((9, 6), (5, 1))   # 9/2 -> ceil(4.5) = 5
        ])
    def test_cambio_de_pinta_a_ases_valido(self, apuesta_actual, apuesta_nueva):
        """
        se verifica que la apuesta nueva cambie a ases de forma válida:
            dividir cantidad actual por 2 (par: +1, impar: redondear hacia arriba)
        """
        validador = ValidadorApuesta()

        assert validador.validar_nueva_apuesta(apuesta_actual, apuesta_nueva) is True

    @pytest.mark.parametrize("apuesta_actual, apuesta_nueva", [
       ((2, 3), (1, 1)),  # 2/2 -> 1 + 1 → 2 != 1
       ((6, 4), (3, 1)),  # 6/2 -> 3 + 1 = 4 != 3
       ((5, 5), (2, 1)),  # 5/2 -> ceil(2.5) = 3 != 2
       ((9, 6), (4, 1))   # 9/2 → ceil(4.5) = 5 != 4
       ])
    def test_cambio_de_pinta_a_ases_invalido(self, apuesta_actual, apuesta_nueva):
        """
        se verifica que si se cambia a ases a otra pinta de forma ilegal (no respetando
        relgas) sea inválido
        """
        validador = ValidadorApuesta()

        assert validador.validar_nueva_apuesta(apuesta_actual, apuesta_nueva) is False

    @pytest.mark.parametrize("apuesta_actual, apuesta_nueva", [
        ((4, 1), (9, 3)), # 4*2 + 1 -> 9
        ((5, 1), (11, 4)), # 5*2 + 1 -> 11
        ((6, 1), (13, 5)), # 6*2 + 1 -> 13
        ((7, 1), (15, 6)) # 7*2 + 1 -> 15
        ])
    def test_cambio_de_ases_a_pinta_valido(self, apuesta_actual, apuesta_nueva):
        """
        se verifica que si la apuesta actual tiene de pinta ases, la nueva
        apuesta cambie de ases a otra pinta de forma válida:
            multiplicar por 2 y sumar 1
        """
        validador = ValidadorApuesta()

        assert validador.validar_nueva_apuesta(apuesta_actual, apuesta_nueva) is True

    @pytest.mark.parametrize("apuesta_actual, apuesta_nueva", [
        ((4, 1), (8, 3)), # 4*2 + 1 -> 9 != 8
        ((5, 1), (12, 4)), # 5*2 + 1 -> 11 != 12
        ((6, 1), (12, 5)), # 6*2 + 1 -> 13 != 12
        ((7, 1), (13, 6)) # 7*2 + 1 -> 15 != 13
        ])
    def test_cambio_de_ases_a_pinta_invalido(self, apuesta_actual, apuesta_nueva):
        """
        se verifica que si se cambia de ases a otra pinta de forma ilegal,
        sea inválido
        """
        validador = ValidadorApuesta()

        assert validador.validar_nueva_apuesta(apuesta_actual, apuesta_nueva) is False

    def test_primer_apuesta_con_pinta_valida(self):
        """
        se verifica que primer apuesta sea sin ases
        """
        validador = ValidadorApuesta()

        assert validador.validar_nueva_apuesta((0, 0), (1, 2)) is True
        assert validador.validar_nueva_apuesta((0, 0), (3, 5)) is True

    def test_primer_apuesta_con_ases_invalida(self):
        """
        se verifica que si primer apuesta es con ases sea inválida
        """
        validador = ValidadorApuesta()

        assert validador.validar_nueva_apuesta((0, 0), (4, 1)) is False
        assert validador.validar_nueva_apuesta((0, 0), (6, 1)) is False


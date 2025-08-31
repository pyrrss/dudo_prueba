from src.juego.dado import Dado

class TestDado:

    def test_lanzar_llama_a_generador(self, mocker):
        """
        se verifica que Dado efectivamente se comunique con servicio
        GeneradorAleatorio
        """
        mock_generador_aleatorio = mocker.patch(
                "src.servicios.generador_aleatorio.GeneradorAleatorio.generar_valor_aleatorio",
                return_value=4
                )
        dado = Dado()
        dado.lanzar()
        mock_generador_aleatorio.assert_called_once()

    def test_lanzar_deja_valor_en_dominio(self):
        """
        se verifica que valores generados pertenecen al dominio 1-6
        """
        dado = Dado()
        for _ in range(10):
            dado.lanzar()
            assert dado.valor_actual in range(1, 7)

    def test_get_nombre_pinta(self):
        """
        se verifica que para un cierto número de pinta se devuelve el nombre correcto
        1: "As"
        2: "Tonto"
        3: "Tren"
        4: "Cuadra"
        5: "Quina":
        6: "Sexto"
        """
        dado = Dado()

        assert dado.get_nombre_pinta(1) == "As"
        assert dado.get_nombre_pinta(2) == "Tonto"
        assert dado.get_nombre_pinta(3) == "Tren"
        assert dado.get_nombre_pinta(4) == "Cuadra"
        assert dado.get_nombre_pinta(5) == "Quina"
        assert dado.get_nombre_pinta(6) == "Sexto"








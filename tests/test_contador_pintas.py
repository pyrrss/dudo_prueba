from src.juego.contador_pintas import ContadorPintas

class TestContadorPintas:

    def test_contar_pinta_sin_ases_devuelve_valor_total_correcto(self):
        """
        se verifica la cantidad de apariciones de una pinta
        específica, sin considerar ases
        """
        lista_valores_dados = [
                [2, 3, 4, 5, 6],
                [3, 2, 5, 4, 6],
                [6, 5, 4, 3, 2]
        ]

        contador_pintas = ContadorPintas()

        total_apariciones = 0
        for valores_dados in lista_valores_dados:
            total_apariciones += contador_pintas.contar_apariciones(valores_dados, 2)

        assert total_apariciones == 3

    def test_contar_pinta_con_ases_como_comodines_devuelve_valor_total_correcto(self):
        """
        se verifica la cantidad de apariciones de una pinta
        específica, considerando ases como comodines
        """
        lista_valores_dados = [
                [1, 2, 3, 4, 6],
                [3, 2, 5, 4, 1],
                [4, 2, 1, 1, 1]
                ]

        contador_pintas = ContadorPintas()

        total_apariciones = 0
        for valores_dados in lista_valores_dados:
            total_apariciones += contador_pintas.contar_apariciones(valores_dados, 2)

        assert total_apariciones == 8

    def test_contar_pinta_sin_ases_como_comodines_devuelve_valor_total_correcto(self):
        """
        se verifica la cantidad de apariciones de una pinta
        específica, pero sin contar ases como comodines
        (ocurre cuando un jugador se queda por primera vez con un
         solo dado)
        """
        lista_valores_dados = [
                [1, 2, 3, 4, 6],
                [3, 2, 5, 4, 1],
                [4, 2, 1, 2, 1]
                ]

        contador_pintas = ContadorPintas()

        total_apariciones = 0
        for valores_dados in lista_valores_dados:
            total_apariciones += contador_pintas.contar_apariciones(valores_dados, 2, False)

        assert total_apariciones == 4

    def test_contar_pinta_sin_apariciones_devuelve_cero(self):
        """
        se verifica que si en los valores no aparece la pinta,
        se devuelve cero
        """
        lista_valores_dados = [
                [4, 5, 3, 4, 6],
                [3, 4, 5, 4, 4],
                [4, 6, 3, 3, 5]
                ]

        contador_pintas = ContadorPintas()

        total_apariciones = 0
        for valores_dados in lista_valores_dados:
            total_apariciones += contador_pintas.contar_apariciones(valores_dados, 2)

        assert total_apariciones == 0

    def test_contar_pinta_todos_ases_como_comodines_devuelve_valor_total_correcto(self):
        """
        se verifica que si todos son ases, se devuelve el total para
        cualquier pinta que se busque (porque cuentan como comodines)
        """
        lista_valores_dados = [
                [1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1]
                ]

        contador_pintas = ContadorPintas()

        total_apariciones = 0
        pintas = [1, 2, 3, 4, 5, 6]

        for pinta in pintas:
            for valores_dados in lista_valores_dados:
                total_apariciones += contador_pintas.contar_apariciones(valores_dados, pinta)

        assert total_apariciones == 180 # -> 30 * 6 = 180

    def test_contar_pinta_todos_ases_no_comodines_devuelve_valor_total_correcto(self):
        """
        se verifica que si todos son ases y estos no cuentan como
        comodines, solo se cuentan si la pinta buscada es 1
        """
        lista_valores_dados = [
                [1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1]
                ]

        contador_pintas = ContadorPintas()

        total_apariciones = 0
        pintas = [1, 2, 3, 4, 5, 6]

        for pinta in pintas:
            for valores_dados in lista_valores_dados:
                total_apariciones += contador_pintas.contar_apariciones(valores_dados, pinta, False)

        assert total_apariciones == 30 # -> solo se cuenta para los ases


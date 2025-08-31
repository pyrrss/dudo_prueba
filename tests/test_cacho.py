from src.juego.cacho import Cacho
from src.juego.dado import Dado

class TestCacho:

    def test_cacho_tiene_cinco_dados_al_inicio(self):
        """
        se verifica que Cacho tiene cinco dados al instanciar
        """
        cacho = Cacho()

        assert len(cacho.dados) == 5

    def test_cacho_tiene_instancias_de_dado(self):
        """
        se verifica que los elementos de cacho son efectivamente
        instancias de dado
        """
        cacho = Cacho()

        for dado in cacho.dados:
            assert isinstance(dado, Dado)

    def test_agitar_deja_valores_en_dominio(self):
        """
        se verifica que al agitar el cacho todos los dados
        queden con valores en dominio 1-6
        """
        cacho = Cacho()
        cacho.agitar()

        for valor in cacho.get_valores():
            assert valor in range(1, 7)

    # TODO: falta testear lo de ocultar/mostrar los dados según estado de juego

    # TODO: REVISAR ESTO LUEGO KOMPAAA

    def test_agregar_dado_a_cacho_con_maximo_de_dados_deja_el_dado_en_espera(self):
        """
        se verifica que al agregar un dado a un cacho y este ya tiene 5 dados,
        se deja el nuevo dado en espera
        """
        cacho = Cacho() # -> inicia con 5 dados
        cacho.agregar_dado()

        assert cacho.dados_en_espera == 1

    def test_agregar_dado_a_cacho_con_menos_de_cinco_dados(self):
        """
        se verifica que al agregar un dado a un cacho que no tiene el máximo
        de dados, este se agrega correctamente (sin quedar en espera)
        """
        cacho = Cacho()
        cacho.quitar_dado()
        cacho.agregar_dado()

        assert cacho.get_cantidad_dados() == 5
        assert cacho.dados_en_espera == 0

    def test_quitar_dado_resta_dados_en_espera(self):
        """
        se verifica que al quitar un dado a un jugador que tenía dados en espera,
        se disminuye la cantidad de dados en espera
        """
        cacho = Cacho()
        cacho.agregar_dado() # -> se agrega un dado, queda en espera
        cacho.quitar_dado() # -> debe quedar sin dados en espera

        assert cacho.dados_en_espera == 0

    def test_quitar_dado_disminuye_cantidad_de_dados(self):
        """
        se verifica que al quitar un dado a un jugador sin dados en espera,
        se disminuye su cantidad de dados
        """
        cacho = Cacho()
        cacho.quitar_dado()
        cacho.quitar_dado()

        assert cacho.get_cantidad_dados() == 3

    def test_no_quitar_dado_a_jugador_sin_dados(self):
        """
        se verifica que se maneja caso en donde se intenta quitar un dado a un
        cacho con 0 dados
        """
        cacho = Cacho()
        for _ in range(5):
            cacho.quitar_dado()

        # -> cacho sin dados, se intenta quitar uno más
        cacho.quitar_dado()

        assert cacho.get_cantidad_dados() == 0

    def test_set_valores_dados_valido(self):
        """
        se verifica que al setear valores de forma arbitraria,
        estos se setean correctamente en el cacho
        """
        cacho = Cacho()
        valores = [1, 2, 3, 4, 5]
        cacho.set_valores_dados(valores)
 
        assert cacho.get_valores() == valores

    def test_set_valores_dados_con_longitud_invalida(self):
        """
        se verifica que al intentar setear valores de forma arbitraria incorrecta,
        estos no se setean en el cacho
        """
        cacho = Cacho()
        valores = [1, 2, 3, 4, 5, 6] # -> 6 valores, invalido
        cacho.set_valores_dados(valores)

        assert len(cacho.get_valores()) == 5 # -> se mantiene con longitud anterior

    def test_set_valores_dados_con_valores_fuera_de_dominio(self):
        """
        se verifica que al intentar setear valores fuera de dominio,
        estos no se setean en el cacho
        """
        cacho = Cacho()
        valores = [54, 234, 123, 342, 32423] # -> valores fuera de dominio
        cacho.set_valores_dados(valores)

        assert cacho.get_valores() != valores # -> mantiene sus valores correctos anteriores

    def test_set_valores_dados_con_valores_no_enteros(self):
        """
        se verifica que al intentar setear valores que no son instancias de int,
        estos no se setean
        """
        cacho = Cacho()
        valores = [1.0, 2.5, 3.0, 4.2, 5.3] # -> valores float
        cacho.set_valores_dados(valores)

        assert cacho.get_valores() != valores # -> mantiene sus valores correctos anteriores
 
    def test_ocultar_y_mostrar_dados(self):
        """
        se verifica que al ocultar dados, sus valores se muestren como '?',
        y luego al mostrarlos se muestren sus valores enteros
        """
        cacho = Cacho()
        cacho.agitar()
        cacho.ocultar_dados()

        for valor in cacho.get_valores():
            assert valor == "?"

        cacho.mostrar_dados()

        for valor in cacho.get_valores():
            assert isinstance(valor, int)





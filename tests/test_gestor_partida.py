from unittest.mock import Mock, patch
from src.juego.gestor_partida import GestorPartida

class TestGestorPartida:

    def test_crear_partida_con_cachos(self):
        """
        crear una partida con cachos como jugadores
        """
        cantidad_jugadores = 3
    
        # act y asserts
        gestor = GestorPartida(cantidad_jugadores)
        assert len(gestor.lista_cachos) == 3
        for cacho in gestor.lista_cachos:
            assert cacho.get_cantidad_dados() == 5
        assert gestor.cacho_actual is None
        assert gestor.direccion is None

    def test_determinar_cacho_inicial_sin_empate(self, mocker):
        """
        el cacho con el dado más alto inicia la partida
        """
        gestor = GestorPartida(3)
    
        # mocks para no usar testear con randoms 
        mock_dados = [3, 6, 4]  
    
        with patch('src.juego.gestor_partida.GeneradorAleatorio.generar_valor_aleatorio', side_effect=mock_dados): # use esto with patch con un mock para reemplazar los numeros random, no se si hay una mejor manera pero lo dejo asi por mientras :D
            # act
            cacho_inicial = gestor.determinar_cacho_inicial()
    
        # assert
        assert cacho_inicial == gestor.cacho_actual


    def test_determinar_cacho_inicial_con_empate(self, mocker):
        """
        en caso de empate se vuelve a tirar dados solo para los empatados
        """
        # Arrange
        gestor = GestorPartida(2)
    
        # mock para randoms
        mock_dados = [5, 5, 2, 6] 
    
        with patch('src.juego.gestor_partida.GeneradorAleatorio.generar_valor_aleatorio', side_effect=mock_dados): # lo mismo por aca
            # act
            cacho_inicial = gestor.determinar_cacho_inicial()
    
        # assert
        assert cacho_inicial == gestor.cacho_actual

    def test_establecer_direccion(self):
        """
        establecer la direccion de la partida
        """
        gestor = GestorPartida(2)
    
        # acts y asserts
        gestor.establecer_direccion("antihorario")
        assert gestor.direccion == "antihorario"
        gestor.establecer_direccion("horario")
        assert gestor.direccion == "horario"

    def test_siguiente_turno_horario(self):
        """
        obtener el cacho que juega en el siguiente turno, en sentido horario
        """
        gestor = GestorPartida(3)
        gestor.direccion = "horario"
        gestor.cacho_actual = gestor.lista_cachos[0]
    
        # act y assert
        siguiente = gestor.obtener_siguiente_cacho()
        assert siguiente == gestor.lista_cachos[1]

    def test_siguiente_turno_antihorario(self):
        """
        obtener el cacho que juega en el siguiente turno, en sentido antihorario
        """
        gestor = GestorPartida(3)
        gestor.direccion = "antihorario"
        gestor.cacho_actual = gestor.lista_cachos[0]
    
        # act y assert
        siguiente = gestor.obtener_siguiente_cacho()
        assert siguiente == gestor.lista_cachos[2] 

    def test_detectar_cachos_con_un_dado(self):
        """
        detectar cuando un cacho queda con un solo dado
        """
        gestor = GestorPartida(2)

        # mock cacho con un dado
        gestor.lista_cachos[1].dados = [Mock()]
    
        # act y assert
        cacho_un_dado = gestor.verificar_cachos_con_un_dado()
        assert cacho_un_dado == gestor.lista_cachos[1]
    
    def test_partida_terminada(self):
        """
        la partida termina cuando solo queda un cacho con dados y es el ganador
        """
        gestor = GestorPartida(3)
    
        # Simular que cacho1 y cacho2 pierden todos sus dados
        gestor.lista_cachos[1].dados = []  # Sin dados
        gestor.lista_cachos[2].dados = []  # Sin dados
    
        # acts y asserts
        terminada = gestor.partida_terminada()
        ganador = gestor.obtener_ganador()    
        assert terminada == True
        assert ganador == gestor.lista_cachos[0]

    def test_iniciar_ronda_con_iniciador_predefinido(self):
        """
        se verifica que si hay un iniciador para la siguiente ronda
        (que ocurre cuando un jugador pierde/gana un dado), este
        se setea como el cacho actual al iniciar la ronda
        """
        gestor = GestorPartida(2)
        cacho_iniciador = gestor.lista_cachos[1]
        gestor.iniciador_proxima_ronda = cacho_iniciador

        gestor.iniciar_ronda() # -> se inicia ronda con iniciador seteado

        assert gestor.cacho_actual == cacho_iniciador
        assert gestor.iniciador_proxima_ronda is None # -> se limpia lueg # -> se inicia ronda con iniciador seteado

        assert gestor.cacho_actual == cacho_iniciador
        assert gestor.iniciador_proxima_ronda is None # -> se limpia luegoo

    def test_iniciar_ronda_con_estado_especial_pendiente(self):
        """
        se verifica que al iniciar la ronda, si habia estado especial pendiente
        (porque un jugador la activó en la ronda anterior), se activa
        """
        gestor = GestorPartida(2)
        gestor.estado_especial_pendiente = True
        gestor.tipo_ronda_especial_pendiente = "abierto"

        gestor.iniciar_ronda()

        assert gestor.estado_especial is True # -> se activa ronda especial 
        assert gestor.tipo_ronda_especial == "abierto" # -> se activa ronda abierta
        assert gestor.estado_especial_pendiente is False # -> se desactiva
        assert gestor.tipo_ronda_especial_pendiente is None # -> se resetea

    def test_obtener_siguiente_cacho_sin_direccion(self):
        """
        cuando no se ha establecido direccion por defecto usa horario
        """
        gestor = GestorPartida(3)
        gestor.cacho_actual = gestor.lista_cachos[0]
        gestor.direccion = None
        
        siguiente = gestor.obtener_siguiente_cacho()
        assert siguiente == gestor.lista_cachos[1]
        assert gestor.direccion == "horario"

    def test_obtener_siguiente_cacho_con_cachos_sin_dados(self):
        """
        si todos los cachos no tienen dados retorna None
        """
        gestor = GestorPartida(2)
        gestor.cacho_actual = gestor.lista_cachos[0]
        for cacho in gestor.lista_cachos:
            cacho.dados = []
        
        resultado = gestor.obtener_siguiente_cacho()
        assert resultado is None

    def test_cachos_con_un_dado_retorna_none(self):
        """
        si ningun cacho tiene exactamente un dado retorna None
        """
        gestor = GestorPartida(2)
        gestor.lista_cachos[0].dados = [Mock(), Mock()]
        gestor.lista_cachos[1].dados = [Mock(), Mock(), Mock()]
        
        resultado = gestor.verificar_cachos_con_un_dado()
        assert resultado is None

    def test_iniciar_ronda_sin_estado_especial_pendiente(self):
        """
        si no hay estado especial pendiente se setea en False
        """
        gestor = GestorPartida(2)
        gestor.estado_especial_pendiente = False
        gestor.estado_especial = True  
        gestor.tipo_ronda_especial = "abierto"
        
        gestor.iniciar_ronda()
        
        assert gestor.estado_especial is False
        assert gestor.tipo_ronda_especial is None
        assert gestor.cacho_que_obligo is None

    def test_ronda_especial_cuando_cacho_tiene_un_dado(self):
        """
        cuando un cacho tiene un dado y no ha usado especial se activa la ronda especial
        """
        gestor = GestorPartida(2)
        cacho_con_un_dado = gestor.lista_cachos[0]
        cacho_con_un_dado.dados = [Mock()] 
        
        gestor.verificar_ronda_especial(cacho_con_un_dado)
        
        assert gestor.cacho_que_obligo == cacho_con_un_dado
        assert gestor.estado_especial_pendiente is True
        assert cacho_con_un_dado in gestor.cachos_que_usaron_especial

    def test_actualizar_visibilidad_dados_ronda_abierta(self):
        """
        en una ronda abierta jugador actual no ve sus dados pero los otros si ven los suyos
        """
        gestor = GestorPartida(3)
        gestor.estado_especial = True
        gestor.tipo_ronda_especial = "abierto"
        gestor.cacho_actual = gestor.lista_cachos[0]
        
        for cacho in gestor.lista_cachos:
            cacho.mostrar_dados = Mock()
            cacho.ocultar_dados = Mock()
        
        gestor.actualizar_visibilidad_dados()
        for cacho in gestor.lista_cachos:
            cacho.ocultar_dados.assert_called()
        
        gestor.lista_cachos[1].mostrar_dados.assert_called()
        gestor.lista_cachos[2].mostrar_dados.assert_called()
        gestor.lista_cachos[0].mostrar_dados.assert_not_called()

    def test_actualizar_visibilidad_dados_ronda_cerrada(self):
        """
        en una ronda cerrada solo el obligador ve sus dados cuando es su turno
        """
        gestor = GestorPartida(2)
        gestor.estado_especial = True
        gestor.tipo_ronda_especial = "cerrado"
        gestor.cacho_actual = gestor.lista_cachos[0]
        gestor.cacho_que_obligo = gestor.lista_cachos[0]
        
        for cacho in gestor.lista_cachos:
            cacho.mostrar_dados = Mock()
            cacho.ocultar_dados = Mock()
        gestor.actualizar_visibilidad_dados()
        
        for cacho in gestor.lista_cachos:
            cacho.ocultar_dados.assert_called()
        gestor.lista_cachos[0].mostrar_dados.assert_called()
        gestor.lista_cachos[1].mostrar_dados.assert_not_called()

    def test_actualizar_visibilidad_dados_ronda_normal(self):
        """
        en una ronda normal solo el jugador actual ve sus dados
        """
        gestor = GestorPartida(2)
        gestor.estado_especial = False
        gestor.cacho_actual = gestor.lista_cachos[0]
        for cacho in gestor.lista_cachos:
            cacho.mostrar_dados = Mock()
            cacho.ocultar_dados = Mock()
        gestor.actualizar_visibilidad_dados()
        
        for cacho in gestor.lista_cachos:
            cacho.ocultar_dados.assert_called()
        gestor.lista_cachos[0].mostrar_dados.assert_called()
        gestor.lista_cachos[1].mostrar_dados.assert_not_called()

    def test_flujo_simple_partida_dos_jugadores(self, mocker):
        """
        este test simula un flujo simple de una partida con 2 jugadores,
        donde se inicia la partida, se simulan los turnos y se verifican
        que los estados intermedios sean los correctos, hasta que un jugador
        queda sin dados y se define un ganador, terminando la partida
        """
        gestor = GestorPartida(2)

        mocker.patch("src.servicios.generador_aleatorio.GeneradorAleatorio.generar_valor_aleatorio", side_effect=[6, 5])
        cacho_inicial = gestor.determinar_cacho_inicial()
        gestor.establecer_direccion("horario")

        def agitar_mock(self):
            num_dados = self.get_cantidad_dados() # -> se generan valores acordes a cantidad de dados
            if self == gestor.lista_cachos[0]:
                valores = list(range(1, num_dados + 1))
            else:
                valores = list(range(2, 2 + num_dados)) # fuera de dominio?
            self.set_valores_dados(valores)

        mocker.patch("src.juego.cacho.Cacho.agitar", new=agitar_mock)
        gestor.iniciar_ronda()
        assert gestor.cacho_actual == cacho_inicial

        # -- RONDA 1 --
        # jugador 0 hace una apuesta válida, jugador 1 duda incorrectamente y pierde un dado
        gestor.apuesta_actual = (2, 2)
        gestor.ultimo_apostador = gestor.cacho_actual
        siguiente_cacho = gestor.obtener_siguiente_cacho()
        assert siguiente_cacho == gestor.lista_cachos[1]
        perdedor = gestor.arbitro_ronda.manejar_duda(
                gestor.lista_cachos,
                gestor.apuesta_actual,
                gestor.ultimo_apostador,
                gestor.lista_cachos[1])
        
        assert perdedor == gestor.lista_cachos[1]
        assert gestor.lista_cachos[1].get_cantidad_dados() == 4

        # -> ronda 2
        # jugador 1 hace apuesta y jugador 0 duda correctamente, jugador 1 pierde un dado
        gestor.iniciador_proxima_ronda = perdedor # -> quien perdió dado inicia siguiente ronda
        gestor.iniciar_ronda()
        assert gestor.cacho_actual == gestor.lista_cachos[1] 
        
        gestor.apuesta_actual = (4, 3)
        gestor.ultimo_apostador = gestor.cacho_actual

        perdedor_ronda2 = gestor.arbitro_ronda.manejar_duda(
            gestor.lista_cachos,
            gestor.apuesta_actual,
            gestor.ultimo_apostador,
            gestor.lista_cachos[0]
        )
        
        assert perdedor_ronda2 == gestor.lista_cachos[1]
        assert gestor.lista_cachos[1].get_cantidad_dados() == 3

        # -> forzar que jugador 1 quede con un solo dado
        gestor.lista_cachos[1].quitar_dado()
        gestor.lista_cachos[1].quitar_dado()
        gestor.verificar_ronda_especial(gestor.lista_cachos[1])
        assert gestor.estado_especial_pendiente is True

        gestor.iniciar_ronda()
        assert gestor.estado_especial is True

        # -> perder último dado, se define ganador y termina partida
        gestor.lista_cachos[1].quitar_dado()
        assert gestor.partida_terminada() is True
        assert gestor.obtener_ganador() == gestor.lista_cachos[0]

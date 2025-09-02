from src.juego.gestor_partida import GestorPartida
from unittest.mock import Mock, patch

def test_crear_gestor_partida():
    """
    crear GestorPartida con numero de jugadores
    """
    gestor = GestorPartida(3)
    assert len(gestor.lista_cachos) == 3
    assert gestor.cacho_actual is None
    assert gestor.direccion is None

def test_establecer_direccion():
    """
    establecer direccion de juego
    """
    gestor = GestorPartida(2)
    gestor.establecer_direccion("horario")
    assert gestor.direccion == "horario"

def test_cambiar_cacho_actual():
    """
    cambiar cacho actual
    """
    gestor = GestorPartida(3)
    nuevo_cacho = gestor.lista_cachos[1]
    gestor.cambiar_cacho_actual(nuevo_cacho)
    assert gestor.cacho_actual == nuevo_cacho
    assert gestor.jugador_idx == 1

def test_manejar_apuesta_valida():
    """
    manejar apuesta valida
    """
    gestor = GestorPartida(2)
    gestor.cacho_actual = gestor.lista_cachos[0]
    gestor.apuesta_actual = (1, 2)
    resultado = gestor.manejar_apuesta((2, 3))
    assert resultado == True
    assert gestor.apuesta_actual == (2, 3)

def test_manejar_apuesta_invalida():
    """
    manejar apuesta invalida
    """
    gestor = GestorPartida(2)
    gestor.cacho_actual = gestor.lista_cachos[0]
    gestor.apuesta_actual = (3, 4)
    resultado = gestor.manejar_apuesta((2, 2))
    assert resultado == False

def test_obtener_siguiente_cacho_horario():
    """
    obtener siguiente cacho jugando en direccion horaria
    """
    gestor = GestorPartida(3)
    gestor.cacho_actual = gestor.lista_cachos[0]
    gestor.direccion = "horario"
    siguiente = gestor.obtener_siguiente_cacho()
    assert siguiente == gestor.lista_cachos[1]

def test_obtener_siguiente_cacho_antihorario():
    """
    obtener siguiente cacho jugando en direccion antihoraria
    """
    gestor = GestorPartida(3)
    gestor.cacho_actual = gestor.lista_cachos[0]
    gestor.direccion = "antihorario"
    siguiente = gestor.obtener_siguiente_cacho()
    assert siguiente == gestor.lista_cachos[2]

def test_partida_terminada():
    """
    verificar si partida termino
    """
    gestor = GestorPartida(3)
    gestor.lista_cachos[1].dados = []
    gestor.lista_cachos[2].dados = []
    assert gestor.partida_terminada() == True

def test_obtener_ganador():
    """
    obtener ganador cuando termina partida
    """
    gestor = GestorPartida(3)
    gestor.lista_cachos[1].dados = []
    gestor.lista_cachos[2].dados = []
    ganador = gestor.obtener_ganador()
    assert ganador == gestor.lista_cachos[0]

def test_verificar_cachos_con_un_dado():
    """
    verificar cachos con un solo dado
    """
    gestor = GestorPartida(2)
    gestor.lista_cachos[1].dados = [Mock()]
    cacho_un_dado = gestor.verificar_cachos_con_un_dado()
    assert cacho_un_dado == gestor.lista_cachos[1]

def test_manejar_duda(mocker):
    """
    manejar duda con mock
    """
    gestor = GestorPartida(2)
    gestor.cacho_actual = gestor.lista_cachos[0]
    gestor.ultimo_apostador = gestor.lista_cachos[1]
    gestor.apuesta_actual = (2, 3)
    
    mock_arbitro = mocker.patch.object(gestor.arbitro_ronda, 'manejar_duda')
    mock_arbitro.return_value = gestor.lista_cachos[0]
    
    resultado = gestor.manejar_duda()
    assert resultado == gestor.lista_cachos[0]
    mock_arbitro.assert_called_once()

def test_manejar_calzar(mocker):
    """
    manejar calzar con mock
    """
    gestor = GestorPartida(2)
    gestor.cacho_actual = gestor.lista_cachos[0]
    gestor.ultimo_apostador = gestor.lista_cachos[1]
    gestor.apuesta_actual = (2, 3)
    
    mock_puede_calzar = mocker.patch.object(gestor.arbitro_ronda, 'puede_calzar')
    mock_puede_calzar.return_value = True
    
    mock_manejar_calzar = mocker.patch.object(gestor.arbitro_ronda, 'manejar_calzar')
    mock_manejar_calzar.return_value = True
    
    resultado = gestor.manejar_calzar()
    assert resultado == True
    mock_puede_calzar.assert_called_once()
    mock_manejar_calzar.assert_called_once()

def test_determinar_cacho_inicial():
    """
    determinar cacho inicial con mock
    """
    gestor = GestorPartida(3)
    
    with patch('src.juego.gestor_partida.GeneradorAleatorio.generar_valor_aleatorio', side_effect=[3, 6, 4]):
        cacho_inicial = gestor.determinar_cacho_inicial()
    
    assert cacho_inicial == gestor.lista_cachos[1]  # El que saco 6
    assert gestor.cacho_actual == gestor.lista_cachos[1]

def test_manejar_apuesta_sin_parametro():
    """
    manejar apuesta sin proporcionar nueva apuesta
    """
    gestor = GestorPartida(2)
    gestor.cacho_actual = gestor.lista_cachos[0]
    
    try:
        gestor.manejar_apuesta()
        assert False, "Deberia lanzar excepcion"
    except ValueError as e:
        assert "Se debe proporcionar una nueva apuesta" in str(e)

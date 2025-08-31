from unittest.mock import Mock, patch
from src.juego.gestor_partida import GestorPartida


def test_crear_partida_con_cachos():
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

def test_determinar_cacho_inicial_sin_empate(mocker):
    """
    el cacho con el dado más alto inicia la partida
    """
    gestor = GestorPartida(3)
    
    # mocks para no usar testear con randoms 
    mock_dados = [3, 6, 4]  
    
    with patch('src.juego.gestor_partida.GeneradorAleatorio.generar_valor_aleatorio', side_effect=mock_dados): # use esto with patch con un mock para reemplazar los numeros random, no se si hay una mejor manera pero lo dejo asi por mientras :D
        # act
        cacho_inicial = gestor._determinar_cacho_inicial()
    
    # assert
    assert cacho_inicial == gestor.cacho_actual


def test_determinar_cacho_inicial_con_empate(mocker):
    """
    en caso de empate se vuelve a tirar dados solo para los empatados
    """
    # Arrange
    gestor = GestorPartida(2)
    
    # mock para randoms
    mock_dados = [5, 5, 2, 6] 
    
    with patch('src.juego.gestor_partida.GeneradorAleatorio.generar_valor_aleatorio', side_effect=mock_dados): # lo mismo por aca
        # act
        cacho_inicial = gestor._determinar_cacho_inicial()
    
    # assert
    assert cacho_inicial == gestor.cacho_actual

def test_establecer_direccion():
    """
    establecer la direccion de la partida
    """
    gestor = GestorPartida(2)
    
    # acts y asserts
    gestor._establecer_direccion("antihorario")
    assert gestor.direccion == "antihorario"
    gestor._establecer_direccion("horario")
    assert gestor.direccion == "horario"

def test_siguiente_turno_horario():
    """
    obtener el cacho que juega en el siguiente turno, en sentido horario
    """
    gestor = GestorPartida(3)
    gestor.direccion = "horario"
    gestor.cacho_actual = gestor.lista_cachos[0]
    
    # act y assert
    siguiente = gestor._obtener_siguiente_cacho()
    assert siguiente == gestor.lista_cachos[1]


def test_siguiente_turno_antihorario():
    """
    obtener el cacho que juega en el siguiente turno, en sentido antihorario
    """
    gestor = GestorPartida(3)
    gestor.direccion = "antihorario"
    gestor.cacho_actual = gestor.lista_cachos[0]
    
    # act y assert
    siguiente = gestor._obtener_siguiente_cacho()
    assert siguiente == gestor.lista_cachos[2] 

def test_detectar_cachos_con_un_dado():
    """
    detectar cuando un cacho queda con un solo dado
    """
    gestor = GestorPartida(2)

    # mock cacho con un dado
    gestor.lista_cachos[1].dados = [Mock()]
    
    # act y assert
    cacho_un_dado = gestor._verificar_cachos_con_un_dado()
    assert cacho_un_dado == gestor.lista_cachos[1]
    
def test_partida_terminada():
    """
    la partida termina cuando solo queda un cacho con dados y es el ganador
    """
    gestor = GestorPartida(3)
    
    # Simular que cacho1 y cacho2 pierden todos sus dados
    gestor.lista_cachos[1].dados = []  # Sin dados
    gestor.lista_cachos[2].dados = []  # Sin dados
    
    # acts y asserts
    terminada = gestor._partida_terminada()
    ganador = gestor._obtener_ganador()    
    assert terminada == True
    assert ganador == gestor.lista_cachos[0]

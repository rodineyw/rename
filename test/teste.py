import sys
import pytest
from PyQt6.QtWidgets import QApplication
# Substitua 'your_module' pelo nome do módulo onde sua classe está
from . import GerenciadorPdf


@pytest.fixture
def app(qtbot):
    """Fixture para criar e retornar a aplicação com qtbot."""
    test_app = QApplication(sys.argv)
    window = GerenciadorPdf()
    qtbot.addWidget(window)
    return window


def test_initial_state(app, qtbot):
    """Teste para verificar o estado inicial da janela."""
    assert app.isVisible()  # Verifica se a janela está visível
    # Verifica se a lista de colunas está inicialmente invisível
    assert not app.lista_colunas.isVisible()


def test_button_click(app, qtbot):
    """Teste para simular cliques de botão e verificar mudanças de estado."""
    qtbot.mouseClick(app.botao_selecionar, Qt.MouseButton.LeftButton)
    # Adicione mais assertivas para verificar os resultados esperados após o clique

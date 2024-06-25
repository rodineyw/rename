from PyQt6.QtWidgets import QApplication
from gerenciador_pdf import GerenciadorPdf


def main():
    app = QApplication([])
    window = GerenciadorPdf()
    window.show()
    app.exec()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Erro inesprado: {e}")
        input("Pressione Enter para encerrar...")

from PyQt6.QtWidgets import QApplication
from gerenciador_pdf import GerenciadorPdf


def main():
    print("Iniciando aplicação...")
    app = QApplication([])
    window = GerenciadorPdf()
    window.show()
    print("Aplicação iniciada com sucesso.")
    app.exec()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Erro inesprado: {e}")
        input("Pressione Enter para encerrar...")

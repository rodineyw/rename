import os
import traceback
from PyQt6.QtWidgets import QApplication
from app.gerenciador_pdf import GerenciadorPdf


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
        with open("erro_log.txt", "w") as f:
            f.write("Ocorreu um erro inesperado:\n")
            traceback.traceback.print_exc(file=f)
        print(f"Erro inesprado: {e}")
        input("Pressione Enter para sair...")

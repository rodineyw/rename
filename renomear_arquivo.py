""" Módulos para renomear arquivos em massa."""

import sys
import os
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QListWidget,
    QFileDialog,
    QMessageBox,
    QProgressBar,
)
import qdarkstyle
import PyPDF2


class GerenciadorPdf(QWidget):
    """Classe para gerenciar funções relacionadas a arquivos PDF."""

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """Inicializa a interface do usuário."""
        self.layout = QVBoxLayout(self)

        self.label = QLabel("Selecione uma ação:", self)
        self.layout.addWidget(self.label)

        self.lista_arquivos = QListWidget(self)
        self.layout.addWidget(self.lista_arquivos)

        self.progress_bar = QProgressBar(self)
        self.layout.addWidget(self.progress_bar)

        self.botao_selecionar = QPushButton("Selecionar Arquivos", self)
        self.botao_selecionar.clicked.connect(self.selecionar_arquivos)
        self.layout.addWidget(self.botao_selecionar)

        self.botao_dividir = QPushButton("Dividir PDFs Selecionados", self)
        self.botao_dividir.clicked.connect(self.dividir_pdfs)
        self.layout.addWidget(self.botao_dividir)

        self.merge_button = QPushButton("Mesclar PDFs Selecionados", self)
        self.merge_button.clicked.connect(self.merge_pdfs)
        self.layout.addWidget(self.merge_button)

        self.botao_renomear = QPushButton("Renomear Arquivos", self)
        self.botao_renomear.clicked.connect(self.renomear_arquivos)
        self.layout.addWidget(self.botao_renomear)

        self.setWindowTitle("Gerenciador de Arquivos PDF")
        self.setGeometry(300, 300, 600, 400)

    def selecionar_arquivos(self):
        """Abre um diálogo para selecionar arquivos PDF."""
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Selecionar Arquivos",
            "",
            "All Files (*);;PDF Files (*.pdf)",
        )
        if files:
            self.lista_arquivos.clear()
            self.lista_arquivos.addItems(files)

    def dividir_pdfs(self):
        """Abre um diálogo para selecionar a pasta de saída e divide os PDFs selecionados."""
        pasta_saida = QFileDialog.getExistingDirectory(
            self, "Selecionar Pasta de Saída",
        )
        if pasta_saida and self.lista_arquivos.count() > 0:
            total_files = self.lista_arquivos.count()
            self.progress_bar.setMaximum(total_files)
            for index in range(total_files):
                caminho_arquivo = self.lista_arquivos.item(index).text()
                if caminho_arquivo.lower().endswith(".pdf"):
                    self.processar_pdf(caminho_arquivo, pasta_saida)
                    self.progress_bar.setValue(index + 1)
            self.progress_bar.setValue(0)

    def merge_pdfs(self):
        """Abre um diálogo para selecionar a pasta de saída e mescla os PDFs selecionados."""
        pasta_saida = QFileDialog.getExistingDirectory(
            self, "Selecionar Pasta de Saída",
        )
        if pasta_saida and self.lista_arquivos.count() > 0:
            total_files = self.lista_arquivos.count()
            self.progress_bar.setMaximum(total_files)
            for index in range(total_files):
                caminho_arquivo = self.lista_arquivos.item(index).text()
                if caminho_arquivo.lower().endswith(".pdf"):
                    self.processar_pdf(caminho_arquivo, pasta_saida)
                    self.progress_bar.setValue(index + 1)
            self.progress_bar.setValue(0)

    def processar_pdf(self, caminho_arquivo, pasta_saida):
        """Processa um arquivo PDF dividindo-o em páginas individuais."""
        try:
            with open(caminho_arquivo, "rb") as arquivo_pdf:
                leitor_pdf = PyPDF2.PdfReader(arquivo_pdf)
                num_paginas = len(leitor_pdf.pages)
                for i in range(num_paginas):
                    escritor_pdf = PyPDF2.PdfWriter()
                    escritor_pdf.add_page(leitor_pdf.pages[i])
                    nome_arquivo_saida = f"{os.path.splitext(os.path.basename(caminho_arquivo))[
                        0]}_pagina_{i + 1}.pdf"
                    caminho_completo = os.path.join(
                        pasta_saida, nome_arquivo_saida)
                    with open(caminho_completo, "wb") as arquivo_saida:
                        escritor_pdf.write(arquivo_saida)
        except ImportError as e:
            QMessageBox.critical(self, "Erro ao dividir PDF", str(e))

    def renomear_arquivos(self):
        """Abre um diálogo para selecionar o arquivo de texto com novos nomes e renomeia os arquivos."""
        arquivo_nomes, _ = QFileDialog.getOpenFileName(
            self,
            "Selecionar Arquivo de Nomes",
            "",
            "Text Files (*.txt)",
        )
        if arquivo_nomes:
            try:
                with open(arquivo_nomes, "r", encoding="utf-8") as file:
                    novos_nomes = file.read().splitlines()
                total_files = len(novos_nomes)
                if total_files == self.lista_arquivos.count():
                    self.progress_bar.setMaximum(total_files)
                    for index in range(total_files):
                        caminho_arquivo_original = self.lista_arquivos.item(
                            index
                        ).text()
                        novo_nome = (
                            novos_nomes[index].strip()
                            + os.path.splitext(caminho_arquivo_original)[1]
                        )
                        novo_caminho_arquivo = os.path.join(
                            os.path.dirname(
                                caminho_arquivo_original), novo_nome
                        )
                        os.rename(caminho_arquivo_original,
                                  novo_caminho_arquivo)
                        self.lista_arquivos.item(
                            index).setText(novo_caminho_arquivo)
                        self.progress_bar.setValue(index + 1)
                    self.progress_bar.setValue(0)
                else:
                    QMessageBox.warning(
                        self,
                        "Erro",
                        "O número de nomes no arquivo não corresponde ao número de arquivos selecionados.",
                    )
            except ImportError as e:
                QMessageBox.critical(self, "Erro ao renomear arquivos", str(e))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet())
    ex = GerenciadorPdf()
    ex.show()
    sys.exit(app.exec_())

import os
import pandas as pd
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel, QListWidget,
    QFileDialog, QMessageBox, QProgressBar, QApplication
)
# Ajuste conforme o caminho real de importação
from app.utils.pdf_utils import dividir_pdf, mesclar_pdfs


class GerenciadorPdf(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout(self)
        self.setup_widgets()
        self.setWindowTitle("Gerenciador de Arquivos PDF")
        self.setGeometry(300, 300, 600, 400)

    def setup_widgets(self):
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

    def selecionar_arquivos(self):
        files, _ = QFileDialog.getOpenFileNames(
            self, "Selecionar Arquivos", "", "All Files (*);;PDF Files (*.pdf)"
        )
        if files:
            self.lista_arquivos.clear()
            self.lista_arquivos.addItems(files)

    def dividir_pdfs(self):
        pasta_saida = QFileDialog.getExistingDirectory(
            self, "Selecionar Pasta de Saída")
        if pasta_saida and self.lista_arquivos.count() > 0:
            total_files = self.lista_arquivos.count()
            self.progress_bar.setMaximum(total_files)
            for index in range(total_files):
                caminho_arquivo = self.lista_arquivos.item(index).text()
                if caminho_arquivo.lower().endswith(".pdf"):
                    dividir_pdf(caminho_arquivo, pasta_saida)
                    self.progress_bar.setValue(index + 1)
            self.progress_bar.setValue(0)
            QMessageBox.information(
                self, "Sucesso", "Os PDFs foram divididos com sucesso!")

    def merge_pdfs(self):
        pasta_saida = QFileDialog.getExistingDirectory(
            self, "Selecionar Pasta de Saída")
        if pasta_saida and self.lista_arquivos.count() > 0:
            files = [self.lista_arquivos.item(
                i).text() for i in range(self.lista_arquivos.count())]
            mesclar_pdfs(files, pasta_saida)
            QMessageBox.information(
                self, "Sucesso", "Os PDFs foram mesclados com sucesso!")


if __name__ == "__main__":
    app = QApplication([])
    window = GerenciadorPdf()
    window.show()
    app.exec()

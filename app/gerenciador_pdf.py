import os
import pandas as pd
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel, QListWidget,
    QFileDialog, QMessageBox, QProgressBar, QApplication
)
from utils.pdf_utils import dividir_pdf, mesclar_pdfs, renomear_com_texto, renomear_com_planilha


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

        self.botao_renomear_arquivos = QPushButton(
            "Renomear Arquivos com Texto", self)
        self.botao_renomear_arquivos.clicked.connect(self.renomear_arquivos)
        self.layout.addWidget(self.botao_renomear_arquivos)

        self.botao_renomear_planilha = QPushButton(
            "Renomear com Planilha", self)
        self.botao_renomear_planilha.clicked.connect(
            self.renomear_com_planilha)
        self.layout.addWidget(self.botao_renomear_planilha)

        self.label_colunas = QLabel(
            "Selecione as Colunas para Renomeação", self)
        self.label_colunas.setVisible(False)
        self.layout.addWidget(self.label_colunas)

        self.lista_colunas = QListWidget(self)
        self.lista_colunas.setSelectionMode(
            QListWidget.SelectionMode.MultiSelection)
        self.lista_colunas.setVisible(False)
        self.layout.addWidget(self.lista_colunas)

        self.botao_aplicar_renomeacao = QPushButton("Aplicar Renomeação", self)
        self.botao_aplicar_renomeacao.setVisible(False)
        self.botao_aplicar_renomeacao.clicked.connect(self.aplicar_renomeacao)
        self.layout.addWidget(self.botao_aplicar_renomeacao)

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

    def renomear_arquivos(self):
        arquivo_nomes, _ = QFileDialog.getOpenFileName(
            self, "Selecionar Arquivo de Nomes", "", "Text Files (*.txt)")
        if arquivo_nomes:
            arquivos = [self.lista_arquivos.item(
                i).text() for i in range(self.lista_arquivos.count())]
            renomear_com_texto(arquivos, arquivo_nomes)
            self.lista_arquivos.clear()
            self.lista_arquivos.addItems(arquivos)

    def renomear_com_planilha(self):
        arquivo_planilha, _ = QFileDialog.getOpenFileNames(
            self, "Selecionar Planilha", "", "Excel Files (*.xlsx)")
        if arquivo_planilha:
            self.carregar_colunas(arquivo_planilha[0])

    def carregar_colunas(self, arquivo_planilha):
        try:
            df = pd.read_excel(arquivo_planilha)
            self.lista_colunas.clear()
            self.lista_colunas.addItems(df.columns)
            self.label_colunas.setVisible(True)
            self.lista_colunas.setVisible(True)
            self.botao_aplicar_renomeacao.setVisible(True)
        except Exception as e:
            QMessageBox.critical(self, "Erro ao carregar Colunas", str(e))

    def aplicar_renomeacao(self):
        colunas_selecionadas = [item.text()
                                for item in self.lista_colunas.selectedItems()]
        if not colunas_selecionadas:
            QMessageBox.warning(self, "Erro", "Selecione ao menos uma coluna.")
            return

        arquivo_planilha, _ = QFileDialog.getOpenFileName(
            self, "Selecionar Planilha", "", "Excel Files (*.xlsx)")

        if arquivo_planilha:
            pasta_saida = QFileDialog.getExistingDirectory(
                self, "Selecionar Pasta de Saída")

            if pasta_saida:
                arquivos = [self.lista_arquivos.item(
                    i).text() for i in range(self.lista_arquivos.count())]
                renomear_com_planilha(arquivos, arquivo_planilha,
                                      colunas_selecionadas, pasta_saida)
                self.lista_arquivos.clear()
                self.lista_arquivos.addItems(arquivos)


if __name__ == "__main__":
    app = QApplication([])
    window = GerenciadorPdf()
    window.show()
    app.exec()

import sys
import os
import pandas as pd
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QListWidget,
    QFileDialog, QMessageBox, QProgressBar
)
import qdarkstyle
import PyPDF2
from PyPDF2 import PdfWriter


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
        self.label = QLabel("Selecione uma ação:")
        self.lista_arquivos = QListWidget()
        self.progress_bar = QProgressBar()
        self.botao_selecionar = QPushButton("Selecionar Arquivos")
        self.botao_dividir = QPushButton("Dividir PDFs Selecionados")
        self.merge_button = QPushButton("Mesclar PDFs Selecionados")
        self.botao_renomear = QPushButton("Renomear Arquivos")
        self.botao_renomear_planilha = QPushButton("Renomear com Planilha")
        self.label_colunas = QLabel("Colunas da Planilha:")
        self.lista_colunas = QListWidget()
        self.botao_aplicar_renomeacao = QPushButton("Aplicar Renomeação")

        for widget in [self.label, self.lista_arquivos, self.progress_bar,
                       self.botao_selecionar, self.botao_dividir, self.merge_button,
                       self.botao_renomear, self.botao_renomear_planilha,
                       self.label_colunas, self.lista_colunas, self.botao_aplicar_renomeacao]:
            self.layout.addWidget(widget)
            if widget in [self.label_colunas, self.lista_colunas, self.botao_aplicar_renomeacao]:
                widget.setVisible(False)

        self.botao_selecionar.clicked.connect(self.selecionar_arquivos)
        self.botao_dividir.clicked.connect(self.dividir_pdfs)
        self.merge_button.clicked.connect(self.merge_pdfs)
        self.botao_renomear.clicked.connect(self.renomear_arquivos)
        self.botao_renomear_planilha.clicked.connect(
            self.renomear_com_planilha)
        self.botao_aplicar_renomeacao.clicked.connect(self.aplicar_renomeacao)
        self.lista_colunas.setSelectionMode(
            QListWidget.SelectionMode.MultiSelection)

    def selecionar_arquivos(self):
        files, _ = QFileDialog.getOpenFileNames(
            self, "Selecionar Arquivos", "", "All Files (*);;PDF Files (*.pdf)")
        if files:
            self.lista_arquivos.clear()
            self.lista_arquivos.addItems(files)

    def dividir_pdfs(self):
        pasta_saida = QFileDialog.getExistingDirectory(
            self, "Selecionar Pasta de Saída")
        if pasta_saida and self.lista_arquivos.count() > 0:
            self.processar_pdfs(pasta_saida, self.dividir_pdf)

    def merge_pdfs(self):
        pasta_saida = QFileDialog.getExistingDirectory(
            self, "Selecionar Pasta de Saída")
        if pasta_saida and self.lista_arquivos.count() > 0:
            self.processar_pdfs(pasta_saida, self.mesclar_pdfs, True)

    def processar_pdfs(self, pasta_saida, func, is_merge=False):
        total_files = self.lista_arquivos.count()
        self.progress_bar.setMaximum(total_files)
        merger = PdfWriter() if is_merge else None
        for index in range(total_files):
            caminho_arquivo = self.lista_arquivos.item(index).text()
            if caminho_arquivo.lower().endswith(".pdf"):
                func(caminho_arquivo, pasta_saida, merger)
                self.progress_bar.setValue(index + 1)
        if is_merge and merger:
            arquivo_saida = QFileDialog.getSaveFileName(
                self, "Salvar PDF Mesclado", pasta_saida, "PDF Files (*.pdf)")
            if arquivo_saida[0]:
                with open(arquivo_saida[0], "wb") as f:
                    merger.write(f)
                QMessageBox.information(
                    self, "Sucesso", "Os PDFs foram mesclados com sucesso!")
        self.progress_bar.setValue(0)

    def dividir_pdf(self, caminho_arquivo, pasta_saida, merger=None):
        try:
            with open(caminho_arquivo, "rb") as arquivo_pdf:
                leitor_pdf = PyPDF2.PdfReader(arquivo_pdf)
                for i, page in enumerate(leitor_pdf.pages):
                    escritor_pdf = PyPDF2.PdfWriter()
                    escritor_pdf.add_page(page)
                    nome_arquivo_saida = f"{os.path.splitext(os.path.basename(caminho_arquivo))[
                        0]}_pagina_{i + 1}.pdf"
                    caminho_completo = os.path.join(
                        pasta_saida, nome_arquivo_saida)
                    with open(caminho_completo, "wb") as arquivo_saida:
                        escritor_pdf.write(arquivo_saida)
        except Exception as e:
            QMessageBox.critical(self, "Erro ao dividir PDF", str(e))

    def mesclar_pdfs(self, caminho_arquivo, pasta_saida, merger):
        with open(caminho_arquivo, "rb") as arquivo_pdf:
            leitor_pdf = PyPDF2.PdfReader(arquivo_pdf)
            for page in leitor_pdf.pages:
                merger.add_page(page)

    def renomear_arquivos(self):
        arquivo_nomes, _ = QFileDialog.getOpenFileName(
            self, "Selecionar Arquivo de Nomes", "", "Text Files (*.txt)")
        if arquivo_nomes:
            self.renomear_com_texto(arquivo_nomes)

    def renomear_com_texto(self, arquivo_nomes):
        try:
            with open(arquivo_nomes, "r", encoding="utf-8") as file:
                novos_nomes = file.read().splitlines()
            total_files = len(novos_nomes)
            if total_files == self.lista_arquivos.count():
                self.processar_renomeacao(novos_nomes)
            else:
                QMessageBox.warning(
                    self, "Erro", "O número de nomes no arquivo não corresponde ao número de arquivos selecionados.")
        except Exception as e:
            QMessageBox.critical(self, "Erro ao renomear arquivos", str(e))

    def processar_renomeacao(self, novos_nomes):
        total_files = len(novos_nomes)
        self.progress_bar.setMaximum(total_files)
        for index, novo_nome in enumerate(novos_nomes):
            caminho_arquivo_original = self.lista_arquivos.item(index).text()
            novo_caminho_arquivo = os.path.join(os.path.dirname(
                caminho_arquivo_original), novo_nome + os.path.splitext(caminho_arquivo_original)[1])
            os.rename(caminho_arquivo_original, novo_caminho_arquivo)
            self.lista_arquivos.item(index).setText(novo_caminho_arquivo)
            self.progress_bar.setValue(index + 1)
        self.progress_bar.setValue(0)

    def renomear_com_planilha(self):
        arquivo_planilha, _ = QFileDialog.getOpenFileNames(
            self, "Selecionar Planilha", "", "Excel Files (*.xlsx)")
        if arquivo_planilha:
            self.carregar_colunas(arquivo_planilha)

    def carregar_colunas(self, arquivo_planilha):
        """ Carregar as colunas de uma planilha do Excel para seleção. """
        try:
            df = pd.read_excel(arquivo_planilha)
            self.lista_colunas.clear()
            for coluna in df.columns:
                self.lista_colunas.addItems(coluna)
            self.label_colunas.setVisible(True)
            self.lista_colunas.setVisible(True)
            self.botao_aplicar_renomeacao.setVisible(True)
        except Exception as e:
            QMessageBox.critical(self, "Erro ao carregar Colunas", str(e))

    def aplicar_renomeacao(self):
        colunas_selecionadas = [item.text()
                                for item in self.lista_colunas.selectedItems()]
        arquivo_planilha, _ = QFileDialog.getOpenFileNames(
            self, "Selecionar Planilha", "", "Excel Files (*.xlsx)")
        if arquivo_planilha:
            self.processar_renomeacao_com_planilha(
                arquivo_planilha[0], colunas_selecionadas)

    def processar_renomeacao_com_planilha(self, arquivo_planilha, colunas_selecionadas):
        df = pd.read_excel(arquivo_planilha)
        total_files = self.lista_arquivos.count()
        self.progress_bar.setMaximum(total_files)
        for index in range(total_files):
            caminho_arquivo = self.lista_arquivos.item(index).text()
            nome_partes = [str(df[col][index]) for col in colunas_selecionadas]
            novo_nome = "_".join(nome_partes) + \
                os.path.splitext(caminho_arquivo)[1]
            novo_caminho_arquivo = os.path.join(
                os.path.dirname(caminho_arquivo), novo_nome)
            os.rename(caminho_arquivo, novo_caminho_arquivo)
            self.lista_arquivos.item(index).setText(novo_caminho_arquivo)
            self.progress_bar.setValue(index + 1)
        self.progress_bar.setValue(0)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet())
    gerenciador_pdf = GerenciadorPdf()
    gerenciador_pdf.show()
    sys.exit(app.exec())

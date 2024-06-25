import os
import pandas as pd
from PyPDF2 import PdfWriter, PdfReader


def dividir_pdf(caminho_arquivo, pasta_saida):
    try:
        with open(caminho_arquivo, "rb") as arquivo_pdf:
            leitor_pdf = PdfReader(arquivo_pdf)
            for i, page in enumerate(leitor_pdf.pages):
                escritor_pdf = PdfWriter()
                escritor_pdf.add_page(page)
                nome_arquivo_saida = f"{os.path.splitext(os.path.basename(caminho_arquivo))[
                    0]}_pagina_{i + 1}.pdf"
                caminho_completo = os.path.join(
                    pasta_saida, nome_arquivo_saida)
                with open(caminho_completo, "wb") as arquivo_saida:
                    escritor_pdf.write(arquivo_saida)
    except Exception as e:
        print(f"Erro ao dividir PDF: {e}")


def mesclar_pdfs(lista_arquivos, pasta_saida):
    merger = PdfWriter()
    for arquivo in lista_arquivos:
        with open(arquivo, "rb") as f:
            reader = PdfReader(f)
            for page in reader.pages:
                merger.add_page(page)
    caminho_saida = os.path.join(pasta_saida, "Documento Mesclado.pdf")
    with open(caminho_saida, "wb") as f_out:
        merger.write(f_out)


def renomear_com_texto(lista_arquivos, arquivo_nomes):
    try:
        with open(arquivo_nomes, "r", encoding="utf-8") as file:
            novos_nomes = file.read().splitlines()
        total_files = len(novos_nomes)
        if total_files == len(lista_arquivos):
            for index, novo_nome in enumerate(novos_nomes):
                caminho_arquivo_original = lista_arquivos[index]
                novo_caminho_arquivo = os.path.join(os.path.dirname(
                    caminho_arquivo_original), novo_nome + os.path.splitext(caminho_arquivo_original)[1])
                os.rename(caminho_arquivo_original, novo_caminho_arquivo)
                lista_arquivos[index] = novo_caminho_arquivo
    except Exception as e:
        print(f"Erro ao renomear arquivos: {str(e)}")


def renomear_com_planilha(lista_arquivos, arquivo_planilha, colunas_selecionadas, pasta_saida):
    try:
        df = pd.read_excel(arquivo_planilha)
        total_files = len(lista_arquivos)
        for index in range(total_files):
            caminho_arquivo = lista_arquivos[index]
            nome_partes = [str(df[col][index]) for col in colunas_selecionadas]
            novo_nome = " - ".join(nome_partes) + ".pdf"
            novo_caminho_arquivo = os.path.join(pasta_saida, novo_nome)

            # Ler o PDF original
            pdf_reader = PdfReader(caminho_arquivo)
            pdf_writer = PdfWriter()

            # Adicionar todas as páginas ao novo PDF
            for page_num in range(len(pdf_reader.pages)):
                pdf_writer.add_page(pdf_reader.pages[page_num])

            # Escrever o novo PDF com o novo nome
            with open(novo_caminho_arquivo, 'wb') as output_pdf:
                pdf_writer.write(output_pdf)

            # Atualizar o caminho do arquivo na lista
            lista_arquivos[index] = novo_caminho_arquivo

    except Exception as e:
        print(f"Erro ao renomear arquivos com planilha: {str(e)}")

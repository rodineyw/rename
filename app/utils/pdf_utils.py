import os
import pandas as pd
import fitz
import re
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


def renomear_com_planilha(lista_arquivos, arquivo_planilha, pasta_saida):
    try:
        df = pd.read_excel(arquivo_planilha)
        for arquivo in lista_arquivos:
            # Abrir o PDF
            pdf_document = fitz.open(arquivo)
            page = pdf_document.load_page(0)
            text = page.get_text()

            # Extrair os dados
            descricao_pattern = re.compile(
                r"\b(\d+)\b\s*Descrição:", re.DOTALL)
            valor_pattern = re.compile(r"R\$\s*([\d,]+,\d{2})", re.MULTILINE)

            descricao_match = descricao_pattern.search(text)
            valor_match = valor_pattern.search(text)

            descricao = descricao_match.group(
                1).strip() if descricao_match else None
            valor = valor_match.group(1).strip().replace(
                '.', '').replace(',', '.') if valor_match else None

            # Verificar valores extraídos
            if descricao and valor:
                valor = float(valor)
                descricao = int(descricao)

                matching_row = df[(df['PJ - Protocolo Jurídico']
                                   == descricao) & (df['Valor Líquido'] == valor)]
                if not matching_row.empty:
                    conta = matching_row['Conta'].values[0]
                    valor = matching_row['Valor Líquido'].values[0]
                    banco = matching_row['Banco'].values[0]
                    titulo = matching_row['Título'].values[0]
                    protocolo_juridico = matching_row['PJ - Protocolo Jurídico'].values[0]
                    novo_nome = f"{
                        protocolo_juridico} - {conta} {valor} {banco} {titulo}.pdf"
                    novo_caminho = os.path.join(pasta_saida, novo_nome)

                    # Fechar o documento PDF antes de renomeá-lo
                    pdf_document.close()

                    os.rename(arquivo, novo_caminho)
                    print(f"Arquivo renomeado para: {novo_caminho}")
                else:
                    print(
                        f"Dados não encontrados no arquivo Excel para o arquivo {arquivo}.")
            else:
                print(
                    f"Falha ao extrair a descrição ou valor do PDF {arquivo}.")
    except Exception as e:
        print(f"Erro ao processar a renomeação com planilha: {str(e)}")

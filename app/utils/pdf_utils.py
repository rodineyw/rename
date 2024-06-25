import os
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

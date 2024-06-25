import os
import pandas as pd
import fitz  # PyMuPDF
import re

# Carregar o arquivo Excel
excel_path = 'notas.xlsx'
df = pd.read_excel(excel_path)

# Carregar o arquivo PDF
pdf_path = 'Comprovante.pdf'
pdf_document = fitz.open(pdf_path)

# Extrair texto da primeira página do PDF
page = pdf_document.load_page(0)
text = page.get_text()

# Ajustar regex para capturar "Protocolo Jurídico" e "Valor"
descricao_pattern = re.compile(r"\b(\d+)\b\s*Descrição:", re.DOTALL)
valor_pattern = re.compile(r"R\$\s*([\d,]+,\d{2})", re.MULTILINE)

descricao_match = descricao_pattern.search(text)
valor_match = valor_pattern.search(text)

descricao = descricao_match.group(1).strip() if descricao_match else None
valor = valor_match.group(1).strip().replace(
    '.', '').replace(',', '.') if valor_match else None

# Verificar valores extraídos
print(f"Descrição: {descricao}, Valor: {valor}")

# Comparar com o arquivo Excel
if descricao and valor:
    valor = float(valor)
    descricao = int(descricao)

    matching_row = df[(df['PJ - Protocolo Jurídico'] ==
                       descricao) & (df['Valor Líquido'] == valor)]
    if not matching_row.empty:
        tipo = matching_row['Tipo'].values[0]
        conta = matching_row['Conta'].values[0]
        protocolo_juridico = matching_row['PJ - Protocolo Jurídico'].values[0]
        novo_nome = f"{protocolo_juridico}_{tipo}_{conta}.pdf"
        novo_caminho = os.path.join(os.path.dirname(pdf_path), novo_nome)

        # Fechar o documento PDF antes de renomeá-lo
        pdf_document.close()

        os.rename(pdf_path, novo_caminho)
        print(f"Arquivo renomeado para: {novo_caminho}")
    else:
        print("Dados não encontrados no arquivo Excel.")
else:
    print("Falha ao extrair a descrição ou valor do PDF.")

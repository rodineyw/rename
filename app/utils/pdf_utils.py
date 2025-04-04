import os
import fitz

from PIL import Image
from io import BytesIO


def dividir_pdf(caminho_arquivo, pasta_saida, paginas_por_arquivo=2):
    try:
        # Log para verificar início da função
        print(f"Iniciando divisão do arquivo: {caminho_arquivo}")
        with open(caminho_arquivo, "rb") as arquivo_pdf:
            leitor_pdf = PdfReader(arquivo_pdf)
            num_paginas = len(leitor_pdf.pages)
            # Log do número de páginas
            print(f"Total de páginas no PDF: {num_paginas}")

            for i in range(0, num_paginas, paginas_por_arquivo):
                escritor_pdf = PdfWriter()
                for j in range(paginas_por_arquivo):
                    if i + j < num_paginas:
                        # Log para cada página adicionada
                        print(f"Adicionando página {i + j + 1}")
                        escritor_pdf.add_page(leitor_pdf.pages[i + j])

                nome_arquivo_saida = f"{os.path.splitext(os.path.basename(caminho_arquivo))[
                    0]}_parte_{i // paginas_por_arquivo + 1}.pdf"
                caminho_completo = os.path.join(
                    pasta_saida, nome_arquivo_saida)
                # Log do caminho de saída
                print(f"Salvando parte em: {caminho_completo}")

                with open(caminho_completo, "wb") as arquivo_saida:
                    escritor_pdf.write(arquivo_saida)

                # Log para confirmar que o arquivo foi salvo
                print(f"Arquivo salvo: {caminho_completo}")
    except Exception as e:
        print(f"Erro ao dividir PDF: {e}")


def mesclar_pdfs(lista_arquivos, pasta_saida):
    pdf_writer = PdfWriter()
    arquivos_ignorados = []

    for caminho_do_pdf in lista_arquivos:
        try:
            print(f"Processando: {caminho_do_pdf}")  # Log para depuração

            if not os.path.exists(caminho_do_pdf):
                print(f"Arquivo não encontrado: {caminho_do_pdf}")
                arquivos_ignorados.append(caminho_do_pdf)
                continue

            if os.path.getsize(caminho_do_pdf) == 0:
                print(f"Arquivo vazio: {caminho_do_pdf}")
                arquivos_ignorados.append(caminho_do_pdf)
                continue

            with open(caminho_do_pdf, 'rb') as f:
                pdf_reader = PdfReader(f)
                if len(pdf_reader.pages) == 0:
                    print(f"Arquivo sem páginas válidas: {caminho_do_pdf}")
                    arquivos_ignorados.append(caminho_do_pdf)
                    continue

                for page in pdf_reader.pages:
                    pdf_writer.add_page(page)

        except EmptyFileError:
            print(f"Erro de arquivo vazio: {caminho_do_pdf}")
            arquivos_ignorados.append(caminho_do_pdf)
        except Exception as e:
            print(f"Erro ao processar {caminho_do_pdf}: {e}")
            arquivos_ignorados.append(caminho_do_pdf)

    if len(pdf_writer.pages) > 0:
        caminho_saida = os.path.join(pasta_saida, "Documento_Mesclado.pdf")
        try:
            with open(caminho_saida, "wb") as f_out:
                pdf_writer.write(f_out)
            print(f"PDF mesclado salvo em: {caminho_saida}")
        except Exception as e:
            print(f"Erro ao salvar PDF mesclado: {e}")
            arquivos_ignorados.append(caminho_saida)

    return arquivos_ignorados


def renomear_com_texto(lista_arquivos, arquivo_nomes):
    try:
        with open(arquivo_nomes, "r", encoding="utf-8") as file:
            novos_nomes = file.read().splitlines()

        total_files = len(novos_nomes)
        if total_files == len(lista_arquivos):
            for index, novo_nome in enumerate(novos_nomes):
                caminho_arquivo_original = lista_arquivos[index].data(
                    Qt.ItemDataRole.UserRole)[0]
                novo_caminho_arquivo = os.path.join(os.path.dirname(
                    caminho_arquivo_original), novo_nome + os.path.splitext(caminho_arquivo_original)[1])
                os.rename(caminho_arquivo_original, novo_caminho_arquivo)
                lista_arquivos[index] = novo_caminho_arquivo
    except Exception as e:
        print(f"Erro ao renomear arquivos: {str(e)}")


def comprimir_pdf(file_path, output_path, reduzir_imagem=False, qualidade=75):
    tamanho_original = None
    try:
        # verifica se o arquivo de entrada existe e tem o tamanho > 0
        if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
            print(f"[ERRO] Arquivo de entrada não encontrado ou vazio: {file_path}")
            return None, None
        
        tamanho_original = os.path.getsize(file_path)
        print(f"Tamanho original: {tamanho_original} bytes")
        
        doc = fitz.open(file_path)
        algo_foi_feito = False

        if reduzir_imagem:
            print(f"Tentando reduzir imagens com qualidade JPEG: {qualidade}")
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                images = page.get_images(full=True)
                if images:
                    print(f" Processando {len(images)} imagens na página {page_num + 1}")
                for img_index, img in enumerate(images):
                    xref = img[0]
                    try:
                        base_image = doc.extract_image(xref)
                        image_bytes = base_image["image"]
                        img_original_size = len(image_bytes)
                        print(f"   Imagem {img_index +1} (xref {xref}): {base_image['width']}x{base_image['height']}, formato original: {base_image['ext']}, tamanho original: {img_original_size} bytes")
                        
                        image = Image.open(BytesIO(image_bytes))
                        
                        if image.mode in ("RGBA", "P", "LA"):
                            print(f" Convertendo imagem de {image.mode} para RGB (pode perder transparência)")
                            image = image.convert("RGB")
                        elif image.mode == "CMYK":
                            print(f" Convertendo imagem de {image.mode} para RGB")
                            image = image.convert("RGB")

                        img_io = BytesIO()
                        
                        image.save(img_io, format="JPEG", quality=qualidade, optimize=True, progressive=True)
                        img_nova_size = img_io.tell()
                        
                        print(f" Imagem re-comprimida como JPEG q={qualidade}: {img_nova_size} bytes")
                        
                        if img_nova_size > 0:
                            doc.update_stream(xref, img_io.getValue())
                            print(f" Imagem xref {xref} atualizada no PDF.")
                            algo_foi_feito = True
                        else:
                            print(f" [AVISO] Stream da imagem re-comprimida ficou vazio. Imagem xref {xref} não atualizado.")
                            
                    except Exception as img_error:
                        print(f" [!] Erro ao processar imagem xref {xref}: {img_error}. Pulando esta imagem.")
                        return
        
        print("Salvando PDF com opções: deflate=True, garbage=4, clean=True")
        doc.save(output_path, garbage=4, deflate=True, clean=True)
        doc.close()
        algo_foi_feito = True
        
        tamanho_final = os.path.getsize(output_path)
        print(f"Tamanho final: {tamanho_final} bytes")
        
        return tamanho_original, tamanho_final
    
    except Exception as e:
        print(f"[ERRO FATAL] Falha na compressão PDF '{file_path}': {e}")
        import traceback
        traceback.print_exc()
        
        if 'output_path' is locals() and os.path.exists(output_path):
            try:
                if 'doc' in locals() and doc.is_open:
                    doc.close()
                os.remove(output_path)
                print(f"Arquivo de saída incompleto '{output_path}' removido devido a erro.")
            except Exception as cleanup_error:
                print(f"Erro adicional ao tentar limpar '{output_path}': {cleanup_error}")
                
        return tamanho_original, None
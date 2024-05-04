""" Módulo de importação Python para renomear arquivos. """

import os
import tkinter as tk
from tkinter import filedialog
from typing import List


def selecionar_arquivos():
    """Função que abre um dialogo para selecionar varios arquivos."""
    arquivos = filedialog.askopenfilenames(title="Selecione os arquivos para renomear")
    return arquivos


def ler_nomes_arquivo(caminho_nomes: str) -> List[str]:
    """Função que lê o conteúdo de um arquivo de texto
    e retorna uma lista com os nomes contidos no arquivo."""
    with open(caminho_nomes, "r", encoding="utf-8") as arquivo:
        nomes = [linha.strip() for linha in arquivo if linha.strip()]
    return nomes


def renomear_arquivos(
    arquivos: List[str], lista_novos_nomes: List[str], diretorio_destino: str
) -> None:
    """Função que renomea uma lista de arquivos para novos nomes."""
    if len(arquivos) != len(lista_novos_nomes):
        print("Número de arquivos e nomes não correspondem!")
        return

    for filepath, novo_nome in zip(arquivos, lista_novos_nomes):
        try:
            diretorio_destino, filename = os.path.split(filepath)
            extensao = os.path.splitext(filename)
            novo_nome_arquivo = f"{novo_nome}{extensao}"
            caminho_novo_arquivo = os.path.join(diretorio_destino, novo_nome_arquivo)

            if not os.path.exists(caminho_novo_arquivo):
                os.rename(filepath, caminho_novo_arquivo)
                print(f"Arquivo renomeado: {filename} -> {novo_nome_arquivo}")
            else:
                print(
                    f"Erro: arquivo {novo_nome_arquivo} já existe em {diretorio_destino}"
                )
        except ImportError as e:
            print(f"Erro ao renomear {filepath}: {e}")


def iniciar_interface():
    """Função que inicia a interface gráfica."""
    root = tk.Tk()
    root.title("Renomear arquivos em massa")

    arquivos_selecionados = []

    def selecionar_arquivos_callback():
        arquivos = selecionar_arquivos()
        if arquivos:
            arquivos_selecionados.clear()
            arquivos_selecionados.extend(arquivos)
            arquivos_listbox.delete(0, tk.END)
            for arquivo in arquivos:
                arquivos_listbox.insert(tk.END, arquivo)

    def renomear_arquivos_callback():
        caminho_nomes = filedialog.askopenfilename(
            title="Selecione o arquivo com os novos nomes"
        )
        if caminho_nomes:
            novos_nomes = ler_nomes_arquivo(caminho_nomes)
        diretorio_destino = filedialog.askdirectory(
            title="Selecione o diretório de destino"
        )
        if arquivos_selecionados and novos_nomes and diretorio_destino:
            renomear_arquivos(arquivos_selecionados, novos_nomes, diretorio_destino)
            resultado_label.config(text="Arquivos renomeados com sucesso!")

    arquivo_label = tk.Label(root, text="Arquivos selecionados:")
    arquivos_listbox = tk.Listbox(root, width=50, height=10)
    arquivo_button = tk.Button(
        root, text="Selecionar Arquivos", command=selecionar_arquivos_callback
    )
    renomear_button = tk.Button(
        root, text="Renomear arquivos", command=renomear_arquivos_callback
    )
    resultado_label = tk.Label(root, text="")

    arquivo_label.grid(row=0, column=0, sticky="w", padx=10, pady=5)
    arquivos_listbox.grid(row=1, column=0, columnspan=2, padx=10, pady=5)
    arquivo_button.grid(row=1, column=2, padx=10, pady=5)
    renomear_button.grid(row=3, column=0, columnspan=3, padx=10, pady=10)
    resultado_label.grid(row=4, column=0, columnspan=3)

    root.mainloop()


iniciar_interface()

import os
import tkinter as tk
from tkinter import filedialog


def selecionar_arquivos():
    arquivos = filedialog.askopenfilenames(title="Selecione os arquivos para renomear")
    return arquivos


def renomear_arquivos(arquivos, novo_nome, diretorio_destino):
    if not os.path.exists(diretorio_destino):
        os.makedirs(diretorio_destino)

    for filepath in arquivos:
        diretorio, filename = os.path.split(filepath)
        nome, extensao = os.path.splitext(filename)
        novo_nome_arquivo = f"{novo_nome}_{nome}{extensao}"
        caminho_novo_arquivo = os.path.join(diretorio_destino, novo_nome_arquivo)
        os.rename(filepath, caminho_novo_arquivo)
        print(f"Arquivo renomeado: {filename} -> {novo_nome_arquivo}")


def iniciar_interface():
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
        novo_nome = novo_nome_entry.get()
        diretorio_destino = filedialog.askdirectory(
            title="Selecione o diretório de destino"
        )
        if arquivos_selecionados and novo_nome and diretorio_destino:
            renomear_arquivos(arquivos_selecionados, novo_nome, diretorio_destino)
            resultado_label.config(text="Arquivos renomeados com sucesso!")

    arquivo_label = tk.Label(root, text="Arquivos selecionados:")
    arquivo_listbox = tk.Listbox(root, width=50, height=10)
    arquivo_button = tk.Button(
        root, text="Selecionar Arquivos", command=selecionar_arquivos_callback
    )

    novo_nome_label = tk.Label(root, text="Novo Nome: ")
    novo_nome_entry = tk.Entry(root, width=50)

    renomear_button = tk.Button(
        root, text="Renomear arquivos", command=renomear_arquivos_callback
    )

    resultado_label = tk.Label(root, text="")

    arquivo_label.grid(row=0, column=0, sticky="w", padx=10, pady=5)
    arquivo_listbox.grid(row=1, column=0, columnspan=2, padx=10, pady=5)
    arquivo_button.grid(row=1, column=2, padx=10, pady=5)

    novo_nome_label.grid(row=2, column=0, sticky="w", padx=10, pady=5)
    novo_nome_entry.grid(row=2, column=1, padx=10, pady=5)

    renomear_button.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

    resultado_label.grid(row=4, column=0, columnspan=3)

    root.mainloop()


iniciar_interface()

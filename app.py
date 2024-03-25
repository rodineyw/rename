import os
import tkinter as tk
from tkinter import filedialog, simpledialog


def selecionar_arquivos():
    # Abre uma janela para o usuário selecionar os arquivos que deseja renomear
    arquivos = filedialog.askopenfilenames(title="Selecione os arquivos para renomear")
    return arquivos


def renomear_arquivos(arquivos, novos_nomes, diretorio_destino):
    # Divide a string de novos nomes em uma lista, removendo espaços extras
    lista_novos_nomes = [nome.strip() for nome in novos_nomes.split(",")]

    # Verifica se o número de arquivos corresponde ao número de novos nomes
    if len(arquivos) != len(lista_novos_nomes):
        print("Número de arquivos e nomes não correspondem!")
        return

    # Cria o diretório de destino se ele não existir
    if not os.path.exists(diretorio_destino):
        os.makedirs(diretorio_destino)

    # Renomeia cada arquivo selecionado com o novo nome fornecido
    for filepath, novo_nome in zip(arquivos, lista_novos_nomes):
        diretorio, filename = os.path.split(filepath)
        _, extensao = os.path.splitext(filename)
        novo_nome_arquivo = f"{novo_nome}{extensao}"
        caminho_novo_arquivo = os.path.join(diretorio_destino, novo_nome_arquivo)
        os.rename(filepath, caminho_novo_arquivo)
        print(f"Arquivo renomeado: {filename} -> {novo_nome_arquivo}")


def iniciar_interface():
    # Inicializa a interface gráfica do usuário
    root = tk.Tk()
    root.title("Renomear arquivos em massa")

    arquivos_selecionados = []

    def selecionar_arquivos_callback():
        # Função de callback para selecionar os arquivos
        arquivos = selecionar_arquivos()
        if arquivos:
            arquivos_selecionados.clear()
            arquivos_selecionados.extend(arquivos)
            arquivos_listbox.delete(0, tk.END)
            for arquivo in arquivos:
                arquivos_listbox.insert(tk.END, arquivo)

    def renomear_arquivos_callback():
        # Função de callback para renomear os arquivos selecionados
        novos_nomes = simpledialog.askstring(
            "Novos Nomes", "Digite os novos nomes, separados por vírgula:"
        )
        diretorio_destino = filedialog.askdirectory(
            title="Selecione o diretório de destino"
        )
        if arquivos_selecionados and novos_nomes and diretorio_destino:
            renomear_arquivos(arquivos_selecionados, novos_nomes, diretorio_destino)
            resultado_label.config(text="Arquivos renomeados com sucesso!")

    # Criação dos componentes da interface gráfica
    arquivo_label = tk.Label(root, text="Arquivos selecionados:")
    arquivo_listbox = tk.Listbox(root, width=50, height=10)
    arquivo_button = tk.Button(
        root, text="Selecionar Arquivos", command=selecionar_arquivos_callback
    )
    renomear_button = tk.Button(
        root, text="Renomear arquivos", command=renomear_arquivos_callback
    )
    resultado_label = tk.Label(root, text="")

    # Organizando os componentes na janela
    arquivo_label.grid(row=0, column=0, sticky="w", padx=10, pady=5)
    arquivo_listbox.grid(row=1, column=0, columnspan=2, padx=10, pady=5)
    arquivo_button.grid(row=1, column=2, padx=10, pady=5)
    renomear_button.grid(row=3, column=0, columnspan=3, padx=10, pady=10)
    resultado_label.grid(row=4, column=0, columnspan=3)

    root.mainloop()  # Executa a interface gráfica


iniciar_interface()  # Inicia a execução do programa

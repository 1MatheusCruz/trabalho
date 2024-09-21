import tkinter as tk
from tkinter import messagebox
import re
import sqlite3

# Conexão com o banco de dados SQLite
conexao = sqlite3.connect("cadastros.db")
cursor = conexao.cursor()

# Cria a tabela de cadastros se não existir
cursor.execute('''CREATE TABLE IF NOT EXISTS cadastros (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    idade INTEGER NOT NULL,
                    email TEXT NOT NULL,
                    endereco TEXT NOT NULL,
                    escola TEXT NOT NULL)''')
conexao.commit()

# Senha de administrador
ADMIN_PASSWORD = "admin123"


# Função para validar os campos
def validar_campos():
    nome = entry_nome.get()
    idade = entry_idade.get()
    email = entry_email.get()
    endereco = entry_endereco.get()
    escola = entry_escola.get()

    if len(nome.split()) < 2 or not all(palavra.isalpha() for palavra in nome.split()):
        messagebox.showwarning("Erro", "Nome deve ser completo (primeiro e último nome) e conter apenas letras.")
        return False

    if not idade.isdigit():
        messagebox.showwarning("Erro", "Idade deve ser um número inteiro.")
        return False

    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        messagebox.showwarning("Erro", "E-mail inválido.")
        return False

    if not endereco or not escola:
        messagebox.showwarning("Erro", "Preencha todos os campos.")
        return False

    return True


# Função para adicionar o cadastro ao banco de dados
def adicionar_cadastro():
    if validar_campos():
        nome = entry_nome.get()
        idade = entry_idade.get()
        email = entry_email.get()
        endereco = entry_endereco.get()
        escola = entry_escola.get()

        # Inserir no banco de dados
        cursor.execute('INSERT INTO cadastros (nome, idade, email, endereco, escola) VALUES (?, ?, ?, ?, ?)',
                       (nome, idade, email, endereco, escola))
        conexao.commit()

        messagebox.showinfo("Sucesso", "Cadastro realizado com sucesso!")
        limpar_campos()


# Função para limpar os campos após o cadastro
def limpar_campos():
    entry_nome.delete(0, tk.END)
    entry_idade.delete(0, tk.END)
    entry_email.delete(0, tk.END)
    entry_endereco.delete(0, tk.END)
    entry_escola.delete(0, tk.END)


# Função para solicitar senha de administrador
def solicitar_senha_deletar():
    janela_senha = tk.Toplevel(janela)
    janela_senha.title("Acesso Restrito")
    janela_senha.geometry("300x150")

    label_senha = tk.Label(janela_senha, text="Digite a senha de administrador:", font=("Arial", 10))
    label_senha.pack(pady=10)

    entry_senha = tk.Entry(janela_senha, show="*", font=("Arial", 10))
    entry_senha.pack(pady=10)

    def verificar_senha():
        senha = entry_senha.get()
        if senha == ADMIN_PASSWORD:
            janela_senha.destroy()  # Fecha a janela de senha
            pedir_id_deletar()  # Chama a função para pedir o ID
        else:
            messagebox.showerror("Erro", "Senha incorreta.")
            janela_senha.destroy()

    botao_confirmar = tk.Button(janela_senha, text="Confirmar", command=verificar_senha)
    botao_confirmar.pack(pady=10)


# Função para pedir o ID do cadastro a ser deletado
def pedir_id_deletar():
    janela_id = tk.Toplevel(janela)
    janela_id.title("Deletar Cadastro")
    janela_id.geometry("300x150")

    label_id = tk.Label(janela_id, text="Digite o ID do cadastro:", font=("Arial", 10))
    label_id.pack(pady=10)

    entry_id = tk.Entry(janela_id, font=("Arial", 10))
    entry_id.pack(pady=10)

    def deletar_cadastro():
        id_cadastro = entry_id.get()

        if id_cadastro == "":
            messagebox.showwarning("Erro", "Por favor, insira o ID do cadastro para deletar.")
            return

        # Confirmar deleção
        confirmacao = messagebox.askyesno("Confirmação",
                                          f"Tem certeza que deseja deletar o cadastro com ID {id_cadastro}?")
        if confirmacao:
            # Deletar do banco de dados
            cursor.execute('DELETE FROM cadastros WHERE id = ?', (id_cadastro,))
            conexao.commit()

            if cursor.rowcount == 0:
                messagebox.showinfo("Erro", "Nenhum cadastro encontrado com esse ID.")
            else:
                messagebox.showinfo("Sucesso", f"O cadastro com ID {id_cadastro} foi deletado com sucesso.")
            janela_id.destroy()  # Fecha a janela de ID
        else:
            janela_id.destroy()  # Fecha a janela se a deleção não for confirmada

    botao_deletar = tk.Button(janela_id, text="Deletar Cadastro", command=deletar_cadastro)
    botao_deletar.pack(pady=10)


# Função para fechar a conexão com o banco de dados ao fechar a janela
def fechar_janela():
    conexao.close()
    janela.destroy()


# Interface gráfica aprimorada com estilos
janela = tk.Tk()
janela.title("Cadastro de Pessoas")
janela.geometry("400x400")
janela.configure(bg="#f0f8ff")

# Estilos personalizados
label_font = ("Arial", 12, "bold")
entry_font = ("Arial", 10)
button_font = ("Arial", 10, "bold")

# Rótulos e entradas para os dados
label_nome = tk.Label(janela, text="Nome completo:", bg="#f0f8ff", font=label_font)
label_nome.grid(row=0, column=0, padx=10, pady=10, sticky='w')
entry_nome = tk.Entry(janela, font=entry_font)
entry_nome.grid(row=0, column=1, padx=10, pady=10, sticky='w')

label_idade = tk.Label(janela, text="Idade:", bg="#f0f8ff", font=label_font)
label_idade.grid(row=1, column=0, padx=10, pady=10, sticky='w')
entry_idade = tk.Entry(janela, font=entry_font)
entry_idade.grid(row=1, column=1, padx=10, pady=10, sticky='w')

label_email = tk.Label(janela, text="E-mail:", bg="#f0f8ff", font=label_font)
label_email.grid(row=2, column=0, padx=10, pady=10, sticky='w')
entry_email = tk.Entry(janela, font=entry_font)
entry_email.grid(row=2, column=1, padx=10, pady=10, sticky='w')

label_endereco = tk.Label(janela, text="Endereço:", bg="#f0f8ff", font=label_font)
label_endereco.grid(row=3, column=0, padx=10, pady=10, sticky='w')
entry_endereco = tk.Entry(janela, font=entry_font)
entry_endereco.grid(row=3, column=1, padx=10, pady=10, sticky='w')

label_escola = tk.Label(janela, text="Escola que deseja participar:", bg="#f0f8ff", font=label_font)
label_escola.grid(row=4, column=0, padx=10, pady=10, sticky='w')
entry_escola = tk.Entry(janela, font=entry_font)
entry_escola.grid(row=4, column=1, padx=10, pady=10, sticky='w')

# Botão para adicionar cadastro
botao_adicionar = tk.Button(janela, text="Adicionar Cadastro", font=button_font, bg="#4682b4", fg="white",
                            command=adicionar_cadastro)
botao_adicionar.grid(row=5, column=1, padx=10, pady=20, sticky='w')

# Botão para deletar cadastro (protegido por senha)
botao_deletar = tk.Button(janela, text="Deletar Cadastro", font=button_font, bg="#ff6347", fg="white",
                          command=solicitar_senha_deletar)
botao_deletar.grid(row=6, column=1, padx=10, pady=20, sticky='w')

# Fecha a conexão com o banco de dados ao fechar a janela
janela.protocol("WM_DELETE_WINDOW", fechar_janela)

# Inicia a interface gráfica
janela.mainloop()








from PyPDF2 import PdfReader
import re
import os
from tkinter import filedialog
from tkinter import messagebox
import customtkinter as ctk

texto = ''
numero_empresa = []
documento = []
mes = []
mes2 = ''

def ler_pdf(pasta_arquivo):
    try:
        with open(pasta_arquivo, 'rb') as file:
            pdf_ler = PdfReader(file)
            conteudo_pdf = pdf_ler.pages[0].extract_text()
                
            texto = ''
            documento = []
            mes = []
            mes2 = ''

            for palavras in conteudo_pdf:
                texto += palavras
                    
            num_cli = []

            for i in range(len(texto)):
                    if 'º' in texto[i]:
                        num_cli.append(texto[i+4:i+7])
        
            for i in texto.split():
                documento.append(i)

            def extrair_mes(documento):
                for i in range(len(documento)):
                    if 'abaixo:' in documento[i]:
                        mes.append(documento[i+1:i+4])

                        
            extrair_mes(documento)

            for mess in mes:
                for l in mess:
                    mes2 += l

            def excluir_caracteres(nome_do_arquivo):
                nome_do_arquivo = re.sub(r'[\\/*?:"<>|]', '-', nome_do_arquivo)
                nome_do_arquivo = re.sub(r'\s+', ' ', nome_do_arquivo)
                nome_do_arquivo = re.sub(r'\n', '', nome_do_arquivo)
                return nome_do_arquivo

            Mes = excluir_caracteres(mes2)

            return f'{num_cli[0]} - {Mes}'
    except Exception as e:
        return str(e)

def renomear_arquivos(local_do_arquivo):
    for nome_do_arquivo in os.listdir(local_do_arquivo):
        if nome_do_arquivo.endswith(".pdf"):
            pasta = os.path.join(local_do_arquivo, nome_do_arquivo)
            texto_extraido = ler_pdf(pasta)
            if texto_extraido:
                Texto_padronizado = ler_pdf(pasta)
                novo_nome_do_arquivo = f"{Texto_padronizado}.pdf"
                novo_arquivo_na_pasta = os.path.join(local_do_arquivo, novo_nome_do_arquivo)
                try:
                    os.rename(pasta, novo_arquivo_na_pasta)
                    
                except OSError as e:
                    print(f"Erro ao renomear {nome_do_arquivo}: {e}")
            else:
                print(f"Não foi possível extrair texto do arquivo: {nome_do_arquivo}")

def selecionar_diretorios():
    local_do_arquivo = filedialog.askdirectory()
    if local_do_arquivo:
        if os.path.isdir(local_do_arquivo):
            renomear_arquivos(local_do_arquivo)
            messagebox.showinfo("Sucesso", "Arquivos renomeados com sucesso!")
        else:
            messagebox.showerror("Erro", "O diretório especificado não existe.")

app = ctk.CTk()
app.geometry("400x200")
app.title("Renomear Arquivos PDF")

label = ctk.CTkLabel(app, text="Selecione o diretório com arquivos PDF:")
label.pack(pady=20)

select_button = ctk.CTkButton(app, text="Selecionar Diretório", command=selecionar_diretorios)
select_button.pack(pady=10)

app.mainloop()

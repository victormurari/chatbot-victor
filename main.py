import streamlit as st
import os
import openai

st.set_page_config(page_title="Chat com Victor Murari")

st.title("Chat com Victor Murari")
st.markdown("Converse com meus projetos e biografia acadêmica.")

# Função para ler todos os arquivos .txt da pasta 'documentos'
def carregar_textos_txt(pasta):
    texto_total = ""
    for nome_arquivo in os.listdir(pasta):
        if nome_arquivo.endswith(".txt"):
            caminho = os.path.join(pasta, nome_arquivo)
            with open(caminho, 'r', encoding='utf-8') as f:
                texto = f.read()
                texto_total += f"\n---\nConteúdo de {nome_arquivo}:\n{texto}\n"
    return texto_total

# Carrega todos os textos .txt da pasta documentos
texto_base = carregar_textos_txt("documentos")

# Campo para a pergunta do usuário
pergunta = st.text_input("Digite sua pergunta:")

if pergunta:
    openai.api_key = st.secrets["OPENAI_API_KEY"]
    resposta = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Você é um assistente acadêmico que responde perguntas sobre Victor Murari com base nos textos dos projetos e biografia dele."},
            {"role": "user", "content": f"Com base neste conteúdo:\n{texto_base}\n\nResponda à pergunta: {pergunta}"}
        ],
        temperature=0.7
    )
    st.write(resposta.choices[0].message["content"])

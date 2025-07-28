import os
import streamlit as st
from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def carregar_textos_txt(pasta):
    textos = []
    for nome_arquivo in os.listdir(pasta):
        if nome_arquivo.endswith(".txt"):
            caminho_arquivo = os.path.join(pasta, nome_arquivo)
            with open(caminho_arquivo, "r", encoding="utf-8") as f:
                textos.append(f.read())
    return "\n\n".join(textos)

texto_base = carregar_textos_txt("documentos")

st.set_page_config(page_title="Chat com Victor Murari")
st.title("Chat com Victor Murari")
st.write("Converse com meus projetos e biografia acadêmica.")

pergunta = st.text_input("Digite sua pergunta:")

if pergunta:
    try:
        resposta = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "Você é um assistente que responde com base na biografia e nos projetos de Victor Murari. Use as informações abaixo como base:\n\n" + texto_base
                },
                {
                    "role": "user",
                    "content": pergunta
                }
            ],
            temperature=0.7,
        )
        st.write(resposta.choices[0].message.content)
    except Exception as e:
        if "RateLimitError" in str(e):
            st.error("Limite de chamadas da API atingido. Por favor, tente novamente mais tarde.")
        else:
            st.error(f"Erro inesperado: {e}")

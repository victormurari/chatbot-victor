import streamlit as st
import os
import PyPDF2
import openai

st.set_page_config(page_title="Chat com Victor Murari")

st.title("Chat com Victor Murari")
st.markdown("Converse com meu currículo e projetos acadêmicos.")

# Função para ler PDFs
def ler_pdf(caminho_pdf):
    with open(caminho_pdf, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        texto = ""
        for page in reader.pages:
            texto += page.extract_text()
        return texto

# Carrega os textos
caminho1 = os.path.join("documentos", "curriculo.pdf")
caminho2 = os.path.join("documentos", "projeto1.txt")

texto_base = ler_pdf(caminho1)
with open(caminho2, 'r', encoding='utf-8') as f:
    texto_base += "\n" + f.read()

# Campo para o usuário perguntar
pergunta = st.text_input("Digite sua pergunta:")

if pergunta:
    openai.api_key = st.secrets["OPENAI_API_KEY"]
    resposta = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Você é um assistente acadêmico que responde perguntas com base no currículo e projetos de Victor Murari."},
            {"role": "user", "content": f"Baseado neste texto: {texto_base}\n\nResponda: {pergunta}"}
        ],
        temperature=0.7
    )
    st.write(resposta.choices[0].message["content"])
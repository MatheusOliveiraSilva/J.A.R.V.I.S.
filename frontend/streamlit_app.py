import streamlit as st
import requests

# Configuração da URL da API
API_URL = "http://localhost:5005/commands/"

st.title("Assistente Inteligente - Histórico de Interações")
st.sidebar.title("Menu")
st.sidebar.write("Escolha uma opção:")

# Exibir histórico de comandos
st.header("Histórico de Comandos")
if st.sidebar.button("Atualizar Histórico"):
    try:
        response = requests.get(API_URL)
        if response.status_code == 200:
            commands = response.json().get("commands", [])
            if commands:
                for command in commands:
                    st.write(f"**Origem:** {command['source']}")
                    st.write(f"**Conteúdo:** {command['content']}")
                    st.write(f"**Ação:** {command['action']}")
                    st.write("---")
            else:
                st.write("Nenhum comando registrado ainda.")
        else:
            st.error(f"Erro ao buscar histórico: {response.status_code}")
    except Exception as e:
        st.error(f"Erro ao conectar à API: {e}")

# Enviar comandos manualmente
st.header("Enviar Comando Manual")
with st.form(key="command_form"):
    source = st.selectbox("Origem do comando", options=["audio", "gesture", "manual"])
    content = st.text_input("Conteúdo do comando")
    action = st.text_input("Ação a ser registrada")
    submit_button = st.form_submit_button("Enviar Comando")

if submit_button:
    try:
        payload = {"source": source, "content": content, "action": action}
        response = requests.post(API_URL, json=payload)
        if response.status_code == 200:
            st.success("Comando enviado com sucesso!")
        else:
            st.error(f"Erro ao enviar comando: {response.status_code}")
    except Exception as e:
        st.error(f"Erro ao conectar à API: {e}")

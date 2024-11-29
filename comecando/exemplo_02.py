import streamlit as st
import logging
from random import randint

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Função para simular o lançamento de um dado
def roll():
    return randint(1, 6)

# Interface Streamlit
st.title("Aplicação com Streamlit e Observabilidade")
player = st.text_input("Digite o nome do jogador (opcional):")

# Lógica para lançar o dado
if st.button("Rolar o Dado"):
    result = roll()
    if player:
        logger.warning("%s está rolando o dado: %s", player, result)
        st.write(f"{player} rolou o dado e obteve: {result}")
    else:
        logger.warning("Jogador anônimo está rolando o dado: %s", result)
        st.write(f"Jogador anônimo rolou o dado e obteve: {result}")

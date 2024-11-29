import streamlit as st
import logging
from random import randint
from opentelemetry import trace

# Configurando o tracer para OpenTelemetry
tracer = trace.get_tracer("streamlit.diceroller")

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Função para lançar o dado
def roll():
    return randint(1, 6)

# Interface com Streamlit
st.title("Rolagem de Dados com Observabilidade")
player = st.text_input("Digite o nome do jogador (opcional):")

# Lógica para lançar o dado
if st.button("Rolar o Dado"):
    with tracer.start_as_current_span("roll_dice"):
        result = roll()
        if player:
            logger.warning("%s está rolando o dado: %s", player, result)
            st.write(f"{player} rolou o dado e obteve: {result}")
        else:
            logger.warning("Jogador anônimo está rolando o dado: %s", result)
            st.write(f"Jogador anônimo rolou o dado e obteve: {result}")

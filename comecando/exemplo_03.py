from random import randint
import streamlit as st
from opentelemetry import trace

# Configurando o tracer
tracer = trace.get_tracer("streamlit.diceroller")

# Função para lançar um dado
def roll():
    # Criação de um novo span manual
    with tracer.start_as_current_span("roll_dice") as roll_span:
        result = randint(1, 6)
        # Adicionando atributos ao span
        roll_span.set_attribute("roll.value", result)
        return result

# Interface do Streamlit
st.title("Instrumentação Manual com OpenTelemetry")
player = st.text_input("Digite o nome do jogador (opcional):")

if st.button("Rolar o Dado"):
    with tracer.start_as_current_span("player_action") as player_span:
        result = roll()
        player_span.set_attribute("player.name", player or "Anônimo")
        st.write(f"Resultado do dado: {result}")

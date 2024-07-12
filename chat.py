__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import streamlit as st
 
from main import chatbot


# Configuration de l'interface
st.title("AuditBot")
st.write("Interact with the chatbot.")

# Initialisation de l'historique des messages
if "messages" not in st.session_state:
    st.session_state.messages = []



# Saisie utilisateur
user_input = st.text_input("Vous:", "")

# Si l'utilisateur a entré un message, ajoutez-le à l'historique et obtenez la réponse du chatbot
if user_input:
    st.session_state.messages.append(f"Vous: {user_input}")
    response = chatbot(user_input)
    st.session_state.messages.append(f"Chatbot: {response}")

# Affichage de l'historique des messages
for message in st.session_state.messages:
    st.write(message)

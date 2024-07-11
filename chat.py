__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import streamlit as st
import requests
from main import chatbot


# Configuration de l'interface
st.title("AuditBot")
st.write("Interact with the chatbot powered by RAG and Gemini.")

# Initialisation de l'historique des messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Fonction pour envoyer le message à l'API Gemini et recevoir une réponse
def get_response_from_gemini(message):
    # Remplacez par votre propre logique pour interagir avec l'API Gemini
    # Par exemple :
    api_url = "https://api.gemini.com/chatbot"  # URL fictive, remplacez par la véritable URL de l'API
    headers = {
        "Authorization": "AIzaSyDebvFeAS_ECJlbKImDBl4mqQRPgg6zEjQ",
        "Content-Type": "application/json"
    }
    data = {
        "input": message
    }
    response = requests.post(api_url, headers=headers, json=data)
    return response.json()["response"]

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

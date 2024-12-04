import streamlit as st
import requests
import json

# URL da API REST do Firestore
FIREBASE_PROJECT_ID = "banco-gps"  # Seu projeto no Firebase
FIREBASE_API_URL = f"https://firestore.googleapis.com/v1/projects/{FIREBASE_PROJECT_ID}/databases/(default)/documents/"

# Sua chave de API (não expor publicamente)
API_KEY = "AIzaSyADYPBbiXNg9u_fUbSDs6KOU3S2GAypOwI"

# Função para acessar o Firestore e obter coordenadas
def get_firestore_data():
    # URL para acessar a coleção no Firestore
    url = f"{FIREBASE_API_URL}coordenadas?key={API_KEY}"
    
    # Fazer a requisição GET
    response = requests.get(url)
    
    if response.status_code == 200:
        # Sucesso, processa a resposta
        data = response.json()
        return data.get('documents', [])
    else:
        # Se houver erro, exibe a mensagem
        st.error(f"Erro ao acessar Firestore: {response.status_code}")
        return []

# Exibe o título no Streamlit
st.title("Exibindo Coordenadas do Firestore")

# Chama a função para obter as coordenadas do Firestore
coordinates = get_firestore_data()

# Exibe as coordenadas no mapa, se houver dados
if coordinates:
    for item in coordinates:
        latitude = item['fields']['latitude']['doubleValue']
        longitude = item['fields']['longitude']['doubleValue']
        st.write(f"Coordenada: Latitude = {latitude}, Longitude = {longitude}")
else:
    st.warning("Nenhuma coordenada encontrada no Firestore.")

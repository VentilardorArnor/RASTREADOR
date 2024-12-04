import streamlit as st
import folium
from streamlit_folium import folium_static
import requests
import json
import time

# URL da API REST do Firestore
FIREBASE_PROJECT_ID = "banco-gps"  # Seu projeto no Firebase
FIREBASE_API_URL = f"https://firestore.googleapis.com/v1/projects/{FIREBASE_PROJECT_ID}/databases/(default)/documents/"

# Sua chave de API
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

# Função para criar o mapa com o ônibus em movimento
def create_map_with_bus(latitude, longitude):
    # Criar o mapa centrado na primeira coordenada do ônibus
    m = folium.Map(location=[latitude, longitude], zoom_start=14)

    # Adicionar o marcador do ônibus no mapa
    bus_marker = folium.Marker([latitude, longitude], popup="Ônibus", icon=folium.Icon(color="blue"))
    bus_marker.add_to(m)

    return m

# Função para simular o movimento do ônibus
def simulate_bus_movement():
    # Exibe o título
    st.title("Simulação de Movimento do Ônibus no OpenStreetMap")
    
    # Inicia a atualização
    while True:
        # Obtém as coordenadas mais recentes do Firestore
        coordinates = get_firestore_data()
        
        if coordinates:
            # Pegue a última coordenada
            lat = coordinates[0]['fields']['latitude']['doubleValue']
            lon = coordinates[0]['fields']['longitude']['doubleValue']
            
            # Crie e exiba o mapa atualizado
            m = create_map_with_bus(lat, lon)
            folium_static(m)
            
            # Aguarda 5 segundos antes de atualizar a posição (simula o movimento)
            time.sleep(5)
        else:
            st.warning("Nenhuma coordenada encontrada no Firestore.")
            break

# Inicia a simulação do movimento do ônibus
simulate_bus_movement()

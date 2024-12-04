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

# Função para criar o mapa inicial com o ônibus
def create_map_with_bus(latitude, longitude):
    # Criar o mapa centrado na posição do ônibus
    m = folium.Map(location=[latitude, longitude], zoom_start=14)

    # Adicionar marcador do ônibus
    folium.Marker([latitude, longitude], popup="Ônibus", icon=folium.Icon(color="blue")).add_to(m)
    
    return m

# Função para simular o movimento do ônibus e atualizar o mapa
def simulate_bus_movement():
    # Exibe o título
    st.title("Simulação de Movimento do Ônibus no OpenStreetMap")
    
    # Inicializa o mapa com as coordenadas iniciais (se houver dados no Firestore)
    coordinates = get_firestore_data()
    if coordinates:
        lat = coordinates[0]['fields']['latitude']['doubleValue']
        lon = coordinates[0]['fields']['longitude']['doubleValue']
        
        # Criar o mapa inicial
        map_display = st.empty()  # Cria um espaço vazio para atualizar o mapa
        m = create_map_with_bus(lat, lon)
        folium_static(m)  # Exibe o mapa inicialmente
        
        # Simulação de movimento do ônibus (atualizações periódicas)
        while True:
            # Obtém as coordenadas mais recentes
            coordinates = get_firestore_data()
            
            if coordinates:
                # Obtém a última coordenada
                lat = coordinates[0]['fields']['latitude']['doubleValue']
                lon = coordinates[0]['fields']['longitude']['doubleValue']
                
                # Atualiza o mapa (limpa e cria novamente o mapa com a nova posição)
                m = create_map_with_bus(lat, lon)
                
                # Atualiza o mapa no espaço vazio
                map_display.empty()  # Limpa o mapa anterior
                folium_static(m)  # Exibe o mapa atualizado
                
                # Aguarda 5 segundos antes de atualizar a posição
                time.sleep(5)
            else:
                st.warning("Nenhuma coordenada encontrada no Firestore.")
                break
    else:
        st.warning("Nenhuma coordenada disponível para exibir.")

# Inicia a simulação do movimento do ônibus
simulate_bus_movement()

import streamlit as st
import json
import firebase_admin
from firebase_admin import credentials, firestore

# Função para conectar ao Firebase usando a variável de ambiente 'firebase_credentials'
def initialize_firebase():
    # Recuperar a chave 'firebase_credentials' diretamente das Secrets do Streamlit
    cred_dict = st.secrets["firebase_credentials"]

    if not cred_dict:
        st.error("As credenciais do Firebase não estão configuradas nas Secrets!")
        st.stop()
    
    # Inicializar o Firebase com as credenciais
    cred = credentials.Certificate(cred_dict)
    firebase_admin.initialize_app(cred)

# Inicializar o Firebase
initialize_firebase()

# Função para criar o mapa
def create_map():
    # Coordenadas de exemplo (São Paulo)
    latitude = -1.4740785281198614
    longitude = -48.45163997645187

    # Criar o mapa usando o OpenStreetMap como base
    m = folium.Map(location=[latitude, longitude], zoom_start=12)

    # Adicionar um marcador
    folium.Marker([latitude, longitude], popup="São Paulo").add_to(m)

    return m

# Criar o título para o Streamlit
st.title("A Bosta do Circular")

# Criar o mapa
m = create_map()

# Exibir o mapa no Streamlit
folium_static(m)

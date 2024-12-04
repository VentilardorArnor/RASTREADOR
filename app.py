import json
import os
import firebase_admin
from firebase_admin import credentials, firestore
import streamlit as st

# Função para conectar ao Firebase
def initialize_firebase():
    # Carregar as credenciais do Firebase a partir das variáveis de ambiente
    cred_json = os.getenv('firebase_credentials')  # Obtém a variável 'firebase_credentials'
    
    if not cred_json:
        st.error("A variável de ambiente 'firebase_credentials' não foi configurada!")
        st.stop()
    
    # O TOML precisa ser convertido de volta para JSON
    cred_dict = json.loads(cred_json)  # Converte a string JSON em dicionário
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

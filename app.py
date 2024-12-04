import streamlit as st
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static
import time
from firebase_config import db

# Função para pegar as coordenadas mais recentes do Firestore
def get_latest_coordinates():
    # Acesso ao Firestore e leitura da coleção 'coordenadas'
    coordenadas_ref = db.collection('coordenadas').order_by('timestamp', direction=firestore.Query.DESCENDING).limit(1)
    coordenadas = coordenadas_ref.stream()
    
    for doc in coordenadas:
        data = doc.to_dict()
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        timestamp = data.get('timestamp')
        return latitude, longitude, timestamp
    
    return None, None, None  # Caso não haja dados

# Função para criar o mapa com as coordenadas
def create_map(latitude, longitude):
    # Criação do mapa centrado na primeira localização ou coordenadas médias
    m = folium.Map(location=[latitude, longitude], zoom_start=14)
    folium.Marker([latitude, longitude]).add_to(m)
    return m

# Função para exibir o mapa no Streamlit
def display_map():
    st.title('Localizações em Tempo Real')

    while True:
        latitude, longitude, timestamp = get_latest_coordinates()
        
        if latitude is not None and longitude is not None:
            st.subheader(f'Última coordenada recebida: {latitude}, {longitude}')
            
            # Criação do mapa com a coordenada mais recente
            m = create_map(latitude, longitude)
            folium_static(m)
        else:
            st.subheader('Aguardando coordenadas...')
            
        # Atualiza a cada 5 segundos
        time.sleep(5)

if __name__ == "__main__":
    display_map()

import streamlit as st
import folium
from streamlit_folium import folium_static

# Função para criar o mapa
def create_map():
    # Coordenadas de exemplo (São Paulo)
    latitude = -23.5505
    longitude = -46.6333
    
    # Criar o mapa usando o OpenStreetMap como base
    m = folium.Map(location=[latitude, longitude], zoom_start=12)

    # Adicionar um marcador
    folium.Marker([latitude, longitude], popup="São Paulo").add_to(m)

    return m

# Criar o título para o Streamlit
st.title("Mapa Interativo com OpenStreetMap")

# Criar o mapa
m = create_map()

# Exibir o mapa no Streamlit
folium_static(m)

import streamlit as st
import folium
from streamlit_folium import folium_static

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

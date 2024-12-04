import streamlit as st
import folium
from folium import plugins
from google.cloud import firestore
import firebase_admin
from firebase_admin import credentials, firestore

# Carregar as credenciais do Firebase
cred = credentials.Certificate('firebase_credentials.json')
firebase_admin.initialize_app(cred)

# Referência ao Firestore
db = firestore.client()

# Função para pegar as coordenadas do Firestore
def get_coordinates():
    # Referência à coleção onde estão as coordenadas
    coordinates_ref = db.collection('coordenadas')
    docs = coordinates_ref.stream()

    coordinates = []
    for doc in docs:
        # Supondo que cada documento tenha 'latitude' e 'longitude'
        data = doc.to_dict()
        latitude = data.get('latitude', {}).get('doubleValue', None)
        longitude = data.get('longitude', {}).get('doubleValue', None)
        if latitude is not None and longitude is not None:
            coordinates.append((latitude, longitude))
    return coordinates

# Função para criar o mapa com folium
def create_map(coordinates):
    # Criar um mapa centrado na primeira coordenada ou em um ponto padrão
    if coordinates:
        lat, lon = coordinates[0]
        m = folium.Map(location=[lat, lon], zoom_start=12)
    else:
        m = folium.Map(location=[0, 0], zoom_start=2)

    # Adicionar marcadores para cada coordenada
    for lat, lon in coordinates:
        folium.Marker([lat, lon]).add_to(m)

    return m

# Título do app
st.title("Mapa Interativo com Coordenadas do Firebase")

# Pegar as coordenadas do Firestore
coordinates = get_coordinates()

# Criar o mapa
m = create_map(coordinates)

# Exibir o mapa no Streamlit
folium_static(m)


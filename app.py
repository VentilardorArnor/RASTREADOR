import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import folium
from geopy.geocoders import Nominatim

# Inicializa o Firebase
cred = credentials.Certificate("caminho/para/seu/arquivo-de-chaves.json")  # Substitua pelo caminho para o seu arquivo de chave JSON
firebase_admin.initialize_app(cred)

# Conectando ao Firestore
db = firestore.client()

# Função para obter a coordenada mais recente do Firestore
def get_last_location():
    # Acessa o Firestore e obtém o documento com o ID 'lastLocation'
    coordenadas_ref = db.collection("coordenadas").document("lastLocation")
    doc = coordenadas_ref.get()

    if doc.exists:
        return doc.to_dict()
    else:
        return None

# Função para criar o mapa
def create_map(latitude, longitude):
    if latitude is not None and longitude is not None:
        # Cria um mapa com folium centrado nas coordenadas
        mapa = folium.Map(location=[latitude, longitude], zoom_start=15)
        folium.Marker([latitude, longitude]).add_to(mapa)
        return mapa
    else:
        return None

# Título da página
st.title("Mapa de Localizações em Tempo Real")

# Obtém a coordenada mais recente do Firestore
location = get_last_location()

if location:
    latitude = location.get('latitude')
    longitude = location.get('longitude')

    # Cria o mapa com a coordenada obtida
    mapa = create_map(latitude, longitude)

    if mapa:
        # Exibe o mapa no Streamlit
        st.map(mapa)
else:
    st.write("Nenhuma coordenada encontrada.")

import streamlit as st
import folium
from streamlit_folium import folium_static

def main():
    st.title("Leaflet Map of India")
    
    # Center of India
    india_center = [20.5937, 78.9629]
    
    # Create a folium map centered at India's coordinates
    m = folium.Map(location=india_center, zoom_start=5)
    
    # Display the map in Streamlit using folium_static
    folium_static(m)

if __name__ == "__main__":
    main()

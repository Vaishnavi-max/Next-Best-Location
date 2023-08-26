import streamlit as st
import folium

# Create a Streamlit app
st.title("Interactive Map with Filters")

# Create a sidebar for filters
st.sidebar.header("Filters")

# Sample data
data = [
    {"name": "Location 1", "lat": 37.7749, "lon": -122.4194, "category": "A"},
    {"name": "Location 2", "lat": 34.0522, "lon": -118.2437, "category": "B"},
    {"name": "Location 3", "lat": 40.7128, "lon": -74.0060, "category": "A"},
    {"name": "Location 4", "lat": 51.5074, "lon": -0.1278, "category": "C"},
]

# Create filters
selected_category = st.sidebar.selectbox("Select Category", ["All"] + list(set(item["category"] for item in data)))

# Create a map using Folium
m = folium.Map(location=[data[0]["lat"], data[0]["lon"]], zoom_start=4)

# Filter and display markers based on selected category
for item in data:
    if selected_category == "All" or item["category"] == selected_category:
        folium.Marker([item["lat"], item["lon"]], tooltip=item["name"]).add_to(m)

# Display the map using Streamlit
st.write("Map with Markers")
st.write(m._repr_html_(), unsafe_allow_html=True)

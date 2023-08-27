import folium
import math
import geopandas
import pandas as pd
import streamlit as st
import geopandas as gpd
from shapely.geometry import Point
from streamlit_folium import st_folium


def init_map(center=[22.6139, 85.2090], zoom_start=4.5, map_type="https://tiles.stadiamaps.com/tiles/alidade_smooth_dark/{z}/{x}/{y}{r}.png", max_zoom=5):
    attr = "<a href='https://stadiamaps.com/'>Stadia Maps</a>"
    return folium.Map(location=center, zoom_start=zoom_start, tiles=map_type, attr=attr, zoom_control=False, min_zoom=max_zoom)

init_map()

def state_prediction():
    st.write("hello")

def calculate_distance(lat1, long1, lat2, long2):
    pi = 3.14159265358979323846
    dist = math.sin(math.radians(lat1)) * math.sin(math.radians(lat2)) + \
           math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * \
           math.cos(math.radians(long1 - long2))
    dist = math.acos(dist)
    dist = (6371 * pi * dist) / 180
    return dist


def create_point_map(df):
    # Cleaning
    df[['Latitude', 'Longitude']] = df[['Latitude', 'Longitude']].apply(pd.to_numeric, errors='coerce')
    # Convert PandasDataFrame to GeoDataFrame
    df['coordinates'] = df[['Latitude', 'Longitude']].values.tolist()
    df['coordinates'] = df['coordinates'].apply(Point)
    df = geopandas.GeoDataFrame(df, geometry='coordinates')
    df = df.dropna(subset=['Latitude', 'Longitude', 'coordinates'])
    return df


def plot_from_df(df, folium_map):
    df = create_point_map(df)
    for i, row in df.iterrows():
        icon = folium.features.CustomIcon(IM_CONSTANTS[row.Icon_ID], icon_size=(row.Icon_Size, row.Icon_Size))
        folium.Marker([row.Latitude, row.Longitude],
                      tooltip=f'{row.ID}',
                      opacity=row.Opacity,
                      icon=icon).add_to(folium_map)
    return folium_map
    
def plot_from_Citydf(df, folium_map):
    df = create_point_map(df)
    for i, row in df.iterrows():
        radius = 5
        folium.CircleMarker(
            location=[row.Latitude, row.Longitude],
            popup="potential walmart location",
            radius=radius,
            color='white',
            fill=True,
            fill_color='skyblue',
            fill_opacity=0.8,
            tooltip=f'{row.ID}'
        ).add_to(folium_map)
    return folium_map

def clear_map_markers(folium_map):
    st.cache_resource.clear()
    children_copy = folium_map._children.copy()  # Create a copy of the dictionary
    for layer_key, layer in children_copy.items():
        if isinstance(layer, (folium.Marker, folium.CircleMarker)):
            folium_map._children.pop(layer_key)  # Remove the marker from the map's dictionary
    return folium_map



def get_point_from_state():
    cityData = load_Citydf()
    cityData[['Latitude', 'Longitude']] = cityData[['Latitude', 'Longitude']].apply(pd.to_numeric, errors='coerce')
    cityData['coordinates'] = cityData[['Latitude', 'Longitude']].values.tolist()
    cityData['coordinates'] = cityData['coordinates'].apply(Point)
    cityData = geopandas.GeoDataFrame(cityData, geometry='coordinates')
    cityData = cityData.dropna(subset=['Latitude', 'Longitude', 'coordinates'])
    if st.session_state.state_select:
        cityData = cityData[cityData['State'].isin(st.session_state.state_select)]
    
    return cityData


def calculate_distance(lat1, long1, lat2, long2):
    pi = 3.14159265358979323846
    dist = math.sin(math.radians(lat1)) * math.sin(math.radians(lat2)) + \
           math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * \
           math.cos(math.radians(long1 - long2))
    dist = math.acos(dist)
    dist = (6371 * pi * dist) / 180
    return dist

def select_top_5():
    walmartData = load_df()
    cityData = get_point_from_state()
    cityData['min_distance'] = float('inf')  # Initialize minimum distance column
    for walmart_index, walmart_row in walmartData.iterrows():
        walmart_lat = walmart_row['Latitude']
        walmart_lon = walmart_row['Longitude']
        cityData['distance'] = cityData.apply(lambda row: calculate_distance(row['Latitude'], row['Longitude'], walmart_lat, walmart_lon), axis=1)
        cityData['min_distance'] = cityData[['min_distance', 'distance']].min(axis=1)  # Update minimum distance column
    cityData = cityData.sort_values(by=['min_distance'])
    cityData = cityData.head(5)
    print(cityData)
    return cityData

def load_df():
    #cityData = pd.read_csv('../data/cityData.csv')
    walmartStores = pd.read_csv('../data/walmart-stores.csv')
    # data = {'ID': ['Monkey', 'B'],
    #         'Icon_ID': [0, 1],
    #         'Icon_Size': [50,50],
    #         'Opacity': [1, 1],
    #         'Latitude': [28.5275544,19.082502],
    #         'Longitude': [77.0441742,72.7163741]}
    df = pd.DataFrame(walmartStores)
    return df

def load_Citydf():
    cityData = pd.read_csv('../data/cityData.csv')
    df = pd.DataFrame(cityData)
    return df


FACT_BACKGROUND = """
                    <div style="width: 100%;">
                        <div style="
                                    background-color: #ECECEC;
                                    border: 1px solid #ECECEC;
                                    padding: 1.5% 1% 1.5% 3.5%;
                                    border-radius: 10px;
                                    width: 100%;
                                    color: white;
                                    white-space: nowrap;
                                    ">
                          <p style="font-size:20px; color: black;">{}</p>
                          <p style="font-size:33px; line-height: 0.5; text-indent: 10px;""><img src="{}" alt="Example Image" style="vertical-align: middle;  width:{}px;">  {} &emsp; &emsp; </p>
                        </div>
                    </div>
                    """

TITLE = 'Next Best Location'

IM_CONSTANTS = {'LOGO': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQorPbeKx3qEC0IMzcqIdCQeyJuf929raImVcPKSWU&s',
                0: 'https://uploads-ssl.webflow.com/64248e7fd5f30d79c9e57d64/64e6177329c2d71389b1b219_walmart.png',
                1: 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQorPbeKx3qEC0IMzcqIdCQeyJuf929raImVcPKSWU&s',
                }
SELECTED_MAP = {'walmart store': 0, 'walmart store': 1}


@st.cache_resource  # @st.cache_data
def load_map():
    # Load the map
    m = init_map()  # init
    df = load_df()  # load data
    m = plot_from_df(df, m)  # plot points
    return m

def add_to_map(m):
    cityData = select_top_5()
    m = plot_from_Citydf(cityData, m)
    return m


    

def main():
    # format page
    
    st.set_page_config(TITLE, page_icon=IM_CONSTANTS['LOGO'], layout='wide')
    if 'state_names' not in st.session_state:
        st.session_state.state_names = []
    if 'population_factor' not in st.session_state:
        st.session_state.population_factor = 0
    if 'road_quality_factor' not in st.session_state:
        st.session_state.road_quality_factor = 0
    if 'economy_factor' not in st.session_state:
        st.session_state.economy_factor = 0
    

    state_names = [
        "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh",
        "Gujarat", "Haryana", "Himachal Pradesh", "Jammu and Kashmir", "Goa",
        "Jharkhand", "Karnataka", "Kerala", "Madhya Pradesh", "Maharashtra",
        "Manipur", "Meghalaya", "Mizoram", "Nagaland", "Odisha", "Punjab",
        "Rajasthan", "Sikkim", "Tamil Nadu", "Telangana", "Tripura",
        "Uttarakhand", "Uttar Pradesh", "West Bengal",
        "Andaman and Nicobar Islands", "Chandigarh", "Dadra and Nagar Haveli",
        "Daman and Diu", "Delhi", "Lakshadweep", "Puducherry"
    ]

    st.sidebar.multiselect('Select State', state_names, key="state_select")
    st.sidebar.slider('Population Factor', 0, 100, key="population_factor")
    st.sidebar.slider('Road Quality Factor', 0, 100, key="road_quality_factor")
    st.sidebar.slider('Economy Factor', 0, 100, key="economy_factor")
    #print(st.session_state)
   



        
    # load map data @st.cache_resource
    
    m = load_map() 
      
    def clearInput():
        for key in list(st.session_state.keys()):  # Using list to avoid RuntimeError due to change in dict size during iteration
            if key != '8d3a683caaa5100ea90e5eb8746e1c21f3fd3aee816274287029aaf969f69332':
                del st.session_state[key]

    #st.sidebar.button('Clear',on_click=clearInput())
    st.sidebar.button('Apply', on_click=state_prediction)
    st.sidebar.button('Suggest', on_click=add_to_map, args=(m,))
    st.sidebar.button('Clear', on_click=clear_map_markers, args=(m,))



    st.markdown("""
            <style>
                   .block-container {
                        padding-top: 1rem;
                        padding-bottom: 0rem;
                        padding-left: 2rem;
                        padding-right: 2rem;
                    }
            </style>
            """, unsafe_allow_html=True)


  
    # init stored values
    if "selected_id" not in st.session_state:
        st.session_state.selected_id = None

    map_col = st.columns([1])
  
    _,map_col,_ = st.columns([1,10,1])
    with map_col:
        level1_map_data = st_folium(m, height=700, width=1024)
        st.session_state.selected_id = level1_map_data['last_object_clicked_tooltip']

        if st.session_state.selected_id is not None:
            st.write(f'You Have Selected: {st.session_state.selected_id}')
            st.image(IM_CONSTANTS[SELECTED_MAP[st.session_state.selected_id]], width=110)


if __name__ == "__main__":
    main()


import folium
import geopandas
import pandas as pd
import streamlit as st
import geopandas as gpd
from shapely.geometry import Point
from streamlit_folium import st_folium

# import requests
# import geopandas as gpd
# from io import StringIO

# url = 'https://raw.githubusercontent.com/datasets/geo-countries/master/data/countries.geojson'
# response = requests.get(url)
# data = StringIO(response.text)

# world = gpd.read_file(data)

def init_map(center=[22.6139, 85.2090], zoom_start=4.5, map_type="https://tiles.stadiamaps.com/tiles/alidade_smooth_dark/{z}/{x}/{y}{r}.png", max_zoom=5):
    attr = "<a href='https://stadiamaps.com/'>Stadia Maps</a>"
    return folium.Map(location=center, zoom_start=zoom_start, tiles=map_type, attr=attr, zoom_control=False, min_zoom=max_zoom)

init_map()




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
# def plot_from_df(df, folium_map):
#     df = create_point_map(df)
#     circle_options = {
#         'color': 'blue',  # Set circle outline color to blue
#         'fill_color': 'blue',  # Set fill color to blue
#         'fill_opacity': 0.5,  # Set fill opacity
#     }
#     for i, row in df.iterrows():
#         radius = row.Icon_Size / 2  # Calculate radius from icon size
#         folium.CircleMarker(
#             location=[row.Latitude, row.Longitude],
#             radius=radius,
#             tooltip=f'{row.ID}',
#             **circle_options
#         ).add_to(folium_map)
#     return folium_map


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
SELECTED_MAP = {'walmart potential location': 0, 'walmart potential location2': 1}

# world = gpd.read_file('countries.geojson')
# india = world[world['ADMIN'] == 'India']

@st.cache_resource  # @st.cache_data
def load_map():
    # Load the map
    m = init_map()  # init
    df = load_df()  # load data
    m = plot_from_df(df, m)  # plot points
    # folium.GeoJson(india, style_function=lambda feature: {
    # 'fillColor': '#0000FF',  # Blue color for India
    # 'color': 'black',
    # 'weight': 2,
    # 'dashArray': '5, 5',}).add_to(m)
    # folium.GeoJson(world, style_function=lambda feature: {
    #         'fillColor': '#FFFFFF',  # White color for other countries
    #         'color': 'black',
    #         'weight': 2,
    #         'dashArray': '5, 5',}).add_to(m)
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

    st.sidebar.multiselect('Select State', state_names, st.session_state.state_names)
    st.sidebar.slider('Population Factor', 0, 100, st.session_state.population_factor)
    st.sidebar.slider('Road Quality Factor', 0, 100, st.session_state.road_quality_factor)
    st.sidebar.slider('Economy Factor', 0, 100, st.session_state.economy_factor)

    if st.sidebar.button('Apply'):
        st.session_state.state_names = st.sidebar.multiselect('Select State', state_names)
        st.session_state.population_factor = st.sidebar.slider('Population Factor', 0, 100)
        st.session_state.road_quality_factor = st.sidebar.slider('Road Quality Factor', 0, 100)
        st.session_state.economy_factor = st.sidebar.slider('Economy Factor', 0, 100)



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
    #st.title(TITLE)

    # load map data @st.cache_resource
    m = load_map()
    # init stored values
    if "selected_id" not in st.session_state:
        st.session_state.selected_id = None

    # setting up the header with its own row
    # _, r1_col1, r1_col2, r1_col3, _ = st.columns([1, 4.5, 1, 6, 1])
    # with r1_col1:
    #     st.markdown(f"<p style='font-size: 27px;'><i>Interactive Mapping Demonstration</i></p>",
    #                 unsafe_allow_html=True)
    # with r1_col3:
    #     st.write('')

    # main information line: includes map location
    map_col = st.columns([1])
    # _, r2_col1, r2_col2, r2_col3, _ = st.columns([1, 4.5, 1, 6, 1])
    # with r2_col1:
        # info sidebar
        # r2_col1.markdown('## Next Best Location')
        # text1, text2 = "stat1", "stat2"
       # st.markdown(FACT_BACKGROUND.format(text1, IM_CONSTANTS[0], 24, text2), unsafe_allow_html=True)
        # st.markdown("""<div style="padding-top: 15px;"></div>""", unsafe_allow_html=True)
        # text1, text2 = "locations", " YY "
        #st.markdown(FACT_BACKGROUND.format(text1, IM_CONSTANTS[1], 30, text2), unsafe_allow_html=True)
        
        # st.multiselect('Select State', state_names)
        # st.slider('Population Factor', 0, 100)
        # st.slider('Road Quality Factor', 0, 100)
        # st.slider('Economy Factor', 0, 100)
        # st.button('Apply')
        # white space
        # for _ in range(10):
        #     st.markdown("")

        # place for logos
        # logo1, logo2, _ = st.columns([1, 1, 2])
        #logo1.image(IM_CONSTANTS['LOGO'], width=110)

    # white space
    # with r2_col2:
    #     st.write("")

    # map container
    # with r2_col3:
    _,map_col,_ = st.columns([1,10,1])
    with map_col:
        level1_map_data = st_folium(m, height=700, width=1024)
        st.session_state.selected_id = level1_map_data['last_object_clicked_tooltip']

        if st.session_state.selected_id is not None:
            st.write(f'You Have Selected: {st.session_state.selected_id}')
            st.image(IM_CONSTANTS[SELECTED_MAP[st.session_state.selected_id]], width=110)


if __name__ == "__main__":
    main()


# st.button('Click me')
# st.data_editor('Edit data', data)
# st.checkbox('I agree')
# st.toggle('Enable')
# st.radio('Pick one', ['cats', 'dogs'])
# st.selectbox('Pick one', ['cats', 'dogs'])
# st.multiselect('Buy', ['milk', 'apples', 'potatoes'])
# st.slider('Pick a number', 0, 100)
# st.select_slider('Pick a size', ['S', 'M', 'L'])
# st.text_input('First name')
# st.number_input('Pick a number', 0, 10)
# st.text_area('Text to translate')
# st.date_input('Your birthday')
# st.time_input('Meeting time')
# st.file_uploader('Upload a CSV')
# st.download_button('Download file', data)
# st.camera_input("Take a picture")
# st.color_picker('Pick a color')

# # Use widgets' returned values in variables:
# >>> for i in range(int(st.number_input('Num:'))):
# >>>   foo()
# >>> if st.sidebar.selectbox('I:',['f']) == 'f':
# >>>   b()
# >>> my_slider_val = st.slider('Quinn Mallory', 1, 88)
# >>> st.write(slider_val)

# # Disable widgets to remove interactivity:
# >>> st.slider('Pick a number', 0, 100, disabled=True)

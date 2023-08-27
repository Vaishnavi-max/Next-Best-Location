import streamlit as st
import pickle
import pandas as pd
import time
import plotly.express as px
import numpy as np

state_rows = pd.read_csv('tat.csv')
df1 = pd.read_csv('superstore.csv')
df = pd.read_csv('state_reading.csv')

input_values = []
prediction = []
result = []

model2 = pickle.load(open('state_prediction.pkl', 'rb'))

tab1, tab2 = st.tabs(['Prediction','Longs&Lats'])


with tab1:
    

    st.title('NextBestLocation')

   
    # st.code('Metrics')
    pop_slider = float(st.slider(label='Population',
                                min_value=10000,
                                max_value=10000000))
    road_factor = float(st.slider(label="Road Quality",
                                min_value=10000,
                                max_value=1000000))
    economy = st.slider(label="Economy Index",
                        min_value=1000,
                        max_value=1000000)
    literacy_rate = st.slider(label="Literacy Rate",
                            min_value=0,
                            max_value=10)
    tier_value = st.selectbox('Tier Place you looking for?',
                            ('Top', 'Intermediate', 'Low'))

    if tier_value == 'Top':
        tier_value = 1
    elif tier_value == 'Intermediate':
        tier_value = 2
    else:
        tier_value = 3
    lst = [pop_slider, road_factor, tier_value,
        economy, literacy_rate]


    for x in lst:
        input_values.append(x)

    # print(input_values)
    # st.write(input_values)


    placeholder = st.empty()
    st.title('Distributed Region Numbers')

    if st.button('Predict', key='same'):
        st.write('__________________________________________________________')
        prediction = model2.predict([input_values])
        # st.write(prediction[0])
        result = str(prediction[0]).strip()
        df['state'] = df['state'].str.replace(' ', '')
        matching_rows = df[df['state'] == f'{result}']
        st.title(f'Prediction : {result}')

        st.write('__________________________________________________________')
        st.title('Possibility of Transactions & Circulations YoY')

        st.write('__________________________________________________________')
        pred_state_rows = state_rows[state_rows['state'] == f'{result}']

        if not pred_state_rows.empty:
            st.write(pred_state_rows)
            st.write('Scale:[ Thousand units ] ')
        else:
            st.write('No Matching row found!')

        for seconds in range(200):

            df1['sales_new'] = df1['Sales']*np.random.choice(range(1, 5))
            df1['proft_new'] = df1['Profit']*np.random.choice(range(1, 5))
            sales = np.mean(df1['sales_new'])
            proft = np.mean(df1['proft_new'])

            with placeholder.container():
                kpi1, kpi2 = st.columns(2)
                kpi1.metric(label='Sales in Thousands', value=round(
                    sales), delta=round(sales)-10)
                kpi2.metric(label='Profit in Thousands', value=round(
                    proft), delta=round(proft - 10, 2))
            time.sleep(0.5)

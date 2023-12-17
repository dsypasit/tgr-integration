import streamlit as st
import numpy as np
import plotly.express as px
import pandas as pd
from streamlit_autorefresh import st_autorefresh
from streamlit_app import client

st.set_page_config(layout="wide")

st_autorefresh(interval=5000, key="fizzbuzzcounter")

def get_water_level():
    db = client.water_data
    items = db.water_level.find()
    items = list(items)
    df = pd.DataFrame(items)
    df['date'] = pd.to_datetime(df['date'], format = r'%d/%m/%Y %H:%M:%S')
    return df

def get_mqtt_logging():
    db = client.water_data
    items = db.logging.find()
    items = list(items)
    df = pd.DataFrame(items)
    df['date'] = pd.to_datetime(df['date'], format = r'%d/%m/%Y %H:%M:%S')
    return df

level_df = get_water_level()
mqtt_df = get_mqtt_logging()

st.markdown('<h1 style="text-align: center;">IoT Logging</h1>', unsafe_allow_html=True)

st.header('water height latest 5 times')
fig = px.line(level_df[-5:], x='date', y='height')
st.plotly_chart(fig)

it, lt = st.tabs(['Iot', 'Logging'])

with it:
    st.header('Water level From IoT')
    st.dataframe(level_df)

with lt:
    st.header('Logging From MQTT')
    fil = st.checkbox('filter')

    event = st.selectbox('event', mqtt_df['event'].unique(), disabled=not fil)
    mqtt_df_filter = mqtt_df
    if fil:
        mqtt_df_filter = mqtt_df.query('event==@event')

    st.dataframe(mqtt_df_filter)
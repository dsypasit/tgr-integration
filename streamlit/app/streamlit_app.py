import streamlit as st
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import pymongo
from streamlit_autorefresh import st_autorefresh
import os

MONGO_DETAILS = "mongodb://tesarally:contestor@mongoDB:27017"
px.set_mapbox_access_token(os.GETENV('MAP_TOKEN'))

st.set_page_config(layout="wide")

st_autorefresh(interval=5000, key="fizzbuzzcounter")

@st.cache_resource()
def init_connection():
    return pymongo.MongoClient(MONGO_DETAILS)

client = init_connection()

def get_predict_data():
    db = client.water_data
    items = db.predict.find().sort('_id', -1).limit(5)
    items = list(items)
    df = pd.DataFrame(items[::-1])
    df['day'] = df['day'].astype(str)
    return df

def get_raw_data():
    db = client.water_data
    items = db.raw_data.find()
    items = list(items)
    df = pd.DataFrame(items)
    return df, df[:-5]

def water_height_response(height):
    if height < 110:
        return f"# Tomorow water discharge <span style='color: #069c56;'>{height:.2f} </span>m"
    elif height <= 115:
        return f"# Tomorow water discharge <span style='color: #FF681E;'>{height:.2f} </span>m"
    elif height > 115:
        return f"# Tomorow water discharge <span style='color: #D3212C;'>{height:.2f} </span>m"
    # st.markdown(f'### พรุ่งนี้น้ำสูง {30} m')

def water_height_status_response(height):
    if height < 110:
        return f"##### Status <span style='color: #069C56;'>Normal</span>"
    elif height <= 115:
        return f"##### Status <span style='color: #FF681E;'>Aleart</span>"
    elif height > 110:
        return f"##### Status <span style='color: #D3212C;'>Beware</span>"

def color_level(value):
    if value > 200 :
        return '#D3212C'
    elif value > 100:
        return '#FF681E'
    else:
        return '#069C56'

def get_map_data(data):
    d1 = data['discharge_s1'].values[0]
    d2 = data['discharge_s2'].values[0]
    d3 = data['discharge_s3'].values[0]
    df = pd.DataFrame({
        "name": ['m7', 'e98', 'm182'],
        "lat": [15.222777, 15.303226,  15.1326420],
        "lon": [104.858055,   104.50032,  104.4884621 ],
        "discharge": [d1, d2, d3 ],
        "color": [None for _ in range(3)],
        "size": [300, 300, 300]
    })
    df.iloc[0,4] = color_level(df.iloc[0,3])
    df.iloc[1,4] = color_level(df.iloc[1,3])
    df.iloc[2,4] = color_level(df.iloc[2,3])
    return df


    # st.markdown(f'### พรุ่งนี้น้ำสูง {30} m')
today = 60

full_raw_df, raw_df = get_raw_data()
predict_df = get_predict_data()
map_df = get_map_data(raw_df.loc[raw_df['day'] == today])

st.markdown('<h1 style="text-align: center;">Water Monitoring</h1>', unsafe_allow_html=True)

c1, c2 = st.columns(2)

height_s1_yesterday = raw_df.loc[raw_df["day"]==today-1]["height_s1"].values[0]
height_s1_today = raw_df.loc[raw_df["day"]==today]["height_s1"].values[0]
height_s1_tomorrow = predict_df['height_s1'][0]
differ_h_from_tommorow =height_s1_tomorrow-height_s1_today
differ_h_from_today =height_s1_today-height_s1_yesterday
with c1:
    st.metric('Today, the water height of Station 1', f'{height_s1_today:.2f} m', f'{differ_h_from_today:.2f} m', delta_color='inverse')
    o1 = water_height_status_response(height_s1_today)
    st.markdown(o1, unsafe_allow_html=True)

with c2:
    o1 = water_height_response(height_s1_tomorrow)
    st.metric('Tomorrow, the water height of Station 1', f'{height_s1_tomorrow:.2f} m', f'{differ_h_from_tommorow:.2f} m', delta_color='inverse')
    o2 = water_height_status_response(predict_df['height_s1'][0])
    st.markdown(o2, unsafe_allow_html=True)

st.header('Today water discharge')
cc1, cc2, cc3 = st.columns(3)
delta_dis_s1 = raw_df.loc[raw_df["day"] == today]["discharge_s1"].values[0] - raw_df.loc[raw_df["day"] == today-1]["discharge_s1"].values[0]
delta_dis_s2 = raw_df.loc[raw_df["day"] == today]["discharge_s2"].values[0] - raw_df.loc[raw_df["day"] == today-1]["discharge_s2"].values[0]
delta_dis_s3 = raw_df.loc[raw_df["day"] == today]["discharge_s3"].values[0] - raw_df.loc[raw_df["day"] == today-1]["discharge_s3"].values[0]
cc1.metric('station 1', f'{raw_df.loc[raw_df["day"] == today]["discharge_s1"].values[0]:0.2f} m^3 ', f'{delta_dis_s1:.2f} m^3', delta_color='inverse')
cc2.metric('station 2', f'{raw_df.loc[raw_df["day"] == today]["discharge_s2"].values[0]:0.2f} m^3 ', f'{delta_dis_s2} m^3', delta_color='inverse')
cc3.metric('station 3', f'{raw_df.loc[raw_df["day"] == today]["discharge_s3"].values[0]:0.2f} m^3 ', f'{delta_dis_s3} m^3', delta_color='inverse')

st.header('Water discharge map today')
fig = px.scatter_mapbox(map_df, lat="lat", lon="lon", hover_name="name", size='size', range_color=(0, 100),
                        color_continuous_scale=['#069c56', '#ffe733','#ff681e', '#d3212c'], zoom=10, height=500, color='discharge')
st.plotly_chart(fig, use_container_width=True)


st.header('predict height 5 days after')
h_select_graph = st.selectbox('select graph', ['line', 'bar'], index=1)

if h_select_graph == 'bar':
    fig = px.bar(predict_df, x='day', y='height_s1', color_discrete_sequence=px.colors.qualitative.Pastel)
    st.plotly_chart(fig, use_container_width=True)
else:
    fig = px.line(predict_df[-5:], x='day', y='height_s1')
    fig.update_layout(
        xaxis = dict(dtick=1),
    )
    st.plotly_chart(fig, use_container_width=True)

st.header('Display data')
fil = st.checkbox('filter')
gt_select_data = st.selectbox('select data', ['all', 'latest 7 days', 'latest 30 days', 'latest 60 days'], index=0, disabled=not fil)

if gt_select_data == 'latest 7 days':
    r = today - 7
    gt_df = raw_df.query('day > @r & day <= @today')
elif gt_select_data == 'latest 30 days':
    r = today - 30
    gt_df = raw_df.query('day >= @r & day <= @today')
elif gt_select_data == 'latest 60 days':
    r = today - 60
    gt_df = raw_df.query('day >= @r & day <= @today')
else:
    gt_df = raw_df

gt, sumt = st.tabs(['graph', 'summary'])
with gt:
    gt_select_graph = st.selectbox('select graph for display', ['line', 'bar'], index=0)
    gt_select_field = st.selectbox('select field for display', ['height_s1', 'height_s3','discharge_s1', 'discharge_s2', 'discharge_s3'])

    if gt_select_graph == 'bar':
        fig = px.bar(gt_df, x='day', y=gt_select_field, color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig, use_container_width=True)
    else:
        predict_checkbox = st.checkbox('predicted')
        if predict_checkbox:
            fig = go.FigureWidget(data = [
                go.Scatter(x=raw_df['day'], y=raw_df[gt_select_field], line={'dash': 'solid'}, name='raw data'),
                go.Scatter(x=full_raw_df['day'][-6:], y=full_raw_df[gt_select_field][-6:], line={'dash': 'dash'}, name='predicted')
            ])

            st.plotly_chart(fig, use_container_width=True)
        else:
            fig = px.line(gt_df, x='day', y=gt_select_field)
            st.plotly_chart(fig, use_container_width=True)

with sumt:
    st.markdown('### Summarize Metrics')
    sumt_df = gt_df.iloc[:, 2:].agg(['min', 'max', 'mean'])
    st.write(sumt_df)

    st.markdown('### Raw Data Table')
    st.write(gt_df)

    st.markdown('### Predict Table')
    st.write(predict_df)


# df = px.data.carshare()
# st.dataframe(df)

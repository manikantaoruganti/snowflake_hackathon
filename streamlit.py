# streamlit_app.py

import streamlit as st
import pandas as pd
import plotly.express as px
import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas

# ---- PAGE CONFIG ----
st.set_page_config(page_title="CulturaVista", layout="wide")

# ---- HEADER ----
st.title("🇮🇳 CulturaVista: Mapping India’s Soul Through Data")
st.subheader("Explore India's traditional art, culture & tourism trends")

# ---- SNOWFLAKE CONNECTION ----
@st.cache_resource
def init_connection():
    return snowflake.connector.connect(
        user="YOUR_USERNAME",
        password="YOUR_PASSWORD",
        account="YOUR_ACCOUNT_ID",
        warehouse="COMPUTE_WH",
        database="CULTURE_DB",
        schema="PUBLIC"
    )

conn = init_connection()

# ---- DATA FETCHING ----
@st.cache_data
def get_data():
    query = "SELECT * FROM TOURISM_CULTURE_DATA;"
    return pd.read_sql(query, conn)

df = get_data()

# ---- FILTERS ----
states = df['state'].unique().tolist()
selected_state = st.sidebar.selectbox("Select State", states)

artforms = df['art_form'].unique().tolist()
selected_art = st.sidebar.selectbox("Select Art Form", artforms)

filtered_df = df[(df['state'] == selected_state) & (df['art_form'] == selected_art)]

# ---- MAIN VISUALIZATION ----
st.markdown("### 📍 Cultural Hotspots Map")
fig_map = px.scatter_mapbox(
    filtered_df,
    lat="latitude",
    lon="longitude",
    hover_name="place",
    hover_data=["art_form", "season", "footfall"],
    color="footfall",
    size="footfall",
    zoom=4,
    mapbox_style="carto-positron"
)
st.plotly_chart(fig_map, use_container_width=True)

# ---- SEASONALITY CHART ----
st.markdown("### 📊 Tourist Footfall by Season")
season_chart = px.bar(
    filtered_df.groupby('season')['footfall'].sum().reset_index(),
    x="season",
    y="footfall",
    color="season",
    title="Seasonal Trends"
)
st.plotly_chart(season_chart, use_container_width=True)

# ---- CLOSING ----
st.markdown("---")
st.markdown("Built with ❤️ using Streamlit + Snowflake")


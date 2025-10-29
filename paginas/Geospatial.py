import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="Titanic Embarkation Ports Map", layout="centered")
st.title("Titanic Embarkation Map")

path = "bestanden/train.csv"
df = pd.read_csv(path)

df = df[df["Embarked"].notna()]

port_coords = {
    "S": {"lat": 50.903, "lon": -1.404, "name": "Southampton"},
    "C": {"lat": 49.633, "lon": -1.616, "name": "Cherbourg"},
    "Q": {"lat": 51.85, "lon": -8.30, "name": "Queenstown/Cobh"}
}

df["lat"] = df["Embarked"].map(lambda x: port_coords[x]["lat"])
df["lon"] = df["Embarked"].map(lambda x: port_coords[x]["lon"])
df["port_name"] = df["Embarked"].map(lambda x: port_coords[x]["name"])

map_center = {"lat": 50.3755, "lon": -4.1427}  # Plymouth

fig = px.scatter_mapbox(
    df,
    lat="lat",
    lon="lon",
    hover_name="port_name",
    color="Embarked",
    zoom=5,
    height=600
)

fig.update_layout(
    mapbox_style="open-street-map",
    mapbox_center=map_center,
    title="Titanic Embarkation Ports",
    margin={"r":0,"t":50,"l":0,"b":0}
)

st.plotly_chart(fig, use_container_width=True)

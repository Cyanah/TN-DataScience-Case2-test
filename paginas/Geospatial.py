import pandas as pd
import streamlit as st
import folium
from streamlit_folium import st_folium
import os

st.set_page_config(page_title="Titanic Embarkation Ports Map", layout="centered")
st.title("Titanic Embarkation Map")

path = os.path.join("bestanden", "train.csv")
df = pd.read_csv(path)

df = df[df["Embarked"].notna()]

port_coords = {
    "S": {"lat": 50.903, "lon": -1.404, "name": "Southampton"},
    "C": {"lat": 49.633, "lon": -1.616, "name": "Cherbourg"},
    "Q": {"lat": 51.85, "lon": -8.30, "name": "Queenstown"}
}

df["lat"] = df["Embarked"].map(lambda x: port_coords[x]["lat"])
df["lon"] = df["Embarked"].map(lambda x: port_coords[x]["lon"])
df["port name"] = df["Embarked"].map(lambda x: port_coords[x]["name"])

agg_df = df.groupby("Embarked").agg(
    most_frequent_class=("Pclass", lambda x: x.mode()[0]),
    most_frequent_sex=("Sex", lambda x: x.mode()[0]),
    avg_age=("Age", "mean"),
    avg_fare=("Fare", "mean"),
    survival_rate=("Survived", "mean"),
    passenger_count=("PassengerId", "count")
).reset_index()

agg_df["lat"] = agg_df["Embarked"].map(lambda x: port_coords[x]["lat"])
agg_df["lon"] = agg_df["Embarked"].map(lambda x: port_coords[x]["lon"])
agg_df["port name"] = agg_df["Embarked"].map(lambda x: port_coords[x]["name"])

m = folium.Map(location=[50.3755, -4.1427], zoom_start=5, tiles="OpenStreetMap") # Plymouth

for _, row in agg_df.iterrows():
    popup_html = f"""
    <b>{row['port name']}</b><br>
    Passenger Count: {row['passenger_count']}<br>
    Most Frequent Class: {row['most_frequent_class']}<br>
    Most Frequent Sex: {row['most_frequent_sex']}<br>
    Average Age: {row['avg_age']:.1f}<br>
    Average Fare: ${row['avg_fare']:.2f}<br>
    Survival Rate: {row['survival_rate']*100:.1f}%
    """
    folium.CircleMarker(
        location=[row["lat"], row["lon"]],
        radius=10 + row["passenger_count"]/50,
        color="blue",
        fill=True,
        fill_opacity=0.6,
        popup=folium.Popup(popup_html, max_width=300)
    ).add_to(m)

st_folium(m, width=700, height=500)

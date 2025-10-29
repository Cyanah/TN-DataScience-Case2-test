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

agg_df = df.groupby("Embarked").agg(
    most_frequent_class=("Pclass", lambda x: x.mode()[0]),
    most_frequent_sex=("Sex", lambda x: x.mode()[0]),
    avg_age=("Age", "mean"),
    avg_fare=("Fare", "mean"),
    survival_rate=("Survived", "mean"),
    count=("PassengerId", "count")
).reset_index()

agg_df["lat"] = agg_df["Embarked"].map(lambda x: port_coords[x]["lat"])
agg_df["lon"] = agg_df["Embarked"].map(lambda x: port_coords[x]["lon"])
agg_df["port_name"] = agg_df["Embarked"].map(lambda x: port_coords[x]["name"])

map_center = {"lat": 50.3755, "lon": -4.1427}  # Plymouth

fig = px.scatter_mapbox(
    agg_df,
    lat="lat",
    lon="lon",
    size="count",
    hover_name="port_name",
    hover_data={
        "Most Frequent Class": agg_df["most_frequent_class"],
        "Most Frequent Sex": agg_df["most_frequent_sex"],
        "Average Age": agg_df["avg_age"].round(1),
        "Average Fare": agg_df["avg_fare"].round(2),
        "Survival Rate": (agg_df["survival_rate"]*100).round(1)
    },
    color="port_name",
    zoom=5,
    height=600
)

fig.update_layout(
    mapbox_style="open-street-map",
    mapbox_center=map_center,
    title="Titanic Embarkation Ports with Stats",
    margin={"r":0,"t":50,"l":0,"b":0},
    showlegend=False
)

st.plotly_chart(fig, use_container_width=True)

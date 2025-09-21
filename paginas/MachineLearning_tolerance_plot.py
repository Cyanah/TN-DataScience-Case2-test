import pandas as pd
import streamlit as st
import plotly.express as px
import os

path = os.path.join("bestanden", "model_tolerance_results.csv")
df = pd.read_csv(path)

st.title("Machine Learning")


tolerance = st.slider("Select tolerance:", 0, 5, 0)

sub = df[df["Tolerance"] == tolerance]

fig = px.bar(
    sub,
    x="Model",
    y="Mean",
    error_y="Std",
    color="Model",
    title=f"Accuracy with {tolerance} points leeway of tolerance")

fig.update_yaxes(range=[0, 1.05])

st.plotly_chart(fig, use_container_width=True)

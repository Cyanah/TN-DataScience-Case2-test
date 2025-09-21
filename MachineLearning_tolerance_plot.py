# -*- coding: utf-8 -*-
"""
Created on Sun Sep 21 12:33:17 2025

@author: Marti
"""

import pandas as pd
import streamlit as st
import plotly.express as px

df = pd.read_csv("model_tolerance_results.csv")

st.title("Student performance accuracy model")


tolerance = st.slider("Select tolerance for accuracy", 0, 5, 0)

sub = df[df["Tolerance"] == tolerance]

fig = px.bar(
    sub,
    x="Model",
    y="Mean",
    error_y="Std",
    color="Model",
    title=f"Accuracy with {tolerance} leeway of tolerance")

fig.update_yaxes(range=[0, 1.05])

st.plotly_chart(fig, use_container_width=True)



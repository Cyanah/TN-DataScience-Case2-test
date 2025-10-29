import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import os

st.set_page_config(page_title="Titanic Model Accuracy Dashboard", layout="centered")

st.title("🚢 Titanic Model Accuracy Dashboard")

path = os.path.join("bestanden", "Titanic_Model_Combination_Accuracies.csv")
df = pd.read_csv(path)

st.subheader("Models & columns to include/exclude")

col1, col2 = st.columns([1,1])

with col1:
    all_models = sorted(df["Model"].unique())
    selected_models = st.multiselect(
        "Select models to include or exclude:",
        options=all_models,
        default=all_models,
        key="models"
    )

with col2:
    all_features = sorted(set(",".join(df["Features"].values).replace(" ", "").split(",")))
    include_features = []
    for feature in all_features:
        if st.checkbox(feature, value=False, key=f"feature_{feature}"):
            include_features.append(feature)

filtered_df = df[df["Model"].isin(selected_models)]
if include_features:
    filtered_df = filtered_df[
        filtered_df["Features"].apply(lambda f: all(feat in f for feat in include_features))
    ]
  
st.dataframe(filtered_df.sort_values(by="Accuracy", ascending=False), use_container_width=True)

fig = go.Figure()

fig.add_trace(go.Bar(
    x=summary["Model"],
    y=summary["Accuracy"],
    text=summary["Accuracy"].apply(lambda x: f"{x:.3f}"),
    textposition="outside",
    marker=dict(color="royalblue"),
    name="Best Accuracy"
))

fig.update_layout(
    title="📊 Best Model Accuracy Based on Selected Features",
    xaxis_title="Model",
    yaxis_title="Accuracy",
    yaxis=dict(range=[0, 1]),
    template="plotly_white",
    height=500
)

st.plotly_chart(fig, use_container_width=True)

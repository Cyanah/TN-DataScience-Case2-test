import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import os

st.set_page_config(page_title="Titanic Model Accuracy Dashboard", layout="wide")

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

if not filtered_df.empty:
    summary = filtered_df.groupby("Model")["Accuracy"].agg(["mean", "max"]).reset_index()

    fig, ax = plt.subplots(figsize=(10, 6))
    bars1 = ax.bar(summary["Model"], summary["max"], label="Best Accuracy")
    bars2 = ax.bar(summary["Model"], summary["mean"], alpha=0.6, label="Mean Accuracy")

    ax.set_title("Model Accuracies (Mean and Best)", fontsize=14)
    ax.set_xlabel("Model")
    ax.set_ylabel("Accuracy")
    ax.set_ylim(0, 1)
    ax.legend()
    plt.xticks(rotation=45, ha="right")

    for i, v in enumerate(summary["max"]):
        ax.text(i, v + 0.01, f"{v:.3f}", ha="center", fontsize=9)

    st.pyplot(fig)

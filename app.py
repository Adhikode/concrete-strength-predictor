import streamlit as st
import pandas as pd
import numpy as np

from model_store import predict_strength, feature_columns

# -------------------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------------------
st.set_page_config(
    page_title="Concrete Strength Predictor",
    layout="wide"
)

# -------------------------------------------------------------
# HEADER
# -------------------------------------------------------------
st.title("Concrete Compressive Strength Predictor")
st.markdown(
    "<p style='font-size:14px; color:gray; margin-top:-12px;'>"
    "CE 612: Machine Learning in Civil Engineering"
    "</p>",
    unsafe_allow_html=True
)

st.markdown("""
This tool predicts compressive strength (MPa) based on your concrete mix design.
All quantities should be provided in **kg/m³**, and Age in **days**.
""")

st.markdown("---")

# -------------------------------------------------------------
# INPUT UI (Two-column layout)
# -------------------------------------------------------------
left_cols = [
    "Cement", "Blast_Furnace_Slag", "Fly_Ash", "Water", "Superplasticizer",
    "Coarse_Aggregate"
]

right_cols = [
    "Fine_Aggregate", "Age", "Slag", "Silica_Fume", "Limestone_Powder",
    "Quartz_Powder", "Nano_Silica", "Fiber"
]

inputs = {}

col1, col2 = st.columns(2)

# LEFT COLUMN INPUTS
with col1:
    st.subheader("Base Materials")
    for col in left_cols:
        inputs[col] = st.number_input(col, min_value=0.0, value=0.0)

# RIGHT COLUMN INPUTS
with col2:
    st.subheader("Supplementary & Special Materials")
    for col in right_cols:
        inputs[col] = st.number_input(col, min_value=0.0, value=0.0)

# Concrete Type
st.subheader("Concrete Type")
inputs["TypeCode"] = st.selectbox(
    "Choose Type",
    [0, 1],
    format_func=lambda x: "Normal Concrete" if x == 0 else "UHPC"
)

# Placeholder for internal flags (not seen by user)
for col in feature_columns:
    if "_Exists" in col:
        inputs[col] = None

# -------------------------------------------------------------
# AUTO-GENERATE EXISTENCE FLAGS
# -------------------------------------------------------------
df_input = pd.DataFrame([inputs])

flag_map = {
    "Slag": "Slag_Exists",
    "Silica_Fume": "Silica_Fume_Exists",
    "Limestone_Powder": "Limestone_Powder_Exists",
    "Quartz_Powder": "Quartz_Powder_Exists",
    "Nano_Silica": "Nano_Silica_Exists",
    "Fiber": "Fiber_Exists",
    "Blast_Furnace_Slag": "Blast_Furnace_Slag_Exists",
}

for mat, flag in flag_map.items():
    if mat in df_input.columns:
        df_input[flag] = 1 if df_input[mat].iloc[0] > 0 else 0
    else:
        df_input[flag] = 0

# -------------------------------------------------------------
# PREDICTION BUTTON
# -------------------------------------------------------------
st.markdown("---")

if st.button("Predict Compressive Strength"):
    pred = predict_strength(df_input)[0]

    # Prediction Card UI
    st.markdown("""
    <div style="
        background-color:#F0F2F6;
        padding:20px;
        border-radius:10px;
        border-left:5px solid #4A90E2;
        margin-top:20px;
    ">
        <h3 style="margin:0;">Predicted Strength</h3>
        <p style="font-size:28px; font-weight:bold; margin:5px 0;">
            {:.2f} MPa
        </p>
    </div>
    """.format(pred), unsafe_allow_html=True)

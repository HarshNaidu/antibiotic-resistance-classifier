import streamlit as st
from preprocess import load_and_preprocess
from model import train_model
import numpy as np

# Load data and train model
filepath = "ANTIBIOTIC.xlsx"
df, resistance_cols = load_and_preprocess(filepath)
model, feature_cols, report = train_model(df, resistance_cols)

# Streamlit app
st.title("Antibiotic Resistance Classifier")

# Dropdowns with 'All' as default option
dept = st.selectbox("Select DEPT", ['All'] + sorted(df['DEPT'].dropna().unique()))
sample = st.selectbox("Select SAMPLE", ['All'] + sorted(df['SAMPLE'].dropna().unique()))
organism = st.selectbox("Select ORGANISM", ['All'] + sorted(df['ORGANISM'].dropna().unique()))
org_group = st.selectbox("Select Org Group", ['All'] + sorted(df['Org Group'].dropna().unique()))

# Filter based on selection
filtered_df = df.copy()
if dept != 'All':
    filtered_df = filtered_df[filtered_df['DEPT'] == dept]
if sample != 'All':
    filtered_df = filtered_df[filtered_df['SAMPLE'] == sample]
if organism != 'All':
    filtered_df = filtered_df[filtered_df['ORGANISM'] == organism]
if org_group != 'All':
    filtered_df = filtered_df[filtered_df['Org Group'] == org_group]

if not filtered_df.empty:
    input_row = filtered_df.iloc[0]
    features = input_row[feature_cols].replace({'R': 1, 'S': 0, 'I': 0})
    features = np.nan_to_num(features).reshape(1, -1)
    prediction = model.predict(features)[0]

    pred_row = input_row[feature_cols]
    resistant = [abx for abx in feature_cols if pred_row[abx] == 'R']
    sensitive = [abx for abx in feature_cols if pred_row[abx] in ['S', 'I']]

    st.success("Prediction Complete!")
    st.write(f"**Resistant to:** {', '.join(resistant) if resistant else 'None'}")
    st.write(f"**Sensitive to:** {', '.join(sensitive) if sensitive else 'None'}")

else:
    st.warning("No matching data found for selected inputs.")

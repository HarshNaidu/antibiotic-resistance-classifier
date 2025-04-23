import streamlit as st
from preprocess import load_and_preprocess
from model import train_model
import numpy as np

# Load and preprocess data
filepath = "ANTIBIOTIC.xlsx"
df, resistance_cols = load_and_preprocess(filepath)
model, feature_cols, report = train_model(df, resistance_cols)

st.title("Antibiotic Resistance Classifier")

# Dropdowns with 'All' options
dept = st.selectbox("Department", ['Select Department'] + ['All'] + sorted(df['DEPT'].dropna().unique()))
sample = st.selectbox("Sample", ['Select Sample type'] + ['All'] + sorted(df['SAMPLE'].dropna().unique()))
organism = st.selectbox("Organism", ['Select Organism'] + ['All'] + sorted(df['ORGANISM'].dropna().unique()))
org_group = st.selectbox("Organism Group", ['Select Organism Group'] + ['All'] + sorted(df['Org Group'].dropna().unique()))

# Submit button to trigger prediction
if st.button("Predict Resistance"):
    # Check if all selections are 'All'
    if dept == 'All' and sample == 'All' and organism == 'All' and org_group == 'All':
        st.warning("Please select at least one specific option to make a prediction.")
    else:
        # Apply filters
        filtered = df.copy()
        if dept != 'All':
            filtered = filtered[filtered['DEPT'] == dept]
        if sample != 'All':
            filtered = filtered[filtered['SAMPLE'] == sample]
        if organism != 'All':
            filtered = filtered[filtered['ORGANISM'] == organism]
        if org_group != 'All':
            filtered = filtered[filtered['Org Group'] == org_group]

        if filtered.empty:
            st.warning("No match found for the selected combination.")
        else:
            # Take first matching row
            input_row = filtered.iloc[0]
            features = input_row[feature_cols].replace({'R': 1, 'S': 0, 'I': 0})
            features = features.replace('-', np.nan).fillna(0).astype(int).values.reshape(1, -1)

            prediction = model.predict(features)[0]

            # Show resistance profile
            resistant_antibiotics = input_row[feature_cols][input_row[feature_cols] == 'R'].index.tolist()
            sensitive_antibiotics = input_row[feature_cols][input_row[feature_cols].isin(['S', 'I'])].index.tolist()

            st.success("Prediction Complete!")
            st.markdown(f"**Resistant to:** {', '.join(resistant_antibiotics) if resistant_antibiotics else 'None'}")
            st.markdown(f"**Sensitive to:** {', '.join(sensitive_antibiotics) if sensitive_antibiotics else 'None'}")

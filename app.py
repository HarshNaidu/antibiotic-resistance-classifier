import streamlit as st
from preprocess import load_and_preprocess
from model import train_model

# Load and preprocess data
filepath = "ANTIBIOTIC.xlsx"
df, resistance_cols = load_and_preprocess(filepath)

# Train model
model, feature_cols, report = train_model(df, resistance_cols)

# GUI
st.title("Antibiotic Resistance Tier Classifier")

# Dropdowns with blank default
sample = st.selectbox("Select SAMPLE type", [''] + sorted(df['SAMPLE'].dropna().unique()))
organism = st.selectbox("Select ORGANISM", [''] + sorted(df['ORGANISM'].dropna().unique()))
dept = st.selectbox("Select DEPT (optional)", [''] + sorted(df['DEPT'].dropna().unique()))
org_group = st.selectbox("Select Org Group (optional)", [''] + sorted(df['Org Group'].dropna().unique()))

# Only predict if required fields are selected
if sample and organism:
    filtered = df.copy()
    filtered = filtered[filtered['SAMPLE'] == sample]
    filtered = filtered[filtered['ORGANISM'] == organism]

    if dept:
        filtered = filtered[filtered['DEPT'] == dept]
    if org_group:
        filtered = filtered[filtered['Org Group'] == org_group]

    if not filtered.empty:
        input_row = filtered.iloc[0]
        features = input_row[feature_cols].replace({'R': 1, 'S': 0, 'I': 0}).values.reshape(1, -1)
        prediction = model.predict(features)[0]
        st.success(f"Predicted Resistance Tier: {prediction + 1}")  # Re-adjust for display
    else:
        st.warning("No match found for the selected combination.")
else:
    st.info("Please select both SAMPLE and ORGANISM to get a prediction.")

# Show classification report
st.subheader("Model Performance")
for label in ['1', '2', '3', '4']:
    if label in report:
        st.write(f"Tier {label}:")
        st.write(f"Precision: {report[label]['precision']:.2f}, Recall: {report[label]['recall']:.2f}, F1-Score: {report[label]['f1-score']:.2f}")

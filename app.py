import streamlit as st
from preprocess import load_and_preprocess
from model import train_model

# Load and preprocess data
filepath = "ANTIBIOTIC.xlsx"
df, resistance_cols = load_and_preprocess(filepath)

# Train the model
model, feature_cols, report = train_model(df, resistance_cols)

# Streamlit UI
st.title("Antibiotic Resistance Predictor")

# Dropdowns with 'All' as default option
dept = st.selectbox("Select DEPT", ['All'] + sorted(df['DEPT'].dropna().unique()))
sample = st.selectbox("Select SAMPLE", ['All'] + sorted(df['SAMPLE'].dropna().unique()))
organism = st.selectbox("Select ORGANISM", ['All'] + sorted(df['ORGANISM'].dropna().unique()))
org_group = st.selectbox("Select Org Group", ['All'] + sorted(df['Org Group'].dropna().unique()))

# Filter based on user input
filtered = df.copy()
if dept != 'All':
    filtered = filtered[filtered['DEPT'] == dept]
if sample != 'All':
    filtered = filtered[filtered['SAMPLE'] == sample]
if organism != 'All':
    filtered = filtered[filtered['ORGANISM'] == organism]
if org_group != 'All':
    filtered = filtered[filtered['Org Group'] == org_group]

# 🔥 This line ensures we only predict if at least one field is selected
if any(field != 'All' for field in [dept, sample, organism, org_group]):
    if not filtered.empty:
        input_row = filtered.iloc[0]
        features = input_row[feature_cols].replace({'R': 1, 'S': 0, 'I': 0}).values.reshape(1, -1)
        prediction = model.predict(features)[0]

        # Determine resistance and sensitivity
        input_data = input_row[feature_cols]
        resistant = list(input_data[input_data == 'R'].index)
        sensitive = list(input_data[input_data.isin(['S', 'I'])].index)

        st.success("Prediction Complete!")
        st.markdown(f"**Resistant to:** {', '.join(resistant) if resistant else 'None'}")
        st.markdown(f"**Sensitive to:** {', '.join(sensitive) if sensitive else 'None'}")
    else:
        st.warning("No match found for the selected combination.")
else:
    st.info("Please select at least one option to make a prediction.")

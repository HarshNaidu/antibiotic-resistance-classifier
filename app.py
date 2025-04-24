import streamlit as st
from preprocess import load_and_preprocess
from model import train_model

# Full names of antibiotics
antibiotic_full_names = {
    'CIP/LE': 'Ciprofloxacin/Levofloxacin',
    'COT': 'Cotrimoxazole (Trimethoprim-Sulfamethoxazole)',
    'GEN': 'Gentamicin',
    'CXM': 'Cefuroxime',
    'CX': 'Cefoxitin',
    'VA(E)': 'Vancomycin (Etest)',
    'LZ': 'Linezolid',
    'TE': 'Tetracycline',
    'E': 'Erythromycin',
    'CD': 'Clindamycin',
    'P': 'Penicillin',
    'HLG': 'High-level Gentamicin',
    'AMP': 'Ampicillin',
    'AMC': 'Amoxicillin-Clavulanate (Amoxiclav)',
    'AK': 'Amikacin',
    'IPM': 'Imipenem',
    'imipenem-EDTA': 'Imipenem with EDTA (for detecting metallo-beta-lactamases)',
    'MRP': 'Meropenem',
    'PIT': 'Piperacillin-Tazobactam',
    'A/S': 'Ampicillin-Sulbactam',
    'CPM': 'Cefepime',
    'AT': 'Aztreonam',
    'FO': 'Fosfomycin',
    'CL': 'Chloramphenicol',
    'TGC': 'Tigecycline',
    'CAZ': 'Ceftazidime',
    'CAC': 'Ceftazidime-Clavulanate',
    'DAP': 'Daptomycin',
    'CTX/CTR': 'Cefotaxime/Ceftriaxone',
    'CEC': 'Cephalexin or Cefaclor',
    'NIT': 'Nitrofurantoin',
    'TOB': 'Tobramycin',
    'PB': 'Polymyxin B',
    'MI': 'Minocycline',
    'MBL': 'Metallo-Beta-Lactamase',
    'ESBL': 'Extended-Spectrum Beta-Lactamase'
}

# Load data and model
filepath = "ANTIBIOTIC.xlsx"
df, resistance_cols = load_and_preprocess(filepath)
model, feature_cols, report = train_model(df, resistance_cols)

# UI
st.title("Smart Antibiotic Advisor")
st.text("Select all options for the better accuracy.")

# Dropdowns
depts = ['--'] + ['All'] + sorted(df['DEPT'].dropna().unique())
samples = ['--'] + ['All'] + sorted(df['SAMPLE'].dropna().unique())
organisms = ['--'] + ['All'] + sorted(df['ORGANISM'].dropna().unique())
org_groups = ['--'] + ['All'] + sorted(df['Org Group'].dropna().unique())

dept = st.selectbox("Select DEPT", depts)
sample = st.selectbox("Select SAMPLE", samples)
organism = st.selectbox("Select ORGANISM", organisms)
org_group = st.selectbox("Select Org Group", org_groups)

# Filter logic
if dept == "--" and sample == "--" and organism == "--" and org_group == "--":
    st.info("Please select any option to get a prediction.")
elif dept == "All" and sample == "All" and organism == "All" and org_group == "All":
    st.info("Please select valid options to get accurate predictions.")
else:
    filtered = df.copy()

    if dept != "All":
        filtered = filtered[filtered['DEPT'] == dept]
    if sample != "All":
        filtered = filtered[filtered['SAMPLE'] == sample]
    if organism != "All":
        filtered = filtered[filtered['ORGANISM'] == organism]
    if org_group != "All":
        filtered = filtered[filtered['Org Group'] == org_group]

    if not filtered.empty:
        input_row = filtered.iloc[0]
        features = input_row[feature_cols].replace({'R': 1, 'S': 0, 'I': 0}).values.reshape(1, -1)
        prediction = model.predict(features)[0]

        # Show results
        raw_values = input_row[feature_cols]
        resistant = [ab for ab in feature_cols if raw_values[ab] == 'R']
        sensitive = [ab for ab in feature_cols if raw_values[ab] in ['S', 'I', 'A']]

        resistant_full = [antibiotic_full_names.get(ab, ab) for ab in resistant]
        sensitive_full = [antibiotic_full_names.get(ab, ab) for ab in sensitive]

        st.success("Prediction Complete!")
        st.write("### Resistant to:")
        for ab in resistant_full:
            st.markdown(f"- **{ab}**")

        st.write("### Sensitive to:")
        for ab in sensitive_full:
            st.markdown(f"- **{ab}**")
    else:
        st.warning("No matching records found for the selected filters.")

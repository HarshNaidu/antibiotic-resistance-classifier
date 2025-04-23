import pandas as pd

def load_and_preprocess(filepath):
    # Load the raw data sheet
    df = pd.read_excel(filepath, sheet_name='ANTIBIOTIC')

    # Clean column names
    df.columns = df.columns.str.strip()

    # Drop rows without an organism
    df = df[df['ORGANISM'].notna()]

    # Select all relevant antibiotic columns
    selected_antibiotics = [
        'CIP/LE', 'COT', 'GEN', 'CXM', 'CX', 'VA(E)', 'LZ', 'TE', 'E', 'CD',
        'P', 'HLG', 'AMP', 'AMC', 'AK', 'IPM', 'imipenem-EDTA', 'MRP', 'PIT',
        'A/S', 'CPM', 'AT', 'FO', 'CL', 'TGC', 'CAZ', 'CAC', 'DAP', 'CTX/CTR',
        'CEC', 'NIT', 'TOB', 'PB', 'MI', 'MBL', 'ESBL'
    ]

    # Drop rows where all antibiotic values are NaN
    df = df.dropna(subset=selected_antibiotics, how='all')

    return df, selected_antibiotics

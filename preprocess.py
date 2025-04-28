import pandas as pd

def load_and_preprocess(filepath):
    df = pd.read_excel(filepath, sheet_name='ANTIBIOTIC')

    df.columns = df.columns.str.strip()

    df = df[df['ORGANISM'].notna()]

    selected_antibiotics = [
        'CIP/LE', 'COT', 'GEN', 'CXM', 'CX', 'VA(E)', 'LZ', 'TE', 'E', 'CD',
        'P', 'HLG', 'AMP', 'AMC', 'AK', 'IPM', 'imipenem-EDTA', 'MRP', 'PIT',
        'A/S', 'CPM', 'AT', 'FO', 'CL', 'TGC', 'CAZ', 'CAC', 'DAP', 'CTX/CTR',
        'CEC', 'NIT', 'TOB', 'PB', 'MI', 'MBL', 'ESBL'
    ]

    df = df.dropna(subset=selected_antibiotics, how='all')

    return df, selected_antibiotics

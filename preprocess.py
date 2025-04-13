import pandas as pd

def load_and_preprocess(filepath):
    df = pd.read_excel(filepath, sheet_name='ANTIBIOTIC')
    df.columns = df.columns.str.strip()

    df = df[df['ORGANISM'].notna()]
    if 'Unnamed: 42' in df.columns:
        df = df.drop(columns=['Unnamed: 42'])

    # These must exist in your data
    selected_antibiotics = ['CIP/LE', 'GEN', 'IPM', 'PIT', 'CAZ', 'CPM']
    df = df.dropna(subset=selected_antibiotics, how='all')

    df['Resistance Count'] = df[selected_antibiotics].apply(lambda row: sum(row == 'R'), axis=1)

    def assign_tier(count):
        if count == 0:
            return 1
        elif count <= 2:
            return 2
        elif count <= 4:
            return 3
        else:
            return 4

    df['Resistance Tier'] = df['Resistance Count'].apply(assign_tier)

    return df, selected_antibiotics

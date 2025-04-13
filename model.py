import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from xgboost import XGBClassifier

def train_model(df, feature_cols):
    x = df[feature_cols].replace({'R': 1, 'S': 0, 'I': 0})
    x = x.apply(pd.to_numeric, errors='coerce').fillna(0).astype(int)
    y = df['Resistance Tier'] - 1  # XGBoost expects 0-based labels

    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.2, random_state=42
    )

    model = XGBClassifier(use_label_encoder=False, eval_metric='mlogloss')
    model.fit(x_train, y_train)

    y_pred = model.predict(x_test)
    report = classification_report(y_test, y_pred, output_dict=True)

    return model, feature_cols, report

import pandas as pd
from sklearn.metrics import classification_report

from model import train_model
from preprocess import load_and_preprocess

# Load and preprocess training data
train_df, resistance_cols = load_and_preprocess("ANTIBIOTIC.xlsx")

# Train the model
model, feature_cols, report = train_model(train_df, resistance_cols)

# Load and prepare validation data
val_df = pd.read_excel("Validation.xlsx")
x_val = val_df[feature_cols].replace({'R': 1, 'S': 0, 'I': 0}).fillna(0).astype(int)
y_val = x_val.sum(axis=1)
y_val = pd.cut(y_val, bins=[-1, 2, 5, 36], labels=[0, 1, 2]).astype(int)

# Predict and evaluate
y_pred = model.predict(x_val)
print("🔍 Validation Report on Unseen Data:")
print(classification_report(y_val, y_pred))

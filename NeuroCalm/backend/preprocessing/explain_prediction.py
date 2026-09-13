import os
import pandas as pd
import joblib
import shap

# -------------------------------
# Project paths
# -------------------------------

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(os.path.dirname(CURRENT_DIR))

DATA_PATH = os.path.join(
    PROJECT_DIR,
    "dataset",
    "processed",
    "StressLevelDataset.csv"
)

MODEL_PATH = os.path.join(
    PROJECT_DIR,
    "models",
    "neurocalm_random_forest.pkl"
)

# -------------------------------
# Load model and dataset
# -------------------------------

model = joblib.load(MODEL_PATH)
df = pd.read_csv(DATA_PATH)

X = df.drop("stress_level", axis=1)

# -------------------------------
# SHAP Explainer
# -------------------------------

explainer = shap.TreeExplainer(model)

# Explain first sample
sample = X.iloc[[0]]

shap_values = explainer.shap_values(sample)

# -------------------------------
# Get prediction
# -------------------------------

prediction = model.predict(sample)[0]

if prediction == 0:
    stress_level = "Low"
elif prediction == 1:
    stress_level = "Moderate"
else:
    stress_level = "High"

print("=" * 60)
print("NEUROCALM - SHAP EXPLANATION")
print("=" * 60)

print("\nPredicted Stress Level:", stress_level)

# -------------------------------
# Handle SHAP output
# -------------------------------

if isinstance(shap_values, list):
    values = shap_values[prediction][0]
else:
    values = shap_values[0, :, prediction]

# Create feature importance table
importance = pd.DataFrame({
    "Feature": X.columns,
    "SHAP Value": values
})

importance["Impact"] = importance["SHAP Value"].abs()

importance = importance.sort_values(
    "Impact",
    ascending=False
)

print("\nTop Stress Contributing Factors:")

for i, row in importance.head(5).iterrows():
    print(
        f"{row['Feature']}: "
        f"{row['SHAP Value']:.4f}"
    )

print("\n" + "=" * 60)
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

# Load dataset
df = pd.read_csv("../data/Final_Augmented_dataset_Diseases_and_Symptoms.csv")

# Features (all symptom columns)
X = df.drop("diseases", axis=1)

# Target
y = df["diseases"]

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Model (VERY GOOD for this type of data)
model = RandomForestClassifier(n_estimators=200)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))

# Save model
joblib.dump(model, "../model/disease_model.pkl")
joblib.dump(X.columns.tolist(), "../model/feature_names.pkl")

print("✅ Model trained successfully!")

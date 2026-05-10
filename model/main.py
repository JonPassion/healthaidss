import joblib
import pandas as pd

from utils.symptom_mapper import map_symptoms
from utils.llm_engine import generate_medical_response

# Load model
import os
MODEL_DIR = os.path.join(os.path.dirname(__file__), 'model')
model = joblib.load(os.path.join(MODEL_DIR, "disease_model.pkl"))
features = joblib.load(os.path.join(MODEL_DIR, "feature_names.pkl"))


def predict(user_symptoms):
    # Create empty vector
    input_data = [0] * len(features)

    # Fill symptoms
    for symptom in user_symptoms:
        if symptom in features:
            idx = features.index(symptom)
            input_data[idx] = 1

    # Convert to dataframe
    input_df = pd.DataFrame([input_data], columns=features)

    # Get probabilities
    probs = model.predict_proba(input_df)

    # Top 3 diseases
    top_indices = probs[0].argsort()[-3:][::-1]

    results = []
    for i in top_indices:
        disease = model.classes_[i]
        confidence = probs[0][i]
        results.append((disease, round(confidence, 2)))

    return results


# 🔥 MAIN EXECUTION
if __name__ == "__main__":
    user_text = input("Describe your symptoms: ")

    mapped_symptoms = map_symptoms(user_text)
    print("Detected symptoms:", mapped_symptoms)

    # 🔥 ADD IT HERE
    if not mapped_symptoms:
        print("⚠️ No recognizable symptoms detected. Please describe more clearly.")
        exit()

    results = predict(mapped_symptoms)
    print("\nTop Predictions (raw):")
    for disease, prob in results:
        print(f"{disease}: {prob*100:.1f}%")

    print("\n🧠 AI Response:\n")

    try:
        response = generate_medical_response(user_text, results)

        if response.startswith("⚠️ LLM Error"):
            print("LLM unavailable. Showing predictions only.\n")
            print(response)
        else:
            print(response)

    except Exception as e:
        print("LLM crashed. Showing predictions only.\n")
        print("Error:", str(e))

    print("\n⚠️ This is not a medical diagnosis. Consult a doctor.")

    while True:
        user_text = input("Describe your symptoms: ")

        mapped_symptoms = map_symptoms(user_text)

        if not mapped_symptoms:
            print("⚠️ Try describing symptoms more clearly.\n")
            continue

        break
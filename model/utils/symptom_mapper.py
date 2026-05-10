from sentence_transformers import SentenceTransformer
import numpy as np

# Load model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Your dataset features
import joblib
import os
MODEL_DIR = os.path.join(os.path.dirname(__file__), '..', 'model')
features = joblib.load(os.path.join(MODEL_DIR, "feature_names.pkl"))

# Create embeddings for symptoms
feature_embeddings = model.encode(features)


def map_symptoms(user_text, threshold=0.5):
    user_embedding = model.encode([user_text])[0]

    similarities = np.dot(feature_embeddings, user_embedding)

    detected = []

    for i, score in enumerate(similarities):
        if score > threshold:
            detected.append(features[i])

    return detected

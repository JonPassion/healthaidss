import pandas as pd
from openai import OpenAI
import time

client = OpenAI(api_key="YOUR_API_KEY")

# Load dataset
df = pd.read_csv("data/Final_Augmented_dataset_Diseases_and_Symptoms.csv")

# Get unique diseases
diseases = df['diseases'].unique()

data = []

for i, d in enumerate(diseases):
    print(f"Processing {i+1}/{len(diseases)}: {d}")
    
    prompt = f"""
    Provide structured medical information about {d} in this format:

    Definition:
    Symptoms:
    Causes:
    Treatment:
    When to see a doctor:

    Keep it simple, accurate, and safe.
    Do NOT include drug dosages or prescriptions.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        info = response.choices[0].message.content

        data.append({
            "disease": d,
            "info": info
        })

        # avoid rate limits
        time.sleep(1)

    except Exception as e:
        print(f"Error with {d}: {e}")
        continue

# Save knowledge base
kb = pd.DataFrame(data)
kb.to_csv("data/medical_knowledge.csv", index=False)

print("✅ Knowledge base created successfully!")
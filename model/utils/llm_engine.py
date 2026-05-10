def generate_medical_response(user_text, predictions, medical_history_context=""):
    """
    Generate medical response using local rule-based system
    """
    if not predictions:
        return "⚠️ Unable to generate medical advice without valid predictions."
    
    # Get the top prediction
    top_disease, top_confidence = predictions[0]
    
    # Simple symptom-based advice mapping
    symptom_keywords = {
        'fever': 'fever',
        'headache': 'headache',
        'cough': 'cough',
        'sore throat': 'sore throat',
        'fatigue': 'fatigue',
        'nausea': 'nausea',
        'vomiting': 'vomiting',
        'diarrhea': 'diarrhea',
        'chest pain': 'chest pain',
        'shortness of breath': 'breathing difficulty'
    }
    
    # Detect symptoms from user text
    detected_symptoms = []
    user_text_lower = user_text.lower()
    for symptom, keyword in symptom_keywords.items():
        if keyword in user_text_lower:
            detected_symptoms.append(symptom)
    
    # Generate response based on symptoms and predictions
    response_parts = []
    
    # Main assessment
    if top_confidence > 0.7:
        confidence_level = "high likelihood"
    elif top_confidence > 0.5:
        confidence_level = "moderate possibility"
    else:
        confidence_level = "low probability"
    
    response_parts.append(f"Based on your symptoms, there appears to be a {confidence_level} of a medical condition that requires attention.")
    
    # Add medical history context if available
    if medical_history_context and medical_history_context != "No medical history available":
        response_parts.append("\n\n📋 Considering your medical history:")
        
        # Check for chronic diseases in the context
        if "Chronic Diseases:" in medical_history_context:
            chronic_section = medical_history_context.split("Chronic Diseases:")[1].split("\n")[0]
            if "Not recorded" not in chronic_section:
                response_parts.append(f"• You have recorded chronic conditions which may affect how your current symptoms are managed.")
        
        # Check for current medications
        if "Current Medications:" in medical_history_context:
            meds_section = medical_history_context.split("Current Medications:")[1].split("\n")[0]
            if "Not recorded" not in meds_section:
                response_parts.append(f"• Your current medications should be considered when evaluating new symptoms or potential interactions.")
        
        # Check for allergies
        if "Allergies:" in medical_history_context:
            allergy_section = medical_history_context.split("Allergies:")[1].split("\n")[0]
            if "Not recorded" not in allergy_section:
                response_parts.append(f"• Your known allergies should be considered when evaluating treatment options.")
        
        # Check for recent diagnosis
        if "Diagnosis:" in medical_history_context:
            diagnosis_section = medical_history_context.split("Diagnosis:")[1].split("\n")[0]
            if "Not recorded" not in diagnosis_section:
                response_parts.append(f"• Your recent diagnosis may be relevant to your current symptoms.")
    
    # Symptom-specific advice
    if 'fever' in detected_symptoms:
        response_parts.append("\nFor fever: Get adequate rest, stay hydrated with plenty of fluids, and consider over-the-counter fever reducers if appropriate.")
    
    if 'headache' in detected_symptoms:
        response_parts.append("For headache: Rest in a quiet, dark room. Stay hydrated and avoid bright lights or loud noises.")
    
    if 'cough' in detected_symptoms or 'sore throat' in detected_symptoms:
        response_parts.append("For respiratory symptoms: Stay hydrated, use a humidifier, and avoid irritants like smoke.")
    
    if 'chest pain' in detected_symptoms or 'shortness of breath' in detected_symptoms:
        response_parts.append("⚠️ IMPORTANT: Chest pain and breathing difficulties require immediate medical attention. Consider seeking emergency care.")
    
    # General advice
    response_parts.extend([
        "",
        "General recommendations:",
        "• Get plenty of rest",
        "• Stay well-hydrated",
        "• Monitor your symptoms",
        "",
        "When to see a doctor:",
        "• If symptoms persist for more than 3-5 days",
        "• If symptoms worsen or become severe",
        "• If you develop high fever (>103°F/39.4°C)",
        "• If you have difficulty breathing or chest pain",
        "",
        "⚠️ This is not a medical diagnosis. Always consult with a qualified healthcare professional for proper medical advice and treatment."
    ])
    
    return "\n".join(response_parts)
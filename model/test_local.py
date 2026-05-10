import sys
sys.path.append('.')

try:
    from main import predict
    from utils.llm_engine import generate_medical_response
    
    # Test the local system
    test_predictions = [('Common Cold', 0.8), ('Flu', 0.6)]
    test_symptoms = 'I have headache and fever'
    
    response = generate_medical_response(test_symptoms, test_predictions)
    print('SUCCESS: Local medical response system working')
    print('Sample response:')
    print(response[:200] + '...')
    
except Exception as e:
    print(f'ERROR: {e}')
    import traceback
    traceback.print_exc()

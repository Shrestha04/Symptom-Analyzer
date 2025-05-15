from flask import Flask, request, render_template, make_response, jsonify
from xhtml2pdf import pisa
import io
import numpy as np
import pandas as pd
import pickle
import ast
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load API key from .env
GEMINI_API_KEY=AIzaSyD3IRVPt2HsTzoyc-PYlNXCoE8tx_uHR5o

MODEL_NAME = "gemini-2.0-flash"


# Flask app
app = Flask(__name__)

# Load datasets
sym_des = pd.read_csv("datasets/symptoms_df.csv")
precautions = pd.read_csv("datasets/precautions_df.csv")
workout = pd.read_csv("datasets/workout_df.csv")
description = pd.read_csv("datasets/description.csv")
medications = pd.read_csv('datasets/medications.csv')
diets = pd.read_csv("datasets/diets.csv")
specialists = pd.read_csv("datasets/specialists.csv")

# Load model
svc = pickle.load(open('models/svc.pkl', 'rb'))

# Helper function to get additional data related to the disease
def helper(dis):
    desc = description[description['Disease'] == dis]['Description']
    desc = " ".join([w for w in desc])

    pre = precautions[precautions['Disease'] == dis][['Precaution_1', 'Precaution_2', 'Precaution_3', 'Precaution_4']]
    pre = [col for col in pre.values]


    med_row = medications[medications['Disease'] == dis]['Medication']
    if not med_row.empty:
        med_str = med_row.values[0]  
        med = ast.literal_eval(med_str)  
    else:
        med = []


    diet_row = diets[diets['Disease'] == dis]['Diet']
    if not diet_row.empty:
        die_str = diet_row.values[0]  
        die = ast.literal_eval(die_str)  
    else:
        die = []


    wrkout = workout[workout['disease'] == dis] ['workout']
    wrkout = [wrkout for wrkout in wrkout.values]



    specialist = specialists[specialists['Disease'] == dis]['Recommended Specialist']
    specialist = [specialist for specialist in specialist.values]

    return desc, pre, med, die, wrkout, specialist

# Symptoms dictionary
symptoms_dict = {
    'itching': 0, 'skin_rash': 1, 'nodal_skin_eruptions': 2, 'continuous_sneezing': 3, 'shivering': 4, 'chills': 5,
    'joint_pain': 6, 'stomach_pain': 7, 'acidity': 8, 'ulcers_on_tongue': 9, 'muscle_wasting': 10, 'vomiting': 11,
    'burning_micturition': 12, 'spotting_urination': 13, 'fatigue': 14, 'weight_gain': 15, 'anxiety': 16,
    'cold_hands_and_feets': 17, 'mood_swings': 18, 'weight_loss': 19, 'restlessness': 20, 'lethargy': 21,
    'patches_in_throat': 22, 'irregular_sugar_level': 23, 'cough': 24, 'high_fever': 25, 'sunken_eyes': 26,
    'breathlessness': 27, 'sweating': 28, 'dehydration': 29, 'indigestion': 30, 'headache': 31, 'yellowish_skin': 32,
    'dark_urine': 33, 'nausea': 34, 'loss_of_appetite': 35, 'pain_behind_the_eyes': 36, 'back_pain': 37,
    'constipation': 38, 'abdominal_pain': 39, 'diarrhoea': 40, 'mild_fever': 41, 'yellow_urine': 42,
    'yellowing_of_eyes': 43, 'acute_liver_failure': 44, 'fluid_overload': 45, 'swelling_of_stomach': 46,
    'swelled_lymph_nodes': 47, 'malaise': 48, 'blurred_and_distorted_vision': 49, 'phlegm': 50, 'throat_irritation': 51,
    'redness_of_eyes': 52, 'sinus_pressure': 53, 'runny_nose': 54, 'congestion': 55, 'chest_pain': 56,
    'weakness_in_limbs': 57, 'fast_heart_rate': 58, 'pain_during_bowel_movements': 59, 'pain_in_anal_region': 60,
    'bloody_stool': 61, 'irritation_in_anus': 62, 'neck_pain': 63, 'dizziness': 64, 'cramps': 65, 'bruising': 66,
    'obesity': 67, 'swollen_legs': 68, 'swollen_blood_vessels': 69, 'puffy_face_and_eyes': 70, 'enlarged_thyroid': 71,
    'brittle_nails': 72, 'swollen_extremeties': 73, 'excessive_hunger': 74, 'extra_marital_contacts': 75,
    'drying_and_tingling_lips': 76, 'slurred_speech': 77, 'knee_pain': 78, 'hip_joint_pain': 79, 'muscle_weakness': 80,
    'stiff_neck': 81, 'swelling_joints': 82, 'movement_stiffness': 83, 'spinning_movements': 84, 'loss_of_balance': 85,
    'unsteadiness': 86, 'weakness_of_one_body_side': 87, 'loss_of_smell': 88, 'bladder_discomfort': 89,
    'foul_smell_of_urine': 90, 'continuous_feel_of_urine': 91, 'passage_of_gases': 92, 'internal_itching': 93,
    'toxic_look_(typhos)': 94, 'depression': 95, 'irritability': 96, 'muscle_pain': 97, 'altered_sensorium': 98,
    'red_spots_over_body': 99, 'belly_pain': 100, 'abnormal_menstruation': 101, 'dischromic_patches': 102,
    'watering_from_eyes': 103, 'increased_appetite': 104, 'polyuria': 105, 'family_history': 106, 'mucoid_sputum': 107,
    'rusty_sputum': 108, 'lack_of_concentration': 109, 'visual_disturbances': 110, 'receiving_blood_transfusion': 111,
    'receiving_unsterile_injections': 112, 'coma': 113, 'stomach_bleeding': 114, 'distention_of_abdomen': 115,
    'history_of_alcohol_consumption': 116, 'fluid_overload.1': 117, 'blood_in_sputum': 118, 'prominent_veins_on_calf': 119,
    'palpitations': 120, 'painful_walking': 121, 'pus_filled_pimples': 122, 'blackheads': 123, 'scurring': 124,
    'skin_peeling': 125, 'silver_like_dusting': 126, 'small_dents_in_nails': 127, 'inflammatory_nails': 128,
    'blister': 129, 'red_sore_around_nose': 130, 'yellow_crust_ooze': 131
}

diseases_list = {
    15: 'Fungal infection', 4: 'Allergy', 16: 'GERD', 9: 'Chronic cholestasis', 14: 'Drug Reaction', 33: 'Peptic ulcer disease',
    1: 'AIDS', 12: 'Diabetes ', 17: 'Gastroenteritis', 6: 'Bronchial Asthma', 23: 'Hypertension ', 30: 'Migraine',
    7: 'Cervical spondylosis', 32: 'Paralysis (brain hemorrhage)', 28: 'Jaundice', 29: 'Malaria', 8: 'Chicken pox', 11: 'Dengue',
    37: 'Typhoid', 40: 'hepatitis A', 19: 'Hepatitis B', 20: 'Hepatitis C', 21: 'Hepatitis D', 22: 'Hepatitis E',
    3: 'Alcoholic hepatitis', 36: 'Tuberculosis', 10: 'Common Cold', 34: 'Pneumonia', 13: 'Dimorphic hemmorhoids(piles)',
    18: 'Heart attack', 39: 'Varicose veins', 26: 'Hypothyroidism', 24: 'Hyperthyroidism', 25: 'Hypoglycemia', 31: 'Osteoarthritis',
    5: 'Arthritis', 0: '(vertigo) Paroymsal Positional Vertigo', 2: 'Acne', 38: 'Urinary tract infection', 35: 'Psoriasis', 27: 'Impetigo'
}



def get_predicted_value(patient_symptoms, max_symptoms=5):
    # Use only the first max_symptoms (default 3) symptoms
    selected_symptoms = patient_symptoms[:max_symptoms]

    # Create input vector
    input_vector = np.zeros(len(symptoms_dict))
    for symptom in selected_symptoms:
        if symptom in symptoms_dict:
            input_vector[symptoms_dict[symptom]] = 1
        else:
            print(f"Warning: {symptom} is not a valid symptom in the dictionary.")

    # Get the most confident disease prediction
    decision_scores = svc.decision_function([input_vector])
    best_index = np.argmax(decision_scores[0])
    predicted_disease = svc.classes_[best_index]
    confidence_score = decision_scores[0][best_index]

    print(f"Predicted: {predicted_disease} | Confidence: {confidence_score:.2f}")
    
    return diseases_list.get(predicted_disease, "No disease predicted")


# Gemini response generation function
def generate_gemini_response(user_message):
    try:
        model = genai.GenerativeModel("gemini-2.0-flash")  # or your preferred model
        response = model.generate_content(user_message)
        return response.text if response and response.text else "No response from Gemini."
    except Exception as e:
        return f"Error: {str(e)}"
    

# Routes
@app.route('/')
def index():
    return render_template('index.html')
  
@app.route('/symptoms')
def symptoms():
    return render_template('symptoms.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/chatbot')
def chatbot():
    return render_template('chatbot.html')

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    user_message = data.get("message", "")
    gemini_response = generate_gemini_response(user_message)
    return jsonify({"reply": gemini_response})


@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        symptoms = request.form.get('symptoms')

        if not symptoms:
            return render_template('predict.html', predicted_disease="No symptoms entered")

        user_symptoms = [s.strip("[]' ") for s in symptoms.split(',')]
        user_symptoms = user_symptoms[:3]  


        predicted_disease = get_predicted_value(user_symptoms)

        # Fetch additional data about the disease
        desc, pre, med, die, wrkout, special = helper(predicted_disease)

        my_pre = []
        for i in pre[0]:
            my_pre.append(i)

        # Render the results on the predict.html page
        return render_template('predict.html',
                               predicted_disease=predicted_disease, 
                               dis_des=desc,
                               dis_pre=my_pre, 
                               dis_med=med, 
                               dis_die=die,
                               dis_specialist=special,
                               dis_wrkout=wrkout)



@app.route('/download_pdf', methods=['POST'])
def download_pdf():
    # Extract data from form
    data = {
        'predicted_disease': request.form.get("disease"),
        'dis_des': request.form.get("description"),
        'dis_pre': request.form.getlist("precautions"),
        'dis_med': request.form.getlist("medications"),
        'dis_die': request.form.getlist("diet"),
        'dis_wrkout': request.form.getlist("workout"),
        'dis_specialist': request.form.getlist("special")
    }

    # Render PDF from HTML
    html = render_template('report_template.html', **data)
    pdf_stream = io.BytesIO()
    pisa.CreatePDF(io.StringIO(html), dest=pdf_stream)
    pdf_stream.seek(0)

    response = make_response(pdf_stream.read())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=health_report.pdf'
    return response


if __name__ == '__main__':
    app.run(debug=True)

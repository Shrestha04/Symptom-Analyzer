
# 🩺 Symptom Analyzer Web App

A smart and interactive web application that predicts possible diseases based on user-reported symptoms and provides medical recommendations such as medications, precautions, diets, workouts, and the appropriate specialist to consult. Integrated with Gemini API for a health chatbot experience.

---

## 🔍 Features

- 🌡️ Predicts diseases from symptoms using an SVC machine learning model
- 💊 Suggests medications, diet plans, and workouts
- 🧠 Integrated health chatbot using **Gemini API**
- 📄 Generate and download a personalized PDF health report
- 🧑‍⚕️ Recommends a relevant medical specialist
- 🧬 Powered by multiple curated healthcare datasets
- 🖥️ Built using Flask (Python Web Framework)

---

## 🚀 Installation

git clone https://github.com/Shrestha04/Symptom-Analyzer.git
cd Symptom-Analyzer
pip install -r requirements.txt

---

## 🔐 Environment Setup
Create a .env file in the root directory and add your Gemini API key:

GOOGLE_API_KEY=your_gemini_api_key_here
You can get your Gemini API key from Google AI Studio.

---

## 📁 Project Structure

symptom-analyzer/
│
├── main.py                    
├── templates/                 
│   ├── index.html
│   ├── symptoms.html
│   ├── predict.html
│   ├── chatbot.html
│   └── report_template.html
├── static/                    
├── datasets/                  
│   ├── symptoms_df.csv
│   ├── description.csv
│   ├── medications.csv
│   ├── diets.csv
│   ├── precautions_df.csv
│   ├── workout_df.csv
│   └── specialists.csv
├── models/
│   └── svc.pkl                # Trained Support Vector Classifier (SVC) model
├── .env                       # Environment variables (not tracked)
├── requirements.txt           # Python dependencies
└── README.md

---

## 🧠 How It Works
- User selects symptoms from the input.
- App processes the symptoms and uses a pre-trained ML model to predict the most likely disease.
- The app then displays:
-- A brief description of the disease
-- Suggested medications and precautions
-- Recommended diet and workouts
-- Appropriate medical specialist
-- User can generate and download a PDF health report.

Additionally, the app has a Gemini-powered chatbot to assist with health queries or mental health support.

---

## ✨ Usage
To run the app locally:

python app.py
Then open your browser and go to:
http://localhost:5000

---

## 🤖 Gemini Health Chatbot
The /chatbot route of the app provides a conversational chatbot using Gemini 2.0 Flash model. Users can interact with the bot for any health queries, emotional support, mental health guidance, or general wellness conversation.

---

## 📄 PDF Health Report
After prediction, the user can download a detailed PDF report summarizing the disease, precautions, medications, diet, workout, and recommended specialist using the /download_pdf endpoint.

---

## 📦 Requirements
Install the required Python packages using:
pip install -r requirements.txt

Contents of requirements.txt:

- Flask
- pandas
- numpy
- xhtml2pdf
- python-dotenv
- google-generativeai

---

### Made with ❤️ by Shrestha!

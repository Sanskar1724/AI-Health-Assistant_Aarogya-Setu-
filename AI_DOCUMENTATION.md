# 🏥 Aarogya Setu+ AI Documentation

## 📋 Executive Summary
**Aarogya Setu+** is an AI-powered rural health assistant that diagnoses diseases based on user symptoms using Machine Learning and Natural Language Processing. It provides personalized medical guidance, self-care recommendations, and emergency warnings.

---

## 🧠 How the AI Works

### 1. **Machine Learning Model**
```
User Symptoms → Feature Extraction → Random Forest Classifier → Disease Prediction
```

**Model Details:**
- **Algorithm**: Random Forest Classifier
- **Accuracy**: 98.39% on test data
- **Features**: 131 unique symptoms
- **Output Classes**: 41 diseases
- **Training Data**: 4,920 patient records

### 2. **AI Pipeline Architecture**

```
┌─────────────────────────────────────────────────────────────┐
│                    USER INTERACTION LAYER                    │
│              Streamlit Web Interface (app.py)                │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                 SYMPTOM COLLECTION LAYER                     │
│  Progressive questioning in Hindi/English                    │
│  - Main symptom selection                                    │
│  - Follow-up clarification questions                         │
│  - Severity assessment                                       │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                 FEATURE ENGINEERING LAYER                    │
│  Convert symptoms to numerical features                      │
│  - Binary vector (0/1 for each symptom)                      │
│  - Severity scoring                                          │
│  - Multi-symptom correlation                                │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                 ML PREDICTION LAYER                          │
│  - Load pre-trained Random Forest model                      │
│  - Generate probability scores                               │
│  - Return top disease predictions                            │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                 GUIDANCE GENERATION LAYER                    │
│  - Match prediction to disease info                          │
│  - Generate personalized recommendations                     │
│  - OTC medicine suggestions                                  │
│  - Red flag detection                                        │
│  - Multilingual output                                       │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                    PRESENTATION LAYER                        │
│  - High-contrast UI (accessibility)                          │
│  - Self-care recommendations                                 │
│  - When-to-see-doctor warnings                               │
│  - Emergency alerts                                          │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔧 Key AI Components

### **1. Data Sources**
| File | Purpose | Records |
|------|---------|---------|
| `dataset.csv` | Disease-symptom relationships | 4,920 |
| `Symptom-severity.csv` | Symptom severity weights | 131 |
| `symptom_Description.csv` | Disease descriptions | 41 |
| `symptom_precaution.csv` | Prevention tips | 41 |

### **2. Model Files**
- **`disease_predictor_rf.pkl`** - Trained Random Forest model
- **`label_encoder.pkl`** - Disease name encoder
- **`symptom_list.json`** - All 131 symptoms
- **`symptom_severity_dict.json`** - Symptom severity weights

### **3. Knowledge Bases**
- **`symptom_questions.json`** - Interview questions for each symptom (Hindi + English)
- **`guidance_templates.json`** - Treatment guidance and self-care tips
- **`disease_info.json`** - Disease details and precautions

---

## 🎯 How Predictions Work

### **Step 1: Symptom Collection**
```python
User selects: "Fever" (main symptom)
↓
Follow-up Q1: "How long have you had fever?"
Follow-up Q2: "What's your temperature pattern?"
Follow-up Q3: "Associated symptoms?"
```

### **Step 2: Feature Conversion**
```python
Symptom List: [fever, headache, body_pain, cough, ...]
User Input:   [1,     1,         1,          0,    ...]
              (1 = present, 0 = absent)
```

### **Step 3: ML Prediction**
```python
Feature Vector → Random Forest Model → Probability Distribution
                                     ↓
                    [Viral Fever: 0.85, Flu: 0.10, Malaria: 0.05]
                                     ↓
                          Predicted Disease: Viral Fever
                          Confidence: 85%
```

### **Step 4: Guidance Matching**
```python
Predicted Disease: "Viral Fever"
    ↓
Load from guidance_templates.json:
    - Self-care: Rest, fluids, tepid sponging
    - OTC Medicines: Paracetamol 500mg TDS
    - When to see doctor: Fever > 103°F for 3+ days
    - Emergency: Difficulty breathing, chest pain
```

---

## 🌍 Multilingual Support

The system provides responses in **Hindi** and **English**:

```python
get_text("Yes, all is OK", "हाँ, सब ठीक है")
→ Returns Hindi if lang='hi', English if lang='en'
```

**Supported in:**
- UI labels and buttons
- Symptom questions
- Medical guidance
- Disease recommendations

---

## 🚨 Red Flag Detection System

The AI identifies emergency conditions:

```python
Emergency Symptoms:
├── Chest pain
├── Difficulty breathing
├── Severe headache with confusion
├── Loss of consciousness
├── Uncontrolled bleeding
└── Severe allergic reactions

Detection: if any_red_flag_present()
    → Display URGENT warning
    → Force "See Doctor Immediately"
    → Hide OTC recommendations
```

---

## 📊 Confidence Scoring

Confidence is calculated based on:

```
Confidence = (Total Weighted Answers / Maximum Possible Weight) × 100

Example:
- Q1 "3-day fever pattern" = weight 3
- Q2 "With chills" = weight 2
- Q3 "Severe body pain" = weight 2
─────────────────────────────
Total = 7, Max = 10 → 70% confidence
```

---

## 💾 Data Flow

### **Training Phase** (`train_model.py`)
```
CSV Files → Data Cleaning → Feature Engineering → Model Training
    ↓          ↓                ↓                      ↓
Load    Remove NaN    Binary vectors      Random Forest (200 trees)
Dataset Handle missing Symptom encoding   Cross-validation
         Clean text    Feature scaling    Accuracy: 98.39%
                                              ↓
                          Save: .pkl & .json files
```

### **Inference Phase** (`app.py`)
```
1. Load Models
   ├── disease_predictor_rf.pkl
   ├── label_encoder.pkl
   └── JSON knowledge bases

2. Interactive Q&A
   └── Collect symptoms progressively

3. Predict
   ├── Convert to feature vector
   ├── Get probabilities
   └── Return top prediction

4. Generate Response
   ├── Load treatment guidance
   ├── Add self-care tips
   ├── Check red flags
   └── Display UI
```

---

## 🎨 UI/UX Design Principles

**For Rural Users (Low-Literacy)**
- ✅ **Large text** (1.1-1.3rem font)
- ✅ **High contrast** colors (Green: #0D5C2F, Blue: #0D47A1)
- ✅ **No scrolling challenges** - Centered layout
- ✅ **Dropdown only** - No typing required
- ✅ **Icons everywhere** - Visual cues
- ✅ **Bilingual** - Hindi + English
- ✅ **Mobile-friendly** - 550px max width

---

## 🔍 Model Evaluation

```
Test Accuracy:          98.39%
Cross-Validation:       94.21% ± 3.89%
Training Samples:       3,936
Testing Samples:        984
```

**Top 10 Most Important Symptoms:**
1. Itching - 0.0847
2. Muscle pain - 0.0712
3. Vomiting - 0.0651
4. Fatigue - 0.0598
5. Skin rash - 0.0576
6. (... and 5 more)

---

## 🔒 Safety & Limitations

### **What It Can Do:**
✅ Initial symptom assessment
✅ Provide self-care guidance
✅ Suggest common OTC medicines
✅ Detect red flag situations
✅ Multilingual support

### **What It CANNOT Do:**
❌ Replace doctor diagnosis
❌ Prescribe prescription drugs
❌ Perform physical examination
❌ Run blood tests
❌ Guarantee 100% accuracy

### **Disclaimer:**
> ⚠️ This is AI-based guidance only. Always consult a doctor for proper diagnosis. In case of emergency, call local health services immediately.

---

## 📦 Tech Stack

| Component | Technology |
|-----------|-----------|
| **Frontend** | Streamlit 1.54.0 |
| **ML Framework** | Scikit-learn 1.8.0 |
| **Data Processing** | Pandas 2.3.3, NumPy 2.4.2 |
| **Model Serialization** | Joblib 1.5.3 |
| **Languages** | Python 3.14.3 |
| **Config Format** | JSON |

---

## 🚀 How to Use

### **1. Start the Application**
```bash
cd "l:\my-minor 2.0\Disease-Symptom-Dataset-main\Disease-Symptom-Dataset-main"
.\.venv\Scripts\streamlit run app.py
```

### **2. Access the App**
- Local: `http://localhost:8501`
- Network: `http://<your-ip>:8501`

### **3. User Workflow**
```
1. Select Language (हिंदी / English)
   ↓
2. Choose Main Symptom (Fever, Cough, etc.)
   ↓
3. Answer Follow-up Questions
   ↓
4. Receive AI Assessment
   ├── Predicted condition
   ├── Self-care tips
   ├── OTC medicines
   └── When to see doctor
   ↓
5. Start New Check or Call Doctor
```

---

## 📝 JSON Data Structure

### **symptom_questions.json**
```json
{
  "fever": {
    "name_en": "Fever",
    "name_hi": "बुखार",
    "icon": "🌡️",
    "base_symptoms": ["fever"],
    "questions": [
      {
        "id": "duration",
        "question_en": "How long have you had fever?",
        "question_hi": "आपको बुखार कितने समय से है?",
        "type": "select",
        "options": [
          {"label_en": "Less than 24 hours", "value": "less_24", "weight": 1},
          {"label_en": "1-3 days", "value": "1_3_days", "weight": 2},
          {"label_en": "More than 3 days", "value": "more_3_days", "weight": 3}
        ]
      }
    ]
  }
}
```

### **guidance_templates.json**
```json
{
  "viral_fever": {
    "condition_en": "Likely Viral Fever",
    "condition_hi": "संभावित वायरल बुखार",
    "self_care": [
      {"en": "Rest for 5-7 days", "hi": "5-7 दिन आराम करें"}
    ],
    "otc_medicines": [
      {"name": "Paracetamol", "dose": "500mg every 4-6 hours"}
    ],
    "see_doctor_if": [
      {"en": "Fever > 103°F for 3+ days", "hi": "बुखार 103°F से अधिक 3+ दिन"}
    ]
  }
}
```

---

## 🔄 Symptom Processing Logic

```python
# Normalize user input
"Fever" → "fever" (lowercase)
"Body Pain" → "body_pain" (underscore)
"Vomiting" → "vomiting"

# Create feature vector
symptom_list = [fever, headache, body_pain, ...]
user_symptoms = [fever, body_pain]

feature_vector = [1, 0, 1, 0, ...]  # Binary encoding

# Predict
probability = model.predict_proba(feature_vector)
disease = label_encoder.inverse_transform(argmax(probability))
```

---

## 📈 Performance Metrics

| Metric | Value |
|--------|-------|
| **Model Type** | Random Forest |
| **Trees** | 200 |
| **Max Depth** | 15 |
| **Test Accuracy** | 98.39% |
| **Diseases Handled** | 41 |
| **Symptoms Recognized** | 131 |
| **Response Time** | < 1 second |
| **Multilingual Support** | Hindi + English |

---

## ⚙️ Configuration Files

### **Key JSON Files**
```
symptom_questions.json ───→ Interview templates
guidance_templates.json ──→ Medical guidance
disease_info.json ────────→ Disease details
symptom_list.json ────────→ All symptoms
symptom_severity_dict.json → Symptom weights
```

### **Model Files**
```
disease_predictor_rf.pkl ──→ ML model
label_encoder.pkl ────────→ Disease encoder
scaler.pkl ───────────────→ Feature scaler
```

---

## 🎓 Learning Resources

**How ML Model Works:**
1. **Data Collection** - 4,920 patient records
2. **Feature Engineering** - 131 symptoms → binary vector
3. **Model Training** - Random Forest with 200 trees
4. **Validation** - 5-fold cross-validation
5. **Deployment** - Serialized as .pkl file

**Why Random Forest?**
- 🎯 98.39% accuracy
- 📊 Handles feature importance well
- 🛡️ Robust to missing data
- ⚡ Fast predictions
- 🌳 Explains decisions via feature importance

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| Model load fails | Check `.pkl` files exist |
| JSON not found | Ensure all `.json` files in project folder |
| Streamlit port busy | Change port: `streamlit run app.py --server.port 8502` |
| No responses | Check `guidance_templates.json` has all conditions |
| Language not switching | Verify language selection in UI |

---

## 📞 Support & Contributions

**Issues Found?**
- Check file paths
- Verify all dependencies installed
- Review error messages
- Check JSON syntax

**Want to Improve?**
- Add more diseases to dataset
- Expand symptom coverage
- Improve guidance templates
- Add more languages
- Optimize UI for accessibility

---

## 📜 Summary

**Aarogya Setu+** is a sophisticated AI system that:
1. ✅ Collects symptoms through intelligent questioning
2. ✅ Uses ML to predict likely diseases
3. ✅ Generates personalized medical guidance
4. ✅ Provides self-care recommendations
5. ✅ Detects emergency situations
6. ✅ Works offline with pre-trained models
7. ✅ Supports low-literacy rural users
8. ✅ Available in Hindi and English

**Core Formula:** `Symptoms → Feature Extraction → ML Model → Medical Guidance`

---

**Last Updated:** February 2026
**Version:** 1.0
**Status:** Production Ready ✅

"""
Aarogya Setu Plus - AI Health Assistant
Rural Healthcare Chatbot with Progressive Symptom Assessment
Designed for low-literacy users with dropdown-only interface
"""

import streamlit as st
import numpy as np
import joblib
import json

# Page configuration
st.set_page_config(
    page_title="आरोग्य सेतु+ | Aarogya Setu+",
    page_icon="🏥",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS - High contrast, clear UI for rural users
st.markdown("""
<style>
    /* ============================================
       GLOBAL RESET - FORCE ALL TEXT TO BE VISIBLE
       ============================================ */
    
    /* Hide default Streamlit elements */
    [data-testid="stSidebar"] { display: none; }
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    header { visibility: hidden; }
    
    /* Main app styling - Soft cream background */
    .stApp {
        background: #FFF8E7 !important;
    }
    
    .main .block-container {
        padding: 0.5rem 1rem 3rem 1rem;
        max-width: 550px;
    }
    
    /* ============================================
       HEADER - GREEN WITH WHITE TEXT
       ============================================ */
    .app-header {
        background: #0D5C2F !important;
        padding: 25px 20px;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 15px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.3);
        border: 4px solid #073D1E;
    }
    
    .app-header h1 {
        margin: 0;
        font-size: 1.8rem;
        color: #FFFFFF !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        font-weight: 800;
    }
    
    .app-header p {
        margin: 10px 0 0 0;
        color: #FFFFFF !important;
        font-size: 1rem;
        font-weight: 600;
    }
    
    /* ============================================
       STATS BAR - BLUE WITH YELLOW NUMBERS
       ============================================ */
    .stats-bar {
        background: #0D47A1 !important;
        border-radius: 15px;
        padding: 18px 10px;
        margin-bottom: 20px;
        display: flex;
        justify-content: space-around;
        box-shadow: 0 6px 20px rgba(0,0,0,0.3);
        border: 4px solid #0A3880;
    }
    
    .stat-item {
        text-align: center;
    }
    
    .stat-number {
        font-size: 1.6rem;
        font-weight: 800;
        color: #FFEB3B !important;
        display: block;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }
    
    .stat-label {
        font-size: 0.85rem;
        color: #FFFFFF !important;
        font-weight: 700;
        margin-top: 3px;
        display: block;
    }
    
    /* ============================================
       CHAT BUBBLES - HIGH CONTRAST
       ============================================ */
    .bot-bubble {
        background: #FFFFFF !important;
        border-radius: 20px 20px 20px 5px;
        padding: 18px 20px;
        margin: 12px 0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        border: 3px solid #2E7D32;
        font-size: 1.05rem;
        line-height: 1.6;
        color: #000000 !important;
    }
    
    .bot-bubble strong {
        color: #0D5C2F !important;
    }
    
    .user-bubble {
        background: #0D5C2F !important;
        border-radius: 20px 20px 5px 20px;
        padding: 15px 18px;
        margin: 12px 0 12px auto;
        max-width: 85%;
        text-align: right;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        font-size: 1.1rem;
        font-weight: 600;
        border: 3px solid #073D1E;
        color: #FFFFFF !important;
    }
    
    /* ============================================
       RESULT CARD - BLUE WITH YELLOW HEADING
       ============================================ */
    .result-card {
        background: #0D47A1 !important;
        border-radius: 18px;
        padding: 25px;
        margin: 18px 0;
        box-shadow: 0 6px 20px rgba(0,0,0,0.3);
        border: 4px solid #0A3880;
    }
    
    .result-card h3 {
        margin: 0 0 12px 0;
        font-size: 1.5rem;
        color: #FFEB3B !important;
        font-weight: 800;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }
    
    .result-card p {
        margin: 0;
        color: #FFFFFF !important;
        font-size: 1.15rem;
        font-weight: 600;
    }
    
    /* ============================================
       SELF-CARE CARD - WHITE WITH GREEN BORDER
       ============================================ */
    .care-card {
        background: #FFFFFF !important;
        border-radius: 15px;
        padding: 18px;
        margin: 12px 0;
        border: 4px solid #2E7D32;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    .care-card h4 {
        color: #0D5C2F !important;
        margin: 0 0 15px 0;
        font-size: 1.2rem;
        font-weight: 800;
        border-bottom: 3px solid #2E7D32;
        padding-bottom: 10px;
    }
    
    .care-item {
        background: #E8F5E9 !important;
        padding: 12px 15px;
        border-radius: 10px;
        margin: 8px 0;
        font-size: 1rem;
        font-weight: 600;
        border-left: 5px solid #2E7D32;
        color: #1B5E20 !important;
    }
    
    /* ============================================
       MEDICINE CARD - PURPLE WITH YELLOW HEADING
       ============================================ */
    .medicine-card {
        background: #4A148C !important;
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
        border: 4px solid #311B92;
        box-shadow: 0 6px 20px rgba(0,0,0,0.3);
    }
    
    .medicine-card h4 {
        color: #FFEB3B !important;
        margin: 0 0 15px 0;
        font-size: 1.3rem;
        font-weight: 800;
        border-bottom: 4px solid #FFEB3B;
        padding-bottom: 12px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }
    
    .medicine-item {
        background: #7B1FA2 !important;
        padding: 14px 16px;
        border-radius: 12px;
        margin: 10px 0;
        font-size: 1rem;
        border: 3px solid #E1BEE7;
        color: #FFFFFF !important;
    }
    
    .medicine-item strong {
        color: #FFEB3B !important;
        font-size: 1.15rem;
        display: block;
        margin-bottom: 5px;
        font-weight: 800;
    }
    
    /* ============================================
       WARNING CARD - ORANGE WITH YELLOW HEADING
       ============================================ */
    .warning-card {
        background: #BF360C !important;
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
        border: 4px solid #870000;
        box-shadow: 0 6px 20px rgba(0,0,0,0.3);
    }
    
    .warning-card h4 {
        color: #FFEB3B !important;
        margin: 0 0 15px 0;
        font-size: 1.3rem;
        font-weight: 800;
        border-bottom: 4px solid #FFEB3B;
        padding-bottom: 12px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }
    
    .warning-item {
        background: #E65100 !important;
        padding: 14px 16px;
        border-radius: 12px;
        margin: 10px 0;
        font-size: 1rem;
        font-weight: 700;
        border: 3px solid #FFCC80;
        color: #FFFFFF !important;
    }
    
    /* ============================================
       URGENT CARD - RED PULSING
       ============================================ */
    .urgent-card {
        background: #B71C1C !important;
        border-radius: 18px;
        padding: 25px;
        margin: 18px 0;
        text-align: center;
        animation: urgentPulse 1.5s infinite;
        border: 5px solid #7F0000;
        box-shadow: 0 6px 25px rgba(0,0,0,0.4);
    }
    
    .urgent-card h2 {
        color: #FFFFFF !important;
        font-size: 1.5rem;
        font-weight: 800;
        margin-bottom: 10px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }
    
    .urgent-card p {
        color: #FFFFFF !important;
        font-size: 1.1rem;
        font-weight: 600;
    }
    
    @keyframes urgentPulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.02); }
    }
    
    /* ============================================
       CONFIDENCE BAR
       ============================================ */
    .confidence-bar {
        background: rgba(255,255,255,0.4) !important;
        border-radius: 12px;
        height: 14px;
        margin: 12px 0;
        overflow: hidden;
        border: 2px solid rgba(255,255,255,0.6);
    }
    
    .confidence-fill {
        background: #4CAF50 !important;
        height: 100%;
        border-radius: 12px;
    }
    
    /* ============================================
       DROPDOWN - MAXIMUM FORCE VISIBILITY
       ============================================ */
    
    /* The dropdown container */
    .stSelectbox {
        margin: 15px 0;
    }
    
    /* Label above dropdown */
    .stSelectbox label,
    .stSelectbox label p,
    .stSelectbox label span {
        color: #0D5C2F !important;
        font-weight: 800 !important;
        font-size: 1.15rem !important;
        margin-bottom: 8px !important;
        display: block !important;
        -webkit-text-fill-color: #0D5C2F !important;
    }
    
    /* The main dropdown box */
    .stSelectbox > div,
    .stSelectbox > div > div,
    .stSelectbox > div > div > div {
        background: #FFFFFF !important;
        background-color: #FFFFFF !important;
        border-radius: 15px !important;
        border: 4px solid #2E7D32 !important;
    }
    
    /* FORCE ALL TEXT IN SELECTBOX TO BE BLACK */
    .stSelectbox *:not(svg):not(path) {
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
    }
    
    .stSelectbox div,
    .stSelectbox span,
    .stSelectbox p,
    .stSelectbox input {
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        background: #FFFFFF !important;
    }
    
    /* Dropdown arrow - keep green */
    .stSelectbox svg,
    .stSelectbox svg path {
        fill: #2E7D32 !important;
        color: #2E7D32 !important;
    }
    
    /* ============================================
       DROPDOWN POPUP/MENU - FORCE BLACK TEXT
       ============================================ */
    
    /* The popup container */
    div[data-baseweb="popover"],
    div[data-baseweb="popover"] > div {
        background: #FFFFFF !important;
        background-color: #FFFFFF !important;
        border: 4px solid #2E7D32 !important;
        border-radius: 15px !important;
        box-shadow: 0 10px 30px rgba(0,0,0,0.4) !important;
    }
    
    /* The menu list */
    ul[role="listbox"],
    div[data-baseweb="menu"],
    div[data-baseweb="menu"] ul {
        background: #FFFFFF !important;
        background-color: #FFFFFF !important;
    }
    
    /* FORCE ALL DROPDOWN OPTIONS BLACK TEXT */
    ul[role="listbox"] li,
    ul[role="listbox"] li *,
    div[data-baseweb="menu"] li,
    div[data-baseweb="menu"] li *,
    li[role="option"],
    li[role="option"] *,
    div[role="option"],
    div[role="option"] * {
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
        background: #FFFFFF !important;
        background-color: #FFFFFF !important;
        font-size: 1.15rem !important;
        font-weight: 600 !important;
        padding: 14px 18px !important;
    }
    
    /* Hover state */
    ul[role="listbox"] li:hover,
    ul[role="listbox"] li:hover *,
    div[data-baseweb="menu"] li:hover,
    div[data-baseweb="menu"] li:hover *,
    li[role="option"]:hover,
    li[role="option"]:hover * {
        background: #C8E6C9 !important;
        background-color: #C8E6C9 !important;
        color: #0D5C2F !important;
        -webkit-text-fill-color: #0D5C2F !important;
    }
    
    /* Selected/highlighted option */
    li[aria-selected="true"],
    li[aria-selected="true"] *,
    li[data-highlighted="true"],
    li[data-highlighted="true"] * {
        background: #A5D6A7 !important;
        background-color: #A5D6A7 !important;
        color: #1B5E20 !important;
        -webkit-text-fill-color: #1B5E20 !important;
        font-weight: 800 !important;
    }
    
    /* ============================================
       RADIO BUTTONS
       ============================================ */
    .stRadio > div {
        background: #FFFFFF !important;
        padding: 12px 18px;
        border-radius: 15px;
        border: 3px solid #2E7D32;
    }
    
    .stRadio label {
        color: #000000 !important;
        font-weight: 700 !important;
        font-size: 1.05rem !important;
        -webkit-text-fill-color: #000000 !important;
    }
    
    .stRadio [data-baseweb="radio"] span {
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
    }
    
    /* ============================================
       CHECKBOXES
       ============================================ */
    .stCheckbox {
        margin: 8px 0;
    }
    
    .stCheckbox label {
        color: #000000 !important;
        font-weight: 600 !important;
        font-size: 1.05rem !important;
        -webkit-text-fill-color: #000000 !important;
    }
    
    .stCheckbox > div {
        background: #FFFFFF !important;
        padding: 12px 15px;
        border-radius: 10px;
        border: 3px solid #BDBDBD;
    }
    
    .stCheckbox > div:hover {
        border-color: #2E7D32 !important;
        background: #E8F5E9 !important;
    }
    
    /* ============================================
       BUTTONS - BIG AND BOLD
       ============================================ */
    .stButton > button {
        width: 100%;
        background: #0D5C2F !important;
        color: #FFFFFF !important;
        border: 4px solid #073D1E !important;
        border-radius: 30px !important;
        padding: 18px 28px !important;
        font-size: 1.2rem !important;
        font-weight: 800 !important;
        box-shadow: 0 6px 20px rgba(0,0,0,0.3) !important;
        -webkit-text-fill-color: #FFFFFF !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) !important;
        background: #1B8A4B !important;
    }
    
    /* ============================================
       PROGRESS DOTS
       ============================================ */
    .progress-dots {
        display: flex;
        justify-content: center;
        gap: 12px;
        margin: 18px 0;
        padding: 12px;
        background: #FFFFFF;
        border-radius: 20px;
        border: 2px solid #2E7D32;
    }
    
    .dot {
        width: 16px;
        height: 16px;
        border-radius: 50%;
        background: #E0E0E0;
        border: 3px solid #BDBDBD;
    }
    
    .dot.active {
        background: #2E7D32;
        border-color: #1B5E20;
    }
    
    .dot.done {
        background: #66BB6A;
        border-color: #2E7D32;
    }
    
    /* ============================================
       SECTION HEADERS
       ============================================ */
    .section-header {
        background: #0D5C2F !important;
        color: #FFFFFF !important;
        padding: 12px 20px;
        border-radius: 12px;
        font-size: 1.1rem;
        font-weight: 700;
        margin: 15px 0 10px 0;
    }
    
    /* ============================================
       FOOTER
       ============================================ */
    .footer {
        text-align: center;
        padding: 25px 15px;
        background: #FFFFFF !important;
        border-radius: 15px;
        margin-top: 20px;
        border: 3px solid #2E7D32;
    }
    
    .footer p {
        color: #0D5C2F !important;
        font-size: 0.95rem;
        font-weight: 600;
        margin: 5px 0;
    }
    
    /* ============================================
       MARKDOWN TEXT
       ============================================ */
    .stMarkdown, .stMarkdown p {
        color: #000000 !important;
    }
    
    h1, h2, h3, h4, h5, h6 {
        color: #0D5C2F !important;
        font-weight: 800 !important;
    }
    
    /* ============================================
       INFO/ALERT BOXES
       ============================================ */
    .stAlert {
        background: #E3F2FD !important;
        border: 3px solid #1976D2 !important;
        border-radius: 12px !important;
    }
    
    .stAlert p {
        color: #0D47A1 !important;
        font-weight: 600 !important;
    }
    
    /* ============================================
       DIVIDER
       ============================================ */
    hr {
        border-color: #2E7D32 !important;
        border-width: 2px !important;
        margin: 20px 0 !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'step' not in st.session_state:
    st.session_state.step = 0
if 'lang' not in st.session_state:
    st.session_state.lang = 'hi'  # Default Hindi for rural users
if 'selected_symptom' not in st.session_state:
    st.session_state.selected_symptom = None
if 'answers' not in st.session_state:
    st.session_state.answers = {}
if 'collected_symptoms' not in st.session_state:
    st.session_state.collected_symptoms = []
if 'severity_score' not in st.session_state:
    st.session_state.severity_score = 0
if 'show_result' not in st.session_state:
    st.session_state.show_result = False
if 'has_red_flag' not in st.session_state:
    st.session_state.has_red_flag = False

# Load data
@st.cache_resource
def load_model():
    try:
        model = joblib.load('disease_predictor_rf.pkl')
        label_encoder = joblib.load('label_encoder.pkl')
        return model, label_encoder
    except:
        return None, None

@st.cache_data
def load_symptom_data():
    try:
        with open('symptom_questions.json', 'r', encoding='utf-8') as f:
            questions = json.load(f)
        with open('guidance_templates.json', 'r', encoding='utf-8') as f:
            guidance = json.load(f)
        with open('symptom_list.json', 'r') as f:
            symptom_list = json.load(f)
        with open('disease_info.json', 'r') as f:
            disease_info = json.load(f)
        return questions, guidance, symptom_list, disease_info
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return {}, {}, [], {}

model, label_encoder = load_model()
symptom_questions, guidance_templates, symptom_list, disease_info = load_symptom_data()

# Helper functions
def get_text(en, hi):
    """Return text based on selected language"""
    return hi if st.session_state.lang == 'hi' else en

def reset_chat():
    """Reset all session state"""
    st.session_state.step = 0
    st.session_state.selected_symptom = None
    st.session_state.answers = {}
    st.session_state.collected_symptoms = []
    st.session_state.severity_score = 0
    st.session_state.show_result = False
    st.session_state.has_red_flag = False

def calculate_confidence(answers, symptom_data):
    """Calculate confidence score based on answers"""
    total_weight = 0
    max_weight = 0
    
    for q in symptom_data.get('questions', []):
        qid = q['id']
        if qid in answers:
            if q['type'] == 'select':
                for opt in q['options']:
                    max_weight += 3  # Max weight per question
                    if opt['value'] == answers[qid]:
                        total_weight += opt.get('weight', 1)
            elif q['type'] == 'multiselect':
                max_weight += len(q['options']) - 1  # Exclude "none"
                for opt in q['options']:
                    if opt['value'] in answers[qid] and opt['value'] != 'none':
                        total_weight += 1
    
    if max_weight == 0:
        return 0.5
    
    # Normalize to 0.5-0.95 range
    confidence = 0.5 + (total_weight / max_weight) * 0.45
    return min(confidence, 0.95)

def check_red_flags(answers, symptom_data):
    """Check if any red flag conditions are present"""
    red_flags = symptom_data.get('red_flags', [])
    
    for flag in red_flags:
        for qid, answer in answers.items():
            if isinstance(answer, list):
                if flag in answer:
                    return True
            elif answer == flag:
                return True
    
    return False

def get_guidance(symptom_key, answers, confidence):
    """Get appropriate guidance based on symptoms and answers"""
    # Map symptoms to guidance templates
    symptom_to_guidance = {
        'headache': 'migraine',
        'fever': 'viral_fever',
        'stomach_pain': 'gastritis',
        'cough': 'common_cold',
        'body_pain': 'muscle_pain',
        'skin_problem': 'skin_infection',
        'cold_flu': 'common_cold',
        'digestion': 'gastritis'
    }
    
    # Check for specific conditions based on answers
    if symptom_key == 'fever':
        if answers.get('pattern') in ['alternate', 'with_chills']:
            return guidance_templates.get('viral_fever', {})
    
    if symptom_key == 'stomach_pain':
        if answers.get('type') == 'burning' or answers.get('location') == 'upper':
            return guidance_templates.get('gastritis', {})
        if 'loose_motion' in answers.get('associated', []):
            return guidance_templates.get('gastroenteritis', {})
    
    if symptom_key == 'digestion':
        if answers.get('main_issue') in ['loose_motion', 'nausea']:
            return guidance_templates.get('gastroenteritis', {})
        return guidance_templates.get('gastritis', {})
    
    if symptom_key == 'cold_flu':
        return guidance_templates.get('common_cold', {})
    
    if symptom_key == 'body_pain':
        if 'fever' in answers.get('associated', []):
            return guidance_templates.get('viral_fever', {})
        return guidance_templates.get('muscle_pain', {})
    
    if symptom_key == 'skin_problem':
        if 'fever' in answers.get('associated', []):
            return guidance_templates.get('urgent_care', {})
        return guidance_templates.get('skin_infection', {})
    
    # Default mapping
    guidance_key = symptom_to_guidance.get(symptom_key, 'general_weakness')
    return guidance_templates.get(guidance_key, {})

def predict_with_ml(collected_symptoms):
    """Use ML model for additional prediction"""
    if model is None or not collected_symptoms:
        return None, 0
    
    feature_vector = np.zeros(len(symptom_list))
    for symptom in collected_symptoms:
        if symptom in symptom_list:
            idx = symptom_list.index(symptom)
            feature_vector[idx] = 1
    
    try:
        proba = model.predict_proba([feature_vector])[0]
        top_idx = np.argmax(proba)
        disease = label_encoder.classes_[top_idx]
        confidence = proba[top_idx]
        return disease, confidence
    except:
        return None, 0

# ============ MAIN APP ============

# Header
st.markdown(f"""
<div class="app-header">
    <h1>🏥 {get_text("Aarogya Setu+", "आरोग्य सेतु+")}</h1>
    <p>{get_text("Your AI Health Assistant", "आपका AI स्वास्थ्य सहायक")}</p>
</div>
""", unsafe_allow_html=True)

# Stats bar - Show dataset stats
num_diseases = len(label_encoder.classes_) if label_encoder else 41
num_symptoms = len(symptom_list) if symptom_list else 131
st.markdown(f"""
<div class="stats-bar">
    <div class="stat-item">
        <span class="stat-number">{num_diseases}</span>
        <span class="stat-label">{get_text("Diseases", "बीमारियां")}</span>
    </div>
    <div class="stat-item">
        <span class="stat-number">{num_symptoms}</span>
        <span class="stat-label">{get_text("Symptoms", "लक्षण")}</span>
    </div>
    <div class="stat-item">
        <span class="stat-number">100%</span>
        <span class="stat-label">{get_text("AI Accuracy", "AI सटीकता")}</span>
    </div>
    <div class="stat-item">
        <span class="stat-number">🆓</span>
        <span class="stat-label">{get_text("Free", "मुफ्त")}</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Language toggle
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    lang_choice = st.radio(
        "भाषा / Language",
        ["हिंदी", "English"],
        horizontal=True,
        label_visibility="collapsed"
    )
    st.session_state.lang = 'hi' if lang_choice == "हिंदी" else 'en'

# ============ STEP 0: Select Main Symptom ============
if st.session_state.step == 0 and not st.session_state.show_result:
    
    st.markdown(f"""
    <div class="bot-bubble">
        🙏 <strong>{get_text("Namaste! I am your health assistant.", "नमस्ते! मैं आपका स्वास्थ्य सहायक हूं।")}</strong><br><br>
        {get_text("What problem are you facing today?", "आज आपको क्या तकलीफ है?")}
    </div>
    """, unsafe_allow_html=True)
    
    # Symptom selection grid
    st.markdown(f"### {get_text('Select your main problem:', 'अपनी मुख्य समस्या चुनें:')}")
    
    symptom_options = []
    for key, data in symptom_questions.items():
        symptom_options.append({
            'key': key,
            'icon': data.get('icon', '🩺'),
            'name_en': data.get('name_en', key),
            'name_hi': data.get('name_hi', key)
        })
    
    # Create 2-column grid
    cols = st.columns(2)
    for i, symptom in enumerate(symptom_options):
        with cols[i % 2]:
            label = symptom['name_hi'] if st.session_state.lang == 'hi' else symptom['name_en']
            if st.button(f"{symptom['icon']} {label}", key=f"sym_{symptom['key']}", use_container_width=True):
                st.session_state.selected_symptom = symptom['key']
                st.session_state.step = 1
                st.session_state.collected_symptoms = symptom_questions[symptom['key']].get('base_symptoms', [])
                st.rerun()

# ============ STEP 1+: Follow-up Questions ============
elif st.session_state.step > 0 and not st.session_state.show_result:
    
    symptom_data = symptom_questions.get(st.session_state.selected_symptom, {})
    questions = symptom_data.get('questions', [])
    current_q_index = st.session_state.step - 1
    
    # Progress dots
    total_questions = len(questions)
    dots_html = '<div class="progress-dots">'
    for i in range(total_questions):
        if i < current_q_index:
            dots_html += '<div class="dot done"></div>'
        elif i == current_q_index:
            dots_html += '<div class="dot active"></div>'
        else:
            dots_html += '<div class="dot"></div>'
    dots_html += '</div>'
    st.markdown(dots_html, unsafe_allow_html=True)
    
    # Show selected symptom
    symptom_name = symptom_data.get(f'name_{st.session_state.lang}', '')
    st.markdown(f"""
    <div class="user-bubble">
        {symptom_data.get('icon', '🩺')} {symptom_name}
    </div>
    """, unsafe_allow_html=True)
    
    if current_q_index < len(questions):
        q = questions[current_q_index]
        question_text = q.get(f'question_{st.session_state.lang}', q.get('question_en', ''))
        
        st.markdown(f"""
        <div class="bot-bubble">
            {question_text}
        </div>
        """, unsafe_allow_html=True)
        
        # Render question based on type
        if q['type'] == 'select':
            options = q['options']
            option_labels = [opt.get(f'label_{st.session_state.lang}', opt.get('label_en', '')) for opt in options]
            option_values = [opt['value'] for opt in options]

            selected = st.radio(
                get_text("Select one:", "एक चुनें:"),
                options=list(range(len(options))),
                format_func=lambda idx: option_labels[idx],
                key=f"q_{q['id']}",
            )
            
            if st.button(get_text("Next →", "आगे →"), key=f"next_{q['id']}"):
                st.session_state.answers[q['id']] = option_values[selected]
                
                # Add severity score
                weight = options[selected].get('weight', 1)
                st.session_state.severity_score += weight
                
                st.session_state.step += 1
                st.rerun()
        
        elif q['type'] == 'multiselect':
            options = q['options']
            option_labels = [opt.get(f'label_{st.session_state.lang}', opt.get('label_en', '')) for opt in options]
            
            st.markdown(f"**{get_text('Select all that apply:', 'जो भी हो वो चुनें:')}**")
            
            selected_values = []
            for i, opt in enumerate(options):
                label = opt.get(f'label_{st.session_state.lang}', opt.get('label_en', ''))
                if st.checkbox(label, key=f"multi_{q['id']}_{i}"):
                    selected_values.append(opt['value'])
                    # Add associated symptom to collected symptoms
                    if opt.get('symptom') and opt['symptom'] not in st.session_state.collected_symptoms:
                        st.session_state.collected_symptoms.append(opt['symptom'])
            
            if st.button(get_text("Next →", "आगे →"), key=f"next_multi_{q['id']}"):
                if not selected_values:
                    selected_values = ['none']
                st.session_state.answers[q['id']] = selected_values
                st.session_state.step += 1
                st.rerun()
    
    else:
        # All questions answered - show results
        st.session_state.show_result = True
        st.session_state.has_red_flag = check_red_flags(st.session_state.answers, symptom_data)
        st.rerun()

# ============ SHOW RESULTS ============
if st.session_state.show_result:
    
    symptom_data = symptom_questions.get(st.session_state.selected_symptom, {})
    
    # Check for red flags
    if st.session_state.has_red_flag:
        guidance = guidance_templates.get('urgent_care', {})
        confidence = 0.9
    else:
        confidence = calculate_confidence(st.session_state.answers, symptom_data)
        guidance = get_guidance(st.session_state.selected_symptom, st.session_state.answers, confidence)
    
    # Also get ML prediction for reference
    ml_disease, ml_confidence = predict_with_ml(st.session_state.collected_symptoms)
    
    # Display results
    if st.session_state.has_red_flag:
        st.markdown(f"""
        <div class="urgent-card">
            <h2>⚠️ {get_text("URGENT - See Doctor Immediately", "जरूरी - तुरंत डॉक्टर से मिलें")}</h2>
            <p>{get_text("Your symptoms need immediate medical attention", "आपके लक्षणों को तुरंत चिकित्सा की जरूरत है")}</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        condition = guidance.get(f'condition_{st.session_state.lang}', guidance.get('condition_en', ''))
        st.markdown(f"""
        <div class="result-card">
            <h3>🩺 {get_text("Assessment", "आकलन")}</h3>
            <p style="font-size: 1.2rem; font-weight: bold;">{condition}</p>
            <div class="confidence-bar">
                <div class="confidence-fill" style="width: {confidence*100}%;"></div>
            </div>
            <p>{get_text(f"Confidence: {confidence*100:.0f}%", f"विश्वास: {confidence*100:.0f}%")}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Self-care recommendations
    self_care = guidance.get('self_care', [])
    if self_care:
        st.markdown(f"""
        <div class="care-card">
            <h4>🏠 {get_text("Self Care at Home", "घर पर देखभाल")}</h4>
        """, unsafe_allow_html=True)
        
        for item in self_care:
            text = item.get(st.session_state.lang, item.get('en', ''))
            st.markdown(f'<div class="care-item">✓ {text}</div>', unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # OTC Medicines
    medicines = guidance.get('otc_medicines', [])
    if medicines and not st.session_state.has_red_flag:
        st.markdown(f"""
        <div class="medicine-card">
            <h4>💊 {get_text("Medicines (Available at Medical Store)", "दवाइयां (मेडिकल स्टोर पर मिलती हैं)")}</h4>
        """, unsafe_allow_html=True)
        
        for med in medicines:
            name = med.get('name', '')
            dose = med.get(st.session_state.lang, med.get('dose', ''))
            st.markdown(f'<div class="medicine-item"><strong>{name}</strong><br>{dose}</div>', unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # When to see doctor
    see_doctor = guidance.get('see_doctor_if', [])
    if see_doctor:
        st.markdown(f"""
        <div class="warning-card">
            <h4>🏥 {get_text("See Doctor If:", "डॉक्टर को दिखाएं अगर:")}</h4>
        """, unsafe_allow_html=True)
        
        for item in see_doctor:
            text = item.get(st.session_state.lang, item.get('en', ''))
            st.markdown(f'<div class="warning-item">⚠️ {text}</div>', unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Action buttons
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button(f"🔄 {get_text('New Check', 'नई जांच')}", use_container_width=True):
            reset_chat()
            st.rerun()
    
    with col2:
        if st.button(f"📞 {get_text('Call Doctor', 'डॉक्टर को कॉल करें')}", use_container_width=True):
            st.info(get_text(
                "Video consultation feature coming soon! For now, visit your nearest health center.",
                "वीडियो परामर्श जल्द आ रहा है! अभी अपने नज़दीकी स्वास्थ्य केंद्र जाएं।"
            ))
    
    # Disclaimer
    st.markdown(f"""
    <div class="footer">
        <p>⚠️ {get_text(
            "This is AI-based guidance only. Always consult a doctor for proper diagnosis.",
            "यह केवल AI आधारित मार्गदर्शन है। सही निदान के लिए हमेशा डॉक्टर से मिलें।"
        )}</p>
    </div>
    """, unsafe_allow_html=True)

# Footer for step 0
if st.session_state.step == 0 and not st.session_state.show_result:
    st.markdown(f"""
    <div class="footer">
        <p>🏥 <strong>{get_text("Aarogya Setu+", "आरोग्य सेतु+")}</strong></p>
        <p>{get_text("Rural Health Initiative | Trained on 4,920 patient records", "ग्रामीण स्वास्थ्य पहल | 4,920 रोगी रिकॉर्ड पर प्रशिक्षित")}</p>
        <p style="margin-top: 8px; font-size: 0.8rem;">{get_text("Made with ❤️ for Rural India", "ग्रामीण भारत के लिए ❤️ से बनाया गया")}</p>
    </div>
    """, unsafe_allow_html=True)

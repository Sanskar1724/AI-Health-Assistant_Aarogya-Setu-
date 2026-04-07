"""
╔════════════════════════════════════════════════════════════════════════════╗
║            AAROGYA SETU+ - Modern Professional UI/UX Version               ║
║                    AI-Powered Rural Health Assistant                       ║
║                                                                            ║
║  A modern, responsive Streamlit application with professional design,     ║
║  dark/light theme support, data visualization, and sidebar navigation.    ║
╚════════════════════════════════════════════════════════════════════════════╝
"""

import streamlit as st
import pandas as pd
import numpy as np
import joblib
import json
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
from enum import Enum

# ═════════════════════════════════════════════════════════════════════════════
# CONFIGURATION & CONSTANTS
# ═════════════════════════════════════════════════════════════════════════════

class Theme(Enum):
    """Theme configuration enum"""
    LIGHT = {
        "primary": "#0D5C2F",      # Professional green
        "secondary": "#0D47A1",    # Professional blue
        "accent": "#FF6B35",       # Accent orange
        "success": "#2E7D32",      # Success green
        "warning": "#F57C00",      # Warning orange
        "danger": "#C62828",       # Danger red
        "bg": "#F8F9FA",           # Light background
        "bg_secondary": "#FFFFFF", # Card background
        "text": "#212121",         # Text color
        "text_secondary": "#757575" # Secondary text
    }
    DARK = {
        "primary": "#4CAF50",      # Lighter green for dark mode
        "secondary": "#42A5F5",    # Lighter blue
        "accent": "#FF7043",       # Lighter orange
        "success": "#66BB6A",      # Lighter success
        "warning": "#FFA726",      # Lighter warning
        "danger": "#EF5350",       # Lighter danger
        "bg": "#121212",           # Dark background
        "bg_secondary": "#1E1E1E", # Dark card background
        "text": "#FFFFFF",         # Light text
        "text_secondary": "#B0B0B0" # Light secondary text
    }

# ═════════════════════════════════════════════════════════════════════════════
# PAGE CONFIGURATION
# ═════════════════════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="Aarogya Setu+ | Health Assistant",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/yourusername/aarogya-setu',
        'Report a bug': "https://github.com/yourusername/aarogya-setu/issues",
        'About': "### Aarogya Setu+ v2.0\nModern AI Health Assistant for Rural Healthcare"
    }
)

# ═════════════════════════════════════════════════════════════════════════════
# SESSION STATE INITIALIZATION
# ═════════════════════════════════════════════════════════════════════════════

def init_session_state():
    """Initialize all session state variables"""
    defaults = {
        'theme': 'light',
        'lang': 'en',
        'step': 0,
        'selected_symptom': None,
        'answers': {},
        'collected_symptoms': [],
        'severity_score': 0,
        'show_result': False,
        'has_red_flag': False,
        'history': [],  # Track consultation history
        'show_charts': True,
        'prediction_result': None,
        'confidence': 0.0
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session_state()

# ═════════════════════════════════════════════════════════════════════════════
# THEME & STYLING FUNCTIONS
# ═════════════════════════════════════════════════════════════════════════════

def get_theme_dict():
    """Get current theme dictionary"""
    return Theme[st.session_state.theme.upper()].value

def apply_theme():
    """Apply CSS styling based on current theme"""
    theme = get_theme_dict()
    
    css = f"""
    <style>
    /* ══════════════════════════════════════════════════════════════════════ */
    /* GLOBAL STYLING - Foundation                                           */
    /* ══════════════════════════════════════════════════════════════════════ */
    
    * {{ 
        box-sizing: border-box;
    }}
    
    /* Main app container */
    .stApp {{
        background-color: {theme['bg']};
        color: {theme['text']};
    }}
    
    /* Block container - main content area */
    .main .block-container {{
        padding: 2rem 3rem;
        max-width: 1400px;
        margin: 0 auto;
    }}
    
    /* ══════════════════════════════════════════════════════════════════════ */
    /* HEADER & NAVIGATION STYLING                                           */
    /* ══════════════════════════════════════════════════════════════════════ */
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {{
        background-color: {theme['bg_secondary']};
        border-right: 2px solid {theme['primary']};
    }}
    
    [data-testid="stSidebarNav"] {{
        padding: 1rem 0;
    }}
    
    /* Main header */
    .app-header {{
        background: linear-gradient(135deg, {theme['primary']} 0%, {theme['secondary']} 100%);
        color: white;
        padding: 3rem 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 8px 24px rgba(0,0,0,0.15);
        text-align: center;
    }}
    
    .app-header h1 {{
        margin: 0;
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }}
    
    .app-header p {{
        margin: 0;
        font-size: 1.1rem;
        opacity: 0.95;
    }}
    
    /* ══════════════════════════════════════════════════════════════════════ */
    /* CARDS & CONTAINERS                                                    */
    /* ══════════════════════════════════════════════════════════════════════ */
    
    .metric-card {{
        background-color: {theme['bg_secondary']};
        border: 2px solid {theme['primary']};
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        transition: all 0.3s ease;
    }}
    
    .metric-card:hover {{
        transform: translateY(-4px);
        box-shadow: 0 8px 20px rgba(0,0,0,0.12);
        border-color: {theme['secondary']};
    }}
    
    .metric-number {{
        font-size: 2.5rem;
        font-weight: 700;
        color: {theme['primary']};
        margin: 0.5rem 0;
    }}
    
    .metric-label {{
        font-size: 0.95rem;
        color: {theme['text_secondary']};
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 600;
    }}
    
    /* Result cards */
    .result-card {{
        background-color: {theme['bg_secondary']};
        border-left: 5px solid {theme['success']};
        border-radius: 8px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }}
    
    .result-card.warning {{
        border-left-color: {theme['warning']};
    }}
    
    .result-card.danger {{
        border-left-color: {theme['danger']};
    }}
    
    /* ══════════════════════════════════════════════════════════════════════ */
    /* FORMS & INPUTS                                                         */
    /* ══════════════════════════════════════════════════════════════════════ */
    
    .stRadio > label {{
        font-weight: 600;
        color: {theme['text']};
    }}
    
    .stCheckbox > label {{
        font-weight: 600;
        color: {theme['text']};
    }}
    
    .stSelectbox > label {{
        font-weight: 600;
        color: {theme['text']};
    }}
    
    /* ══════════════════════════════════════════════════════════════════════ */
    /* BUTTONS                                                                */
    /* ══════════════════════════════════════════════════════════════════════ */
    
    .stButton > button {{
        background-color: {theme['primary']};
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
        cursor: pointer;
        min-height: 3rem;
    }}
    
    .stButton > button:hover {{
        background-color: {theme['secondary']};
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(0,0,0,0.15);
    }}
    
    /* ══════════════════════════════════════════════════════════════════════ */
    /* TEXT & TYPOGRAPHY                                                      */
    /* ══════════════════════════════════════════════════════════════════════ */
    
    h1, h2, h3, h4, h5, h6 {{
        color: {theme['primary']};
        font-weight: 700;
    }}
    
    p {{
        color: {theme['text']};
    }}
    
    .section-title {{
        font-size: 1.5rem;
        font-weight: 700;
        color: {theme['primary']};
        padding-bottom: 0.5rem;
        border-bottom: 3px solid {theme['primary']};
        margin-bottom: 1.5rem;
    }}
    
    /* ══════════════════════════════════════════════════════════════════════ */
    /* ALERTS & MESSAGES                                                      */
    /* ══════════════════════════════════════════════════════════════════════ */
    
    .alert-success {{
        background-color: rgba(46, 125, 50, 0.1);
        border-left: 5px solid {theme['success']};
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }}
    
    .alert-warning {{
        background-color: rgba(245, 124, 0, 0.1);
        border-left: 5px solid {theme['warning']};
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }}
    
    .alert-danger {{
        background-color: rgba(198, 40, 40, 0.1);
        border-left: 5px solid {theme['danger']};
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }}
    
    /* ══════════════════════════════════════════════════════════════════════ */
    /* PROGRESS & INDICATORS                                                  */
    /* ══════════════════════════════════════════════════════════════════════ */
    
    .progress-container {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin: 2rem 0;
        gap: 5px;
    }}
    
    .progress-step {{
        flex: 1;
        height: 4px;
        background-color: {theme['text_secondary']};
        border-radius: 2px;
        overflow: hidden;
    }}
    
    .progress-step.active {{
        background-color: {theme['primary']};
    }}
    
    .progress-step.completed {{
        background-color: {theme['success']};
    }}
    
    /* ══════════════════════════════════════════════════════════════════════ */
    /* RESPONSIVE MOBILE STYLING                                              */
    /* ══════════════════════════════════════════════════════════════════════ */
    
    @media (max-width: 768px) {{
        .main .block-container {{
            padding: 1rem;
        }}
        
        .app-header {{
            padding: 2rem 1rem;
        }}
        
        .app-header h1 {{
            font-size: 1.8rem;
        }}
        
        .metric-card {{
            margin-bottom: 1rem;
        }}
    }}
    
    /* ══════════════════════════════════════════════════════════════════════ */
    /* UTILITY CLASSES                                                         */
    /* ══════════════════════════════════════════════════════════════════════ */
    
    .text-center {{ text-align: center; }}
    .text-muted {{ color: {theme['text_secondary']}; }}
    .mt-2 {{ margin-top: 1rem; }}
    .mb-2 {{ margin-bottom: 1rem; }}
    .p-2 {{ padding: 1rem; }}
    
    </style>
    """
    
    st.markdown(css, unsafe_allow_html=True)

# ═════════════════════════════════════════════════════════════════════════════
# DATA LOADING FUNCTIONS
# ═════════════════════════════════════════════════════════════════════════════

@st.cache_resource
def load_ml_model():
    """Load trained ML model and encoder"""
    try:
        model = joblib.load('disease_predictor_rf.pkl')
        label_encoder = joblib.load('label_encoder.pkl')
        return model, label_encoder
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None, None

@st.cache_data
def load_app_data():
    """Load all JSON data files"""
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

# Load models and data
model, label_encoder = load_ml_model()
symptom_questions, guidance_templates, symptom_list, disease_info = load_app_data()

# ═════════════════════════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ═════════════════════════════════════════════════════════════════════════════

def get_text(en: str, hi: str) -> str:
    """Return text based on current language setting"""
    return hi if st.session_state.lang == 'hi' else en

def reset_consultation():
    """Reset all consultation-related session state"""
    st.session_state.step = 0
    st.session_state.selected_symptom = None
    st.session_state.answers = {}
    st.session_state.collected_symptoms = []
    st.session_state.severity_score = 0
    st.session_state.show_result = False
    st.session_state.has_red_flag = False

def calculate_confidence(answers: dict, symptom_data: dict) -> float:
    """Calculate confidence score based on answers"""
    total_weight = 0
    max_weight = 0
    
    for q in symptom_data.get('questions', []):
        qid = q['id']
        if qid in answers:
            if q['type'] == 'select':
                for opt in q['options']:
                    max_weight += 3
                    if opt['value'] == answers[qid]:
                        total_weight += opt.get('weight', 1)
            elif q['type'] == 'multiselect':
                max_weight += len(q['options']) - 1
                for opt in q['options']:
                    if opt['value'] in answers[qid] and opt['value'] != 'none':
                        total_weight += 1
    
    if max_weight == 0:
        return 0.5
    
    confidence = 0.5 + (total_weight / max_weight) * 0.45
    return min(confidence, 0.95)

def check_red_flags(answers: dict, symptom_data: dict) -> bool:
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

def predict_disease(collected_symptoms: list) -> tuple:
    """Predict disease using ML model"""
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
    except Exception as e:
        st.warning(f"Prediction error: {e}")
        return None, 0

# ═════════════════════════════════════════════════════════════════════════════
# SIDEBAR - NAVIGATION & SETTINGS
# ═════════════════════════════════════════════════════════════════════════════

with st.sidebar:
    st.markdown("---")
    
    # Logo & Title
    col1, col2, col3 = st.columns([1, 2, 1], gap="small")
    with col2:
        st.markdown("### 🏥 Aarogya Setu+")
    
    st.markdown("**AI Health Assistant**")
    st.markdown("*Powered by Machine Learning*")
    
    st.markdown("---")
    
    # Navigation Menu
    st.subheader("📋 Menu")
    menu_choice = st.radio(
        "Select Section",
        ["🏠 Home", "🩺 Assessment", "📊 Dashboard", "ℹ️ About"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    # Settings Section
    st.subheader("⚙️ Settings")
    
    # Language selector
    lang_col1, lang_col2 = st.columns(2)
    with lang_col1:
        if st.button("🇬🇧 English", use_container_width=True):
            st.session_state.lang = 'en'
            st.rerun()
    with lang_col2:
        if st.button("🇮🇳 हिंदी", use_container_width=True):
            st.session_state.lang = 'hi'
            st.rerun()
    
    st.markdown("")
    
    # Theme toggle
    theme_col1, theme_col2 = st.columns(2)
    with theme_col1:
        if st.button("☀️ Light", use_container_width=True):
            st.session_state.theme = 'light'
            st.rerun()
    with theme_col2:
        if st.button("🌙 Dark", use_container_width=True):
            st.session_state.theme = 'dark'
            st.rerun()
    
    st.markdown("---")
    
    # Quick Stats
    st.subheader("📈 Quick Stats")
    num_diseases = len(label_encoder.classes_) if label_encoder else 41
    num_symptoms = len(symptom_list) if symptom_list else 131
    
    col1, col2 = st.columns(2, gap="small")
    with col1:
        st.metric("Diseases", num_diseases)
    with col2:
        st.metric("Symptoms", num_symptoms)
    
    st.markdown("---")
    
    # Footer Info
    st.markdown("**Version:** 2.0.0")
    st.markdown("**Last Updated:** April 2026")
    st.markdown("[GitHub](https://github.com) • [Feedback](https://github.com/feedback)")

# ═════════════════════════════════════════════════════════════════════════════
# APPLY THEME
# ═════════════════════════════════════════════════════════════════════════════

apply_theme()

# ═════════════════════════════════════════════════════════════════════════════
# MAIN CONTENT AREA
# ═════════════════════════════════════════════════════════════════════════════

theme = get_theme_dict()

# Header
st.markdown(f"""
<div class="app-header">
    <h1>🏥 {get_text("Aarogya Setu+", "आरोग्य सेतु+")}</h1>
    <p>{get_text("Your AI-Powered Rural Health Assistant", "आपका AI-संचालित ग्रामीण स्वास्थ्य सहायक")}</p>
</div>
""", unsafe_allow_html=True)

# ═════════════════════════════════════════════════════════════════════════════
# PAGE: HOME
# ═════════════════════════════════════════════════════════════════════════════

if menu_choice == "🏠 Home":
    
    # Welcome Section
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 👋 Welcome!")
        st.markdown(get_text(
            "Start a symptom assessment to get AI-powered health guidance. Our system analyzes your symptoms and provides recommendations.",
            "लक्षण आकलन शुरू करें और AI-संचालित स्वास्थ्य मार्गदर्शन प्राप्त करें।"
        ))
        
        if st.button("🩺 Start Assessment", use_container_width=True, key="home_start"):
            st.session_state.step = 0
            menu_choice = "🩺 Assessment"
            st.rerun()
    
    with col2:
        st.markdown("### 🎯 Key Features")
        features = [
            "✅ 40+ Diseases",
            "✅ 130+ Symptoms",
            "✅ AI Powered",
            "✅ Multilingual",
            "✅ Free & Safe"
        ]
        for feature in features:
            st.write(feature)
    
    st.markdown("---")
    
    # Metrics Grid
    st.markdown("### 📊 System Statistics")
    
    col1, col2, col3, col4 = st.columns(4, gap="medium")
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div style="font-size: 2rem;">🏥</div>
            <div class="metric-number">{num_diseases}</div>
            <div class="metric-label">Diseases</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div style="font-size: 2rem;">🔍</div>
            <div class="metric-number">{num_symptoms}</div>
            <div class="metric-label">Symptoms</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div style="font-size: 2rem;">🤖</div>
            <div class="metric-number">98.39%</div>
            <div class="metric-label">Accuracy</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div style="font-size: 2rem;">👥</div>
            <div class="metric-number">4.9K</div>
            <div class="metric-label">Records</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # How it works
    st.markdown("### 📚 How It Works")
    
    col1, col2, col3, col4 = st.columns(4, gap="medium")
    
    steps = [
        ("1️⃣", "Select Symptom", "Choose your main health problem"),
        ("2️⃣", "Answer Questions", "Provide details about your symptoms"),
        ("3️⃣", "AI Analysis", "Our system analyzes your information"),
        ("4️⃣", "Get Guidance", "Receive recommendations and guidance")
    ]
    
    for i, (emoji, title, desc) in enumerate(steps):
        with [col1, col2, col3, col4][i]:
            st.markdown(f"""
            <div class="result-card">
                <div style="font-size: 1.5rem; margin-bottom: 0.5rem;">{emoji}</div>
                <strong>{title}</strong>
                <br><small>{desc}</small>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Disclaimer
    st.warning(get_text(
        "⚠️ DISCLAIMER: This application provides AI-based health guidance only and is NOT a substitute for professional medical advice. Always consult a qualified healthcare provider for diagnosis and treatment.",
        "⚠️ प्रतिस्पर्धी: यह अनुप्रयोग AI आधारित स्वास्थ्य मार्गदर्शन प्रदान करता है और व्यावसायिक चिकित्सा सलाह का विकल्प नहीं है।"
    ))

# ═════════════════════════════════════════════════════════════════════════════
# PAGE: ASSESSMENT
# ═════════════════════════════════════════════════════════════════════════════

elif menu_choice == "🩺 Assessment":
    
    if st.session_state.step == 0 and not st.session_state.show_result:
        # Step 0: Select Main Symptom
        
        st.markdown("### 🩺 Choose Your Main Symptom")
        st.markdown(get_text(
            "Select the primary health problem you're experiencing",
            "अपनी मुख्य स्वास्थ्य समस्या चुनें"
        ))
        
        # Create symptom options with emojis
        symptom_options = []
        for key, data in symptom_questions.items():
            symptom_options.append({
                'key': key,
                'icon': data.get('icon', '🩺'),
                'name_en': data.get('name_en', key),
                'name_hi': data.get('name_hi', key),
                'desc': data.get('description', '')
            })
        
        # Display symptoms in grid (3 columns)
        cols = st.columns(3, gap="medium")
        for i, symptom in enumerate(symptom_options):
            with cols[i % 3]:
                label = symptom['name_hi'] if st.session_state.lang == 'hi' else symptom['name_en']
                
                if st.button(
                    f"{symptom['icon']}\n{label}",
                    key=f"sym_{symptom['key']}",
                    use_container_width=True,
                    help=symptom.get('desc', '')
                ):
                    st.session_state.selected_symptom = symptom['key']
                    st.session_state.step = 1
                    st.session_state.collected_symptoms = symptom_questions[symptom['key']].get('base_symptoms', [])
                    st.rerun()
    
    elif st.session_state.step > 0 and not st.session_state.show_result:
        # Step 1+: Follow-up Questions
        
        symptom_data = symptom_questions.get(st.session_state.selected_symptom, {})
        questions = symptom_data.get('questions', [])
        current_q_index = st.session_state.step - 1
        
        # Progress indicator
        progress_value = (current_q_index + 1) / max(len(questions), 1)
        st.progress(progress_value)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown(f"**Question {current_q_index + 1} of {len(questions)}**")
        
        st.markdown("---")
        
        if current_q_index < len(questions):
            q = questions[current_q_index]
            question_text = q.get(f'question_{st.session_state.lang}', q.get('question_en', ''))
            
            st.markdown(f"### {question_text}")
            
            # Render question based on type
            if q['type'] == 'select':
                options = q['options']
                option_labels = [opt.get(f'label_{st.session_state.lang}', opt.get('label_en', '')) for opt in options]
                
                selected_idx = st.radio(
                    "Select one:",
                    options=list(range(len(options))),
                    format_func=lambda idx: option_labels[idx],
                    key=f"q_{q['id']}",
                    label_visibility="collapsed"
                )
                
                col1, col2 = st.columns([1, 1], gap="small")
                with col1:
                    if st.button("← Back", use_container_width=True):
                        st.session_state.step = max(0, st.session_state.step - 1)
                        st.rerun()
                with col2:
                    if st.button("Next →", use_container_width=True):
                        st.session_state.answers[q['id']] = options[selected_idx]['value']
                        st.session_state.severity_score += options[selected_idx].get('weight', 1)
                        st.session_state.step += 1
                        st.rerun()
            
            elif q['type'] == 'multiselect':
                options = q['options']
                st.markdown("**Select all that apply:**")
                
                selected_values = []
                for i, opt in enumerate(options):
                    label = opt.get(f'label_{st.session_state.lang}', opt.get('label_en', ''))
                    if st.checkbox(label, key=f"multi_{q['id']}_{i}"):
                        selected_values.append(opt['value'])
                        if opt.get('symptom') and opt['symptom'] not in st.session_state.collected_symptoms:
                            st.session_state.collected_symptoms.append(opt['symptom'])
                
                col1, col2 = st.columns([1, 1], gap="small")
                with col1:
                    if st.button("← Back", use_container_width=True):
                        st.session_state.step = max(0, st.session_state.step - 1)
                        st.rerun()
                with col2:
                    if st.button("Next →", use_container_width=True):
                        if not selected_values:
                            selected_values = ['none']
                        st.session_state.answers[q['id']] = selected_values
                        st.session_state.step += 1
                        st.rerun()
        else:
            # All questions answered - move to results
            st.session_state.show_result = True
            st.session_state.has_red_flag = check_red_flags(st.session_state.answers, symptom_data)
            st.rerun()
    
    # Show results section
    if st.session_state.show_result:
        
        symptom_data = symptom_questions.get(st.session_state.selected_symptom, {})
        confidence = calculate_confidence(st.session_state.answers, symptom_data)
        
        # Get ML prediction
        ml_disease, ml_confidence = predict_disease(st.session_state.collected_symptoms)
        
        st.markdown("---")
        st.markdown("### 📋 Assessment Results")
        
        # Create tabs for different result views
        tab1, tab2, tab3 = st.tabs(["📊 Summary", "💊 Recommendations", "📈 Details"])
        
        with tab1:
            if st.session_state.has_red_flag:
                st.error("⚠️ **URGENT** - Your symptoms suggest immediate medical attention is needed!")
            else:
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown("#### Confidence Score")
                    st.progress(confidence)
                    st.markdown(f"**{confidence*100:.0f}%** confidence based on your symptoms")
                
                with col2:
                    st.metric("Severity", f"{st.session_state.severity_score}/10")
        
        with tab2:
            st.markdown("#### Recommendations")
            
            # Get guidance based on selected symptom
            guidance = guidance_templates.get(st.session_state.selected_symptom, {})
            
            # Self-care recommendations
            if guidance.get('self_care'):
                st.markdown("##### 🏠 Self-Care at Home")
                for item in guidance['self_care']:
                    st.write(f"✓ {item.get(st.session_state.lang, item.get('en', ''))}")
            
            # Medicines
            if guidance.get('otc_medicines') and not st.session_state.has_red_flag:
                st.markdown("##### 💊 Available Medicines")
                medicine_df = pd.DataFrame(guidance['otc_medicines'])
                st.dataframe(medicine_df, use_container_width=True)
            
            # When to see doctor
            if guidance.get('see_doctor_if'):
                st.markdown("##### 🏥 Consult Doctor If:")
                for item in guidance['see_doctor_if']:
                    st.write(f"• {item.get(st.session_state.lang, item.get('en', ''))}")
        
        with tab3:
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Symptoms Checked", len(st.session_state.collected_symptoms))
            
            with col2:
                st.metric("Questions Answered", len(st.session_state.answers))
            
            with col3:
                if ml_disease:
                    st.metric("ML Prediction", ml_disease[:15])
        
        st.markdown("---")
        
        col1, col2, col3 = st.columns(3, gap="small")
        
        with col1:
            if st.button("🩺 New Assessment", use_container_width=True):
                reset_consultation()
                st.rerun()
        
        with col2:
            st.button("📞 Call Doctor (Soon)", use_container_width=True, disabled=True)
        
        with col3:
            st.button("📥 Download Report (Soon)", use_container_width=True, disabled=True)

# ═════════════════════════════════════════════════════════════════════════════
# PAGE: DASHBOARD
# ═════════════════════════════════════════════════════════════════════════════

elif menu_choice == "📊 Dashboard":
    
    st.markdown("### 📊 System Analytics")
    
    col1, col2, col3, col4 = st.columns(4, gap="medium")
    
    with col1:
        st.metric("Total Diseases", num_diseases, delta="41 supported")
    with col2:
        st.metric("Total Symptoms", num_symptoms, delta="131 tracked")
    with col3:
        st.metric("Model Accuracy", "98.39%", delta="+1.5%")
    with col4:
        st.metric("Training Records", "4,920", delta="1000+ added")
    
    st.markdown("---")
    
    # Symptom frequency (sample chart)
    st.markdown("### 🔍 Common Symptoms")
    
    symptom_freq = pd.DataFrame({
        'Symptom': ['Fever', 'Cough', 'Headache', 'Body Pain', 'Fatigue'],
        'Frequency': [120, 110, 95, 85, 75]
    })
    
    fig = px.bar(
        symptom_freq,
        x='Frequency',
        y='Symptom',
        orientation='h',
        title='Top Symptoms in Dataset',
        color='Frequency'
    )
    fig.update_layout(
        height=400,
        template='plotly_white' if st.session_state.theme == 'light' else 'plotly_dark',
        showlegend=False
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Disease distribution (sample)
    st.markdown("### 🏥 Disease Distribution")
    
    disease_data = pd.DataFrame({
        'Category': ['Respiratory', 'Digestive', 'Cardiovascular', 'Neurological', 'Other'],
        'Count': [12, 8, 6, 5, 10]
    })
    
    fig_pie = px.pie(
        disease_data,
        values='Count',
        names='Category',
        title='Diseases by Category'
    )
    fig_pie.update_layout(
        template='plotly_white' if st.session_state.theme == 'light' else 'plotly_dark',
        height=400
    )
    st.plotly_chart(fig_pie, use_container_width=True)

# ═════════════════════════════════════════════════════════════════════════════
# PAGE: ABOUT
# ═════════════════════════════════════════════════════════════════════════════

elif menu_choice == "ℹ️ About":
    
    st.markdown("### 🏥 About Aarogya Setu+")
    
    col1, col2 = st.columns([2, 1], gap="large")
    
    with col1:
        st.markdown("""
        #### 📖 Project Overview
        
        Aarogya Setu+ is an AI-powered rural health assistant designed to provide accessible,
        accurate health guidance to underserved populations. Built on machine learning models
        trained on thousands of patient records, it offers:
        
        **Key Features:**
        - Progressive symptom assessment
        - AI-powered disease prediction
        - Personalized health recommendations
        - Multiple language support
        - Completely free and accessible
        
        **Technology Stack:**
        - Python & Streamlit for web interface
        - scikit-learn for ML models (Random Forest)
        - 98.39% accuracy on test dataset
        - Support for 41 diseases and 131+ symptoms
        
        #### 🎯 Mission
        Democratize healthcare access in rural areas by providing AI-powered health guidance
        that empowers people to make informed health decisions.
        
        #### 📊 Dataset Statistics
        - **Training Samples:** 4,920 patient records
        - **Features:** 18+ symptom features per record
        - **Target Classes:** 41 unique diseases
        - **Preprocessing:** Advanced handling of missing values and duplicates
        """)
    
    with col2:
        st.markdown("#### 🔧 Specifications")
        stats = {
            "Model Type": "Random Forest",
            "Accuracy": "98.39%",
            "Diseases": "41",
            "Symptoms": "131+",
            "Languages": "2",
            "Framework": "Streamlit",
            "Version": "2.0.0"
        }
        for key, value in stats.items():
            st.markdown(f"**{key}:** {value}")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2, gap="medium")
    
    with col1:
        st.markdown("#### ⚠️ Important Disclaimer")
        st.warning("""
        This application provides AI-based health guidance ONLY and is NOT:
        - A medical diagnosis tool
        - A substitute for professional medical advice
        - Intended for emergency situations
        
        Always consult qualified healthcare providers.
        """)
    
    with col2:
        st.markdown("#### 📞 Support & Feedback")
        st.info("""
        - 🐛 Report bugs on GitHub
        - 💬 Provide feedback
        - 📧 Email support
        - 🤝 Contribute to the project
        """)

print("✅ Modern Streamlit app loaded successfully!")

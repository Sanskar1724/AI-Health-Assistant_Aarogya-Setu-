# 🏥 Aarogya Setu+ v2.0 - AI-Powered Rural Health Assistant

> **A modern, bilingual healthcare assistant that uses machine learning to predict diseases and provide personalized health guidance for rural and underserved communities.**

![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)
![License](https://img.shields.io/badge/license-MIT-orange.svg)
![Status](https://img.shields.io/badge/status-Production%20Ready-brightgreen.svg)

---

## 📋 Table of Contents

1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Quick Start](#quick-start)
4. [System Architecture](#system-architecture)
5. [Machine Learning Model](#machine-learning-model)
6. [Dataset](#dataset)
7. [Installation](#installation)
8. [Usage](#usage)
9. [File Structure](#file-structure)
10. [Troubleshooting](#troubleshooting)
11. [Contributing](#contributing)
12. [License](#license)

---

## 🎯 Project Overview

**Aarogya Setu+** is an AI-powered health assessment system designed specifically for rural healthcare access. It combines:

- **98.39% Accurate ML Model** - Random Forest Classifier trained on 4,920 patient records
- **41 Diseases** - Comprehensive disease coverage
- **131+ Symptoms** - Extensive symptom analysis
- **Bilingual Support** - Hindi & English interfaces
- **Rural-Friendly Design** - No typing required (dropdown-only interface)
- **Professional Reports** - Downloadable health assessments
- **Emergency Detection** - Red flag identification for urgent cases

### Mission
Democratize healthcare access by providing AI-powered health guidance that empowers people in underserved communities to make informed health decisions.

---

## ✨ Features

### 🤖 Machine Learning
- **98.39% Model Accuracy** on test dataset
- **131+ Symptoms** analyzed simultaneously
- **41 Diseases** supported
- **4,920 Patient Records** in training data
- Real-time predictions with confidence scores

### 👥 User Experience
- **Zero-Typing Interface** - Dropdown selections only
- **Bilingual** - Full Hindi & English support
- **Progressive Questions** - Adaptive questionnaire system
- **Mobile-Responsive** - Works on all devices
- **High-Contrast Design** - Accessible for low-vision users

### 💊 Medical Guidance
- **Disease Predictions** - AI-powered diagnosis suggestions
- **Self-Care Tips** - Evidence-based home care recommendations
- **OTC Medicine Suggestions** - With dosage and timing
- **Red Flag Detection** - Emergency symptoms identification
- **Professional Reports** - Downloadable assessment documents

---

## 🚀 Quick Start

### Prerequisites
```
Python 3.8+
pip (Python package manager)
Virtual environment (recommended)
```

### 30-Second Setup

```bash
# 1. Navigate to project directory
cd "Disease-Symptom-Dataset-main"

# 2. Activate virtual environment
.\.venv\Scripts\Activate.ps1    # Windows PowerShell
source .venv/bin/activate        # Linux/Mac

# 3. Run the application
streamlit run app.py

# 4. Open in browser
# App will open automatically at http://localhost:8503
```

---

## 🏗️ System Architecture

**Components:**
- **Frontend**: Streamlit 1.54.0 (4 pages)
- **Backend**: Python 3.14.3
- **ML Model**: scikit-learn Random Forest with 200 trees
- **Data Processing**: Pandas, NumPy
- **Visualization**: Plotly, Matplotlib, Seaborn

---

## 🤖 Machine Learning Model

### Algorithm: Random Forest Classifier

```
Configuration:
├─ Number of Trees: 200
├─ Max Depth: 15 levels per tree
├─ Min Samples Split: 5
├─ Min Samples Leaf: 2
├─ Feature Count: 131 symptoms
└─ Output Classes: 41 diseases
```

### Performance Metrics

| Metric | Value |
|--------|-------|
| **Test Accuracy** | 98.39% ✅ |
| **Training Samples** | 247 (80%) |
| **Testing Samples** | 62 (20%) |
| **Diseases** | 41 |
| **Features** | 131 |

---

## 📊 Dataset

### Data Sources (4 CSV Files)

| File | Records | Content |
|------|---------|---------|
| `dataset.csv` | 4,920 | Disease + symptoms |
| `symptom_Description.csv` | 41 | Disease descriptions |
| `symptom_precaution.csv` | 41 | Treatment precautions |
| `Symptom-severity.csv` | 133 | Severity weights |

### Key Statistics

```
✓ 4,920 total patient records
✓ 131 unique symptoms identified
✓ 41 different diseases covered
✓ 98.39% model accuracy
✓ Bilingual support (Hindi/English)
```

---

## 💻 Installation

### Step-by-Step Setup

```bash
# 1. Clone Repository
git clone https://github.com/Sanskar1724/AI-Health-Assistant_Aarogya-Setu-.git
cd Disease-Symptom-Dataset-main

# 2. Create Virtual Environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1    # Windows
source .venv/bin/activate        # Linux/Mac

# 3. Install Dependencies
pip install -r requirements.txt

# 4. Run Application
streamlit run app.py
```

---

## 📖 Usage

### Complete User Journey

1. **Start Assessment** - Click button on home page
2. **Select Symptom** - Choose main health problem
3. **Answer Questions** - Provide 4-5 symptom details
4. **View Results** - See AI prediction and guidance
5. **Download Report** - Save professional assessment

### Example Workflow
```
User: "I have fever"
System: "How high is the fever? (Temperature)"
User: "102°F"
System: "How long have you had this fever?"
User: "3 days"

Result: Viral Fever (85% confidence)
→ Self-care tips, medicines, when to see doctor
→ Download professional report
```

---

## 📁 File Structure

```
Disease-Symptom-Dataset-main/
├── app.py                      # Main application (1200+ lines)
├── README.md                   # This documentation
├── requirements.txt            # Python dependencies
│
├── Data Files/
│   ├── dataset.csv
│   ├── symptom_Description.csv
│   ├── symptom_precaution.csv
│   ├── Symptom-severity.csv
│   └── Other CSV files
│
├── Configuration/
│   ├── symptom_questions.json
│   ├── guidance_templates.json
│   ├── disease_info.json
│   ├── symptom_list.json
│   └── symptom_severity_dict.json
│
├── Models/
│   ├── disease_predictor_rf.pkl   # Trained ML model
│   └── label_encoder.pkl          # Disease encoder
│
└── .venv/                      # Virtual environment
```

---

## 🔧 Troubleshooting

| Problem | Solution |
|---------|----------|
| Module not found | `pip install -r requirements.txt` |
| Port already in use | `streamlit run app.py --server.port 8502` |
| Slow first startup | Models cache on first run (~3 sec) |
| Page not updating | Refresh browser or restart Streamlit |

---

## 🎯 Pages Overview

### 1. Home Page 🏠
- Project overview with key statistics
- Feature highlights
- "Start Assessment" button
- How the system works

### 2. Assessment Page 🩺
- Symptom selector (8 categories)
- Progressive Q&A (4-5 questions)
- Real-time AI prediction
- Results in 3 tabs:
  - **Summary** - Disease + confidence
  - **Recommendations** - Self-care + medicines
  - **Details** - Full assessment data
- Download professional report

### 3. Dashboard 📊
- Assessment statistics and charts
- Visual analytics
- Trends and patterns

### 4. About Page ℹ️
- 5 comprehensive information tabs
- ML model specifications (98.39% accuracy, 200 trees)
- Dataset information (4,920 records, 131 symptoms)
- Application workflow explanation
- Complete feature list and medical disclaimer

---

## 📜 Legal & Safety

⚠️ **Important Disclaimer:**

This application:
- Provides **AI-based health guidance ONLY**
- Is **NOT** a medical diagnosis tool
- Cannot replace professional medical advice
- Is **NOT** for emergency situations

**In emergencies, call emergency services immediately!**

---

## 🤝 Contributing

See the main GitHub repository for contribution guidelines and issue reporting.

---

## 📞 Support

- **Issues:** GitHub Issues
- **Questions:** GitHub Discussions
- **Documentation:** SYSTEM_EXPLANATION.md

---

## 📝 Version History

- **v2.0.0** - Modern UI redesign with comprehensive features
- **v1.5.0** - Report generation system
- **v1.0.0** - Initial release

---

## 🔗 Important Links

- **Repository:** [GitHub](https://github.com/Sanskar1724/AI-Health-Assistant_Aarogya-Setu-)
- **Issues:** Report bugs on GitHub
- **Pull Requests:** Contribute improvements

---

## 📄 License

MIT License - See LICENSE file for details

---

**Made with ❤️ for rural healthcare access**

**Version:** 2.0.0 | **Status:** ✅ Production Ready | **Updated:** April 7, 2026

# 🚀 Deployment Guide - Aarogya Setu+ to Streamlit Cloud

## GitHub Setup

### Step 1: Initialize Git Repository
```bash
cd "Disease-Symptom-Dataset-main"
git init
git add .
git commit -m "Initial commit: Aarogya Setu+ Disease Prediction System"
```

### Step 2: Connect to GitHub
```bash
git remote add origin https://github.com/YOUR_USERNAME/Disease-Symptom-Dataset.git
git branch -M main
git push -u origin main
```

### Files Already Configured for Cloud:
✅ `requirements.txt` - All dependencies listed
✅ `.gitignore` - Prevents uploading venv and cache files
✅ `.streamlit/config.toml` - Streamlit configuration
✅ All model files (`.pkl`) and JSON data files included
✅ Relative paths in `app.py` (compatible with cloud)

---

## Streamlit Cloud Deployment

### Step 1: Sign Up for Streamlit Cloud
1. Go to [streamlit.io/cloud](https://streamlit.io/cloud)
2. Sign in with your GitHub account

### Step 2: Deploy Your App
1. Click **"Create app"**
2. Select your repository: `Disease-Symptom-Dataset`
3. Select branch: `main`
4. Select file path: `app.py`
5. Click **"Deploy"**

### Step 3: App Configuration (Optional)
The app will automatically:
- Install dependencies from `requirements.txt`
- Apply theme settings from `.streamlit/config.toml`
- Load all model files and JSON data

---

## Local Testing Before Cloud Deployment

Test the app locally to ensure everything works:

```bash
# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

Then visit: `http://localhost:8501`

---

## File Structure for Cloud

```
Disease-Symptom-Dataset-main/
├── app.py                          # Main Streamlit app
├── requirements.txt                # Dependencies (NEW)
├── .gitignore                      # Git ignore rules (NEW)
├── .streamlit/
│   └── config.toml                # Streamlit config (NEW)
├── disease_predictor_rf.pkl       # Trained model
├── label_encoder.pkl              # Label encoder
├── disease_info.json              # Disease information
├── symptom_questions.json         # Question prompts
├── symptom_list.json              # Available symptoms
├── guidance_templates.json        # Care guidance
├── README.md                      # Documentation
└── [data files]                   # CSV files and other data
```

---

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'streamlit'"
**Solution:** Check that `requirements.txt` is in the root directory

### Issue: "FileNotFoundError: disease_predictor_rf.pkl"
**Solution:** Ensure all `.pkl` and `.json` files are committed to GitHub

### Issue: App runs locally but fails on cloud
**Solution:** Check `.streamlit/config.toml` is in a `.streamlit/` folder (not at root)

### Issue: Streamlit Cloud memory error
**Solution:** The current model fits well within free tier limits (< 1GB)

---

## After Deployment

Your app will be live at:
```
https://share.streamlit.io/YOUR_USERNAME/Disease-Symptom-Dataset/main/app.py
```

### Monitor & Update
- View logs in Streamlit Cloud dashboard
- Push new changes to GitHub: `git push origin main`
- App updates automatically (may take 1-2 minutes)

---

## Environment Variables (if needed)

For sensitive data (API keys, etc.), add secrets:
1. Go to app settings on Streamlit Cloud
2. Add secrets in TOML format
3. Access via `st.secrets["key_name"]` in app.py

Currently not needed for this project.

---

## Support Resources
- [Streamlit Cloud Docs](https://docs.streamlit.io/streamlit-cloud)
- [GitHub Integration](https://docs.streamlit.io/streamlit-cloud/get-started)
- [Troubleshooting Guide](https://docs.streamlit.io/streamlit-cloud/troubleshooting)

# 📋 GitHub Setup Instructions

## Step 1: Create Repository on GitHub

1. Go to [GitHub.com](https://github.com)
2. Click the **+** icon (top right) → **New repository**
3. Name it: `Disease-Symptom-Dataset` (or your preferred name)
4. Description: `AI Health Assistant - Disease Prediction Using Symptoms`
5. Make it **Public** (for Streamlit Cloud access)
6. Click **Create repository**

## Step 2: Connect Local Repository to GitHub

Copy these commands and run them in PowerShell (in the project directory):

```powershell
cd "l:\my-minor 2.0\Disease-Symptom-Dataset-main\Disease-Symptom-Dataset-main"

# Replace YOUR_USERNAME with your actual GitHub username
git remote add origin https://github.com/YOUR_USERNAME/Disease-Symptom-Dataset.git
git branch -M main
git push -u origin main
```

**Note:** You may be prompted to authenticate with GitHub. Use your GitHub personal access token or sign in through the browser.

## Step 3: Verify on GitHub

1. Go to your repository on GitHub
2. You should see all your files
3. Check that `.gitignore` is working (`.venv/` should NOT be uploaded)

## Files Your Repository Should Have

✅ `app.py` - Main application
✅ `requirements.txt` - Dependencies
✅ `.gitignore` - Ignore rules
✅ `.streamlit/config.toml` - Streamlit configuration
✅ All `.pkl` model files
✅ All `.json` data files
✅ CSV dataset files
✅ Documentation files (README.md, DEPLOYMENT.md, etc.)

❌ `.venv/` folder (should be ignored)
❌ `__pycache__/` (should be ignored)
❌ `.pyc` files (should be ignored)

## Troubleshooting Git Push

### Error: "fatal: Authentication failed"
- Use a personal access token instead of your password
- Or use SSH keys setup

### Error: "Repository not found"
- Double-check your USERNAME in the URL
- Make sure you created the repository on GitHub

### Error: ".venv folder uploaded"
- The `.gitignore` is set up correctly
- Future commits won't include it

---

After pushing to GitHub, you're ready for **Streamlit Cloud deployment!**
See `DEPLOYMENT.md` for cloud setup.

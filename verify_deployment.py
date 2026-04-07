#!/usr/bin/env python3
"""
Deployment verification script - checks if all required files are present
and the ML model can be loaded successfully.
"""

import os
import sys
import json

def verify_files():
    """Verify all required files exist"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    required_files = [
        'disease_predictor_rf.pkl',
        'label_encoder.pkl',
        'scaler.pkl',
        'symptom_questions.json',
        'guidance_templates.json',
        'disease_info.json',
        'symptom_list.json',
        'app.py'
    ]
    
    print("=" * 60)
    print("DEPLOYMENT VERIFICATION")
    print("=" * 60)
    print(f"\nScript Directory: {script_dir}\n")
    
    missing_files = []
    found_files = []
    
    for fname in required_files:
        fpath = os.path.join(script_dir, fname)
        if os.path.exists(fpath):
            size = os.path.getsize(fpath)
            found_files.append(f"✓ {fname} ({size:,} bytes)")
        else:
            missing_files.append(f"✗ {fname} - NOT FOUND")
    
    # Print found files
    print("FOUND FILES:")
    for f in found_files:
        print(f"  {f}")
    
    # Print missing files
    if missing_files:
        print("\nMISSING FILES:")
        for f in missing_files:
            print(f"  {f}")
        return False
    
    print("\n" + "=" * 60)
    print("All files verified successfully!")
    print("=" * 60)
    
    # Try loading the model
    print("\nTesting model load...")
    try:
        import joblib
        model_path = os.path.join(script_dir, 'disease_predictor_rf.pkl')
        model = joblib.load(model_path)
        print(f"✓ Model loaded successfully: {type(model).__name__}")
        return True
    except Exception as e:
        print(f"✗ Failed to load model: {e}")
        return False

if __name__ == "__main__":
    success = verify_files()
    sys.exit(0 if success else 1)

"""
Disease Prediction Model Training Script
This script trains the ML models and saves them for the chatbot application
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib
import json
import warnings
warnings.filterwarnings('ignore')

print("=" * 60)
print("DISEASE PREDICTION MODEL TRAINING")
print("=" * 60)

# Load datasets
print("\n[1/7] Loading datasets...")
dataset = pd.read_csv('dataset.csv')
symptom_severity = pd.read_csv('Symptom-severity.csv')
symptom_description = pd.read_csv('symptom_Description.csv')
symptom_precaution = pd.read_csv('symptom_precaution.csv')

print(f"   - Main dataset: {dataset.shape[0]} records, {dataset.shape[1]} columns")
print(f"   - Symptom severity: {symptom_severity.shape[0]} symptoms")
print(f"   - Disease descriptions: {symptom_description.shape[0]} diseases")
print(f"   - Precautions: {symptom_precaution.shape[0]} records")

# Clean symptom names
print("\n[2/7] Cleaning and preprocessing data...")

def clean_text(text):
    if pd.isna(text):
        return None
    return str(text).strip().lower().replace(' ', '_').replace('__', '_')

# Clean all symptom columns in main dataset
for col in dataset.columns:
    if dataset[col].dtype == 'object':
        dataset[col] = dataset[col].apply(clean_text)

# Clean symptom severity
symptom_severity['Symptom'] = symptom_severity['Symptom'].apply(clean_text)

# Get all unique symptoms from the dataset
symptom_cols = [col for col in dataset.columns if 'Symptom' in col]
all_symptoms = set()
for col in symptom_cols:
    symptoms = dataset[col].dropna().unique()
    all_symptoms.update(symptoms)

all_symptoms = sorted([s for s in all_symptoms if s])
print(f"   - Found {len(all_symptoms)} unique symptoms")

# Create symptom to severity mapping
severity_dict = dict(zip(symptom_severity['Symptom'], symptom_severity['weight']))
print(f"   - Severity weights mapped for {len(severity_dict)} symptoms")

# Create binary feature matrix (one-hot encoding for symptoms)
print("\n[3/7] Creating feature matrix...")

def create_symptom_vector(row, all_symptoms):
    """Create binary vector indicating presence of each symptom"""
    symptoms_in_row = []
    for col in symptom_cols:
        if pd.notna(row[col]) and row[col]:
            symptoms_in_row.append(row[col])
    
    vector = [1 if symptom in symptoms_in_row else 0 for symptom in all_symptoms]
    return vector

# Create feature matrix
X_data = []
for idx, row in dataset.iterrows():
    X_data.append(create_symptom_vector(row, all_symptoms))

X = pd.DataFrame(X_data, columns=all_symptoms)
y = dataset['Disease']

print(f"   - Feature matrix shape: {X.shape}")
print(f"   - Number of diseases: {y.nunique()}")

# Encode target variable
print("\n[4/7] Encoding target variable...")
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)
print(f"   - Classes encoded: {len(label_encoder.classes_)}")

# Split data
print("\n[5/7] Splitting data...")
X_train, X_test, y_train, y_test = train_test_split(
    X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
)
print(f"   - Training set: {X_train.shape[0]} samples")
print(f"   - Testing set: {X_test.shape[0]} samples")

# Train Random Forest model
print("\n[6/7] Training Random Forest model...")
rf_model = RandomForestClassifier(
    n_estimators=200,
    max_depth=15,
    min_samples_split=5,
    min_samples_leaf=2,
    random_state=42,
    n_jobs=-1
)
rf_model.fit(X_train, y_train)

# Evaluate model
y_pred = rf_model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"   - Test Accuracy: {accuracy:.4f}")

# Cross-validation
cv_scores = cross_val_score(rf_model, X, y_encoded, cv=5)
print(f"   - Cross-validation scores: {cv_scores.mean():.4f} (+/- {cv_scores.std()*2:.4f})")

# Feature importance
print("\n   Top 10 Important Symptoms:")
importances = rf_model.feature_importances_
indices = np.argsort(importances)[::-1][:10]
for i, idx in enumerate(indices):
    print(f"      {i+1}. {all_symptoms[idx]}: {importances[idx]:.4f}")

# Save models and data
print("\n[7/7] Saving models and data...")

# Save Random Forest model
joblib.dump(rf_model, 'disease_predictor_rf.pkl')
print("   - Saved: disease_predictor_rf.pkl")

# Save Label Encoder
joblib.dump(label_encoder, 'label_encoder.pkl')
print("   - Saved: label_encoder.pkl")

# Save symptom list
with open('symptom_list.json', 'w') as f:
    json.dump(all_symptoms, f)
print("   - Saved: symptom_list.json")

# Save severity dictionary
with open('symptom_severity_dict.json', 'w') as f:
    json.dump(severity_dict, f)
print("   - Saved: symptom_severity_dict.json")

# Create and save disease info dictionary
disease_info = {}
for idx, row in symptom_description.iterrows():
    disease_name = clean_text(row['Disease'])
    if disease_name:
        disease_info[disease_name] = {
            'description': row['Description']
        }

# Add precautions
for idx, row in symptom_precaution.iterrows():
    disease_name = clean_text(row['Disease'])
    if disease_name:
        precautions = []
        for i in range(1, 5):
            col_name = f'Precaution_{i}'
            if col_name in row and pd.notna(row[col_name]):
                precautions.append(row[col_name])
        if disease_name in disease_info:
            disease_info[disease_name]['precautions'] = precautions
        else:
            disease_info[disease_name] = {'precautions': precautions}

with open('disease_info.json', 'w') as f:
    json.dump(disease_info, f, indent=2)
print("   - Saved: disease_info.json")

# Save training data for reference
X_train_df = pd.DataFrame(X_train, columns=all_symptoms)
X_train_df.to_csv('X_train.csv', index=False)
X_test_df = pd.DataFrame(X_test, columns=all_symptoms)
X_test_df.to_csv('X_test.csv', index=False)
pd.DataFrame(y_train, columns=['Disease']).to_csv('y_train.csv', index=False)
pd.DataFrame(y_test, columns=['Disease']).to_csv('y_test.csv', index=False)
print("   - Saved: X_train.csv, X_test.csv, y_train.csv, y_test.csv")

print("\n" + "=" * 60)
print("TRAINING COMPLETE!")
print("=" * 60)
print(f"\nModel Performance Summary:")
print(f"  - Test Accuracy: {accuracy:.2%}")
print(f"  - CV Mean Accuracy: {cv_scores.mean():.2%}")
print(f"  - Number of symptoms: {len(all_symptoms)}")
print(f"  - Number of diseases: {len(label_encoder.classes_)}")
print("\nAll required files have been saved. You can now run the chatbot app!")

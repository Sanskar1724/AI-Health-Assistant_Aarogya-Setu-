# Disease Prediction Model

## Overview
This project aims to predict diseases based on symptoms using a dataset containing disease-symptom mappings, symptom descriptions, precautions, and severity scores. The repository includes data preprocessing steps, exploratory data analysis (EDA), and baseline machine learning models to classify diseases. The best-performing model is a Random Forest Classifier, achieving an accuracy of 98.39% on the test set.

## Dataset
The dataset consists of four CSV files:
1. **dataset.csv**: Main dataset with diseases and associated symptoms (4920 rows, 18 columns).
2. **symptom_Description.csv**: Descriptions of diseases (41 rows, 2 columns).
3. **symptom_precaution.csv**: Precautions for each disease (41 rows, 5 columns).
4. **Symptom-severity.csv**: Severity weights for symptoms (133 rows, 2 columns).

### Key Features
- **Symptoms**: Up to 17 symptoms per disease entry, with many missing values handled during preprocessing.
- **Disease**: 41 unique diseases as the target variable.
- **Severity**: Symptom severity scores merged into the main dataset for a total severity feature.

## Project Structure
- **Data Exploration & Preprocessing**: Cleaning, handling missing values, encoding, and merging datasets.
- **Baseline Models**: Logistic Regression, Random Forest, SVM, and k-NN classifiers.
- **Saved Artifacts**: Trained Random Forest model, scaler, label encoder, and feature names.

## Setup Instructions
### Prerequisites
- Python 3.8+
- Required libraries:
  ```bash
  pip install pandas numpy matplotlib seaborn scikit-learn joblib
  ```

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/hemasriram111/Disease-Symptom-Dataset.git
   cd disease-prediction
   ```
## Preprocessing Steps
- **Missing Values**: Filled categorical columns with mode and numerical columns with median.
- **Cleaning**: Standardized symptom names (lowercase, stripped spaces).
- **Duplicates**: Removed 4618 duplicate rows from the main dataset.
- **Feature Engineering**: Merged symptom severity scores and calculated total severity per entry.
- **Encoding**: Label-encoded diseases; symptoms converted to numerical codes.
- **Train-Test Split**: 80% training (247 samples), 20% testing (62 samples).

## Model Performance
| Model              | Accuracy  | Notes                                      |
|--------------------|-----------|--------------------------------------------|
| Logistic Regression| 83.87%    | Good baseline, struggles with some classes |
| Random Forest      | 98.39%    | Best performer, robust feature importance  |
| SVM (Linear)       | 85.48%    | Decent, but slower on larger datasets      |
| k-NN (k=5)         | 85.48%    | Sensitive to scaling, good local patterns  |

### Top Features (Random Forest)
- `Disease_Encoded`: 0.1458
- `Symptom_2`: 0.0685
- `Symptom_3`: 0.0527
- `Symptom_1`: 0.0511
- `Total_Severity`: 0.0504

## Visualizations
- **Disease Distribution**: Bar plot showing frequency of each disease.
- **Severity Distribution**: Histogram of total severity scores with KDE.

## Usage
To predict a disease:
1. Load the model and preprocess input data using the saved scaler and feature names.
2. Pass the scaled input to the Random Forest model.
3. Decode the prediction using the label encoder.


## Future Improvements
- Hyperparameter tuning for Random Forest.
- Incorporate symptom descriptions and precautions into the model.
- Handle class imbalance if present.
- Deploy as a web application for real-time predictions.

Let me know if you'd like to refine this further!

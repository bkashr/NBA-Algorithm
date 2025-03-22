# NBA Score Prediction Model

## Overview
This project builds a predictive model for estimating NBA game scores based on team statistics. It follows a structured pipeline from raw data collection to model training and evaluation.

## Project Structure
```
NBA Model/
│-- data_prep.py               # Cleans and prepares raw game data
│-- feature_engineering.py     # Creates new statistical features (if applicable)
│-- model_training.py          # Trains the machine learning model
│-- model_prediction.py        # Uses the trained model for score predictions
│-- data_vis.py                # Visualizes dataset trends and model performance
│-- correlation.py             # Analyzes stat correlations with points scored
│-- cleaned_nba_games_fixed.csv  # Processed dataset used for model training
│-- nba_model.pkl              # Saved trained model
│-- nba_games_2023_24.csv      # Original raw dataset
│-- README.md                  # This document
```

## Data Collection & Processing
### 1. **Raw Data (nba_games_2023_24.csv)**
- Contains **NBA game stats from the 2023-24 season**, including points, rebounds, assists, and shooting percentages.
- Includes both **Team A and its opponent**.

### 2. **Data Preparation (data_prep.py)**
- Cleans the dataset and ensures both teams have complete stats.
- Splits matchups into `Team A` and `Team B` to create **a structured dataset**.
- Saves cleaned data as `cleaned_nba_games_fixed.csv`.

### 3. **Feature Engineering (feature_engineering.py)** *(if used)*
- Calculates new features such as **Offensive Efficiency, Pace, and Adjusted Stats** to improve predictions.

## Model Training
### 4. **Training the Model (model_training.py)**
- Loads `cleaned_nba_games_fixed.csv`.
- Encodes categorical variables like team names using **Label Encoding**.
- Splits data into **Training (80%)** and **Testing (20%)** sets.
- Uses **Random Forest Regressor** to predict team scores.
- Saves the trained model as `nba_model.pkl`.

### 5. **Evaluating the Model**
- Uses **Mean Absolute Error (MAE)** to measure accuracy.
- Current model has **MAE ≈ 1.35**, meaning predictions are, on average, **1.35 points off per game**.

## Making Predictions
### 6. **Predicting Game Scores (model_prediction.py)** *(if implemented)*
- Loads `nba_model.pkl`.
- Takes **two teams as input** and retrieves their season stats.
- Uses the model to **predict expected points per team**.

## Data Analysis & Visualization
### 7. **Understanding Trends (data_vis.py, correlation.py)**
- **`correlation.py`** checks **which stats impact scoring the most**.
- **`data_vis.py`** generates **heatmaps, distributions, and prediction vs. actual plots**.

## Next Steps
- **Improve the model** by testing different algorithms (e.g., XGBoost, Neural Networks).
- **Make it dynamic** by integrating **live game data for real-time predictions**.
- **Enhance feature engineering** with more advanced metrics.

## Installation & Usage
### Requirements
- Python 3.10+
- Required libraries: `pandas`, `scikit-learn`, `joblib`, `matplotlib`, `seaborn`

### Running the Project
1. **Prepare Data**:
   ```bash
   python data_prep.py
   ```
2. **Train the Model**:
   ```bash
   python model_training.py
   ```
3. **Make Predictions**:
   ```bash
   python model_prediction.py
   ```

---
## Contributors
- **Ryan Boubsil**  

**🚀 Thanks for checking out the NBA Score Prediction Model!**


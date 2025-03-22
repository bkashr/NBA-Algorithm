import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_absolute_error

# Load cleaned dataset
df = pd.read_csv("cleaned_nba_games_fixed.csv")

# Print initial dataset shape
print(f"Initial dataset shape: {df.shape}")

# Print column names
print("Columns in dataset:", df.columns.tolist())

# Check missing values
missing_values = df.isna().sum()
print("Missing values per column:\n", missing_values)

# Drop rows where the target column is missing
df = df.dropna(subset=['PTS'])  # Using 'PTS' instead of 'team_a_pts'
print(f"Dataset shape after dropping NaN target values: {df.shape}")

# Ensure target column exists
target_column = 'PTS'
if target_column not in df.columns:
    raise ValueError(f"Target column '{target_column}' not found in dataset!")

# Encode categorical columns
categorical_columns = ['TEAM_NAME', 'TEAM_NAME_opp']  # Adjusted for new dataset structure
label_encoders = {}

for col in categorical_columns:
    if col in df.columns:
        label_encoders[col] = LabelEncoder()
        df[col] = label_encoders[col].fit_transform(df[col])

# Define features (X) and target (y)
X = df.drop(columns=[target_column], errors='ignore')
y = df[target_column]

# Drop unnecessary columns safely
columns_to_drop = ['TEAM_ABBREVIATION', 'TEAM_ABBREVIATION_opp']
X = X.drop(columns=[col for col in columns_to_drop if col in X.columns])

# Ensure X is not empty
if X.shape[1] == 0:
    print("Columns in X after preprocessing:", X.columns.tolist())
    raise ValueError("Feature set X is empty after preprocessing! Check column selection.")

# Check data types
print(X.dtypes)
print(X.isnull().sum())  # Ensure no missing values

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print("Data split successfully!")

# Train a Random Forest Regressor
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

# Evaluate model performance
mae = mean_absolute_error(y_test, y_pred)
print(f"Mean Absolute Error: {mae:.4f}")

# Save model
joblib.dump(model, "nba_model.pkl")
print("Model saved successfully!")

# -*- coding: utf-8 -*-
"""water_prediction_model.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/10YcQ1TmdUVtvXXlAYZemRlK-KrhFmatV
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.impute import SimpleImputer

from google.colab import drive
drive.mount('/content/drive')

# Step 1: Data Preprocessing
# Load your dataset (replace 'your_dataset.csv' with the actual file path)
df = pd.read_csv('/content/feeds_data.csv')

print(df.head())

# Getting last 3 rows from df
df_last_3 = df.tail(3)

# Printing df_last_3
print(df_last_3)

# Handle missing values (if any)
# For simplicity, we'll fill missing values with the mean for numerical columns
df.fillna(df.mean(), inplace=True)

print(df.head())

df['created_at'] = pd.to_datetime(df['created_at'])

# Convert categorical variables to numerical using one-hot encoding
df = pd.get_dummies(df, columns=['Location', 'Type of Hydroponics System', 'plant type', 'crop stage'])

print(df.head())

# Drop columns that are not relevant for prediction (if any)
df = df.drop(['created_at','entry_id'], axis=1)

print(df.head())

from sklearn.preprocessing import StandardScaler

# Assuming X_train and X_test contain your feature data

# Standardize numerical variables (Temperature, Humidity, Heat index, pH Level)
scaler = StandardScaler()
df[['Temperature', 'Humidity', 'Heat index', 'pH Level of Nutrient Solution']] = scaler.fit_transform(df[['Temperature', 'Humidity', 'Heat index', 'pH Level of Nutrient Solution']])

print(df.head())

# Getting last 3 rows from df
df_last_3 = df.tail(3)

# Printing df_last_3
print(df_last_3)

# Assuming df is your DataFrame

# Check for missing values
missing_values = df['Water Usage(Litres)'].isna().sum()
print(f'Number of missing values in Water Usage: {missing_values}')

# Fill missing values with a default value (e.g., 0)
df['Water Usage(Litres)'].fillna(0, inplace=True)

# Check for missing values
missing_values = df['Temperature'].isna().sum()
print(f'Number of missing values in Temperature: {missing_values}')

# Fill missing values with a default value (e.g., 0)
df['Temperature'].fillna(0, inplace=True)

# Check for missing values
missing_values = df['Humidity'].isna().sum()
print(f'Number of missing values in Humidity: {missing_values}')

# Fill missing values with a default value (e.g., 0)
df['Humidity'].fillna(0, inplace=True)


# Check for missing values
missing_values = df['Heat index'].isna().sum()
print(f'Number of missing values in Heat index: {missing_values}')

# Fill missing values with a default value (e.g., 0)
df['Heat index'].fillna(0, inplace=True)


# Extract numerical value from 'Water Usage' column and convert to integer
#df['Water Usage'] = df['Water Usage'].str.extract('(\d+)').astype(int)

# Assuming df is your DataFrame

# Impute missing values in 'Heat index' with mean
imputer = SimpleImputer(strategy='mean')
df['Heat index'] = imputer.fit_transform(df[['Heat index']])

# Getting last 3 rows from df
df_last_3 = df.tail(3)

# Printing df_last_3
print(df_last_3)

# Impute missing values in Temperature, Humidity, and Heat index
imputer = SimpleImputer(strategy='mean')
df[['Temperature', 'Humidity', 'Heat index']] = imputer.fit_transform(df[['Temperature', 'Humidity', 'Heat index']])

# Split the dataset into features (X) and target variable (y)
X = df.drop(['Water Usage(Litres)'], axis=1)
y = df['Water Usage(Litres)']

# Getting last 3 rows from df
df_last_3 = df.tail(3)

# Printing df_last_3
print(df_last_3)

# Step 2: Feature Selection/Engineering
# In this example, we'll use all available features. You can perform more advanced feature selection/engineering as needed.

# Step 3: Data Splitting
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 4: Selecting a Model
model = LinearRegression()  # Linear Regression is chosen as an example. You can try different models.

# Step 5: Model Training
model.fit(X_train, y_train)

# Step 6: Model Evaluation
y_pred = model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f'Mean Absolute Error: {mae}')
print(f'Mean Squared Error: {mse}')
print(f'R-squared: {r2}')

train_score = model.score(X_train, y_train)
val_score = model.score(X_test, y_test)

print(f"Training R-squared: {train_score}")
print(f"Validation R-squared: {val_score}")

from sklearn.model_selection import cross_val_score

# Perform k-fold cross-validation
scores = cross_val_score(model, X, y, cv=5)  # 5-fold cross-validation
print(f"Cross-validated R-squared scores: {scores}")

import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import learning_curve

# Generate learning curves
train_sizes, train_scores, val_scores = learning_curve(model, X, y, cv=5)

# Plot learning curves
plt.plot(train_sizes, np.mean(train_scores, axis=1), label='Training score')
plt.plot(train_sizes, np.mean(val_scores, axis=1), label='Validation score')
plt.xlabel('Training examples')
plt.ylabel('R-squared')
plt.legend(loc='best')
plt.show()

from sklearn.linear_model import Ridge

# Use Ridge regression with regularization
ridge_model = Ridge(alpha=1.0)  # Adjust alpha as needed
ridge_model.fit(X_train, y_train)
ridge_train_score = ridge_model.score(X_train, y_train)
ridge_val_score = ridge_model.score(X_test, y_test)

print(f"Ridge Training R-squared: {ridge_train_score}")
print(f"Ridge Validation R-squared: {ridge_val_score}")

# Assuming 'model' is your trained Linear Regression model
coefficients = model.coef_
feature_names = X.columns

# Pair feature names with their coefficients
feature_coefficients = list(zip(feature_names, coefficients))

# Sort features by absolute coefficient value
feature_coefficients = sorted(feature_coefficients, key=lambda x: abs(x[1]), reverse=True)

# Print or inspect the most important features
print("Top Features and Their Coefficients:")
for feature, coefficient in feature_coefficients:
    print(f"{feature}: {coefficient}")

# Assuming you have a separate test set X_test and y_test
test_score = model.score(X_test, y_test)
print(f"Test R-squared: {test_score}")

# Getting last 3 rows from df
df_last_3 = df.tail(3)

# Printing df_last_3
print(df_last_3)

print(df.head(5))

# Assuming 'X_train' is your DataFrame used for training
features_used = X_train.columns.tolist()

print("Features used during training:")
for feature in features_used:
    print(feature)

import pandas as pd

# Assuming X_new is a DataFrame
X_new = pd.DataFrame({
    'Temperature': [25.0, 28.0, 30.0],
    'Humidity': [60, 65, 70],
    'Heat index': [27.0, 29.0, 32.0],
    'pH Level of Nutrient Solution': [6.5, 6.8, 7.0],
    'Electrical Conductivity (EC) of Nutrient Solution(mS/cm)': [1.2, 1.3, 1.4],
    'Number of Plants': [50, 50, 50],
    'Location_Greenhouse': [1, 0, 1],
    'Type of Hydroponics System_NFT': [1, 0, 1],
    'plant type_Lettuce':[0, 1, 0],
    'crop stage_germination': [0, 1, 0],
    'crop stage_ideal': [0, 1, 0],

    # Add other features as needed
})

# Now, you can use your trained model to make predictions
predictions = model.predict(X_new)

print(predictions)

y_train_pred = model.predict(X_train)
y_test_pred = model.predict(X_test)

# Step 3: Evaluate the model
train_mse = mean_squared_error(y_train, y_train_pred)
test_mse = mean_squared_error(y_test, y_test_pred)

print(f"Training Mean Squared Error: {train_mse}")
print(f"Testing Mean Squared Error: {test_mse}")

r_squared = r2_score(y_test, y_test_pred)

print(f"R-squared (coefficient of determination): {r_squared}")

print(len(y_test), len(predictions))
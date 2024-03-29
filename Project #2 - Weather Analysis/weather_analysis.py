# -*- coding: utf-8 -*-
"""Weather Analysis.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1jqqMz99t808xxpwiRD0SKZ_PyT6lHPOW
"""

from google.colab import files
upload = files.upload()

import pandas as pd
import seaborn as sns
from sklearn.impute import SimpleImputer
import matplotlib.pyplot as plt

import io

data = pd.read_csv(io.BytesIO(upload['weather.csv']))
data.head()

data.info()

data.isnull().sum()   #checking for null values or missing values

data.duplicated().sum() #checking for duplicated entries

#Clearing Missing Values for columns with string Datatype

mode_WindGustDir = data['WindGustDir'].mode()[0]
data['WindGustDir'].fillna(mode_WindGustDir, inplace=True)

mode_WindDir9am = data['WindDir9am'].mode()[0]
data['WindDir9am'].fillna(mode_WindDir9am, inplace=True)

mode_WindDir3pm = data['WindDir3pm'].mode()[0]
data['WindDir3pm'].fillna(mode_WindDir3pm, inplace=True)

# Clearing missing values in other columns

to_be_cleaned_columns = ['Sunshine', 'WindGustSpeed', 'WindSpeed9am']
imputer = SimpleImputer(strategy='mean')
data[to_be_cleaned_columns] = imputer.fit_transform(data[to_be_cleaned_columns])


data.isnull().sum()

data.to_csv('cleaned_data.csv', index=False)

data.info()

plt.figure(figsize=(12,10))
sns.heatmap(data.corr(), annot=True)

# @title Correlation and Regression Analysis Part

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

df = pd.read_csv('cleaned_data.csv')

df = pd.get_dummies(df, columns=['WindGustDir', 'WindDir9am', 'WindDir3pm'])

X = df.drop(['RainToday', 'RISK_MM', 'RainTomorrow'], axis=1)
y = df['RainToday']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LogisticRegression()

model.fit(X_train, y_train)
y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy: {accuracy:.2f}\n')

print('Classification Report:')
print(classification_report(y_test, y_pred))

df['RainTomorrow'] = df.apply(lambda row: 'Yes' if row['RISK_MM'] > 1 else row['RainToday'], axis=1)

print(df[['RainToday', 'RISK_MM', 'RainTomorrow']])
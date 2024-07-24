# -*- coding: utf-8 -*-
"""Predictive_Analysis_Diabetes.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/github/Shivamkrishna1913/Predictive_Analysis_Diabetes/blob/main/Predictive_Analysis_Diabetes.ipynb
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('diabetes.csv')

df.head()

df.columns

df.isnull().sum()

df.dtypes

df.info()

df.describe()

df.shape

"""

1.   Target value is given , therefore supervised machine learning.
2.   768 records

1.   Binary classification task



"""

df.corr()

"""OBSERVEATIONS:-

1.   NO 2 features are highly correlated.
2.   List item


"""

plt.figure(figsize=(15,15))
ax=sns.heatmap(df.corr(),annot=True)
plt.savefig('correlation-coefficient.jpg')
plt.show()

sns.distplot(df.Pregnancies)
print(df.Pregnancies.mode())

sns.displot(df.BloodPressure)
print(df.BloodPressure.mode())

sns.distplot(df.Insulin)
print(df.Insulin.mode())



# sns.distplot(df.Glucose)
# sns.distplot(df.SkinThickness)
# sns.distplot(df.BMI)
# sns.distplot(df.DiabetesPedigreeFunction)
sns.distplot(df.Age)

df['Insulin'] = df['Insulin'].replace(0, df['Insulin'].median())
df['Pregnancies'] = df['Pregnancies'].replace(0, df['Pregnancies'].median())
df['Glucose'] = df['Glucose'].replace(0, df['Glucose'].mean())
df['BloodPressure'] = df['BloodPressure'].replace(0, df['BloodPressure'].mean())
df['SkinThickness'] = df['SkinThickness'].replace(0, df['SkinThickness'].median())
df['BMI'] = df['BMI'].replace(0, df['BMI'].mean())
df['DiabetesPedigreeFunction'] = df['DiabetesPedigreeFunction'].replace(0, df['DiabetesPedigreeFunction'].median())
df['Age'] = df['Age'].replace(0, df['Age'].median())

sns.distplot(df.Pregnancies)
print(df.Pregnancies.mode())

"""separating dependent and independent features"""

x = df.iloc[:,:-1]
y = df.iloc[:,-1]

"""To detect the outliers---"""

fig,ax = plt.subplots(figsize=(15,5))
sns.boxplot(data = df,ax=ax)
plt.savefig('boxplot-Outliers.jpg')

"""# **OUTLIER REMOVAL::**"""

cols = ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age']
# mask = pd.Series(True, index=x.index)
for col in cols:
    Q1 = x[col].quantile(0.25)
    Q3 = x[col].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    # mask &= (x[col] >= lower_bound) & (x[col] <= upper_bound)
    mask = (x[col] >= lower_bound) & (x[col] <= upper_bound)

x_rem_out = x[mask]
y_rem_out = y[mask]

x_rem_out.shape

fig,ax = plt.subplots(figsize=(15,5))
sns.boxplot(data = x_rem_out,ax=ax)
plt.savefig('boxplot-Outliers.jpg')

"""STANDARDISATION

"""

from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
x_scaled = scaler.fit_transform(x_rem_out)

fig,ax = plt.subplots(figsize=(15,5))
sns.boxplot(data = x_scaled,ax=ax)
plt.savefig('boxplot-removed-outlier.jpg')

x_scaled = pd.DataFrame(x_scaled)
x_scaled.describe()

"""# **QUANTILE APPROACH:-**


1.   Resetting Indexes:
2.   Quantile-based Filtering:
3.   Visualization with Box Plot


"""

x_scaled.reset_index(drop = True,inplace=True)
y_rem_out.reset_index(drop = True,inplace=True)

x_scaled.columns = ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age']

q = x_scaled['Insulin'].quantile(0.95)
mask = x_scaled['Insulin']<q
datanew = x_scaled[mask]
y_rem_out = y_rem_out[mask]

fig,ax = plt.subplots(figsize=(15,5))
sns.boxplot(data = datanew,ax=ax)
plt.savefig('boxPlot-rem-out-qurtile-approach')

datanew.shape
y_rem_out.shape

"""# **Model Training**"""

from sklearn.model_selection import train_test_split
x_train,x_test,y_train,y_test = train_test_split(datanew,y_rem_out,test_size = 0.33,random_state=42)

x_train.shape

x_test.shape

print(y_train.value_counts())

"""HANDLING IMBALANCE DATA:"""

from imblearn.over_sampling import SMOTE
smote = SMOTE(random_state=42)
x_train_resampled,y_train_resampled = smote.fit_resample(x_train,y_train)

y_train_resampled.value_counts()

from imblearn.under_sampling import RandomUnderSampler
undersampler = RandomUnderSampler(random_state=42)
x_train_resampled2, y_train_resampled2 = undersampler.fit_resample(x_train, y_train)

y_train_resampled2.value_counts()

"""# **LOGISTIC REGRESSION**"""

from sklearn.linear_model import LogisticRegression
log_reg_model = LogisticRegression()
log_reg_model.fit(x_train_resampled,y_train_resampled)

"""**Model Predcitions**"""

y_pred = log_reg_model.predict(x_test)
print(y_pred)

"""#

**Model Evaluation**
"""

from sklearn.metrics import accuracy_score
accuracy_score(y_test, y_pred)

from sklearn.metrics import classification_report
target_names = ['Non-Diabetic', 'Diabetic']
print(classification_report(y_test, y_pred, target_names=target_names))

"""**saving the model**"""

import pickle as pk

pk.dump(log_reg_model,open('logistic_regression_model.pkl','wb'))

log_model = pk.load(open('logistic_regression_model.pkl','rb'))

log_model.predict(x_test)

x_train_resampled

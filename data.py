import pandas as pd
from sklearn.model_selection import train_test_split


df = pd.read_csv("heart_disease_data.csv")

x_features = df.drop(columns='target', axis = 1)
y_target = df['target']
train_x, test_x, train_y, test_y = train_test_split(x_features, y_target, test_size=0.2, stratify=y_target, random_state=2)

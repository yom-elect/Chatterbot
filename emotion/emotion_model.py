import pandas as pd
import numpy as np
import neattext.functions as nfx
import joblib

# Load ML Pkgs
# Estimators
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB

# Transformers
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split

# Build Pipeline
from sklearn.pipeline import Pipeline

# Load Dataset
df = pd.read_csv("data/emotion_dataset_raw.csv")

# User handles
df['Clean_Text'] = df['Text'].apply(nfx.remove_userhandles)

# Stopwords
df['Clean_Text'] = df['Clean_Text'].apply(nfx.remove_stopwords)

# Features & Labels
Xfeatures = df['Clean_Text']
ylabels = df['Emotion']

#  Split Data
x_train,x_test,y_train,y_test = train_test_split(Xfeatures,ylabels,test_size=0.3,random_state=42)

# LogisticRegression Pipeline
pipe_lr = Pipeline(steps=[('cv',CountVectorizer()),('lr',LogisticRegression())])

# Train and Fit Data
pipe_lr.fit(x_train,y_train)

# Make A Prediction
ex1 = "This book was so interesting it made me happy"

pipe_lr.predict([ex1])

# Save Model & Pipeline
pipeline_file = open("emotion_classifier_model_1.pkl","wb")
joblib.dump(pipe_lr,pipeline_file)
pipeline_file.close()
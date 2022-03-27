from unittest import result
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



cv= CountVectorizer()

def process_dataset(type):
    # Load Dataset
    df = pd.read_csv("emotion/data/emotion_dataset_raw.csv")

    # User handles
    df['Clean_Text'] = df['Text'].apply(nfx.remove_userhandles)

    # Stopwords
    df['Clean_Text'] = df['Clean_Text'].apply(nfx.remove_stopwords)

    # Punctuations
    df['Clean_Text'] = df['Clean_Text'].apply(nfx.remove_punctuations)

    # Features & Labels
    Xfeatures = df['Clean_Text']
    ylabels = df['Emotion']


    if (type== "logistic"):
        return train_test_split(Xfeatures,ylabels,test_size=0.2,random_state=42)
    else:
        X = cv.fit_transform(Xfeatures)
        return train_test_split(X,ylabels,test_size=0.2,random_state=42)
    

def train_emotion_model_logistic_reg():
    x_train, _ , y_train, _ = process_dataset("logistic")
    # LogisticRegression Pipeline
    pipe_lr = Pipeline(steps=[('cv',CountVectorizer()),('lr',LogisticRegression())])

    # Train and Fit Data
    pipe_lr.fit(x_train,y_train)

    # Save Model & Pipeline
    pipeline_file = open("emotion/emotion_classifier_model_1.pkl","wb")
    joblib.dump(pipe_lr,pipeline_file)
    pipeline_file.close()

    return pipe_lr

def train_emotion_model_nv_model():
    x_train, _ , y_train, _ = process_dataset("naive")
    
    nv_model = MultinomialNB()
    # Train and Fit Data
    nv_model.fit(x_train,y_train)

    # Save Model & Pipeline
    pipeline_file = open("emotion/emotion_nv_classifier_model_1.pkl","wb")
    joblib.dump(nv_model,pipeline_file)
    pipeline_file.close()

    return nv_model 

# Fxn
def predict_nv_emotion(model, docx):
    vect = cv.transform([docx]).toarray()
    results = model.predict(vect)

    return results[0]

def get_nv_prediction_proba(model, docx):
    vect = cv.transform([docx]).toarray()
    results = model.predict_proba(vect)
    return np.max(results)

def predict_linear_emotions(model, docx):
	results = model.predict([docx])
	return results[0]

def get_linear_prediction_proba(model, docx):
    results = model.predict_proba([docx])
    return np.max(results)

def best_prediction(userResponse):
    try:
        pipe_lr = joblib.load("emotion/emotion_classifier_model_1.pkl")
        nv_model = joblib.load("emotion/emotion_nv_classifier_model_1.pkl")

        if(get_linear_prediction_proba(pipe_lr, userResponse) >  get_nv_prediction_proba(nv_model, userResponse)):
            return predict_linear_emotions(pipe_lr, userResponse)
        else:
            return predict_nv_emotion(nv_model, userResponse)
    except:
        pipe_lr = train_emotion_model_logistic_reg()
        nv_model = train_emotion_model_nv_model()

        if(get_linear_prediction_proba(pipe_lr, userResponse) >  get_nv_prediction_proba(nv_model, userResponse)):
            return predict_linear_emotions(pipe_lr, userResponse)
        else:
            return predict_nv_emotion(nv_model, userResponse)


def predict_emotion(userResponse):
    return best_prediction(userResponse)

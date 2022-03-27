import random
import nltk
nltk.download('punkt')
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()
import numpy as np

import intent.conversations_model as cm
from emotion.emotion_model import predict_emotion

def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]

    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    for se in s_words:
        for i , w in enumerate(words):
            if w == se:
                bag[i] = 1
    
    return np.array(bag)

def get_bot_response(userInput):
    data = cm.read_intents()
    result = cm.process_intent_data()
    model = cm.conversation_model(result["training"], result["output"])
    
    res = model.predict([bag_of_words(userInput, result["words"])])[0]
    res_index = np.argmax(res)
    tag = result["labels"][res_index]

    if res[res_index] > 0.75:   
        for tg in data["intents"]:
            if tg['tag'] == tag:
                responses = tg['responses']
        # print(predict_emotion(userInput))
        return random.choice(responses)
    else:
        # print(predict_emotion(userInput), "=================")
        return "I didnt get that , try again"      

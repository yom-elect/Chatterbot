import random
from re import search
import nltk
nltk.download('punkt')
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()
import numpy as np

import intent.conversations_model as cm
from emotion.emotion_model import predict_emotion
from utils.track_respose import bot_question

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
    data = cm.read_intents() #get intents
    result = cm.process_intent_data()
    model = cm.conversation_model(result["training"], result["output"])
    bot_response = {}
    
    res = model.predict([bag_of_words(userInput, result["words"])])[0]
    res_index = np.argmax(res)
    tag = result["labels"][res_index]
    if res[res_index] > 0.25:   
        for tg in data["intents"]:
            if tg['tag'] == tag:
                responses = tg['responses']
       
        user_emotion = predict_emotion(userInput)
        (bot_ask, stat) = bot_question(tag, user_emotion)
        if (tag == "diagnosis"):
            if (stat == 5 or stat == 3):
                bot_response["bot_response"] = responses[0]
            elif (stat == 2 or stat == 4):
                bot_response["bot_response"] = responses[1]
            else:
                bot_response["bot_response"] = responses[2]
        else:
            bot_response["bot_response"] = random.choice(responses)
        if search('https', bot_ask):
            bot_response["play_video"] = bot_ask
        else:
            bot_response["bot_question"] = bot_ask
        return bot_response
    else:
        user_emotion = predict_emotion(userInput)
        bot_ask = bot_question('uncertain', user_emotion)
        bot_response["bot_response"] = "I didnt get that , try again"
        bot_response["bot_question"] = bot_ask

        return bot_response


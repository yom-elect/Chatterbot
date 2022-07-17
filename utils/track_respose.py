import csv
import random
from utils.questions_bank import questions

result = []

def reset_state():
    return result.clear()

def bot_question(tag, emotion):
    asides= ["greeting","goodbye","age","name", 'uncertain']
    result_index = len(result)
    next_index = result_index + 1


    if tag == 'goodbye':
        reset_state()

    if(tag in asides):
        try:
            return (questions[result_index]["all"], 0)
        except:
            valid_emotion = validate_emotion(emotion)
            return (questions[result_index][valid_emotion], 0)       

    if (result_index == 0):
        norm_emotion = normalize_emotion(emotion)
        result.append(norm_emotion)
        try:
            emotion_stat = round(sum(result) / len(result))
            return (questions[next_index]["all"], emotion_stat)
        except:
            valid_emotion = validate_emotion(emotion)
            emotion_stat = round(sum(result) / len(result))
            return (questions[next_index][valid_emotion], emotion_stat)
    elif (result_index < 10):
        try:
            norm_emotion = normalize_emotion(emotion)
            result.append(norm_emotion)
            emotion_stat = round(sum(result) / len(result))
            return (questions[next_index]["all"], emotion_stat)
        except:
            norm_emotion = normalize_emotion(emotion)
            result.append(norm_emotion)
            valid_emotion = validate_emotion(emotion)
            emotion_stat = round(sum(result) / len(result))
            return (questions[next_index][valid_emotion], emotion_stat)  
    elif (result_index >= 9 or tag == "Play_ Music"):
        emotion_songs = []
        emotion_stat = round(sum(result) / len(result))
        with open("music/Music_score.csv") as file:
            csv_reader = csv.reader(file)
            headings =next(csv_reader)
            for music in csv_reader:
                if (int(music[2]) == emotion_stat):
                    emotion_songs.append(music[1])
        return (random.choice(emotion_songs), emotion_stat)

def normalize_emotion(emotion):
    if (emotion == 'joy'): return 5
    if (emotion == 'neutral'): return 3
    if (emotion == 'depressed'): return 4
    if (emotion == 'sadness'): return 2
    if (emotion == 'anger'): return 1

def validate_emotion(emotion):
    if (emotion == "neutral" or emotion == "surprise"): emotion = "joy"
    if (emotion == "shame"): emotion = "sadness"
    if (emotion == "disgust"): emotion = "anger"
    return emotion
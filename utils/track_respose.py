import csv
import random
from utils.questions_bank import questions

result = []

def bot_question(tag, emotion):
    asides= ["greeting","goodbye","age","name", 'uncertain']
    result_index = len(result)
    next_index = result_index + 1

    if(tag in asides):
        try:
            return questions[result_index]["all"]
        except:
            valid_emotion = validate_emotion(emotion)
            return questions[result_index][valid_emotion]       

    if (result_index == 0):
        norm_emotion = normalize_emotion(emotion)
        result.append(norm_emotion)
        try:
            return questions[next_index]["all"]
        except:
            valid_emotion = validate_emotion(emotion)
            return questions[next_index][valid_emotion]
    elif (result_index < 10):
        try:
            norm_emotion = normalize_emotion(emotion)
            result.append(norm_emotion)
            return questions[next_index]["all"]
        except:
            norm_emotion = normalize_emotion(emotion)
            result.append(norm_emotion)
            valid_emotion = validate_emotion(emotion)
            return questions[next_index][valid_emotion]  
    elif (result_index >= 9 or tag == "Play_ Music"):
        emotion_songs = []
        emotion_stat = round(sum(result) / len(result))
        with open("music/Music_score.csv") as file:
            csv_reader = csv.reader(file)
            headings =next(csv_reader)
            for music in csv_reader:
                if (int(music[2]) == emotion_stat):
                    emotion_songs.append(music[1])
        return random.choice(emotion_songs)

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
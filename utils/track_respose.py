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
            if (emotion == "neutral"): emotion = "joy"
            return questions[result_index][emotion]       

    if (result_index == 0):
        result.append(emotion)
        try:
            return questions[result_index]["all"]
        except:
            if (emotion == "neutral"): emotion = "joy"
            return questions[result_index][emotion]
    elif (result_index < 10):
        try:
            result.append(emotion)
            return questions[next_index]["all"]
        except:
            result.append(emotion)
            if (emotion == "neutral"): emotion = "joy"
            return questions[next_index][emotion]   
    elif (result_index >= 10):
        return "music time"

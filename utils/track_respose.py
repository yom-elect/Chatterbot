from utils.questions_bank import questions

result = []

def bot_question(tag, emotion):
    asides= ["greeting","goodbye","age","name", 'uncertain']
    result_index = len(result)
    next_index = result_index + 1

    if(tag in asides):
        if (questions[result_index]["all"]):
            return questions[result_index]["all"]
        else:
            if (emotion == "neutral"): emotion = "joy"
            return questions[result_index][emotion]

    if (result_index == 0):
        result.append(emotion)
        return questions[next_index]["all"]
    elif (result_index < 10):
        if (questions[next_index]["all"]):
            result.append(emotion)
            return questions[next_index]["all"]
        else:
            result.append(emotion)
            if (emotion == "neutral"): emotion = "joy"
            return questions[next_index][emotion]
    elif (result_index >= 10):
        return "music time"

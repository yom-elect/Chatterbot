import os
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer, ChatterBotCorpusTrainer
from flask import Flask, render_template, request
from flask.helpers import safe_join

app = Flask(__name__)
static = safe_join(os.path.dirname(__file__), 'static')

bot = ChatBot("chatbot", read_only=False, 
    logic_adapters=[
        
        {
            "import_path":"chatterbot.logic.BestMatch",
            "default_response": "Sorry I dont have an answer",
            "maximum_similarity_threshold": 0.9
        }
        
    ])

trainer = ChatterBotCorpusTrainer(bot)
trainer.train("chatterbot.corpus.english")

# list_to_train = [
#     "hi",
#     "hi there",
#     "what's your name?",
#     "I'm a chatbot",
#     "how old are you?",
#     "I'm ageless!"
# ]


# list_to_train2 = [
#     "hi",
#     "Hello Friend",
#     "what's your name?",
#     "My Name is tixton",
#     "how old are you?",
#     "I'm  about 8years old"
# ]

# list_trainer = ListTrainer(bot)

# list_trainer.train(list_to_train)
# list_trainer.train(list_to_train2)

# user_response = input("User: ")

# bot_response = bot.get_response(user_response)

# print("Bot: ", bot_response)

@app.route("/")
def main():
    return render_template("index.html")

@app.route("/get")
def get_chatbot_response():
    userText = request.args.get('userMessage')
    botResponse = str(bot.get_response(userText))
    return botResponse


if __name__ == "__main__":
    app.run(debug=True)
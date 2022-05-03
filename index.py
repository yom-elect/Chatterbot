import os
from flask import Flask, render_template, request
from flask.helpers import safe_join

from intent.model import get_bot_response


app = Flask(__name__)
static = safe_join(os.path.dirname(__file__), 'static')


@app.route("/")
def main():
    return render_template("index.html")

@app.route("/get")
def get_chatbot_response():
    userText = request.args.get('userMessage')
    botResponse = get_bot_response(userText)

    return botResponse
    

if __name__ == "__main__":
    app.run(ssl_context='adhoc')

# print("Start talking with the bot! type quit to stop")
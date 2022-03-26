import os
from flask import Flask, render_template, request, Response
from flask.helpers import safe_join
from boto3 import Session
import base64


from intent.model import get_bot_response


app = Flask(__name__)
static = safe_join(os.path.dirname(__file__), 'static')

session = Session(profile_name="playht-test", region_name="us-east-1")
polly = session.client("polly")

# polly_client = boto3.Session(
#                 aws_access_key_id=,                     
#     aws_secret_access_key=,
#     region_name='us-west-2').client('polly')

@app.route("/")
def main():
    return render_template("index.html")

@app.route("/get")
def get_chatbot_response():
    userText = request.args.get('userMessage')
    botResponse = str(get_bot_response(userText))
    buffer = polly.synthesize_speech(Text=botResponse, OutputFormat="mp3",
                                        VoiceId="Joanna")
    buffer["botResponse"] = botResponse
    return  Response(buffer["AudioStream"],
                    mimetype='multipart/x-mixed-replace; boundary=frame')
    
    


if __name__ == "__main__":
    app.run(debug=True)

# print("Start talking with the bot! type quit to stop")
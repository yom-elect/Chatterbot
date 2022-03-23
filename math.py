from chatterbot import ChatBot

bot = ChatBot("Math", logic_adapters=["chatterbot.logic.MathematicalEvaluation"])

print("--------- Math Chatbot -----------")

user_response = input("type the equation to be solved: ")
bot_response = bot.get_response(user_response)
print("Bot: ", str(bot_response))
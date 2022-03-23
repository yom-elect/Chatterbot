from chatterbot import ChatBot

bots = ChatBot("units", logic_adapters=['chatterbot.logic.UnitConversion'])

user_response = input("Ask a question (unit conversion): ")
bot_response = bots.get_response(user_response)
print("bot: ", str(bot_response))
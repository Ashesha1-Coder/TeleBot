import os
import telepot
from flask import Flask, request
from telegram_bot import CommandReceiveView

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the token from environment variables
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')



# Debug print statements
print("Script started")
print(f"Token defined: {TOKEN}")

# Initialize the bot with the token
TelegramBot = telepot.Bot(TOKEN)

app = Flask(__name__)

@app.route("/")
def welcome():
    return "hello world"

@app.route("/home")
def home():
    return "This is home page"

@app.route("/telegram/<bot_token>", methods=['POST'])
def telegram(bot_token):
    view = CommandReceiveView.as_view('command_receive_view')
    return view(request, bot_token)

if __name__ == "__main__":
    from controller import user_signup  # Ensure other routes are imported if needed
    app.run(debug=True)

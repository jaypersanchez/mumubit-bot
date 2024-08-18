from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import datetime

# Token from BotFather
TOKEN = '7210118618:AAFVBb97mo6nlPTVO9nlnTr8BSRcUd4zfjA'

# Initialize bot and updater
bot = Bot(TOKEN)
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

# Dictionary to keep track of user message times
user_last_message_time = {}

def check_spam(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    chat_id = update.message.chat.id
    current_time = datetime.datetime.now()

    # Check the last message time and compare
    if user_id in user_last_message_time:
        last_message_time = user_last_message_time[user_id]
        time_difference = (current_time - last_message_time).total_seconds()
        if time_difference < 5:  # Less than 5 seconds between messages
            # Remove user from chat (kick)
            try:
                bot.kick_chat_member(chat_id, user_id)
                print(f"User {user_id} kicked for spamming.")
            except Exception as e:
                print(f"Failed to kick user {user_id}: {str(e)}")
            finally:
                # Optionally, you can also unban the user if you just want to remove them temporarily
                bot.unban_chat_member(chat_id, user_id)
        else:
            # Update the last message time if not spamming
            user_last_message_time[user_id] = current_time
    else:
        # If no previous record, just log the time
        user_last_message_time[user_id] = current_time

def testbot(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="ping")


# Handler for all text messages
testbot_handler = CommandHandler('testbot', testbot)
message_handler = MessageHandler(Filters.text & (~Filters.command), check_spam)
dispatcher.add_handler(message_handler)

# Command handler to start the bot
def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hello, I am your anti-spam bot. I monitor your messages!")

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

# Start the bot
updater.start_polling()
updater.idle()

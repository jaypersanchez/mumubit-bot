from dotenv import load_dotenv
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackContext
from telegram.ext.filters import MessageFilter
from telegram.ext import filters, CallbackQueryHandler
import re
import tweepy
from faqs import faqs

# Access Twitter credentials from environment variables
api_key = os.getenv('TWITTER_API_KEY')
api_secret = os.getenv('TWITTER_API_SECRET')
access_token = os.getenv('TWITTER_ACCESS_TOKEN')
access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')

# Twitter authentication
auth = tweepy.OAuthHandler(api_key, api_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# Command Handlers
async def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start_mumubit is issued with an inline keyboard."""
    keyboard = [
        [InlineKeyboardButton("About Nodes", callback_data='nodes')],
        [InlineKeyboardButton("Investment Options", callback_data='investment')],
        [InlineKeyboardButton("FAQ", callback_data='faq')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Welcome! How can I assist you today? Choose an option below:', reply_markup=reply_markup)

async def button(update: Update, context: CallbackContext) -> None:
    """Handle button presses from the inline keyboard."""
    query = update.callback_query
    query.answer()
    # Retrieve the full FAQ response based on the button pressed
    data = query.data
    response = faqs[data]['response']  # Use callback_data as the key to fetch the full response
    await query.edit_message_text(text=response)


async def faq(update: Update, context: CallbackContext) -> None:
    """Respond to the /faq_mumubit command with an answer from the FAQs."""
    question = ' '.join(context.args).lower()

    if not question:
        await update.message.reply_text("Please ask a question after the command. For example, '/faq_mumubit how to invest'.")
        return

    answer = next((info['response'] for key, info in faqs.items() if any(keyword in question for keyword in info['keywords'])), None)
    if answer:
        await update.message.reply_text(answer)
    else:
        await update.message.reply_text("Sorry, I couldn't find an answer to your question. Please check your input or try asking something else.")

def get_faq_keyboard():
    """Generate an inline keyboard with FAQ topics."""
    keyboard = []
    for key, value in faqs.items():
        # Each button in the inline keyboard corresponds to an FAQ entry
        keyboard.append([InlineKeyboardButton(value['response'][:40] + "...", callback_data=key)])
    return InlineKeyboardMarkup(keyboard)


def get_faq_keyboard():
    """Generate an inline keyboard with FAQ topics."""
    keyboard = []
    for key, value in faqs.items():
        # Each button in the inline keyboard corresponds to an FAQ entry
        keyboard.append([InlineKeyboardButton(value['response'][:40] + "...", callback_data=key)])
    return InlineKeyboardMarkup(keyboard)

def is_question(text):
    # Pattern to find sentence starts with a question word followed by any word until end of sentence or a punctuation
    pattern = r'\b(who|what|when|where|why|how|do|does|can|could|would|should|is|are|will)\b.*[\?\.\!]?'
    if re.search(pattern, text, re.I):  # re.I makes the search case-insensitive
        return True
    return False

async def process_question(update: Update, context: CallbackContext) -> None:
    """Automatically respond to questions posted in the chat if they seem like FAQs."""
    text = update.message.text.lower()
    if is_question(text):
        # Check if the text contains keywords that match FAQs
        matched_response = None
        for key, value in faqs.items():
            if any(keyword in text for keyword in value['keywords']):
                matched_response = value['response']
                break

        # Respond with the matched answer or a default message
        if matched_response:
            await update.message.reply_text(matched_response)
        else:
            await update.message.reply_text("I'm sorry, I couldn't find a specific answer to your question. Please see the topics below for more information:")

        # Provide additional FAQ topics as buttons regardless of whether a direct answer was found
        reply_markup = get_faq_keyboard()
        await update.message.reply_text("You can also explore the following FAQ topics:", reply_markup=reply_markup)
    else:
        await update.message.reply_text("Hello! How can I assist you today? Feel free to ask any questions.")


def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    load_dotenv()
    TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    application = Application.builder().token(TOKEN).build()

    # twitter test
    api.update_status("Hello from Mumubot!")
    
    # Adding handlers
    #application.add_handler(CommandHandler("start_mumubit", start))
    #application.add_handler(CommandHandler("faq_mumubit", faq))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), process_question))
    application.add_handler(CallbackQueryHandler(button))
    print("MumuBot started")
    # Start the application
    application.run_polling()
    

if __name__ == '__main__':
    main()

from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, CallbackContext, Application

faqs = {
    "registration": {
        "keywords": ["registration", "register", "signup", "sign up"],
        "response": "To register, please visit our website and follow the instructions."
    },
    "investment": {
        "keywords": ["invest", "investment", "how to invest", "investing"],
        "response": "You can invest in Mumubit by purchasing nodes. For more details, visit our investment page or check out our node sales."
    },
    "nodes": {
        "keywords": ["nodes", "node sale", "what are nodes", "benefits of nodes"],
        "response": "Nodes represent different identities within our Builder system. Validators, Influencers, and Contributors play different roles in our ecosystem, offering various benefits including minting MCTP tokens and earning from ecosystem projects."
    },
    "staking": {
        "keywords": ["staking", "how to stake", "staking details", "how to earn", "earn"],
        "response": "Staking requires holding a certain number of MCTP tokens and locks them for a period to support network operations. Rewards include income from DEX earnings and other ecosystem projects."
    },
    "partnerships": {
        "keywords": ["partnerships", "partners", "collaborations", "reputable partners"],
        "response": "Mumubit has partnered with several industry leaders like Polygon and Metis, as well as with various IDO platforms like Enjinstarter."
    },
    "community": {
        "keywords": ["community", "importance of community", "community role"],
        "response": "Community is crucial to Mumubit. Our Builder program allows community members to engage as nodes, contributing to and benefiting from the platform’s growth."
    },
    "future plans": {
        "keywords": ["future plans", "upcoming", "what to expect"],
        "response": "We plan to release several games through our Builder program in 2024 and launch our DEX to support liquidity for MCTP and other project tokens."
    },
    "mumubit": {
        "keywords": ["what is mumubit", "about mumubit", "mumubit information"],
        "response": "Mumubit is an IDO and web3 project launch platform that supports third-party projects and releases ecosystem projects through our Builder system."
    }
}


async def faq(update: Update, context: CallbackContext) -> None:
    """Respond to the /faq_mumubit command with an answer from the FAQs."""
    question = ' '.join(context.args).lower()

    if not question:
        await update.message.reply_text("Please ask a question after the command. For example, '/faq_mumubit how to invest'.")
        return

    # Find a matching answer using enhanced keyword search
    answer = None
    for topic, info in faqs.items():
        if any(keyword in question for keyword in info['keywords']):
            answer = info['response']
            break

    if answer:
        await update.message.reply_text(answer)
    else:
        await update.message.reply_text("Sorry, I couldn't find an answer to your question. Please check your input or try asking something else.")

# Define your command handlers
async def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start_mumubit is issued."""
    await update.message.reply_text('Hello! I am MumuBot. How can I help you?')

async def test(update: Update, context: CallbackContext) -> None:
    """Respond to the /test_mumubit command."""
    await update.message.reply_text('MumuBot is alive!')

def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    TOKEN = '7210118618:AAFVBb97mo6nlPTVO9nlnTr8BSRcUd4zfjA'
    application = Application.builder().token(TOKEN).build()

    # Adding handlers
    application.add_handler(CommandHandler("start_mumubit", start))
    application.add_handler(CommandHandler("test_mumubit", test))
    application.add_handler(CommandHandler("faq_mumubit", faq))
    
    # Start the application
    application.run_polling()

if __name__ == '__main__':
    main()

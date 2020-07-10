import telegram
# from telebot.credentials import bot_token, bot_username, URL
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, ConversationHandler)

TOKEN = "1167359926:AAEl5xxn1enjFpmygGD7wEY9M0hQvU4uR-M"
USERNAME = "t.me/RedBlack_Wholesome_Bot"

players = [] # List of players in the current game

## Define callbacks for functions

def begin(update, context):
    # Send a message when the /start command is issued
    update.message.reply_text("The Red Black Game has started! Keep it wholesome :)")

def join(update, context):
    # Lets player join the Red Black Game
    newPlayer = update.message.from_user.username
    players.append(newPlayer)
    update.message.reply_text("%s has joined the game!" %(newPlayer))

def returnPlayers(update, context):
    playerList = "The current players are:\n"
    for x in players:
        playerList += x + "\n"
    update.message.reply_text(playerList)

# def question(update, context):
#     question = ["Red", "Black"]
#     message = context.bot.send_poll(update.effective_user.id, "How are you?", question,
#                                     is_anonymous=False, allows_multiple_answers=True)

#     # Save some info about the poll the bot_data for later use in receive_poll_answer
#     payload = {message.poll.id: {"questions": question, "message_id": message.message_id,
#                                  "chat_id": update.effective_chat.id, "answers": 0}}

#     context.bot_data.update(payload)

# def vote(update, context):
#     pass


# State machine for the bot
state = ("Init", "Sort", "Queue", "Question", "RedBlack", "DisplayResults", "Vote", "Reveal")
statePtr = 0
# The internal state of the bot. Iterate through the state.

def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    print("Starting bot!")

    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("begin", begin))
    dp.add_handler(CommandHandler("players", returnPlayers))
    dp.add_handler(CommandHandler("join", join))

    
    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()
    

if __name__ == '__main__':
    main()
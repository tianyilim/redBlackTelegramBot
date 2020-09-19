import telegram
import time
import random
# from telebot.credentials import bot_token, bot_username, URL
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, ConversationHandler)

TOKEN = "" # Your token here
USERNAME = "t.me/RedBlack_Wholesome_Bot"

players = [] # Set of players in the current game
playerIt = 0

START, QUESTION, ECHO = range(3)

# State machine
def start(update, context):
    update.message.reply_text("%s has started the game, and will be added to the player list." %(update.message.from_user.username))
    players.append(update.message.from_user.username)

    # reply_keyboard = [['Yes', 'No']]

    # update.message.reply_text(
    #     'Lolol123 yes or no',
    #     reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return QUESTION

def question(update, context):
    global playerIt # Treat with caution. Declares the player iterator variable as global

    if len(players) != 0:
        currPlayer = players[playerIt]
    else:
        print("No players in the game.")
    update.message.reply_text("%s, please ask a question by replying to me." %(currPlayer))

    playerIt += 1
    if playerIt >= len(players):
        playerIt = 0
    
    print("playerIt is currently:", playerIt)

    return ECHO

def echo(update, context):
    user = update.message.from_user
    update.message.reply_text('%s said \"%s\".' %(user.username, update.message.text),
                              reply_markup=ReplyKeyboardRemove() )

    if update.message.text=="/random@redBlack_Wholesome_bot" or update.message.text=="random":
        print("random1")
    
    return QUESTION

def reply(update, context):
    update.message.reply_text("uwu %s senpai noticed me?!" %(update.message.from_user.username))
    if update.message.from_user.username not in players:
        update.message.reply_text("%s, would you like to join the game?" %(update.message.from_user.username))
    return ECHO

# Helper functions
def join(update, context):
    # Lets player join the Red Black Game
    newPlayer = update.message.from_user.username
    if newPlayer not in players:
        players.append(newPlayer)
        update.message.reply_text("%s has joined the game!" %(newPlayer))
    else:
        print("Player already in the game!")
        update.message.reply_text("%s tried to join, but is already in the game!" %(newPlayer))
    

def returnPlayers(update, context):
    playerList = "The current players are:\n"
    for x in players:
        playerList += x + "\n"
    update.message.reply_text(playerList)

def cancel(update, context):
    players.clear()
    update.message.reply_text("The Red Black game has ended. Hope you had fun!",
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END

def main():
    print("Starting bot!")

    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher # Get the dispatcher to register handlers

    dp.add_handler(CommandHandler("players", returnPlayers))
    dp.add_handler(CommandHandler("join", join))
    dp.add_handler(CommandHandler("stop", cancel))

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            QUESTION : [MessageHandler(Filters.reply, question)],
            ECHO: [MessageHandler(Filters.text, echo)],
        },

        fallbacks=[CommandHandler('stop', cancel)]
    )

    dp.add_handler(conv_handler)

    # Start the bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

    print("Stopping bot!")

if __name__ == '__main__':
    main()
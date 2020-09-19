import telegram
import time
import random
# from telebot.credentials import bot_token, bot_username, URL
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, ConversationHandler)

TOKEN = "" # Your token here
USERNAME = "t.me/RedBlack_Wholesome_Bot"

QUESTION, REDBLACK, REDBLACK_REVEAL, VOTE_PLAYER, PLAYER_REVEAL, VOTE_COLOR, COLOR_REVEAL = range(7)

players = [] # List of players in the current game
queueIt = 0 # Queue Iterator
redVotes = 0  # number of red votes
blackVotes = 0 # number of black votes
tries = [0, True] # Tries for voting

## Define callbacks for functions

def begin(update, context):
    # Send a message when the /start command is issued
    update.message.reply_text("The Red Black Game has started! Keep it wholesome :)")

    return QUESTION

def question(update, context):
    # Goes down the queue of players and lets the player at the top of the queue ask a qn
    currPlayer = players[queueIt] # TODO where to define this?

    # currPlayer asks a question to the group.
    update.message.reply_text("%s, it is your turn to ask a question! Reply to this message when you've thought of a suitable one!" %(currPlayer))

    # TODO Wait for response
    queueIt += 1
    if queueIt > len(players):
        queueIt = 0

    return REDBLACK

def redBlack(update, context):
    # Voting time! Red or Black? :P
    red_black_poll = ["Red", "Black"]
    
    message = context.bot.send_poll(update.effective_user.id, "Red or Black?\nRemember Red is Yes, and Black is No!", red_black_poll,
                                    is_anonymous=False, allows_multiple_answers=True)

    # DEBUG
    update.message.reply_text("The total number of voters is %d." %(len(players)))

    # Save some info about the poll the bot_data for later use in receive_poll_answer
    payload = {message.poll.id: {"red_black": red_black_poll, "message_id": message.message_id,
                                 "chat_id": update.effective_chat.id, "answers": 0}}

    context.bot_data.update(payload)

    # wait for 30s before transitioning, or after everyone has responded.
    now = time.time()
    messageSent = [True, True] # Keep track...
    while now < 30:
        now = time.time()

        if now > 20 and messageSent[0]:
            update.message.reply_text("10s more to answer!")
            messageSent[0] = False
        elif now > 10 and messageSent[1]:
            update.message.reply_text("20s more to answer!")
            messageSent[1] = False
        
        # TODO break if everyone answers
        if update.poll.total_voter_count == len(players):
            update.message.reply_text("Everyone has answered!")
            break
    
    update.message.reply_text("Poll closed!")

    return REDBLACK_REVEAL

def redblack_reveal(update, context):

    # Display results of poll
    update.message.reply_text("The results are in!\nRed: %d votes.\nBlack: %d votes." %(redVotes, blackVotes))
    update.message.reply_text("Now, the fun part! Who do you think voted what?")

    return VOTE_PLAYER

def vote_player(update, context):
    # Displays the results of the poll.
    if redVotes == blackVotes:
        # Need to vote on to decide on red or black.
        update.message.reply_text("As the number of red and black votes is the same, an additional round of voting will be held to see which color is to be revealed.")
        return VOTE_COLOR
    else:
        if redVotes > blackVotes:
            if tries[1]:
                tries[0] = redVotes + 1 # Set tries flag, now we are in this mode.
                tries[1] = False
            update.message.reply_text("Red votes were higher than black votes. You have %d to vote for people you think voted red!" %(redVotes+1))
        else:
            if tries[1]:
                tries[0] = blackVotes + 1
                tries[1] = False
            update.message.reply_text("Black votes were higher than red votes. You have %d to vote for people you think voted black!" %(blackVotes+1))
    
    update.message.reply_text("Voting starts now! If there's a tie, *all* tied participants will be revealed!")
    update.message.reply_text("_This was totally not because the dev was lazy._")

    # TODO Another round of voting
    message = context.bot.send_poll(update.effective_user.id, "Who do you guess?", players,
                                    is_anonymous=False, allows_multiple_answers=True)

    # Save some info about the poll the bot_data for later use in receive_poll_answer
    payload = {message.poll.id: {"players": players, "message_id": message.message_id,
                                 "chat_id": update.effective_chat.id, "answers": 0}}

    context.bot_data.update(payload)

    # wait for 30s before transitioning, or after everyone has responded.
    now = time.time()
    messageSent = [True, True] # Keep track...
    while now < 30:
        now = time.time()

        if now > 20 and messageSent[0]:
            update.message.reply_text("10s more to answer!")
            messageSent[0] = False
        elif now > 10 and messageSent[1]:
            update.message.reply_text("20s more to answer!")
            messageSent[1] = False
        
        # TODO break if everyone answers
        if update.poll.total_voter_count == len(players):
            update.message.reply_text("Everyone has answered!")
            break
    
    update.message.reply_text("Poll closed!")

    return PLAYER_REVEAL

def player_reveal(update, context):
    update.message.reply_text("The player voting results are in!")
    # Reveal if the player was indeed chosen
    # Reduce the number of tries
    

    # Count number of votes for the certain player.
    # See how it's done.
    # Reveal all players if there's a tie! And reduce tries by that number! :P
    tries[0] -= 1

    if tries[0] == 0:
        tries[1] = True # Reset tries flag.
        return QUESTION
    else:
        return VOTE_PLAYER

def vote_color(update, context):
    update.message.reply_text("Vote for the color you'd like to reveal the answer to.")

    # wait for 30s before transitioning, or after everyone has responded.
    now = time.time()
    messageSent = [True, True] # Keep track...
    while now < 30:
        now = time.time()

        if now > 20 and messageSent[0]:
            update.message.reply_text("10s more to answer!")
            messageSent[0] = False
        elif now > 10 and messageSent[1]:
            update.message.reply_text("20s more to answer!")
            messageSent[1] = False
        
        # TODO break if everyone answers
        if update.poll.total_voter_count == len(players):
            update.message.reply_text("Everyone has answered!")
            break
    
    update.message.reply_text("Poll closed!")

    return COLOR_REVEAL

def color_reveal(update, context):
    update.message.reply_text("The color voting results are in!")
    
    # TODO parse votes

    if redVotes == blackVotes:
            # Need to vote on to decide on red or black.
            update.message.reply_text("As the number of red and black votes is the same, an additional round of voting will be held to see which color is to be revealed.")
            return VOTE_COLOR
    
    else:
        return VOTE_PLAYER

# Helper functions
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

def cancel (update, context):
    update.message.reply_text("The Red Black game has ended. Hope you had fun!",
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END

def main():
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    print("Starting bot!")

    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states
    conv_handler = ConversationHandler(
        
        entry_points=[CommandHandler('begin', begin)],

        states={
            # QUESTION: [MessageHandler(Filters.reply and Filters.chat(username=players[queueIt]), question)], 
            QUESTION: [MessageHandler(Filters.reply, question)], 
            # Next state only when replied to by the next person.

            REDBLACK: [MessageHandler(Filters.text, redBlack),
                        CommandHandler('skip', redblack_reveal)], # Lets you skip till the next one

            REDBLACK_REVEAL: [MessageHandler(Filters.text, redblack_reveal)],
            
            VOTE_PLAYER: [MessageHandler(Filters.text, vote_player),
                        CommandHandler('skip', player_reveal)],

            PLAYER_REVEAL: [MessageHandler(Filters.text, player_reveal)],

            VOTE_COLOR: [MessageHandler(Filters.text, vote_color),
                        CommandHandler('skip', color_reveal)],

            COLOR_REVEAL: [MessageHandler(Filters.text, color_reveal)]
        },

        fallbacks= [CommandHandler("stop", cancel)]

    )

    dp.add_handler(conv_handler)

    # on different commands - answer in Telegram
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
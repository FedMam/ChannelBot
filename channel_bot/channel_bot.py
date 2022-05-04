import random

from telegram import *
from telegram.ext import *
from datetime import datetime

def start(update: Update, context: CallbackContext):
    if update.message.chat_id in users:
        context.bot.send_message(chat_id=update.message.chat_id, \
                                 text='You have already registered')
        return
    context.bot.send_message(chat_id=update.message.chat_id, \
                                 text='Hello. Please send me your username:')

def time():
    updater.bot.send_message(chat_id=channelID, \
                             text = 'Date and time is now ' + datetime.now().strftime("%d/%m/%Y %H:%M:%S"))

def textCmd(update: Update, context: CallbackContext):
    if update.message.chat_id in users:
        context.bot.send_message(chat_id=channelID, \
                                 text=('<b>' + users[update.message.chat_id] + \
                                 '</b>\non ' + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ":\n" + \
                                 update.message.text), parse_mode=ParseMode.HTML)
    else:
        username = update.message.text
        if len(username) > 30:
            context.bot.send_message(chat_id=update.message.chat_id, \
                                     text='Username cannot be longer than 30 characters')
        else:
            users[update.message.chat_id] = username
            context.bot.send_message(chat_id=update.message.chat_id, \
                                     text='You have been successfully registered.' + \
                                     '\nYour messages will be automatically posted into my channel:\nt.me/channel_bot_channel')
            context.bot.send_message(chat_id=channelID, \
                     text='A new user <b>' + username + '</b> has registered', \
                     parse_mode = ParseMode.HTML)

# constants & variables
users = {}
channelID = "-1001758576601"
# -----

updater = Updater("5357309935:AAHddwuM0y7Ri1iW5TwEpUG30PCKZiopX7k", use_context=True)

updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(MessageHandler(Filters.text, textCmd))

updater.start_polling()

prev_news = []
running = True
news_messages = ['Breaking news\n', 'BREAKING NEWS!!!\n', '']
while running:
    with open('channel_bot.txt', 'r') as file:
        for line in file.readlines():
            if line not in prev_news:
                nline = line
                if nline[-1] == '\n':
                    nline = nline[:len(nline)-1]
                updater.bot.send_message(chat_id=channelID, \
                                         text=('<b>'+random.choice(news_messages)+'</b>'\
                                               +datetime.now().strftime("%d/%m/%Y %H:%M:%S")+'\n'+line), \
                                         parse_mode=ParseMode.HTML)
                prev_news.append(line)

from requests import check_compatibility
import telebot
from random import randint
from telebot import types
from time import sleep

#app = Flask(__name__)
#port = int(os.environ.get("PORT", 5000))
#app.run(host='0.0.0.0', port=port)

TOKEN = "1980873038:AAHU0QP1NCVGjk4Qzx8SlzLLlZMQJrc8c5Q"
bot = telebot.TeleBot(TOKEN)

start_dialogue = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
start_dialogue.row('Начать диалог')

users = []

class Room():
    def check_connection(self):
        if self.pal == None:
            return True
        else:
            return False

    def find_pal(self):
        if len(users)!=0:
                if self.user_id != users[0].user_id:
                    self.pal = users[0].user_id
                    users[0].pal = self.user_id
                    users[0].status = "in_chat"
                    self.status = "in_chat"
                    bot.send_message(self.user_id, "Собеседник найден")
                    return self.pal
                else:
                    users.remove(users[0])
                    self.pal = users[0].user_id
                    users[0].pal = self.user_id
                    users[0].status = "in_chat"
                    self.status = "in_chat"
                    bot.send_message(self.user_id, "Собеседник найден")
                    return self.pal

        else:
            self.status = "seeking"
            self.pal = None
            users.append(self)
            while True:
                if not self.check_connection():
                    bot.send_message(self.user_id, "Собеседник найден")
                    return self.pal



    def __init__(self, user_id, status):
        self.user_id = user_id
        self.status = status
        self.pal = self.find_pal()
    
    def stop_chat(self):
        global users
        self.status = "ended"
        users.remove(self)
        bot.send_message(self.user_id, "Чат был остановлен :(")
        bot.send_message(self.pal, "Чат был остановлен :(")

    def send_messages(self, message):
        if self.status == "in_chat":
            if message.from_user.id == self.user_id:
                bot.send_message(self.pal, message.text)
            else:
                bot.send_message(self.user_id, message.text)

@bot.message_handler(commands=['start', 'help'])
def start(message):
    global users
    bot.send_message(message.from_user.id, f"Это анонимный чат-бот телеграма. Для поиска собеседника нажмите /search. Сейчас общается:{len(users)*2}")


@bot.message_handler(content_types=['text'])
def get_messages(message):
    global users
    global user
    if message.text == "/stop":
        print(users)
        user.stop_chat()
    elif message.text == "/search" or message.text == "Начать диалог":
        bot.send_message(message.from_user.id, "Ищем собеседника...")
        user = Room(message.from_user.id, "seeking")
    else:
        try:
            user.send_messages(message) 
        except Exception:
            bot.send_message(message.from_user.id, "Вы не в чате :/")

bot.polling(none_stop=True, interval=0)
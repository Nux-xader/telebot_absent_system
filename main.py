import telebot, config, time, json, sys, os
from threading import Thread

bot = telebot.TeleBot("5083702955:AAF7gxDMwaa-fJjTXcvsu6eBoi8A-ZJczvk")
db_user = "db/users.json"


class DB_RW:
    def __init__(self, path):
        self.path = path

    def dump(self, data):
        json.dump(data, open(self.path, 'w'), ensure_ascii=False, indent=4)

    def load(self):
        return json.load(open(self.path, 'r'))


users_data = DB_RW(db_user)

def sent_absent():
    start, end = True, True
    while True:
        t = time.localtime()
        t = f"{t.tm_hour}:{t.tm_min}"
        # sending alert start absent
        if (t == config.ABSENT_START) and (start):
            start, end = False, True
            for i in list(users_data.load().keys()):
                bot.send_message(i, config.ABSENT_START_MSG)

        # sending alert end absent
        if (t == config.ABSENT_FINISH) and (end):
            start, end = True, False
            for i in list(users_data.load().keys()):
                bot.send_message(i, config.ABSENT_FINISH_MSG)
        time.sleep(1)

Thread(target=sent_absent).start()

@bot.message_handler(commands=['start'])
def askname(message):
    database = users_data.load()
    if  str(message.chat.id) not in list(database.keys()):
        bot.send_message(message.chat.id, "Halo!\nMohon kirimkan nama lengkap anda")


@bot.message_handler(func=lambda m: True)
def save_name(message):
    database = users_data.load()
    if  str(message.chat.id) not in list(database.keys()):
        database[str(message.chat.id)] = str(message.text)
        users_data.dump(database)
        bot.send_message(message.chat.id, "Terimakasih\nNama anda telah di daftarkan")



print("Bot running!")
bot.polling()
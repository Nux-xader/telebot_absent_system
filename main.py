import telebot, json, sys, os

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
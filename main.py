import requests, telebot, config, time, json, sys, os
from threading import Thread

bot = telebot.TeleBot("5083702955:AAF7gxDMwaa-fJjTXcvsu6eBoi8A-ZJczvk")
db_user = "db/users.json"
db_was_absent = "temp/was_absent.json"
headers = {
    "user-agent": 
    "Mozilla/5.0 (Linux; Android 6.0.1; Redmi Note 3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Mobile Safari/537.36", 
    "x-api-key": "abc"
}

class DB_RW:
    def __init__(self, path):
        self.path = path

    def dump(self, data):
        json.dump(data, open(self.path, 'w'), ensure_ascii=False, indent=4)

    def load(self):
        return json.load(open(self.path, 'r'))


class Absent:
    _api = ""


users_data = DB_RW(db_user)
was_absent = DB_RW(db_was_absent)
absent = Absent()

def thread1():
    start, end = True, True
    while True:
        t = time.localtime()
        m  = f"{t.tm_min}"
        if len(m) == 1: m = "0"+m
        t = f"{t.tm_hour}:{m}"
        # print(t)
        # sending alert start absent
        if (t == config.ABSENT_START) and start:
            start, end = False, True
            # reset temp was_absent.json
            was_absent.dump([])
            for i in list(users_data.load().keys()):
                bot.send_message(i, config.ABSENT_START_MSG)

        # sending alert end absent
        if (t == config.ABSENT_FINISH) and end:
            start, end = True, False
            # reset temp was_absent.json
            was_absent.dump([])
            for i in list(users_data.load().keys()):
                bot.send_message(i, config.ABSENT_FINISH_MSG)


        time.sleep(1)

Thread(target=thread1).start()

@bot.message_handler(commands=['hadir'])
def absent_first(message):
    database = users_data.load()
    if  str(message.chat.id) in list(database.keys()):
        temp = was_absent.load()
        if str(message.chat.id) not in temp:
            t = time.localtime()
            m  = f"{t.tm_min}"
            if len(m) == 1: m = "0"+m
            t = f"{t.tm_hour}:{m}"
            h_now, m_now = t.split(":")
            h_first, m_first = config.ABSENT_START.split(":")
            h_late, m_late = config.LATE_ABSENT.split(":")
            h_finish, m_finish = config.ABSENT_FINISH.split(":")

            # checking absent time
            if (int(h_now) >= int(h_first)) and (int(m_now) >= int(m_first))\
                and ((int(h_now)*60)+m_now < (int(h_finish)*60)+m_finish):
                # store was absent
                temp.append(str(message.chat.id))
                was_absent.dump(temp)
                # first absent
                if int(h_now) < int(h_late):
                    bot.send_message(message.chat.id, "Terimakasih telah absen tepat waktu")
                elif (int(h_now) == int(h_late)) and (int(m_now) < int(m_late)):
                    bot.send_message(message.chat.id, "Terimakasih telah absen tepat waktu")

                # late absent
                else:
                    bot.send_message(message.chat.id, config.LATE_ABSENT_MSG)

                response = requests.post(
                    config.START_ABSENT_URL, 
                    data={"idtelegram": str(message.chat.id), "jam":t}, 
                    headers=headers
                    ).json()
                print(response)
            else:
                bot.send_message(message.chat.id, "Mohon absen sesuai waktu yang telah di tentukan")
        else:
            bot.send_message(message.chat.id, "Anda telah melakukan absen sebelumnya.\nsilahkan kembali berkerja")
    else:
        bot.send_message(message.chat.id, "Halo! akun anda belum terdaftar\nMohon kirimkan nama lengkap anda")


@bot.message_handler(commands=['selesaikerja'])
def absent_end(message):
    database = users_data.load()
    if  str(message.chat.id) in list(database.keys()):
        temp = was_absent.load()
        if str(message.chat.id) not in temp:
            t = time.localtime()
            t = f"{t.tm_hour}:{t.tm_min}"
            h_now, m_now = t.split(":")
            h_first, m_first = config.ABSENT_START.split(":")
            h_finish, m_finish = config.ABSENT_FINISH.split(":")

            if (int(h_now) >= int(h_finish)) and (int(m_now) >= int(m_finish)):
                bot.send_message(message.chat.id, "Terimakasih telah melakukan absen:)")
                response = requests.post(
                    config.END_ABSENT_URL, 
                    data={"idtelegram": str(message.chat.id), "jam":t}, 
                    headers=headers
                    ).json()
                print(response)
            else:
                bot.send_message(message.chat.id, f"Jam kerja kamu belum habis loh\n\
sabar ya jam kerja kamu itu dari jam {config.ABSENT_START} sampai {config.ABSENT_FINISH}")
        else:
            bot.send_message(message.chat.id, "Anda telah melakukan absen sebelumnya.\nsilahkan kembali berkerja")
    else:
        bot.send_message(message.chat.id, "Halo! akun anda belum terdaftar\nMohon kirimkan nama lengkap anda")

@bot.message_handler(regexp=f'^attention {config.ATTENTION_PASSWORD}')
def action(message):
    database = users_data.load()
    dataMessage = str(message.text).split("[", 1)[-1]
    dataMessage = dataMessage.split("]", dataMessage.count("]"))
    for i in list(database.keys()):
        if str(message.chat.id) == i: continue
        try:
            bot.send_message(i, dataMessage)
            # bot.send_message("1146054597", "Successfully send send to "+str(i))
        except Exception as e:
            pass
#             bot.send_message("1146054597", """
# Filed send to {}
# Error : {}""". format(str(i), e))
    bot.send_message(message.chat.id, "Attetion was done")
    pass

@bot.message_handler(commands=['start'])
def askname(message):
    database = users_data.load()
    if  str(message.chat.id) not in list(database.keys()):
        bot.send_message(message.chat.id, "Halo!\nMohon kirimkan NIP anda")
    else:
        bot.send_message(message.chat.id, f"Halo, \
akun telegram kmu sebelumnya sudah terdaftar di sistem kami. NIP : {database[str(message.chat.id)]}")


@bot.message_handler(func=lambda m: True)
def save_name(message):
    database = users_data.load()
    if  str(message.chat.id) not in list(database.keys()):
        database[str(message.chat.id)] = str(message.text)
        response = requests.post(
            config.REGISTER_ABSENT_URL, 
            data={"idtelegram": str(message.chat.id), "nip":str(message.text)}, 
            headers=headers
            ).json()
        print(response)
        users_data.dump(database)
        bot.send_message(message.chat.id, "Terimakasih\nNIP anda telah di daftarkan")

print("Bot running!")
bot.polling()
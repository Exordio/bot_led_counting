#Rofl bot for сounting LEDs to create a suitable spectrum for plants.


import tokens
import telebot
import math
import json
import cherrypy

webhook_host = ''
webhook_port = 443
webhook_listen = '0.0.0.0'
webhook_SSL_cert = '/home/ubuntu/Boot_webhook_pooling/webhook_ledbot_cert.pem'
webhook_SSL_PRIV = '/home/ubuntu/Boot_webhook_pooling/webhook_ledbot_pkey.pem'
webhook_url_kekbase = "https://%s:%s" % (webhook_host, webhook_port)
webhook_url_path = "/%s/" % (tokens.bot_token)

bot = telebot.TeleBot(tokens.bot_token)

class WebhookServer(object):
    @cherrypy.expose
    def index(self):
        if 'content-length' in cherrypy.request.headers and \
                        'content-type' in cherrypy.request.headers and \
                        cherrypy.request.headers['content-type'] == 'application/json':
            length = int(cherrypy.request.headers['content-length'])
            json_string = cherrypy.request.body.read(length).decode("utf-8")
            update = telebot.types.Update.de_json(json_string)
            # Эта функция обеспечивает проверку входящего сообщения ( не трогать )
            bot.process_new_updates([update])
            return ''
        else:
            raise cherrypy.HTTPError(403)

def log_from_bot(message, ans):
    print("\n =========================================")
    from datetime import datetime
    print(datetime.now())
    now = datetime.now()
    print("Получено сообщение от {0} {1}. id = {2} \n Содержание : {3}".format(message.from_user.first_name,
                                                                             message.from_user.last_name,
                                                                             str(message.from_user.id),
                                                                             message.text))
    print('Бот : ', ans)
    LOGFILE = open("/home/ubuntu/Yandex.Disk/LEDBOT/LOG_FILES/{0}.{1}.{2}:{3}:{4}.LOGZ".format(message.from_user.first_name,message.from_user.last_name,now.year, now.month, now.day),"a")
    LOGFILE.write("==================================================================================\n"
                  "Получено сообщение от {0} {1}. id = {2} \nСодержание : {3} \nБот ответил:{5}\nВремя сообщения : {4}\n".format(message.from_user.first_name,
                                                                                                                message.from_user.last_name,
                                                                                                                str(message.from_user.id),
                                                                                                                message.text,
                                                                                                                datetime.today(),ans))
    LOGFILE.close()


@bot.message_handler(func=lambda message: True, commands=['start'])
def START_KEYBOARD(message):
    bot.send_message(message.chat.id, "Шалом 🤝, этот бот подсчитает за тебя, сколько каких LEDов нужно исходя из общего количества :) 💎💎")
    user_markup = telebot.types.ReplyKeyboardMarkup(True, False, True)
    user_markup.row('Провести расчёты :D','rofl')
    user_markup.row('/stop')
    bot.send_message(message.from_user.id, "Отличные японские диоды (Йоши рекомендует) http://cobkits.com/product/citizen-clu048-1212-90cri-gen6/ ", reply_markup=user_markup)
    ans = "HELLO MESSAGE FROM BOT"
    log_from_bot(message,ans)

@bot.message_handler(func=lambda message: True, commands=['stop'])
def CLOSE_KEYBOARD(message):
    close_markup = telebot.types.ReplyKeyboardRemove(True)
    bot.send_message(message.from_user.id, 'Заходи ещё 🌈⛈🎉🌹🐧😊', reply_markup=close_markup)
    ans = "CLOSE KEYBOARD command"
    log_from_bot(message,ans)

Proporz1 = 66.66666666666666666667; Proporz2 = 26.66666666666666666667; Proporz3 = 6.66666666666666666667

@bot.message_handler(func=lambda message: True, content_types=['text'])
def TEXT_V_message(message):
    global changeX
    if (message.text == "Провести расчёты :D"):
        changeX = "raschet"
        ans = 'Введи общее число диодов 💭 (Пальчиками, с клавиатуры, в виде цифр)'
        close_markup = telebot.types.ReplyKeyboardRemove(True)
        bot.send_message(message.from_user.id, 'Введи общее число диодов 💭 (Пальчиками, с клавиатуры, в виде цифр)', reply_markup=close_markup)
        log_from_bot(message,ans)
    if (message.text == 'rofl'):
        bot.send_message(message.from_user.id, "https://www.youtube.com/watch?v=_CL6n0FJZpk")
        ans = "Отправлена ссылка на видео"
        log_from_bot(message,ans)
    if (message.text.isdigit()):
        if ((int(message.text) >= 1) and (int(message.text) <= 100000) and changeX == 'raschet'):
            al_ledz = int(message.text)
            RED = round((al_ledz * Proporz1)/100);BLUE = round((al_ledz * Proporz2)/100);WHITE = round((al_ledz*Proporz3)/100)
            changeX = ""
            user_markup = telebot.types.ReplyKeyboardMarkup(True, False, True)
            user_markup.row('Провести расчёты :D', 'rofl')
            user_markup.row('/stop')
            ans = "Красных : {0}, Синих : {1}, Белых : {2}\nКак то так  😊".format(RED,BLUE,WHITE)
            bot.send_message(message.from_user.id,ans, reply_markup=user_markup)
            log_from_bot(message,ans)
        elif (int(message.text) == 0):
            user_markup = telebot.types.ReplyKeyboardMarkup(True, False, True)
            user_markup.row('Провести расчёты :D', 'rofl')
            user_markup.row('/stop')
            ans = ";/ 0?? "
            bot.send_message(message.from_user.id,ans, reply_markup=user_markup)
            log_from_bot(message,ans)
bot.remove_webhook()

bot.set_webhook(url=webhook_url_kekbase + webhook_url_path, certificate=open(webhook_SSL_cert, 'r'))
cherrypy.config.update({
    'server.socket_host': webhook_listen,
    'server.socket_port': webhook_port,
    'server.ssl_module': 'builtin',
    'server.ssl_certificate': webhook_SSL_cert,
    'server.ssl_private_key': webhook_SSL_PRIV
})

cherrypy.quickstart(WebhookServer(), webhook_url_path, {'/':{}})



























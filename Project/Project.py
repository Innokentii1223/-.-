# Библиотеки и конфиг
import telebot
import config
import os
import Нейросеть
import speech_recognition as sr
import sqlite3
# Соединенее с базой данных
conn = sqlite3.connect("Users.db")
cur = conn.cursor()
# Иницализация синхронного бота
bot = telebot.TeleBot(config.token)
# Переменые
r = sr.Recognizer()
password = "1234"
asset = False
phonet = ""
URL = ""
if URL == "":
    URL = "Увы ссылки нет"


# Хэндлеры
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, """Привет! Этот бот сделан для тех. поддержки задавайте сюда вопросы которые вас интересуют
""")


@bot.message_handler(commands=['help'])
def send_file(message):
    if asset:
        files = os.listdir("Files")
        file = open("Files" + "/" + files[0], 'rb')
        bot.send_document(message.from_user.id, file)
    else:
        bot.send_message(message.from_user.id, "У вас нет доступа")


@bot.message_handler(commands=['asset'])
def get_asset(message):
    global asset
    word = message.text.split(maxsplit=1)[1]
    if password == word:
        asset = not asset
        if asset:
            bot.send_message(message.from_user.id, "Вам выдан доступ")
        elif not asset:
            bot.send_message(message.from_user.id, "Вы заблокировали доступ")
    else:
        bot.send_message(message.from_user.id, "Не правильный пароль")


@bot.message_handler(commands=['phone'])
def phone(message):
    bot.send_message(message.from_user.id, f"Телефон тех. поддержки: {phonet}")


@bot.message_handler()
def tech_support(message):
    user = ""
    name = message.from_user.first_name
    ides = message.from_user.id
    probel = True
    for i in range(len(message.text.split(maxsplit=1))):
        user += message.text.split(maxsplit=1)[i]
        if probel:
            user += " "
            probel = False
    user = user.lower()
    word = Нейросеть.cosine_sim("как оформить заказ?", user)
    word1 = Нейросеть.cosine_sim("Как узнать статус моего заказа?", user)
    word2 = Нейросеть.cosine_sim("Как отменить заказ?", user)
    word3 = Нейросеть.cosine_sim("Что делать, если товар пришел поврежденным?", user)
    word4 = Нейросеть.cosine_sim("Как связаться с вашей технической поддержкой?", user)
    word5 = Нейросеть.cosine_sim("Как узнать информацию о доставке?", user)
    cur.execute(f"""INSERT INTO users VALUES
                        ({name}, {ides}, {user})""")
    conn.commit()
    if word >= 0.5:
        bot.send_message(message.from_user.id, f"""Для оформления заказа, пожалуйста, выберите интересующий вас товар
         и нажмите кнопку "Добавить в корзину", затем перейдите в корзину и следуйте инструкциям для завершения покупки.
         Ссылка на сайт: {URL}""")
    elif word1 >= 0.5:
        bot.send_message(message.from_user.id, f"""Вы можете узнать статус вашего заказа, войдя в свой аккаунт на нашем
        сайте и перейдя в раздел "Мои заказы". Там будет указан текущий статус вашего заказа. Ссылка на сайт: {URL}""")
    elif word2 >= 0.5:
        bot.send_message(message.from_user.id, f"""Если вы хотите отменить заказ, пожалуйста, свяжитесь с нашей службой
        поддержки как можно скорее. Мы постараемся помочь вам с отменой заказа до его отправки.
        Ссылка на сайт: {URL}""")
    elif word3 >= 0.5:
        bot.send_message(message.from_user.id, f"""При получении поврежденного товара, пожалуйста, сразу свяжитесь с
        нашей службой поддержки и предоставьте фотографии повреждений. Мы поможем вам с обменом или возвратом товара.
        Ссылка на сайт: {URL}""")
    elif word4 >= 0.5:
        bot.send_message(message.from_user.id, f"""Вы можете связаться с нашей технической поддержкой через телефон на
        нашем сайте или написать нам в чат-бота командой /phone, я отправлю телефон тех. поддержки.
        Ссылка на сайт: {URL}""")
    elif word5 >= 0.5:
        bot.send_message(message.from_user.id, f"""Информацию о доставке вы можете найти на странице оформления заказа
        на нашем сайте. Там указаны доступные способы доставки и сроки.
        Ссылка на сайт: {URL}""")
    else:
        bot.send_message(message.from_user.id, f"""Пожалуйста скажите более конкретнее. Я не понял""")





bot.infinity_polling()
conn.close()

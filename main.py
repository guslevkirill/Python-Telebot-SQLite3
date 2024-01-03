import sqlite3
import telebot
from TOKEN import tgToken

connection = sqlite3.connect('TGDatabase.db', check_same_thread=False)
cursor = connection.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS Users (
id INTEGER PRIMARY KEY,
tg_id VARCHAR,
username VARCHAR,
first_name VARCHAR,
last_name VARCHAR
)
''')
connection.commit()


bot = telebot.TeleBot(token=tgToken)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    tg_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    bot.send_message(message.chat.id, 'Привет, ' + first_name + ", будем знакомы.")
    user_exist = cursor.execute('SELECT * FROM Users WHERE tg_id = ?', (tg_id,)).fetchone()
    if user_exist is None:
        cursor.execute(
            "INSERT INTO Users (tg_id, username, first_name, last_name)"
            "VALUES (?, ?, ?, ?)",
            (tg_id, username, first_name, last_name,)
        )
    connection.commit()


@bot.message_handler(commands=['sendall'])
def sendall(message):
    users = cursor.execute('SELECT tg_id FROM Users').fetchall()
    if message.from_user.id == 332155717:
        text = message.text[9:]
        for row in users:
            bot.send_message(row[0], text)
        bot.send_message(message.from_user.id, "Успешная рассылка!")


bot.infinity_polling()












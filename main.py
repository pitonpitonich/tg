
import os
from background import keep_alive #импорт функции для поддержки работоспособности
import pip
pip.main(['install', 'pytelegrambotapi'])
import telebot
from telebot import types

bot = telebot.TeleBot(os.getenv("token"), parse_mode="HTML")

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет!\nВведи /idea, чтобы отправить идею разработчику\nВведи /bug, чтобы отправить сообщение об ошибке разработчику ')
@bot.message_handler(commands=['idea'])
def idea(message):
    bot.send_message(message.chat.id, 'Введите идею')

    @bot.message_handler(content_types=['text'])
    def handle_idea(message):
        bot.send_message(int(os.getenv("myid")),f'{message.from_user.first_name} {message.from_user.last_name}, с ником @{message.from_user.username} предложил идею:\n{message.text}')
@bot.message_handler(commands=['bug'])
def bug(message):
    markup=types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("С картинкой", callback_data='pic'))
    markup.add(types.InlineKeyboardButton("Без картинки", callback_data='nopic'))
    bot.send_message(message.chat.id, 'Выбери режим', reply_markup=markup)
    @bot.callback_query_handler(func=lambda callback: True)
    def callback(callback):
        if callback.data == 'pic':
            bot.send_message(callback.message.chat.id, 'Введите баг и прикрепите картинку')
            @bot.message_handler(content_types=['document'])
            def bug_photo(message):
                document_id = message.document.file_id
                bot.send_document(int(os.getenv("myid")),document_id, caption=f'{message.from_user.first_name} {message.from_user.last_name}, с ником @{message.from_user.username} сообщил об ошибке:\n{message.caption}')

        else:
            bot.send_message(message.chat.id, 'Введите баг')

            @bot.message_handler(content_types=['text'])
            def bug_text(message):
                bot.send_message(int(os.getenv("myid")),f'{message.from_user.first_name} {message.from_user.last_name}, с ником @{message.from_user.username} сообщил об ошибке:\n{message.text}')

keep_alive()
bot.infinity_polling() 

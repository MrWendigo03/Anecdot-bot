import requests
import random
import os
import telebot

from aiogram.utils import executor
from bs4 import BeautifulSoup as bs
from dotenv import load_dotenv

load_dotenv(".env")
TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)

URL = "https://www.anekdot.ru/last/anekdot/"


def pars(url):
    r = requests.get(url)
    soup = bs(r.text, 'lxml')
    anecdotes = soup.find_all("div", class_="text")
    return [anec.text for anec in anecdotes]


joke_list = pars(URL)
random.shuffle(joke_list)

@bot.message_handler(commands=["start"])
def hello(message):
    bot.send_message(message.chat.id, "Здравсивуйте, я ваш персональный Бот со сборником анекдотов, напишите "
                                      "мне любую цифру.")

@bot.message_handler(content_types=['text'])
def joker(message):
    if message.text.lower() in '123456789':
        bot.send_message(message.chat.id, joke_list[0])
        del joke_list[0]
    else:
        bot.send_message(message.chat.id, "Напишите мне любую цифру.")

bot.polling()
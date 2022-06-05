import time
import telepot
import os, sys, re
from bot_token import bot_token
import random
import pykakasi
import pandas as pd

KKS = pykakasi.kakasi()
HIRAGANA = list(map(chr, range(ord(u'\u3040'), ord(u'\u309F'))))

def get_hiragana():
    return random.choice(HIRAGANA)

bot = telepot.Bot(bot_token)
bot.SAMPLED_KANA = None


def handle(msg):
    chat_id = msg['chat']['id']
    if msg['text'] == '/start':
        bot.sendMessage(chat_id, r"Ciao, sono KANAbot, il bot che ti interroga sugli hiragana! Scrivi /hiragana per iniziare, /stop quando vuoi fermarti")
    elif msg['text'] == '/hiragana':
        bot.SAMPLED_KANA = KKS.convert(get_hiragana())[0]
        bot.sendMessage(chat_id, f"Come si legge questa?")
        bot.sendMessage(chat_id, bot.SAMPLED_KANA['orig'])
    elif msg['text'] == '/stop':
        if bot.SAMPLED_KANA is not None:
            bot.sendMessage(chat_id, f"Ok! Ti lascio soltanto la soluzione dell'ultimo hiragana!")
            bot.sendMessage(chat_id, bot.SAMPLED_KANA['hepburn'])
            bot.SAMPLED_KANA = None

    else:
        if bot.SAMPLED_KANA is not None:
            if (msg['text'].lower() == bot.SAMPLED_KANA['hepburn']):
                bot.sendMessage(chat_id, f"Giusto! Ecco il prossimo:")
                bot.SAMPLED_KANA = KKS.convert(get_hiragana())[0]
                bot.sendMessage(chat_id, bot.SAMPLED_KANA['orig'])
            else:
                bot.sendMessage(chat_id, 'No! Riprova!')
        else:
            bot.sendMessage(chat_id, r"Scusa, non ho capito... Scrivi /hiragana per iniziare, /stop quando vuoi fermarti")
    return None

bot.message_loop(handle)

while(1):
    time.sleep(1)
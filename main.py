import telebot
import datetime
from pycoingecko import CoinGeckoAPI
from time import sleep
from multiprocessing import Process
import get_instant_trades
import os


TOKEN = ''
bot = telebot.TeleBot(TOKEN)
cg = CoinGeckoAPI()
#Bot testing
#GROUP_ID = 
#Test2
GROUP_ID = 


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Hello! \nWrite /crypto to see cryptocurrency description.\n'
                                      'Write /social to follow different channels.\n'
                                      'Write /others to see other commands.')
    #print(message.chat.id)


'''@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text.lower() == 'hello':
        bot.send_message(message.chat.id, 'Привет, мой создатель')
    elif message.text.lower() == 'bye':
        bot.send_message(message.chat.id, 'Прощай, создатель')'''


@bot.message_handler(content_types=["new_chat_members"])
def handler_new_member(message):
    first_name = message.new_chat_members[0].first_name
    bot.send_message(message.chat.id, "Welcome, {0}!".format(first_name))


def check_count_transactions():
    while True:
        ts = datetime.datetime.now().timestamp()
        hey_inst = float(get_instant_trades.get_trades()[0])
        hey_erc = float(get_instant_trades.get_erc_trades())
        if abs(ts - hey_erc) >= 86400.0 and abs(ts - hey_inst) >= 86400.0:
            bot.send_message(GROUP_ID, 'There were no trades for more than 24h')
            x = 60 * 60 * 24
        elif hey_erc >= hey_inst:
            x = hey_erc + 86400 - ts
        else:
            x = hey_inst + 86400 - ts

        sleep(x)

def ping():
    #timestamp = 1608558087
    trades = get_instant_trades.get_trades()
    last_tran_time = trades[0]
    bot.send_message(GROUP_ID, trades[1])
    while True:
        hey = get_instant_trades.get_trades()
        if last_tran_time != hey[0]:
            last_tran_time = hey[0]
            bot.send_message(GROUP_ID, hey[1])

        #bot.send_message(GROUP_ID)
        sleep(60*1)

def health_check():
    while True:
        status = get_instant_trades.healthcheck()
        if status != 'OK':
            bot.send_message(GROUP_ID, '1inch api is unavailable')

        sleep(30*60)

def market_rate():
    difference = get_instant_trades.get_course()
    if difference >= 50.0:
        bot.send_message(GROUP_ID, 'Rubic market rate differs from CoinGecko for more than 50%')

    sleep(60*60*3)


if __name__ == '__main__':
    procs = []
    for i in range(4):
        if i == 0:
            proc = Process(target=ping)
            procs.append(proc)
            proc.start()
        if i == 1:
            proc = Process(target=health_check)
            procs.append(proc)
            proc.start()
        if i == 2:
            proc = Process(target=check_count_transactions)
            procs.append(proc)
            proc.start()
        if i == 3:
            proc = Process(target=market_rate)
            procs.append(proc)
            proc.start()
    for proc in procs:
        proc.join()

    '''proc2 = Process(target=ping)
    proc3 = Process(target=check_count_transactions)
    proc4 = Process(target=health_check)
    proc2.start()
    proc3.start()
    proc4.start()'''
    bot.polling(none_stop=True)

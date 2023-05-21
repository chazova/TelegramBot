import telebot
from config import currency, TOKEN
from extensions import APIException, MoneyConverter

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start','help'])
def handle_start_help(message: telebot.types.Message):
    text = 'Чтобы начать работу отправьте сообщение боту в следующем формате:\n \
<имя валюты, цену которой нужно узнать> <имя валюты, в которой нужно узнать цену первой валюты> \
<количество первой валюты> \n*Отправьте команду /values для вывода списка доступных валют'
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['values'])
def handle_values(message: telebot.types.Message):
    text = 'Доступные валюты:\n' + '\n'.join(currency.keys())
    bot.send_message(message.chat.id, text)

@bot.message_handler(content_types=['text',])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise APIException('Количество введенных данных не равно 3.')

        quote, base, amount = values
        exchange_rate = MoneyConverter.get_price(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду \n{e}')
    else:
        text = f'{amount} {quote} = {float(exchange_rate) * float(amount)} {base}'
        bot.reply_to(message, text)


bot.polling(none_stop=True)
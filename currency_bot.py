import telebot
from config import keys, TOKEN
from extensions import APIException, CurrencyConverter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Для начала работы бота введите команду в формате:\n \
<название конвертируемой валюты> <название целевой валюты> \
<количество конвертируемой валюты>\n \
Чтобы увидеть все доступные валюты для конвертации, введите команду /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def help(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text',])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise APIException('Некорректное колличество вводных. Попробуйте снова.')

        quote, base, amount = values
        total_result = CurrencyConverter.get_price(quote, base, amount)

    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя:\n{e}')

    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команту\n{e}')

    else:
        text = f'{amount} {quote} = {total_result} {base}'
        bot.send_message(message.chat.id, text)


bot.polling()

import telebot
from extensions import ConversionException, MoneyConverter
from config import keys, token, api_key
bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start', 'help'])
def start(message: telebot.types.Message):
    text = 'Для начала работы введите команду в следующем формате:\n \
<имя исходной валюты> <в какую валюту перевести> <количество переводимой валюты>\n \
Для получения списка доступных валют введите команду "/values"'
    bot.reply_to(message,text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message,text)

@bot.message_handler(content_types=['text',])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
        if len(values) != 3:
            raise ConversionException('Неверное количество параметров')
        quote, base, amount = values
        text = MoneyConverter.convert(quote,base,amount)
    except ConversionException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        bot.send_message(message.chat.id,text)

bot.polling()


import telebot
from extensions import APIException, CurrencyConverter
from config import TOKEN

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def help_command(message):
    text = (
        "Чтобы узнать цену валюты, введите запрос в формате:\n"
        "<имя валюты> <валюта для пересчета> <количество>\n\n"
        "Пример: USD EUR 100\n\n"
        "Доступные валюты:\n"
        "/values - просмотр всех валют"
    )
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values_command(message):
    available_currencies = "Доступные валюты: USD, EUR, RUB"
    bot.reply_to(message, available_currencies)

@bot.message_handler(func=lambda message: True)
def convert_currency(message):
    try:
        base, quote, amount = message.text.split()
        amount = float(amount)
    except ValueError:
        bot.reply_to(message, "Ошибка: введите данные в формате: <имя валюты> <валюта для пересчета> <количество>")
        return

    try:
        total_price = CurrencyConverter.get_price(base.upper(), quote.upper(), amount)
    except APIException as e:
        bot.reply_to(message, f"Ошибка: {str(e)}")
        return
    except Exception as e:
        bot.reply_to(message, f"Произошла ошибка: {str(e)}")
        return

    text = f"{amount} {base.upper()} = {total_price} {quote.upper()}"
    bot.send_message(message.chat.id, text)

if __name__ == "__main__":
    bot.polling(none_stop=True)
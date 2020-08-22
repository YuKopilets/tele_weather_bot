import telebot
from config import TOKEN
from l10n import languages
from telebot import types
from observation import ObservationHandler


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def execute_command(message):
    lang = define_lang(message.from_user.language_code)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = types.KeyboardButton(text=languages[lang]['find out'], request_location=True)
    markup.add(button)
    bot.send_message(message.chat.id, languages[lang]['start info'], reply_markup=markup)


@bot.message_handler(content_types=['location'])
def location_handler(message):
    lang = define_lang(message.from_user.language_code)
    if message.location is not None:
        handler = ObservationHandler(message.location.latitude, message.location.longitude, lang)
        bot.send_message(message.chat.id, handler.location_info())
        bot.send_photo(message.chat.id, handler.weather_image())
        bot.send_message(message.chat.id,
                         handler.weather_status(),
                         reply_markup=weather_details(handler.__str__(), lang))


def weather_details(coords, lang):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(languages[lang]['details'], callback_data='details:' + coords))
    return markup


@bot.callback_query_handler(func=lambda cq: cq.data and cq.data.startswith('details:'))
def process_details(callback_query):
    cq = callback_query.data.replace('details:', '')
    coords = cq.split('&')
    latitude = float(coords[0].replace('lat:', ''))
    longitude = float(coords[1].replace('lon:', ''))
    lang = define_lang(callback_query.from_user.language_code)
    handler = ObservationHandler(latitude, longitude, lang)
    bot.send_message(callback_query.from_user.id, handler.detailed_status())


def define_lang(language):
    if languages.__contains__(language):
        return language
    else:
        return 'en'


bot.polling(none_stop=True)

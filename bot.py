import telebot
from config import *
from logic import *

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Привет! Я бот, который может показывать города на карте. Напиши /help для списка команд.")

@bot.message_handler(commands=['help'])
def handle_help(message):
    bot.send_message(message.chat.id, "Доступные команды:  ...")
    # Допиши команды бота


@bot.message_handler(commands=['show_city'])
def handle_show_city(message):
    city_name = message.text.split()[-1]
    # Реализуй отрисовку города по запросу
    user_id = message.from_user.id
    manager.create_grapf(f'image/{city_name}_{user_id}.png', [city_name])
    with open(f'{city_name}_{user_id}.png','rb') as map:
        bot.send_photo(message.chat.id, map)

@bot.message_handler(commands=['remember_city'])
def handle_remember_city(message):
    user_id = message.chat.id
    city_name = message.text.split()[-1]
    if manager.add_city(user_id, city_name):
        bot.send_message(message.chat.id, f'Город {city_name} успешно сохранен!')
    else:
        bot.send_message(message.chat.id, 'Такого города я не знаю. Убедись, что он написан на английском!')

@bot.message_handler(commands=['show_my_cities'])
def handle_show_visited_cities(message):
    user_id = message.chat.id
    cities = manager.select_cities(message.chat.id)
    # Реализуй отрисовку всех городов
    if cities:
        map_path = 'my_cities.png'
        manager.create_grapf(map_path, cities)
        with open(map_path, 'rb') as map_file:
                bot.send_photo(message.chat.id, map_file)
    else:
        bot.send_message(message.chat.id, "У вас нет сохранённых городов.")

if __name__=="__main__":
    manager = DB_Map(DATABASE)
    bot.polling()

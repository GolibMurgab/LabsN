import telebot
from telebot import types
import psycopg2
import datetime

token = "6118295403:AAH6T7CId8Yq2CIhAtfpegzTFNitWj8Wcn4"

bot = telebot.TeleBot(token)

conn = psycopg2.connect(database="timelab",
                        user="postgres",
                        password="пароль",
                        host="localhost",
                        port="5432")

cursor = conn.cursor()

def dayTable(day, nub):
    wk = datetime.datetime.now().isocalendar().week
    if wk % 2 == 1 and nub == 1:
        wk = 1
    elif wk % 2 == 0 and nub == 1:
        wk = 2
    elif wk % 2 == 1 and nub == 2:
        wk = 2
    elif wk % 2 == 0 and nub == 2:
        wk = 1

    cursor.execute("""SELECT nomer, teacher.subject, room_numb, start_time,
    teacher.full_name FROM timetable INNER JOIN subject ON timetable.subject = subject.subject_name
    INNER JOIN teacher ON subject.subject_name = teacher.subject WHERE day = %s AND week = %s""", (day, wk))
    records = list(cursor.fetchall())
    lan = len(records)
    t = day + '\n' + '--------------------\n'
    for i in range(1, 6):
        k = 1
        for j in range(lan):
            if int(records[j][0]) == i:
                t += str(records[j][0]) + ' | ' + records[j][1] + ' | ' + records[j][2] + ' | ' + records[j][
                    3] + ' | ' + records[j][4] + '\n'
                k = 0
                break
        if k == 1 and i == 1:
            x = str(i) + ' | ' + 'Нет пары' + ' | ' + '9:30 - 11:05' + '\n'
            t += x
        if k == 1 and i == 2:
            x = str(i) + ' | ' + 'Нет пары' + ' | ' + '11:20 - 12:55' + '\n'
            t += x
        if k == 1 and i == 3:
            x = str(i) + ' | ' + 'Нет пары' + ' | ' + '13:10 - 14:45' + '\n'
            t += x
        if k == 1 and i == 4:
            x = str(i) + ' | ' + 'Нет пары' + ' | ' + '15:25 - 17:00' + '\n'
            t += x
        if k == 1 and i == 5:
            x = str(i) + ' | ' + 'Нет пары' + ' | ' + '17:15 - 18:40' + '\n'
            t += x
    t = t + '--------------------\n'
    return t


def forweek(nub):
    wk = datetime.datetime.now().isocalendar().week
    if wk % 2 == 0 and nub == 1:
        x = '(Чётная)\n\n'
    elif wk % 2 == 1 and nub == 1:
        x = '(Нечётная)\n\n'
    if wk % 2 == 0 and nub == 2:
        x = '(Нечётная)\n\n'
    elif wk % 2 == 1 and nub == 2:
        x = '(Чётная)\n\n'
    x = x + dayTable('Понедельник', nub) + dayTable('Вторник', nub) + dayTable('Среда', nub) + dayTable('Четверг', nub) + dayTable('Пятница', nub) + dayTable('Суббота', nub)
    return x


@bot.message_handler(commands=['easter_egg'])
def egg(message):
    bot.send_message(message.chat.id, 'поздравляю, вы нашли пасхалку')


@bot.message_handler(commands=['monday'])
def monday(message):
    bot.send_message(message.chat.id, dayTable('Понедельник', 1))


@bot.message_handler(commands=['tuesday'])
def monday(message):
    bot.send_message(message.chat.id, dayTable('Вторник', 1))


@bot.message_handler(commands=['wednesday'])
def monday(message):
    bot.send_message(message.chat.id, dayTable('Среда', 1))


@bot.message_handler(commands=['thursday'])
def monday(message):
    bot.send_message(message.chat.id, dayTable('Четверг', 1))


@bot.message_handler(commands=['friday'])
def monday(message):
    bot.send_message(message.chat.id, dayTable('Пятница', 1))


@bot.message_handler(commands=['saturday'])
def monday(message):
    bot.send_message(message.chat.id, dayTable('Суббота', 1))


@bot.message_handler(commands=['week'])
def monday(message):
    bot.send_message(message.chat.id, forweek(1))


@bot.message_handler(commands=['nextweek'])
def monday(message):
    bot.send_message(message.chat.id, forweek(2))


@bot.message_handler(commands=['start'])
def start(message):
    keyboard = types.ReplyKeyboardMarkup()
    keyboard.row("Хочу", 'Не хочу', "/help")
    bot.send_message(message.chat.id, 'Привет! Хотите узнать свежую информацию о МТУСИ?', reply_markup=keyboard)


@bot.message_handler(commands=['net'])
def dont(message):
    keyboard = types.ReplyKeyboardMarkup()
    keyboard.row('Понедельник', 'Вторник', 'Среда')
    keyboard.row('Четверг', 'Пятница', 'Суббота')
    keyboard.row('Расписание на текущую неделю', 'Расписание на следующую неделю')
    bot.send_message(message.chat.id, 'Выбирете день или неделю', reply_markup=keyboard)


@bot.message_handler(commands=['help'])
def start_message(message):
    t = 'Список доступных команд:\n/mtuci - Показать сайт мтуси\n/monday - Расписание на Понедельник\n'\
    '/tuesday - Расписание на Вторник\n/wednesday - Расписание на Среду\n/thursday - Расписание на Четверг\n'\
    '/friday - Расписание на Пятницу\n/saturday - Расписание на Субботу\n/week - Расписание на текущую неделю\n'\
    '/nextweek - Расписание на следующую неделю'
    bot.send_message(message.chat.id, t)


@bot.message_handler(commands=['mtuci'])
def mtuci(message):
    bot.send_message(message.chat.id, 'Официальный сайт МТУСИ – https://mtuci.ru/')


@bot.message_handler(content_types=['text'])
def answer(message):
    if message.text.lower() == "не хочу":
        dont(message)
    elif message.text.lower() == "хочу":
        bot.send_message(message.chat.id, 'Тогда тебе сюда - https://mtuci.ru/')
    elif message.text.lower() == 'понедельник':
        bot.send_message(message.chat.id, dayTable('Понедельник', 1))
    elif message.text.lower() == 'вторник':
        bot.send_message(message.chat.id, dayTable('Вторник', 1))
    elif message.text.lower() == 'среда':
        bot.send_message(message.chat.id, dayTable('Среда', 1))
    elif message.text.lower() == 'четверг':
        bot.send_message(message.chat.id, dayTable('Четверг', 1))
    elif message.text.lower() == 'пятница':
        bot.send_message(message.chat.id, dayTable('Пятница', 1))
    elif message.text.lower() == 'суббота':
        bot.send_message(message.chat.id, dayTable('Суббота', 1))
    elif message.text.lower() == 'расписание на текущую неделю':
        bot.send_message(message.chat.id, 'Расписание на текущую неделю\n' + forweek(1))
    elif message.text.lower() == 'расписание на следующую неделю':
        bot.send_message(message.chat.id, 'Расписание на следующую неделю\n' + forweek(2))
    else:
        bot.send_message(message.chat.id, 'Извините, я Вас не понял.\nНажмите /help для просмотра того что я умею.')




bot.polling(none_stop=True)


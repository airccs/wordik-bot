import datetime
import time
import telebot
from telebot import types
import threading
import sql
import СWordik
import Keyboards as K

bot = telebot.TeleBot('6678321800:AAHV8iIZSrAFzmMARV1Uv_rCazbYnB2_4YI')
flagConnect = False


# Функция, которая берет слово из вордик и подставляет в строку, которая будет печататься в боте
def getword(type):
    word = wordik.word

    if type == 'hide':  # Выдает слово со скрытым переводом
        return "{} {}\n  {}  ".format(word[1], word[2],
                                      word[0][1])

    if type == 'show':  # Выдает слово с показанным переводом
        return "{} {}\n    {} -\n     {}".format(word[1], word[2],
                                                 word[0][1], word[0][2])


def slice(arr, direction, q=1):  # Функция, котора сдвигает список(для  help)
    if direction == '->':
        return arr[-q:] + arr[:-q]
    if direction == '<-':
        return arr[q:] + arr[:q]


def gethelp():  # Функция, которая выдает список с текстом, для как пользоваться
    a = '''
Раздел заучивание:
▪️ - Метка  новых слов(то есть те, которые вы еще не видели).
⬜️ - Метка  слов, которые вы пытаетесь запомнить в первый раз. Они будут мешаться с новыми словами.

Раздел повторение:
🔳 - Метка слов для повторения(они переходят сюда из раздела заучивания).

 Раздел уже известные:
🟩 - Метка  слов, которые вы либо уже знали, либо повторили достаточно, чтобы запомнить надолго.

 '''
    b = '''Алгоритм работы:

▪️- Новое слово:
Знаю: ▪️—> 🟩 (слово переходит в раздел уже известные)
Не знаю: ▪️—> ⬜️ (слово переходит в раздел запоминания и      попадется в том же списочке)

⬜️ - Слово для запоминания:
Знаю: ⬜️ —> 🔳(слово переходит в режим повторения)
Не знаю: ⬜️ —> ⬜️(слово никуда не уходит, а остается в том же списке и скоро попадется вам снова)

🔳- Слово для повторения:
Знаю: 🔳 —> 🔳+time (слово остается в режиме запоминания, но добавляется время до следующего его повторения)
Не знаю: 🔳 —> 🔳(слово никуда не уходит, а идет в конец списка)

🟩- Уже известное слово слово:
Знаю: 🟩 —> 🟩 (слово никуда не уходит, а идет в конец списка)
Не знаю: 🟩 —> ⬜️ (слово переходит в раздел запоминания)'''
    return [a, b]


Helptext = gethelp()  # Глобальная переменная, где хранится текст - как пользоваться


@bot.message_handler(content_types=['text'])
def get_text_messages(message):  # Функция, которая принимает текст, от пользователя
    global wordik
    global flagConnect
    flagConnect = True
    # sql.resetbase(message.from_user.id)
    wordik = СWordik.Wordik(userid=message.from_user.id)

    if message.text == "/start":  # Если старт, то выводит меню

        bot.send_message(message.from_user.id, text=wordik.getMenu(), reply_markup=K.menuKeyboard())

        def f():
            threading.Timer(3600.0, f).start()  # Перезапуск через 5 секунд
            bot.send_message(message.from_user.id, text="Hey, it's time to learn English !")

        f()




# В большинстве случаев целесообразно разбить этот хэндлер на несколько маленьких
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):  # Функция обработчик кнопок
    global wordik
    if flagConnect:
        print(call)
        # Если сообщение из чата с ботом
        if call.message:
            ################################ для как пользоваться
            if call.data == "help":
                helpFunc('menu', Helptext, bot, call)
            if call.data == "Hnext":
                helpFunc('Hnext', Helptext, bot, call)

            if call.data == "Hback":
                helpFunc('Hback', Helptext, bot, call)
            ##################################

            if call.data == "show":  # Кнопка показать
                learn('show', wordik.word[0][0], getword('hide'), bot, call)

            if call.data == "hide":  # Кнопка скрыть
                learn('hide', wordik.word[0][0], getword('show'), bot, call)

            if call.data == "addword":  # Кнопка добавить слово
                wordik.flow.decksize += 5
                wordik.takeword()
                learn('show', wordik.takeword()[0][0],
                      getword('hide') + "+{}".format(wordik.flow.decksize - wordik.flow.statToday[1]), bot, call)

            if call.data == "kn":  # Кнопка знаю
                word = wordik.remembered()
                print('знаю 2', str(datetime.datetime.now()))
                if wordik.flow.mode == 'r':
                    repeat('show', wordik.takeword()[0][0], getword('hide'), bot, call)
                else:
                    learn('show', wordik.takeword()[0][0], getword('hide'), bot, call)

            if call.data == "dkn":  # Кнопка не знаю
                word = wordik.forgot()
                if wordik.flow.mode == 'r':
                    repeat('show', wordik.takeword()[0][0], getword('hide'), bot, call)
                else:
                    learn('show', wordik.takeword()[0][0], getword('hide'), bot, call)

            if call.data == "menu":  # Кнопка меню
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text=wordik.getMenu(), reply_markup=K.menuKeyboard())

            if call.data == "learn":  # Кнопка заучивание
                wordik.changeMode('m')
                print(wordik.takeword()[0][0])
                learn('show', wordik.takeword()[0][0], getword('hide'), bot, call)

            if call.data == "repeat":  # Кнопка повторить
                wordik.changeMode('r')
                word = wordik.takeword()
                print('gg', wordik.word)
                repeat('show', wordik.takeword()[0][0], getword('hide'), bot, call)

            if call.data == "learned":  # Кнопка выученные
                wordik.changeMode('l')
                word = wordik.takeword()
                AMcheck('show', wordik.takeword()[0][0], getword('hide'), bot, call)

            if call.data == "statToday":  # Кнопка статистика сегодня
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text=wordik.flow.getStat('today'), reply_markup=K.statKeyboard())
            if call.data == "statAll":  # Кнопка статистика за все время
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text=wordik.flow.getStat('alltime'), reply_markup=K.statKeyboard())


def helpFunc(type, word, bot, call):  # функция, меняющая сообщение во вкладке как пользоваться
    global Helptext
    if type == 'Hnext':
        Helptext = slice(word, '->')
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=Helptext[0],
                              reply_markup=K.helpKeyboard())

    if type == 'Hback':
        Helptext = slice(word, '<-')
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=Helptext[0],
                              reply_markup=K.helpKeyboard())

    if type == 'menu':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=Helptext[0],
                              reply_markup=K.helpKeyboard())


def learn(type, flag, word, bot, call):  # функция, меняющая сообщение во вкладке Заучивание

    if type == 'show':
        if flag:

            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=word,
                                  reply_markup=K.wordKeyboard('hide'))
        else:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=word, reply_markup=K.addwordKeyboard())
    if type == 'hide':
        if flag:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=word,
                                  reply_markup=K.wordKeyboard(''))
        else:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=word, reply_markup=K.addwordKeyboard())


def repeat(type, flag, word, bot, call):  # функция, меняющая сообщение во вкладке повторение
    if type == 'show':
        if flag:
            print(word)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=word,
                                  reply_markup=K.wordKeyboard('hide'))
        else:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=word, reply_markup=K.repeatEmptyKeyboard())
    if type == 'hide':
        if flag:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=word,
                                  reply_markup=K.wordKeyboard(''))
        else:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=word, reply_markup=K.repeatEmptyKeyboard())


def AMcheck(type, flag, word, bot, call):  # функция, меняющая сообщение во вкладке выученные
    if type == 'show':
        if flag:

            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=word,
                                  reply_markup=K.AMKeyboard('hide'))
        else:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=word, reply_markup=K.AMEmptyKeyboard())
    if type == 'hide':
        if flag:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=word,
                                  reply_markup=K.AMKeyboard(''))
        else:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=word, reply_markup=K.AMEmptyKeyboard())


if __name__ == '__main__':  # чтобы бот постоянно ждал сообщение
    bot.infinity_polling()

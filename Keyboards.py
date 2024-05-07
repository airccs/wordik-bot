import telebot
from telebot import types

# расстановка кнопок для разных вкладок
def wordKeyboard(typeShow):
    key_show = types.InlineKeyboardButton(text='Cкрыть перевод', callback_data='show')
    keyboard = types.InlineKeyboardMarkup()
    if typeShow == 'hide':
        key_show = types.InlineKeyboardButton(text='Показать перевод', callback_data='hide')
    key_no = types.InlineKeyboardButton(text='Знаю', callback_data='kn')
    key_k = types.InlineKeyboardButton(text='Не знаю', callback_data='dkn')
    key_menu = types.InlineKeyboardButton(text='Меню', callback_data='menu')


    keyboard.add(key_show)
    keyboard.add(key_no)
    keyboard.add(key_k)
    keyboard.add(key_menu)
    return keyboard

def repeatEmptyKeyboard():
    keyboard = types.InlineKeyboardMarkup()
    key_menu = types.InlineKeyboardButton(text='Меню', callback_data='menu')
    key_k = types.InlineKeyboardButton(text='Обновить', callback_data='dkn')
    keyboard.add(key_k)
    keyboard.add(key_menu)
    return keyboard

def AMEmptyKeyboard():
    keyboard = types.InlineKeyboardMarkup()
    key_menu = types.InlineKeyboardButton(text='Меню', callback_data='menu')
    keyboard.add(key_menu)
    return keyboard

def AMKeyboard(typeShow):
    key_show = types.InlineKeyboardButton(text='Cкрыть перевод', callback_data='show')
    keyboard = types.InlineKeyboardMarkup()
    if typeShow == 'hide':
        key_show = types.InlineKeyboardButton(text='Показать перевод', callback_data='hide')
    key_no = types.InlineKeyboardButton(text='Далее', callback_data='kn')
    key_k = types.InlineKeyboardButton(text='Не помню слово', callback_data='dkn')
    key_menu = types.InlineKeyboardButton(text='Меню', callback_data='menu')


    keyboard.add(key_show)
    keyboard.add(key_no)
    keyboard.add(key_k)
    keyboard.add(key_menu)
    return keyboard
def addwordKeyboard():
    keyboard = types.InlineKeyboardMarkup()
    key_k = types.InlineKeyboardButton(text='Обновить', callback_data='dkn')
    key_add = types.InlineKeyboardButton(text='Добавить слов', callback_data='addword')
    key_menu = types.InlineKeyboardButton(text='Меню', callback_data='menu')


    keyboard.add(key_add)
    keyboard.add(key_k)
    keyboard.add(key_menu)
    return keyboard

def helpKeyboard():
    keyboard = types.InlineKeyboardMarkup()
    key_Rememb = types.InlineKeyboardButton(text='Вперед', callback_data='Hnext')
    key_Repeat = types.InlineKeyboardButton(text='Назад', callback_data='Hback')
    key_Stat = types.InlineKeyboardButton(text='Меню', callback_data='menu')

    keyboard.add(key_Rememb)
    keyboard.add(key_Repeat)
    keyboard.add(key_Stat)
    return keyboard

def menuKeyboard():
    global key_show
    keyboard = types.InlineKeyboardMarkup()
    key_Rememb = types.InlineKeyboardButton(text='Запоминание', callback_data='learn')
    key_Repeat = types.InlineKeyboardButton(text='Повторение', callback_data='repeat')
    key_Learned = types.InlineKeyboardButton(text='Выученные', callback_data='learned')
    key_Help = types.InlineKeyboardButton(text='Как пользоваться', callback_data='help')
    key_Stat = types.InlineKeyboardButton(text='Cтатистика', callback_data='statToday')

    keyboard.add(key_Rememb)
    keyboard.add(key_Repeat)
    keyboard.add(key_Learned)
    keyboard.add(key_Help)
    keyboard.add(key_Stat)
    return keyboard


def statKeyboard():
    global key_show
    keyboard = types.InlineKeyboardMarkup()
    key_statToday = types.InlineKeyboardButton(text='За сегодня', callback_data='statToday')
    key_statAll = types.InlineKeyboardButton(text='За все время', callback_data='statAll')
    key_menu = types.InlineKeyboardButton(text='Меню', callback_data='menu')
    keyboard.add(key_statToday)
    keyboard.add(key_statAll)
    keyboard.add(key_menu)
    return keyboard
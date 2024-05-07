import sqlite3
import datetime
import divword as div


def strToTime(a): # функция, для преобразования времени из базы, к типу, с которым сможет взаимодействовать программа

    a = [list(map(int, str(a).split()[0].split('-'))),
         list(map(int, list(map(float, str(a).split()[1].split(':')))))]
    return datetime.datetime(a[0][0], a[0][1], a[0][2], a[1][0], a[1][1], a[1][2])


def strToDate(a): # функция, для преобразования времени из базы, к типу, с которым сможет взаимодействовать программа
    a = a[:10]
    a = [list(map(int, str(a).split()[0].split('-'))),
         list(map(int, list(map(float, str(a).split('-')))))]
    return datetime.datetime(a[0][0], a[0][1], a[0][2])


###-------------------------------------------

def addNewUser(userid=''): # функция, которая выполняется, если пользователя нет в базе. Она добавляет таблицы в базу, для конкретного пользователя
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('SELECT id FROM Words ')
    results = cursor.fetchall()
    for i in results:
        cursor.execute('INSERT INTO UsersWord ( UserId, TypeList,IdWord) VALUES (?, ?, ?)', (userid, 'NW', *i))
    cursor.execute('INSERT INTO UsersStat ( Tdate, LearnedNew, Repeated, AlreadyKnown, UserId) VALUES (?, ?, ?, ?, ? )',
                   (str(datetime.datetime.now()), 0, 0, 0, userid,))
    connection.commit()
    connection.close()


def takelist(typelist, userid):# функция, которая берет из базы список слов и возвращает его
    listw = list()

    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('SELECT IdWord FROM UsersWord WHERE TypeList = (?) AND UserId = ?', (typelist, userid,))
    idwords = cursor.fetchall()
    for i in idwords:
        cursor.execute('SELECT id, engword, rusword FROM Words WHERE Words.id = (?)', (*i,))
        listw.append(*cursor.fetchall())
    return listw


def taketimes(userid):# функция, которая берет из базы список со временем, приводит к нужному типу и возвращает его
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('SELECT  IdWord, wTime, repeat FROM UsersWord WHERE wTime != (?) AND UserId = ?', ('NULL', userid,))
    wtimes = cursor.fetchall()
    wtimes = [list(wtimes[i]) for i in range(0, len(wtimes))]
    print(wtimes)
    for i in range(0, len(wtimes)):
        wtimes[i][1] = strToTime(wtimes[i][1])
    return wtimes


def takeStat(userid):# функция, которая берет статистику из базы и возвращает
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('SELECT  Tdate, LearnedNew, Repeated, AlreadyKnown FROM UsersStat WHERE UserId = ?', (userid,))
    ustat = cursor.fetchall()
    ustat = [list(ustat[i]) for i in range(0, len(ustat))]
    for i in range(0, len(ustat)):
        ustat[i][0] = strToDate(ustat[i][0])
    return ustat


def takeSize(userid):# функция, которая берет размер колоды для заучивания из базы
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('SELECT Sizedeck FROM UsersSizedeck WHERE Tdate = ? AND UserId = ?',
                   (str(datetime.datetime.today())[:10], userid,))
    usize = cursor.fetchall()
    # print(usize)
    return usize[0][0]


def setSize(userid, SD):# функция, которая закидывает в базу размер колоды
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute(
        'UPDATE UsersSizedeck SET Sizedeck = ? WHERE Tdate = ? AND UserId = ?',
        (SD, str(datetime.datetime.now())[:10], userid,))
    connection.commit()
    connection.close()


def setStat(userid, LearnedNew, Repeated, AlreadyKnown): # функция, которая записывает статистику в базу
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute(
        'UPDATE UsersStat SET Tdate = ?, LearnedNew = ?, Repeated = ?, AlreadyKnown = ? WHERE Tdate = ? AND UserId = ?',
        (str(datetime.datetime.now())[:10], LearnedNew, Repeated, AlreadyKnown, str(datetime.datetime.now())[:10],
         userid,))
    connection.commit()
    connection.close()


def changelist(idw, typenewlist, userid, repeat = 0, dateT=''): # функция, которая меняет инфу по словам
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    if typenewlist == 'RW':
        print((typenewlist, str(dateT), repeat, idw, userid,))
        cursor.execute('UPDATE UsersWord SET TypeList = ?, wTime = ?, repeat = ? WHERE IdWord = ? AND UserId = ?',
                       (typenewlist, str(dateT), repeat, idw, userid,))
    elif typenewlist == 'AM':
        cursor.execute('UPDATE UsersWord SET TypeList = ?, wTime = ?, repeat = ? WHERE IdWord = ? AND UserId = ?',
                       (typenewlist, None, None, idw, userid,))
    else:
        cursor.execute('UPDATE UsersWord SET TypeList = ? WHERE IdWord = ? AND UserId = ?',
                       (typenewlist, idw, userid,))  ########
    connection.commit()
    connection.close()


def checkNewUser(userid): # функция, проверяет, новый ли пользователь и есть ли у него сохраненный размер колоды на сегодня
    connection = sqlite3.connect('database.db')# размер колоды - это количество слов, которые учатся в разделе заучивания, сначала их пять, а потом можно добавить еще
    cursor = connection.cursor()
    cursor.execute('SELECT UserId FROM UsersWord WHERE UserId = ?', (userid,))
    results = cursor.fetchall()
    if (len(results) == 0):
        addNewUser(userid)
    cursor.execute('SELECT Tdate FROM UsersSizedeck WHERE Tdate = ? AND UserId = ?',
                   (str(datetime.datetime.now())[:10], userid,))
    results = cursor.fetchall()
    if (len(results) == 0):
        cursor.execute('INSERT INTO UsersSizedeck ( UserId, Tdate,Sizedeck) VALUES (?, ?, ?)',
                       (userid, str(datetime.datetime.now())[:10], 5))
    if (strToDate(str(sorted(takeStat(userid), key=lambda x: x[0])[0][0])) < strToDate(str(datetime.datetime.now())[:10])):
        cursor.execute('INSERT INTO UsersStat (Tdate, LearnedNew, Repeated, AlreadyKnown, UserId) VALUES (?, ?, ?, ?, ?)',
                       (str(datetime.datetime.now())[:10], 0, 0, 0, userid,))

    connection.commit()
    connection.close()


# addNewUser()
# checkNewUser('4')
# 4

def resetbase(userid):# функция, которая сбрасывает базу данных для пользователя
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('DELETE FROM UsersWord WHERE UserId = ?', (userid,))
    cursor.execute('DELETE FROM UsersStat WHERE UserId = ?', (userid,))
    cursor.execute('DELETE FROM UsersSizedeck WHERE UserId = ?', (userid,))
    connection.commit()
    connection.close()


def createbase(): # функция,которая создает все пустые базы данных(если удалить всю базу, нужно запустить эту функцию и она обратно появится)
    # Устанавливаем соединение с базой данных
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    # Создаем таблицу Words со словами
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Words (
    id INTEGER PRIMARY KEY,
    engword TEXT NOT NULL,
    rusword TEXT NOT NULL
    )
    ''')

    # Создаем таблицу Users с прогрессом каждого пользователя по словам
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS UsersWord (
    id INTEGER PRIMARY KEY,
    UserId INTEGER NOT NULL,
    TypeList TEXT NOT NULL,
    IdWord INTEGER,
    wTime TEXT,
    repeat INTEGER 
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS UsersStat (
    id INTEGER PRIMARY KEY,
    UserId INTEGER NOT NULL,
    Tdate TEXT,
    LearnedNew INTEGER,
    Repeated INTEGER,
    AlreadyKnown INTEGER
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS UsersSizedeck (
    id INTEGER PRIMARY KEY,
    UserId INTEGER NOT NULL,
    Tdate TEXT,
    Sizedeck INTEGER
    )
    ''')

    # Сохраняем изменения и закрываем соединение
    connection.commit()
    connection.close()


createbase()

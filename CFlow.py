import sql as sql
import random
import datetime
import time



def calcTime(time): # функция, которая преобразует данные для программы, в данные для вывода в бота


    time = str(time)[:19]
    print(time)
    a = (datetime.datetime.strptime(str(time)[:10], '%Y-%m-%d') -
             datetime.datetime.strptime(str(datetime.datetime.now())[:10], '%Y-%m-%d'))
    b = (datetime.datetime.strptime(str(time)[11:], '%H:%M:%S') -
             datetime.datetime.strptime(str(datetime.datetime.now())[11:-7], '%H:%M:%S'))
    s = a.total_seconds() + b.total_seconds()
    return list(map(int, [s // 86400,(s % 86400) //  (60*60), (s % 86400) //  60 % 60, (s % 86400) % 60]))


def checkRepeat(wordWithTime):# функция, которая проверяет время уже прошло или нет
    if wordWithTime[1] < datetime.datetime.now():
        return True
    else:
        return False

# класс, в котором происходит весь механизм по словам
class Flow:
    def __init__(self, userid):# конструктор класса, принимает айди пользователя
        self._userid = userid

        # это списки, в которых хранятся все слова
        self.NW = sql.takelist('NW', self._userid)  ##0 - эта цифра это код группы  ▪NW - это новые слова
        self.AM = sql.takelist('AM', self._userid)  ##1      AM - это уже известные   🟩
        self.MW = sql.takelist('MW', self._userid)  ##2        MW -это ⬜ заучиваемые
        self.RW = sorted(sql.takelist('RW', self._userid), key=lambda x: x[1])  ##3  RW - это повторение🔳
        # они записываются сюда сразу из базы данных
        self.addtimes()

        self.statToday = sorted(sql.takeStat(self._userid), reverse=True, key=lambda x: x[0])[0] # статистика
        self.statAll = sql.takeStat(self._userid) # тоже статистика
        self.mode = 'm'
        self.decksize = sql.takeSize(userid) # размер колоды
        self.deck = list() # список, который определяет порядок выбора слова
        self.makeflow()

    def getStat(self, mode): # функция, функция, которая выдает статистику
        alltimestat = [x[1:] for x in self.statAll]
        if mode == 'today':
            return "За Сегодня:\n\nВыучено новых: {}\nПовторено: {}\nУже известно: {}\nОсталось: {}\n".format(
                self.statToday[1], self.statToday[2], self.statToday[3], 1000 - sum([sum(x) for x in zip(*alltimestat)]))
        if mode == 'alltime':
            return "За Все время:\n\nВыучено новых: {}\nПовторено: {}\nУже известно: {}\nОсталось: {}\n".format(
                [sum(x) for x in zip(*alltimestat)][0], [sum(x) for x in zip(*alltimestat)][1],
                [sum(x) for x in zip(*alltimestat)][2], 1000 - sum([sum(x) for x in zip(*alltimestat)]))


    @staticmethod
    def setRepTime(repeat):  # функция, которая меняет время в зависимости от повтореня слова
        if repeat == 1:
            return datetime.datetime.now() + datetime.timedelta(0, 1200)
        if repeat == 2:
            return datetime.datetime.now() + datetime.timedelta(0, 28800)
        if repeat == 3:
            return datetime.datetime.now() + datetime.timedelta(0, 86400)
        if repeat == 4:
            return datetime.datetime.now() + datetime.timedelta(0, 259200)
        if repeat == 5:
            return datetime.datetime.now() + datetime.timedelta(0, 345600)
        if repeat == 6:
            return datetime.datetime.now() + datetime.timedelta(0, 604800)
        return 'NULL'

    def addtimes(self): # функция, которая добавляет времена к каждому слову в репит
        times = sql.taketimes(self._userid)

        for i in range(0, len(self.RW)):
            for j in times:
                if j[0] == self.RW[i][0]:
                    self.RW[i] = [self.RW[i], j[1], j[2]]

    def RWlen(self): # функция, которая возвращает количество годных к выдаче слов из списка повторения
        count = 0

        for i in range(0, len(self.RW)):
            if checkRepeat(self.RW[i]):
                count += 1
        return count

    def remembered(self): # функция, которая выполняет действия при нажатии кнопки  знаю

        if self.deck[0] == 0: # если это слово новое, те NW, то добавляет в заучиваемое
            sql.changelist(self.NW[0][0], 'AM', self._userid)
            self.AM.append(self.NW.pop(0))
            self.statToday[3] += 1

        elif self.deck[0] == 1: #если это слово уже известное, те AM, то кидает в конец списка
            self.AM.append(self.AM.pop(0))

        elif self.deck[0] == 2: #если это слово заучиваемое то кидает в повторение
            sql.changelist(self.MW[0][0], 'RW', self._userid, dateT=datetime.datetime.now())
            self.RW.append([list(self.MW.pop(0)), datetime.datetime.now(), 0])
            self.statToday[1] += 1

        elif self.deck[0] == 3:# ну у повторения два случая, либо выучилось слово, либо нет, от этого зависит, попадет ли оно в
            if self.RW[0][2] >= 6: # уже известное или нет
                self.RW[0][2] += 1
                sql.changelist(self.RW[0][0], 'AM', self._userid)
                self.AM.append(self.RW.pop(0)[0])
                self.statToday[3] += 1
            else:
                self.RW[0][2] += 1
                self.RW[0][1] = self.setRepTime(self.RW[0][2])
                if self.RW[0][0] != 0:
                    sql.changelist(self.RW[0][0][0], 'RW', self._userid, self.RW[0][2], self.RW[0][1])
                self.RW.append(self.RW.pop(0))
                self.statToday[2] += 1

        return self.nextword()

    @property
    def forgot(self):# функция, которая выполняет действия при нажатии кнопки  не знаю
        if self.deck[0] == 0: # тут в принципе все логично, те же действия, которые написаны в хелп(как пользоваться)
            sql.changelist(self.NW[0][0], 'MW', self._userid)
            self.MW.append(self.NW.pop(0))

        elif self.deck[0] == 1:
            sql.changelist(self.AM[0][0], 'MW', self._userid)
            self.MW.append(self.AM.pop(0))

        elif self.deck[0] == 2:
            self.MW = ([self.MW[0]] + random.sample(self.MW[1:], len(self.MW[1:])))[::-1]

        elif self.deck[0] == 3:
            self.RW.append(self.RW.pop(0))
        sql.setSize(self._userid, self.decksize)
        sql.setStat(self._userid, self.statToday[1], self.statToday[2], self.statToday[3])
        return self.nextword()

    def update(self):# функция, которая записывает обновленные данные в базу, те сохраняет их
        for i in self.NW:
            sql.changelist(i[0], 'NW', self._userid)

        for i in self.AM:
            sql.changelist(i[0], 'AM', self._userid)

        for i in self.MW:
            sql.changelist(i[0], 'MW', self._userid)

        for i in self.RW:
            if self.RW[0][0] != 0:
                sql.changelist(i[0][0], 'RW', self._userid, self.RW[0][2], self.RW[0][1])
        sql.setSize(self._userid, self.decksize)
        sql.setStat(self._userid, self.statToday[1], self.statToday[2], self.statToday[3])

    def nextword(self): # функция, которая выдает следующее слово, используется в знаю и не знаю
        self.makeflow()
        self.RW = sorted(self.RW, key=lambda x: x[1])
        if not ((self.deck[0] == 3 and self.RWlen() == 0) or self.deck[0] == 1 or self.deck == [2,0]):
            self.deck.pop(0)
        time.sleep(0.2)
        # self.update()
        return self.takeword

    def makeflow(self): # функция, которая создает поток слов, определяет колоду в зависимости от режима
        if self.mode == 'm':
            self.deck = list()

            if (self.decksize - self.statToday[1]) > 0:
                for j in range(0, len(self.MW)):
                    self.deck.append(2)

                for j in range(0, self.decksize - self.statToday[1] - len(self.MW)+1):
                    self.deck.append(0)

            else:
                self.deck = [4 for i in range(0, 2)]

        if self.mode == 'r':
            if not self.RWlen():
                self.deck = [4 for i in range(0, 2)]

            else:
                self.deck = [3 for i in range(0, self.RWlen()+1)]

        if self.mode == 'l':
            self.deck = [1]


        if(len(self.deck)>2):
            random.shuffle(self.deck)


    def repeatIsEmpty(self):# функция, которая проверяет пуст ли список репит или нет
        if sorted(self.RW, key=lambda x: x[1])[0][1] < datetime.datetime.now():
            return False

        else:
            return True

    @property
    def takeword(self):# Функция, которая выдает слово которое верхнее в колоде, типо, если в deck[0] лежит 0, то выдает новое слово, если 2, то слово для заучивания

        if self.deck[0] == 0:
            return [self.NW[0]] + ['▪New word'] + ['']

        elif self.deck[0] == 1:
            if len(self.AM) == 0:
                return [(0, "пусто", " ;(")] + [''] + ['']
            else:
                return [self.AM[0]] + ['🟩Already known'] + ['']

        elif self.deck[0] == 2:
            return [self.MW[0]] + ['⬜Memorization word'] + ['']

        elif self.deck[0] == 3:

            if not(self.repeatIsEmpty()):
                print(checkRepeat(self.RW[0]),self.RW[0])
                if checkRepeat(self.RW[0]):

                    return [self.RW[0][0]] + ['🔳Repeat word'] + ['r:'.format(self.RW[0][2])]
                else:
                    return [(0, "пусто", " ;(")] + [''] + ['']

        elif self.deck[0] == 4:
            if self.mode == 'r':
                try:
                    nearTime = calcTime(sorted(self.RW,key=lambda x: x[1])[0][1])

                    if not(nearTime[0]):
                        return [(0, "пусто", " ;(")] + [
                            'Повторение через: {}:{}:{}'.format(nearTime[1], nearTime[2], nearTime[3])] + ['']
                    else:
                        return [(0, "пусто", " ;(")] + [
                            'Повторение через: {}d {}:{}:{}'.format(nearTime[0], nearTime[1], nearTime[2], nearTime[3])] + [
                            '']
                except:
                    return [(0, "пусто", " ;(")] + [''] + ['']

            if self.mode == 'm':
                return [(0, "пусто", " ;(")] + [
                    'Выучено сегодня: {} слов'.format(self.statToday[1])] + ['']


#228
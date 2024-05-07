import sql as sql
import CFlow
import sqlite3
import datetime



# Класс, который соединяет в себе всю работу со словами, по факту является каркасом приложения, а в мэйн просто его интерфейс
class Wordik():
    def __init__(self, decksize = 5, userid=0):# конструктор класса, который принимает сколько слов учить в день и айди пользователя
        self.userid = userid
        self.checkUser()
        self.flow = CFlow.Flow(userid)
        self.word = ''

    def getMenu(self):# слова для меню
        return 'Привет, меня зовут wordik, я бот, который поможет тебе выучить английские слова.'
    def takeword(self): # берет слово из флоу и запоминает, а также возвращает его
        self.word = self.flow.takeword
        return self.word

    def remembered(self): # это кнопка знаю
        print('знаю 1', str(datetime.datetime.now()))
        self.word = self.flow.remembered()
        return self.word

    def forgot(self): # это кнопка не знаю
        self.word = self.flow.forgot
        return self.word

    def changeMode(self, mode):# меняет режим(из заучивания в повторения и тд)
        self.flow.mode = mode
        self.flow.makeflow()
        print(self.flow.deck,self.flow.mode)
    @property
    def userid(self): # возвращает айди
        return self._userid

    @userid.setter
    def userid(self, newid): # меняет айди
        self._userid = newid

    def checkUser(self): # проверяет пользователя, подробнее в файле скл
        sql.checkNewUser(self.userid)

    @staticmethod
    def createbase(): # подробнее в файле скл
        sql.createbase()

    def takelist(self, typelist):
        return sql.takelist(typelist, self._userid)

    def changelist(self, idw, typelist):
        return sql.changelist(idw, typelist, self._userid)

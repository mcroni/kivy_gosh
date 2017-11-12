from peewee import *
import peewee as pw
##db = SqliteDatabase('peewee.sqlite')
myDB = pw.MySQLDatabase("****", host="****.com", port=3306, user="ahmedpar_cro", passwd="******")

class Testify(Model):
    name = CharField()
    message = CharField()

    class Meta:
        database = myDB

    
class PrayerRequest(Model):
    name = CharField()
    prayer_request = CharField()

    class Meta:
        database = myDB


class PastorsCircle(Model):
    name = CharField()
    password = CharField()

    class Meta:
        database = myDB

    
class Announcementss(Model):
    message = CharField()

    class Meta:
        database = myDB


class DailyGuide(Model):
    title = CharField()
    message = CharField()

    class Meta:
        database = myDB


class Quotations(Model):
    name = CharField()
    quotes = CharField()

    class Meta:
        database = myDB


class Calen(Model):
    time = CharField()
    event = CharField()

    class Meta:
        database = myDB


class Person(Model):
    name = CharField()
    number = IntegerField()

    class Meta:
        database = myDB
##myDB.connect()


# db.create_tables([Person])
#db.create_tables([Testify,PrayerRequest,
               # PastorsCircle,Announcementss,DailyGuide,Quotations,Calen])

print('\\\\ Peewee is Working ///////')

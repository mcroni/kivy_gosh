from kivy.lib import osc
from random import sample, randint
from string import ascii_letters
from time import localtime, asctime, sleep
from kivy.storage.jsonstore import JsonStore
import peewee
from models_sql import *
store = JsonStore('count.json')
from os.path import dirname
from os.path import join
from os.path import realpath
from plyer import notification
from plyer.utils import platform
from plyer.compat import PY2
from plyer import vibrator



def ping(*args):
    count = 0
    try:
        for message in Announcementss.select():
            count += 1
        print count
        if count == store.get('announcements')['count']:
            print 'yeah'
            osc.sendMsg(
                '/message',
                [''.join('yeah'), ],
                port=3002)
        else:
            kwargs = {'title': 'hey', 'message': 'New Devotion in ', 'ticker': 'New Devotion','timeout':4}
            print 'nah'
            store.put('announcements',count=count)
            notification.notify(**kwargs)
            vibrator.vibrate(.5)
    except peewee.OperationalError:
        print('cant connect')
    else:
        pass



def send_date():
    osc.sendMsg('/date', [asctime(localtime()), ], port=3002)


if __name__ == '__main__':
    osc.init()
    oscid = osc.listen(ipAddr='0.0.0.0', port=3000)
    osc.bind(oscid, ping, '/ping')
    while True:
        osc.readQueue(oscid)
        send_date()
        ping()
        sleep(10)

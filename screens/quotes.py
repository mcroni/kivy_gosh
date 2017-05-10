from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty
from kivymd.list import TwoLineListItem
from kivy.metrics import dp
# from kivy.uix.image import AsyncImage
# from kivymd.list import ILeftBody
from packs import peewee
import thread
from threading import Thread
from kivymd.dialog import MDDialog
from kivymd.label import MDLabel
from packs.models_sql import *
import time
import kivymd.snackbar as Snackbar
from kivy.clock import Clock
import time
from kivymd.toast import Toast
# Clock.max_iterations= 100
""" chale release this lines when ready to deploy
this will activate the share intent in android"""
from jnius import autoclass
PythonActivity = autoclass('org.renpy.android.PythonActivity')
Intent = autoclass('android.content.Intent')
String = autoclass('java.lang.String')

# from __future__ import print_function

class Foo(object):
    def start(self):
        # thread.start_new_thread(self.callback,('name,'))
        thread.start_new_thread(self.callback,('name',))

    def callback(self,dt):
        # print ';;;;'
        Snackbar.make('damn')


class Quotes(Screen,FloatLayout):
    ml = ObjectProperty(None)
    scroller = ObjectProperty(None)

    def __init__(self,**kwargs):
        super(Quotes,self).__init__(**kwargs)

    def on_enter(self, *args):
        # Clock.schedule_once(self.go)
        Clock.schedule_once(self.load_announcements)

    def go(self,*args):
        # print ';adad'
        for i in range(1,100):
            time.sleep(1)
            print i

    def load_announcements(self,*largs):
        try:
            # foo = Foo()
            # foo.start()
            # Thread(target=lambda :print('hi'))
            # Thread(target=(lambda x: self.go()))
            # thread.start_new_thread(self.go,('nae',))
            # time.sleep(2)
            for quotes in Quotations.select():
                self.but = QuoteButton(text=str(quotes.name),secondary_text= str(quotes.quotes))
                # self.but.add_widget(Photo(source='./assets/tower.png'))
                # time.sleep(1)
                self.ids.ml.add_widget(self.but)
            self.ids.spinner.active = False

        except peewee.OperationalError:
            self.ids.spinner.active = True
            self.login_failure('No Network Connection')
            # Snackbar.make('Please Check Internet Connection\n or try Again')
        else:
            pass

    def _show_toast(self, text):
        self.ids['toast'].show(text)

    def login_failure(self, error):
        self._show_toast(error)


class QuoteButton(TwoLineListItem):
    def __init__(self,**kwargs):
        super(QuoteButton,self).__init__(**kwargs)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.pressed = touch.pos
            if touch.is_double_tap:
                print('doouble')
            else:
                content = MDLabel(font_style='Body1',
                                  theme_text_color='Secondary',
                                  text="{}".format(self.secondary_text),
                                  valign='top')

                content.bind(size=content.setter('text_size'))
                self.dialog = MDDialog(title="{}".format(self.text), content=content, size_hint=(.9, None),
                                       height=dp(200), auto_dismiss=False)

                self.dialog.add_action_button("Dismiss",
                                              action=lambda *x: self.dialog.dismiss())
                self.dialog.add_action_button("Share",
                                              action=lambda *x: self.share())
                self.dialog.open()
        super(QuoteButton, self).on_touch_down(touch)

    def share(self):
        print 'sharing'
        intent = Intent()
        intent.setAction(Intent.ACTION_SEND)
        intent.putExtra(Intent.EXTRA_TEXT, String('{}'.format(self.secondary_text)))
        intent.setType('text/plain')
        chooser = Intent.createChooser(intent, String('Share...'))
        PythonActivity.mActivity.startActivity(chooser)

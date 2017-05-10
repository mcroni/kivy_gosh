from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivymd.list import MDList
from kivy.properties import ObjectProperty
from kivymd.list import TwoLineListItem
from packs.models_sql import *
import thread
import time
from kivymd.dialog import MDDialog
from kivymd.label import MDLabel
from kivy.metrics import dp
from kivy.uix.floatlayout import FloatLayout
from packs import peewee
from kivy.clock import Clock
# import kivymd.snackbar as Snackbar
from kivymd.toast import Toast

class F(Popup):
    shiermor_button = ObjectProperty(None)
    def __init__(self, **kwargs):
        super(F, self).__init__(**kwargs)

    def shiermor_thread(self):
        thread.start_new_thread(self.shiemor,('dbb',))

    def shiemor(self,dbb):
        testi_name = self.ids.name.text
        testi_message = self.ids.message.text
        if len(testi_name)== 0:
            self.ids.shiermor_button.text = 'Try Again'
        if len(testi_message)== 0:
            self.ids.shiermor_button.text = 'Try Again'

        else:
            try:
                time.sleep(1)
                self.ids.spinner.active =True
                self.ids.shiermor_button.text='Sending'
                testify = Testify(name=testi_name,message=testi_message)
                testify.save()

                self.dismiss()
            except peewee.OperationalError:
                self.ids.spinner.active = False
                self.ids.shiermor_button.text = 'Plz Try Again'
                # Snackbar.make('Check Internet Connection',4)
                self.login_failure('Check Internet Connection')
            else:
                pass


    def _show_toast(self, text):
        self.ids['toast'].show(text)

    def login_failure(self, error):
        self._show_toast(error)


class Testimonies(Screen, BoxLayout):
    def __init__(self, **kwargs):
        super(Testimonies, self).__init__(**kwargs)

    def thread_read(self):
        # thread.start_new_thread(self.read,('dbb',))
        Clock.schedule_once(self.read)

    def read(self,*largs):
        content = FloatLayout()
        scroll = ScrollView()
        mdlist = MDList()
        content.add_widget(scroll)
        scroll.add_widget(mdlist)
        title = "Testimonies"
        pop = Popup(title= title,content= content,)
        pop.open()
        try:
            for message in Testify.select():
                time.sleep(0.50)
                mdlist.add_widget(PopList(text=str(message.name),secondary_text=str(message.message)))
            print('reading testimonies')
        except peewee.OperationalError:
            self.login_failure('Check Network Connection')
            # mdlist.add_widget(PopList(text=str('Error'), secondary_text=str('Please Check Internet Connection')))

    def share(self):
        pop = F()
        pop.open()

    def _show_toast(self, text):
        self.ids['toast'].show(text)

    def login_failure(self, error):
        self._show_toast(error)



class PopList(TwoLineListItem):
    def __init__(self,**kwargs):
        super(PopList,self).__init__(**kwargs)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.pressed = touch.pos
            print(str(self.text))
            content = MDLabel(font_style='Body1',
                          theme_text_color='Secondary',
                          text="{}".format(self.secondary_text),
                          size_hint_y=None,
                          valign='top')
            content.bind(texture_size=content.setter('size'))
            self.dialog = MDDialog(title="{}".format(self.text),
                                   content=content,
                                   size_hint=(.9, None),
                                   height=dp(300),
                                   auto_dismiss=False)

            self.dialog.add_action_button("Dismiss",
                                          action=lambda *x: self.dialog.dismiss())
            self.dialog.open()

        super(PopList, self).on_touch_down(touch)

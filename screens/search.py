from kivy.uix.screenmanager import Screen
from kivymd.list import TwoLineListItem
from packs.models_sql import Person
from plyer import call
from plyer import vibrator
import thread
from packs import peewee
from kivymd.toast import Toast

class Search(Screen):
    def __init__(self, **kwargs):
        super(Search, self).__init__(**kwargs)

    lists_of_names = []

    def loader(self):
        thread.start_new_thread(self.load, ('name',))
        self.ids.search_input.bind(text=self.some_func)

    def load(self,name):
        temp = '0'
        try:
            for name in Person.select():
                self.ids.ml.add_widget(CallerButton(text=name.name, secondary_text= temp + str(name.number)))
                contact = []
                contact.append(name.name)
                contact.append(name.number)
                self.lists_of_names.append(contact)
            print(self.lists_of_names)
            self.ids.spinner.active = False
        except peewee.OperationalError:
            self.login_failure('Try Again')

    tem = '0'

    def some_func(self, *args):
        returned_name = self.ids.search_input.text
        print(returned_name)
        self.ids.ml.clear_widgets()
        for name in self.lists_of_names:
            if name[0].startswith(returned_name):
                print('yea')
                numm = self.tem + str(name[1])
                print(numm)
                self.ids.ml.add_widget(CallerButton(text=str(name[0]),secondary_text=numm))

        if len(self.ids.ml.children) == 0:
            self.login_failure('Person not Found')

    def _show_toast(self, text):
        self.ids['toast'].show(text)

    def login_failure(self, error):
        self._show_toast(error)


class CallerButton(TwoLineListItem):
    def __init__(self,**kwargs):
        super(CallerButton,self).__init__(**kwargs)

    def on_touch_down(self,touch):
        if self.collide_point(*touch.pos):
            self.pressed = touch.pos
            number =self.secondary_text
            print(number)
            tel = number
            vibrator.vibrate(.3)
            call.makecall(tel=tel)
            return True
        return super(CallerButton, self).on_touch_down(touch)


from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen
from packs.models_sql import *
# from kivymd.toast import Toast
from packs import peewee
import thread
import time


class Requests(Screen):
    name = ObjectProperty(None)
    prayer = ObjectProperty(None)

    def add_thread(self):
        thread.start_new_thread(self.add_request,('dbb',))

    def _show_toast(self, text):
        self.ids['toast'].show(text)

    def login_failure(self, error):
        self._show_toast(error)

    def add_request(self,dbb):
        name_text = self.ids.name.text
        prayer_text = self.ids.prayer.text

        if len(name_text) == 0:
            self.login_failure('Empty Slot')
        if len(prayer_text) == 0:
            self.login_failure('Empty Slot')
        else:
            try:
                self.ids.spinner.active = True
                time.sleep(2)
                add_request = PrayerRequest(name=name_text, prayer_request=prayer_text)
                add_request.save()
                self.ids.name.text = ""
                self.ids.prayer.text = ''
                self.ids.spinner.active = False
                print("committed")
                self.login_failure('Request Sent')
            except peewee.OperationalError:
                self.ids.spinner.active = False
                self.ids.float_act_btn.text = 'Try Again'
                self.login_failure('Check Connection')
            else:
                pass




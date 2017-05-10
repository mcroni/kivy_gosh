from kivy.uix.screenmanager import Screen
from kivymd.list import TwoLineListItem
from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.storage.jsonstore import JsonStore
store = JsonStore('tithe_card.json')

months_list = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']


class TitheViewer(Screen):
    ml = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(TitheViewer, self).__init__(**kwargs)

    def adder(self):
        self.ml.clear_widgets()
        for month in months_list:
            for item in store.find(month=month):
                month = item[1]['month']
                amount = item[1]['amount']
                print month,amount
            self.ml.add_widget(TwoLineListItem(text=str(month),
                                                   secondary_text=str(amount)))

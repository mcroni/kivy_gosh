from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.storage.jsonstore import JsonStore
from kivy.uix.effectwidget import EffectWidget


class Tithe(Screen,EffectWidget):
    grid = ObjectProperty(None)

    def __init__(self,**kwargs):
        super(Tithe,self).__init__(**kwargs)

    def adder(self):
        months_list = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
        for month in months_list:
            self.grid.add_widget(TitheButton(text=month,on_pressed = lambda x: self.add_tithe()))


class TitheButton(Button):
    def __init__(self,**kwargs):
        super(TitheButton,self).__init__(**kwargs)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.pressed = touch.pos
            print('touched',self.text)
            self.add_tithe()
        return super(TitheButton, self).on_touch_down(touch)

    def add_tithe(self):
        p = TithePopup()
        p.title= self.text
        p.open()

store = JsonStore('tithe_card.json')


class TithePopup(Popup):
    amount = ObjectProperty(None)

    def __init__(self,**kwargs):
        super(TithePopup,self).__init__(**kwargs)

    def on_add(self):
        print('called me',self.title)
        kudi = self.amount.text
        try:
            original = float(kudi)
            deduc = 10/100.0
            real = deduc * original
            cr = ("%.02f" % real)
            print(cr)
            month = self.title
            old_amount = 0
            for item in store.find(month='{}'.format(month)):
                old_amount = item[1]['amount']
                print old_amount
            new_amount = float(cr) + old_amount
            print new_amount
            store.put("{}".format(month), month="{}".format(month), amount= new_amount)
            self.dismiss()

        except ValueError:
            print('enter a figure')
            self.amount.text = ''
            self.amount.hint_text='sorry,enter an amount'
        else:
            pass


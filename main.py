from kivy.app import App
from kivy.metrics import dp
from kivy.core.window import Window as Win
from kivy.properties import ObjectProperty

from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen,ScreenManager

from kivymd.button import MDIconButton
from kivymd.list import ILeftBody, ILeftBodyTouch, IRightBodyTouch
from kivymd.navigationdrawer import NavigationDrawer
from kivymd.theming import ThemeManager

from screens.testimonies import *
from screens.request import *
from screens.sermons import *
from screens.guide import *
from screens.pastors import *
from screens.tithe import *
from screens.tithe_viewer import *
from screens.search import *
from screens.quotes import *
from screens.gallery import *

from kivy.utils import platform
from kivy.lib import osc
from kivy.clock import Clock

class AvatarSampleWidget(ILeftBody, Image):
    pass


class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)


class GbeeRoot(BoxLayout):
    def __init__(self,**kwargs):
        super(GbeeRoot,self).__init__(**kwargs)
        self.screen_list = []

    def next_screen(self, neoscreen):
        self.screen_list.append(self.ids.gbee_screen_manager.current)
        print(self.screen_list)

        if self.ids.gbee_screen_manager.current == neoscreen:
            cur_screen = self.ids.gbee_screen_manager.get_screen(neoscreen)
        else:
            self.ids.gbee_screen_manager.current = neoscreen

    def go_to(self, neoscreen):
        self.ids.gbee_screen_manager.current = neoscreen

    def onBackBtn(self):
        # check if there are screens we can go back to
        if self.screen_list:
            currentscreen = self.screen_list.pop()
            self.ids.gbee_screen_manager.current = currentscreen
            # Prevents closing of app
            return True
        # no more screens to go back to, close app
        return False

class Drawer(NavigationDrawer):
    def __init__(self,**kwargs):
        super(Drawer, self).__init__(**kwargs)


class IconLeftSampleWidget(ILeftBodyTouch, MDIconButton):
    pass


class Jarvis(App):
    theme_cls = ThemeManager()
    nav_drawer = ObjectProperty()

    def __init__(self, **kwargs):
        super(Jarvis, self).__init__(**kwargs)
        Win.bind(on_keyboard=self.onBackBtn)

    def build(self):
        self.title = "GoshenApp"
        #from kivy.core.window import Window
        #Window.size = (450, 600)
        #self.service = None
        self.start_service()
        osc.init()
        oscid = osc.listen(port=3002)
        osc.bind(oscid, self.display_message, '/message')
        Clock.schedule_interval(lambda *x: osc.readQueue(oscid), 0)
        self.theme_cls.theme_style = 'Dark'
        self.theme_cls.primary_palette = 'Indigo'
        self.nav_drawer = Drawer()
        return GbeeRoot()
    
    def display_message(self, message, *args):
        print 'received'
        
    def onBackBtn(self, window, key, *args):
        if key == 27:
            return self.root.onBackBtn()
        
    def start_service(self):
        if platform == 'android':
            import android
            android.start_service(title='goshen_app',
                                  description='hello',arg='')
            #from android import AndroidService
            #service = AndroidService()
            #service.start('Gosh')
            #self.service = service
            
    def on_pause(self):
        return True

    def on_resume(self):
        pass

if __name__=="__main__":
    Jarvis().run()

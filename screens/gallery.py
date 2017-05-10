from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen
from kivymd.grid import SmartTileWithLabel2
from kivy.clock import Clock
import requests
import webbrowser
from packs.ehp import Html
import time
import thread

class Gallery(Screen):
    grid = ObjectProperty(None)
    passed = []

    def __init__(self,**kwargs):
        super(Gallery,self).__init__(**kwargs)

    def load(self):
        # thread.start_new_thread(self.list_files,('name',))
        Clock.schedule_once(self.list_files)

    def _show_toast(self, text):
        self.ids['toast'].show(text)

    def login_failure(self, error):
        self._show_toast(error)

    def go(self,*args):
        self.ids.spinner.active = True

    def list_files(self, *largs):
        print('display thread')
        self.ids.grid.clear_widgets()
        # self.ids.spinner.active = True
        url = 'http://ahmedpartey.com/assets/images/'
        try:
            r = requests.get(url)
            thread.start_new_thread(self.go,('name',))
        except requests.exceptions.ConnectionError:
            print('cant connect')
            # self.ids.spinner.active = False
            self.login_failure('Connection Error')

        else:
            d = requests.get(url)
            o = d.text
            dom = Html().feed(o)
            for ind in dom.find('a'):
                if ind.text()[-4:] == '.jpg':
                    self.passed.append(str(ind.text()))
            self.ids.spinner.active = False

            # print(self.passed)
            for pic in self.passed:
                src = 'http://ahmedpartey.com/assets/images/{}'.format(pic)
                # print(src)
                # self.p.append(src)
                self.album = SM(source=str(src))
                self.ids.grid.add_widget(self.album)
            self.ids.spinner.active = False
            # print(self.links)


class SM(SmartTileWithLabel2):
    def __init__(self,**kwargs):
        super(SM,self).__init__(**kwargs)

    def load(self):
        # thread.start_new_thread(self.save, ('name',))
        Clock.schedule_once(self.save)

    def save(self,*largs):
        print(self.source)
        """lets reserve u for v1.1, add folder functionality so that
        the images gets stored in a special gbee folder"""
        print 'downloading'
        webbrowser.open(self.source)
        # except ConnectionError:
        #     print 'cant download'
        #
        #     # filename = self.source[35:]
        # r = requests.get(self.source)
        # i = PI.open(BytesIO(r.content))
        # i.save(filename)
        # print('downloaded', filename)
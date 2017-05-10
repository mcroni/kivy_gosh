from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen
from kivymd.list import OneLineAvatarListItem
from kivy.core.audio import SoundLoader
from kivy.uix.popup import Popup
from kivy.uix.image import AsyncImage
from kivymd.list import ILeftBody
import thread
from kivy.clock import Clock
import webbrowser
import requests
from packs.ehp import Html
from kivymd.toast import Toast

# Clock.max_iteration = 100
# i did this to prevent the app from crashing when looping through the images


""" chale release this lines when ready to deploy
this will activate the share intent in android"""
from jnius import autoclass
PythonActivity = autoclass('org.renpy.android.PythonActivity')
Intent = autoclass('android.content.Intent')
String = autoclass('java.lang.String')


class AudioButton(OneLineAvatarListItem):
    def __init__(self,**kwargs):
        super(AudioButton,self).__init__(**kwargs)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.pressed = touch.pos
            print(str(self.text))
            a = DownPop(title=str(self.text))
            self.link = 'http://ahmedpartey.com/sermons/{}'.format(str(self.text))
            print(self.link)
            a.open()

        super(AudioButton, self).on_touch_down(touch)


class DownPop(Popup):
    def __init__(self,**kwargs):
        super(DownPop,self).__init__(**kwargs)
        self.source = 'http://ahmedpartey.com/sermons/{}'.format(str(self.title))

    def load_play(self):
        thread.start_new_thread(self.play, ('name',))

    def play(self,name):
        print 'playing'
        from jnius import autoclass
        from time import sleep
        MediaPlayer = autoclass('android.media.MediaPlayer')
        mPlayer = MediaPlayer()
        mPlayer.setDataSource('{}'.format(self.source))
        mPlayer.prepare()
        duration = mPlayer.getDuration()
        if self.ids.play_stop.text =='Play':
            # mPlayer.prepare()
            print 'play'
            self.ids.play_stop.text = 'Stop'
            mPlayer.start()
            # print 'current position:', mPlayer.getCurrentPosition()
            sleep(int(duration))
        elif self.ids.play_stop.text =='Stop':
            print 'stop'
            self.ids.play_stop.text = 'Play'
            # sleep(3)
            mPlayer.pause()

    def download(self):
        try:
            webbrowser.open(self.source)
        except webbrowser.Error:
            pass



    def share(self):
        from jnius import autoclass
        PythonActivity = autoclass('org.renpy.android.PythonActivity')
        Intent = autoclass('android.content.Intent')
        String = autoclass('java.lang.String')
        intent = Intent()
        intent.setAction(Intent.ACTION_SEND)
        intent.putExtra(Intent.EXTRA_TEXT, String('{}'.format(self.source)))
        intent.setType('text/plain')
        chooser = Intent.createChooser(intent, String('Share...'))
        PythonActivity.mActivity.startActivity(chooser)


class Sermons(Screen):
    scroller = ObjectProperty(None)
    grid = ObjectProperty(None)
    passed = []
    links = []

    def __init__(self, **kwargs):
        super(Sermons, self).__init__(**kwargs)

    def load(self):
        Clock.schedule_once(self.list_files)
        # thread.start_new_thread(self.list_files, ('name',))
        self.ids.search_input.bind(text=self.some_func)

    def go(self, *args):
        self.ids.spinner.active = True

    def list_files(self, *largs):
        print('display thread')
        self.ids.grid.clear_widgets()
        # self.ids.spinner.active = True
        url = 'http://ahmedpartey.com/sermons/'
        try:
            r = requests.get(url)
            thread.start_new_thread(self.go, ('name',))
        except requests.exceptions.ConnectionError:
            # print('cant connect')
            # self.ids.spinner.active = False
            self.login_failure('Connection Error')
            # Snackbar.make('Connection Error, Try Again')

        else:
            url = 'http://ahmedpartey.com/sermons/'
            d = requests.get(url)
            o = d.text
            dom = Html().feed(o)
            for ind in dom.find('a'):
                if ind.text()[-4:] == '.mp3':
                    self.passed.append(str(ind.text()))
            self.ids.spinner.active = False

            # print(self.passed)
            for track in self.passed:
                src = 'http://ahmedpartey.com/sermons/{}'.format(track)
                # print(src)
                self.links.append(src)
                self.album = AudioButton(text=str(track))
                self.album.add_widget(Photo(source='./assets/tower.png'))
                self.ids.grid.add_widget(self.album)
            self.ids.spinner.active = False
            # print(self.links)

    def _show_toast(self, text):
        self.ids['toast'].show(text)

    def login_failure(self, error):
        self._show_toast(error)

    def some_func(self, *args):
        returned_name = self.ids.search_input.text
        self.ids.grid.clear_widgets()
        for track in self.passed:
            if track.startswith(returned_name):
                self.album = AudioButton(text=str(track))
                self.album.add_widget(Photo(source='./assets/tower.png'))

                self.ids.grid.add_widget(self.album)
        print(len(self.ids.grid.children))
        if len(self.ids.grid.children) == 0:
            self.login_failure('Sermon Not Found')
            # Snackbar.make('sermon not found')


class Photo(ILeftBody, AsyncImage):
    pass

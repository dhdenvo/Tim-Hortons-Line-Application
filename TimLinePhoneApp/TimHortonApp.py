from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.network.urlrequest import UrlRequest
from kivy.clock import Clock
from kivy.properties import ObjectProperty
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.camera import Camera
import time

class MyApp(App):
    def build(self):
        #Create screen manager
        self.sm = ScreenManager()


#Create main window----------------------------------------------------------------------
        self.w1 = Screen(name='main')

        #Create single column space
        self.g1 = GridLayout(cols=1)

        #Create images for g1
        self.title_image = Image(source='tim.png')
        self.graph_image = Image(source='line.png')


        #Create Double column space---------------------------------------------
        self.g2 = GridLayout(cols=2)

        #Create widgets for g2
        self.l1 = Label(text = "Line length: ")
        self.people = Label(text = "8")
        self.l2 = Label(text = "Time of last \nAI snapshot: ")
        self.wait = Label(text = "00:05:30")

        #Add widgets to g2
        self.g2.add_widget(self.l1)
        self.g2.add_widget(self.people)
        self.g2.add_widget(self.l2)
        self.g2.add_widget(self.wait)
        self.update()
        #-----------------------------------------------------------------------


        #Create button for g1
        self.capture = Button(text="Crowd Source Wait Times", on_press=self.crowdSource)

        #Add widgets to g1
        self.g1.add_widget(self.title_image)
        self.g1.add_widget(self.graph_image)
        self.g1.add_widget(self.g2)
        self.g1.add_widget(self.capture)

        #Add g1 to main screen
        self.w1.add_widget(self.g1)
#----------------------------------------------------------------------------------------


#SecondScreen----------------------------------------------------------------------------
        self.w2 = Screen(name='camera',)

        #Create single column space
        self.sg1 = GridLayout(cols=1)
        self.cam = Camera(resolution=(640, 480),allow_stretch=True, size_hint=[1, 1])
        self.sb1 = Button(text="Take Picture",size_hint=(.3, .3), on_press= self.snap)

        #Add widgets to sg1
        self.sg1.add_widget(self.cam)
        self.sg1.add_widget(self.sb1)

        #Add sg1 to second screen
        self.w2.add_widget(self.sg1)
#----------------------------------------------------------------------------------------

        #Add windows to screen manager
        self.sm.add_widget(self.w1)
        self.sm.add_widget(self.w2)

        Clock.schedule_interval(self.update, 20)

        return self.sm

    def change(self,request, result):
        self.people.text, self.wait.text = result.split(" ")

    def update(self, instance=None):
        req = UrlRequest('http://127.0.0.1:5000/d', on_success=self.change)

    def crowdSource(self, instance):
        self.sm.current = 'camera'

    def snap(self, instance):
        self.cam.export_to_png("IMG_{}.png".format(timestr))
        print("Click")
        # self.sm.current = 'main'


if __name__ == "__main__":
    MyApp().run()

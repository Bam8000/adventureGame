#Game Central File. Runs App

import xml.etree.ElementTree as ET
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.clock import Clock
from xml_parse import *
from render import *
from character import *


class RootWidget(Widget):

    def __init__(self, **kwargs):
        Widget.__init__(self, **kwargs)
        Top = Layer(root[2].attrib['name'], int(root[2].attrib['width']), int(root[2].attrib['height']))
        CharacterControls = char_controls()
        Controls = OtherControls()
        self.widgets = []
        self.widgets_add(Ground) #The order of widgets from bottom to top is the order in which they are added
        self.widgets_add(character)
        self.widgets_add(Top)
        self.widgets_add(CharacterControls)
        self.widgets_add(Objects)
        self.widgets_add(Controls)
        Clock.schedule_interval(character.update, 1.0/60.0)
        Clock.schedule_interval(self.update, 1.0/60.0)
        

    def update(self, dt):
        if character.z_pos == 1 and character.z_pos_firsttime:
            self.widgets_update(1, 2)
            character.z_pos_firsttime = False
        if character.z_pos == 0 and character.z_pos_firsttime:
            self.widgets_update(1, 2)
            character.z_pos_firsttime = False
            

    def widgets_update(self, wid_ind1, wid_ind2):
        '''takes the indices of the two elements in self.widgets and switches them in both lists.
           Note: switching the same index doesn't work.'''
        child_ind1 = len(self.widgets) - wid_ind2 - 1
        child_ind2 = len(self.widgets) - wid_ind1 - 1
        
        self.widgets[wid_ind1], self.widgets[wid_ind2] = self.widgets[wid_ind2], self.widgets[wid_ind1]

        tmp = self.children[child_ind1]
        self.remove_widget(tmp)
        self.add_widget(tmp)

        for _ in range(child_ind2-child_ind1-1):
            tmp = self.children[child_ind2-1]
            self.remove_widget(tmp)
            self.add_widget(tmp)

        tmp = self.children[child_ind2]
        self.remove_widget(tmp)
        self.add_widget(tmp)
        
        for _ in range(child_ind1):
            tmp = self.children[child_ind2]
            self.remove_widget(tmp)
            self.add_widget(tmp)
        


    def widgets_add(self, widget):
        '''takes a widget object and adds it to the self.widgets list and the self.children list'''
        self.widgets.append(widget)
        self.add_widget(widget)



class GameApp(App):

    def build(self):
        Root = RootWidget()
        return Root



if __name__ == '__main__':
    GameApp().run()

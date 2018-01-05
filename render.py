#Map Rendering File
#Renders Tilesets, Objects

import xml.etree.ElementTree as ET
from random import randrange
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.graphics.texture import Texture
from kivy.core.image import Image
from kivy.graphics import Canvas, Rectangle
from kivy.graphics.context_instructions import Translate
from kivy.properties import BooleanProperty
from kivy.metrics import dp
from xml_parse import *


#global variable that is set to true when character collides with select objects.
char_obj_collide = False



def get_tileset(gid):
    """takes an integer, the gid. Returns an instance of the tileset that has that gid"""

    for i in tilesetList:
        if gid <= i.tilesetLastGid:
            return i


class Layer(Widget):
    """creates a grid of tiles based on information from a layer."""

    def __init__(self, name, width, height, **kwargs):
        Widget.__init__(self, **kwargs)
        self.name = str(name)
        self.width = width
        self.height = height

        #get the layer for ease of iteration below
        #using XPath to find all 'data' nodes that are children of nodes
        #that have the name of the instance of the class
        self.layer = root.find(".//*[@name='"+self.name+"']/data")

        x = 0
        y = self.height*dp(32) - dp(32) #assuming all the tiles will be 32px. To render the tileset from top left to bottom right.
        firsttime = True
        for gid in self.layer:
            gid = int(gid.attrib['gid'])
            ts = get_tileset(gid)
            if x % (self.width * dp(32)) == 0 and not firsttime:
                y -= dp(32)
                x -= self.width * dp(32)
            if gid != 0:
                self.canvas.add(Rectangle(size=(dp(ts.tilesetTileWidth), dp(ts.tilesetTileHeight)),
                                            pos=(x, y), texture=tile_atlas[gid]))
            x += dp(32)
            if firsttime:
                firsttime = False
    

class FirstLayer(Layer):
    '''Ensures that the Translate() function is only called for all the canvases once'''
    up = BooleanProperty(False) #the value of the boolean doesn't matter - we are just looking for changes.
    down = BooleanProperty(False)
    right = BooleanProperty(False)
    left = BooleanProperty(False)
    

    #remember, the screen moves in the opposite direction of the character to follow it.
    #these on_<property name> methods react to changes in the property
    def on_up(self, *args): #on_up references the character's motion.
        with self.canvas.before:
            Translate(0, dp(-2))

    def on_down(self, *args):
        with self.canvas.before:
            Translate(0, dp(2))

    def on_right(self, *args):
        with self.canvas.before:
            Translate(dp(-2), 0)

    def on_left(self, *args):
        with self.canvas.before:
            Translate(dp(2), 0)


class GameObject(Widget):
    """Stores data about the objects in the game.
    There are differnt types which the character behaves differently towards."""

    def __init__(self, name, obj_type, x_pos, y_pos, width, height, **kwargs):
        Widget.__init__(self, **kwargs)
        self.name = name
        self.obj_type = obj_type
        self.width = width
        self.height = height
        self.x_pos = x_pos
        self.y_pos = 50 * 32 - y_pos - self.height #Adjusts where the object is rendered.
        #The map data (ie 50*32) aren't dynamic; make sure to change!
        if self.obj_type == 'Tree' and name == 'default':
            self.has_key = False

        #changing the properties of the widget according to the above data.
        self.size = (dp(self.width), dp(self.height))
        self.size_hint = (None, None)
        self.pos = (dp(self.x_pos), dp(self.y_pos))
    

class ObjectsLayer(FloatLayout):
    """When initiated, it reads in objects from the xml file as a GameObject instance
    and adds them as widgets to a FloatLayout. The type of widget varies depending on
    the attributes of the instance. Each widget has a separate id and type that is
    referenced by the character object when it interacts with it."""


    def __init__(self, **kwargs):
        super(ObjectsLayer, self).__init__(**kwargs)
        self.trees = []
        self.x_pos = 0
        self.y_pos = 0
        self.pos = (self.x_pos, self.y_pos)
        self.size = (50*dp(32), 50*dp(32))  #make dynamic!

        for obj in root.find('objectgroup'):
            obj = GameObject(obj.attrib['name'], obj.attrib['type'], int(obj.attrib['x']),
                             int(obj.attrib['y']), int(obj.attrib['width']), int(obj.attrib['height']))
            if obj.obj_type == 'Tree' and obj.name == 'default':
                self.trees.append(obj)
            self.add_widget(obj)

        self.trees[randrange(len(self.trees))].has_key = True #randomly assigns True to one tree in map.
        

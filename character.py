#Character object and all of its interactions with the game.

from functools import partial
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from kivy.graphics import Canvas, Rectangle, Color
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.properties import BooleanProperty
from kivy.properties import *
from kivy.core.window import Window
from kivy.metrics import dp
from main import *
from render import *


#this must be defined in the file that references it, so that's why it's not in main.py
Ground = FirstLayer(root[1].attrib['name'], int(root[1].attrib['width']), int(root[1].attrib['height']))
Objects = ObjectsLayer()


class Character(Widget):
    '''The character class.'''

    def __init__(self, **kwargs):
        super(Character, self).__init__(**kwargs)
        self.x_pos = Window.width//2
        self.y_pos = Window.height//2
        self.pos = (self.x_pos, self.y_pos)
        self.size = (0.8*dp(27), 0.8*dp(48))
        self.frame = 0 #the initial frame of the sprite animation
        self.vel = [0, 0] #the initial velocity of the character. Up= 1, Down= -1, Right= 2, Left= -2. vel[0] is previous velocity.
        self.count = 0 #counts even and odd frames so that character is animated 30 times a sec, not 60.
        self.z_pos = 0 #layer level of the character. One level up = 1, one level down = -1
        self.z_pos_firsttime = False #records whether a value has just been changed
        self.have_key = False
        with self.canvas:
            self.sprite = Rectangle(pos=self.pos, size=self.size, texture=spr_right[0])

        self.win_popup = Popup(title='YAY!', content=Label(text='You Win!',
                                                           font_size='12sp'),
                               size_hint=(0.7, 0.7), pos_hint={'center_x':0.5, 'center_y':0.5})

        self.sorry_popup = Popup(title='Sorry!', content=Label(text='You haven\'t found the key!\n\nPress \'Help\' for instructions.',
                                                              font_size='12sp'),
                                 size_hint=(0.7, 0.7), pos_hint={'center_x':0.5, 'center_y':0.5})

        

    #the main update loop for the character. Deals with collisions and character movement.
    def update(self, dt):

        for obj in Objects.children:
            self.collision_obj(obj)
            self.tree_obj(obj)
            self.gate_obj(obj)
            
        #moves the character.           
        if self.count == 0: #this check animates/moves the character every 30th of a second (looks better).
            self.move(self.vel)
            self.count += 1
        else:
            self.count = 0
        

    def collision_obj(self, obj):
        #check collision with 'Collision' type objects
        if obj.obj_type == 'Collision':
            if self.collide_widget(obj):                      
                self.move(self.vel, True)
                self.vel[0], self.vel[1] = self.vel[1], 0
            


    def tree_obj(self, obj):
        #handles the character's interaction with trees
        #NOTE: the layer of trees must be a single layer with nothing else in it.
        if obj.obj_type == 'Tree':
            if self.collide_widget(obj):
                if self.y_pos/dp(1) < (obj.y_pos - self.size[1]/dp(5)): #walking in front of tree
                    if self.z_pos != 1:
                        self.z_pos = 1
                        self.z_pos_firsttime = True
                elif (obj.y_pos - self.size[1]/dp(5)) < self.y_pos/dp(1) < (obj.y_pos + obj.size[1]//dp(8)): #colliding with tree
                    if obj.name == 'default': #collision with real trees
                        if (obj.x_pos + dp(24) - self.size[0]) < self.x_pos/dp(1) < (obj.x_pos + obj.size[0]/dp(1) - dp(14)):
                            self.move(self.vel, True)
                            self.vel[0], self.vel[1] = self.vel[1], 0
                            if obj.has_key:
                                with obj.canvas:
                                    Rectangle(size=(dp(64), dp(64)), pos=(dp(obj.x_pos-12), dp(obj.y_pos)), source='gold_outline.png')
                                self.have_key = True
                            else:
                                with obj.canvas:
                                    Rectangle(size=(dp(64),dp(64)), pos=(dp(obj.x_pos-12), dp(obj.y_pos)), source='black_outline.png')
                    else:
                        self.move(self.vel, True)
                        self.vel[0], self.vel[1] = self.vel[1], 0
                else:
                    if self.z_pos != 0:
                        self.z_pos = 0
                        self.z_pos_firsttime = True


    def gate_obj(self, obj):
        if obj.obj_type == 'Gate':
            if self.collide_widget(obj):
                if self.y_pos/dp(1) < (obj.y_pos - self.size[1]/dp(2)):
                    if self.z_pos != 1:
                        self.z_pos = 1
                        self.z_pos_firsttime = True
                elif (obj.y_pos - self.size[1]/dp(2)) < self.y_pos/dp(1) < (obj.y_pos + obj.size[1]//dp(5)):
                    if self.vel[1] == 1 or self.vel[1] == -1:
                        if self.have_key:
                            self.win_popup.open()
                        else:
                            self.sorry_popup.open()
                    self.move(self.vel, True)
                    self.vel[0], self.vel[1] = self.vel[1], 0
                else:
                    if self.z_pos != 0:
                        self.z_pos = 0
                        self.z_pos_firsttime = True
                    

    def move(self, vel, bounce=False):
        '''uses a list of the velocities and moves the character depending on the velocity.
           If the bounce parameter is set to True, it will handle collisions so that the
           canvas moves with the character.'''
        if self.frame < 29:
            self.frame += 1
        else:
            self.frame = 0
            
        if vel[1] != 0:
            if vel[1] == 1:
                if not bounce:
                    self.y_pos += dp(2)
                    if Window.height//2 < self.y_pos < Ground.height*dp(32) - Window.height//2:
                        Ground.up = not(Ground.up) #by changing the value of this property, the window moves.
                else: #will move the character back 2px on a collision
                    self.y_pos -= dp(2)
                    if Window.height//2 < self.y_pos < Ground.height*dp(32) - Window.height//2:
                        Ground.down = not(Ground.down)
                self.sprite.texture = spr_up[(self.frame//6)]
            elif vel[1] == -1:
                if not bounce:
                    self.y_pos -= dp(2)
                    if Window.height//2 < self.y_pos < Ground.height*dp(32) - Window.height//2:
                        Ground.down = not(Ground.down)
                else:
                    self.y_pos += dp(2)
                    if Window.height//2 < self.y_pos < Ground.height*dp(32) - Window.height//2:
                        Ground.up = not(Ground.up)
                self.sprite.texture = spr_down[(self.frame//6)]
            elif vel[1] == 2:
                if not bounce:
                    self.x_pos += dp(2)
                    if Window.width//2 < self.x_pos < Ground.width*dp(32) - Window.width//2:
                        Ground.right = not(Ground.right)
                else:
                    self.x_pos -= dp(2)
                    if Window.width//2 < self.x_pos < Ground.width*dp(32) - Window.width//2:
                        Ground.left = not(Ground.left)
                self.sprite.texture = spr_right[(self.frame//6)]
            elif vel[1] == -2:
                if not bounce:
                    self.x_pos -= dp(2)
                    if Window.width//2 < self.x_pos < Ground.width*dp(32) - Window.width//2:
                        Ground.left = not(Ground.left)
                else:
                    self.x_pos += dp(2)
                    if Window.width//2 < self.x_pos < Ground.width*dp(32) - Window.width//2:
                        Ground.right = not(Ground.right)
                self.sprite.texture = spr_left[(self.frame//6)]
            self.pos = (self.x_pos, self.y_pos)
            self.sprite.pos = self.pos
            
        else:
            self.frame = 0 #makes the sprite return to standing
            if vel[0] == 1:
                self.sprite.texture = spr_up[(self.frame//6)]
            elif vel[0] == -1:
                self.sprite.texture = spr_down[(self.frame//6)]
            elif vel[0] == 2:
                self.sprite.texture = spr_right[(self.frame//6)]
            elif vel[0] == -2:
                self.sprite.texture = spr_left[(self.frame//6)]
                



character = Character() #Note: all places where "character" is used refer to this particular instance.




class char_controls(FloatLayout):
    '''controls where the character moves. There are 4 regions where the player can tap:
       the top third to go up, the bottom third to go down, the center left to go left
       and the center right to go right. They are buttons.'''
    

    def __init__(self, **kwargs):
        super(char_controls, self).__init__(**kwargs)
        self.opacity = 0 #if this were visible, you would notice that canvas moves with background, but objects stay in place.
        self.size = (Window.width, Window.height)

        anchor_bc = AnchorLayout(anchor_x = 'center', anchor_y = 'bottom')
        down_btn = Button(text='', size_hint = (1, 0.3333))
        down_btn.bind(on_press=self.schedule_down, on_release=self.schedule_stop)
        anchor_bc.add_widget(down_btn)
        self.add_widget(anchor_bc)

        anchor_cl = AnchorLayout(anchor_x = 'left', anchor_y = 'center')
        left_btn = Button(text='', size_hint = (0.5, 0.3333))
        left_btn.bind(on_press=self.schedule_left, on_release=self.schedule_stop)
        anchor_cl.add_widget(left_btn)
        self.add_widget(anchor_cl)

        anchor_cr = AnchorLayout(anchor_x = 'right', anchor_y = 'center')
        right_btn = Button(text='', size_hint = (0.5, 0.3333))
        right_btn.bind(on_press=self.schedule_right, on_release=self.schedule_stop)
        anchor_cr.add_widget(right_btn)
        self.add_widget(anchor_cr)

        anchor_tc = AnchorLayout(anchor_x = 'center', anchor_y = 'top')
        up_btn = Button(text='', size_hint = (1, 0.3333))
        up_btn.bind(on_press=self.schedule_up, on_release=self.schedule_stop)
        anchor_tc.add_widget(up_btn)
        self.add_widget(anchor_tc)

        #note: visual canvas moves with the background; but the object stays in the same place.

    presses = 0 #keeps track of when there is only one finger on the screen.

    def schedule_up(self, *args):
        char_controls.presses += 1
        character.vel[0] = character.vel[1]
        character.vel[1] = 1

    def schedule_down(self, *args):
        char_controls.presses += 1
        character.vel[0] = character.vel[1]
        character.vel[1] = -1

    def schedule_right(self, *args):
        char_controls.presses += 1
        character.vel[0] = character.vel[1]
        character.vel[1] = 2

    def schedule_left(self, *args):
        char_controls.presses += 1
        character.vel[0] = character.vel[1]
        character.vel[1] = -2

    def schedule_stop(self, *args):
        if char_controls.presses > 0: #this prevents the character from stopping prematurely.
            char_controls.presses -= 1
        if char_controls.presses == 0: #i.e. if the last finger has been lifted off the screen.
            character.vel[0] = character.vel[1]
            character.vel[1] = 0
            


class OtherControls(FloatLayout):
    '''other controls for the game including instructions, check button, pause.
       Move with the character to stay at the top of the screen.'''
    

    def __init__(self, **kwargs):
        super(OtherControls, self).__init__(**kwargs)
        self.size = (Window.width, Window.height)

        help_btn = Button(text='Help', size_hint=(0.15, 0.15), pos_hint={'top':0.15, 'center_x':0.5}, opacity=0.7)
        help_btn.bind(on_press=self.help_open)
        self.add_widget(help_btn)

        self.help_popup = Popup(title='Instructions', content=Label(text='''You\'re in an unfamiliar world!
To leave, you need to open the gate by finding a key in the trees.
Press the sides of the screen to move in that direction.
Walk up to a tree and make sure to hit it.\nIf the tree border turns gold, you\'ve found the key! If it turns black, try another tree.
Once you have the key, walk through the gate and you\'ll win!
\nNote: this help button won\'t work when you walk far away.''',
                                                            font_size='10sp'),
                                size_hint=(0.7, 0.7), pos_hint={'center_x':0.5, 'center_y':0.5})


    def help_open(self, *args):
        self.help_popup.open()
    
    

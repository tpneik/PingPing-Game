import pyglet
from . import settings
class menu:
    def __init__(self,window_width,window_height):
        self.width=window_width
        self.height=window_height
        self.button_width=200
        self.button_heigth=200
        self.x= (self.width/2)-(self.button_width/2)
        self.y= (self.height/2)-(self.button_heigth/2)
        


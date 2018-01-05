#XML Parsing File.

import xml.etree.ElementTree as ET
from kivy.graphics.texture import Texture
from kivy.core.image import Image
from kivy.metrics import dp



tree = ET.parse('map.tmx')
root = tree.getroot()


#import general elements from <map> tag
mapWidth = int(root.attrib['width'])
mapHeight = int(root.attrib['height'])
tileWidth = int(root.attrib['tilewidth'])
tileHeight = int(root.attrib['tileheight'])



class TileSet(object):
    """Stores data about tilesets to be accessed by tiles from that tileset"""

    def __init__(self, imagePath, imageWidth, imageHeight,      #creating instance attributes of the class,
                 tilesetFirstGid, tilesetTileWidth, tilesetTileHeight): #change values with each instance
        self.imagePath = imagePath
        self.imageWidth = imageWidth
        self.imageHeight = imageHeight
        self.tilesetFirstGid = tilesetFirstGid
        self.tilesetTileWidth = tilesetTileWidth
        self.tilesetTileHeight = tilesetTileHeight
        self.tilesetLastGid = (imageHeight//tilesetTileHeight)*(imageWidth//tilesetTileWidth)



#make a list of all the tilesets
tilesetList = []

#import data for each tileset from each <tileset> tag
Test = TileSet(root[0][0].attrib['source'], int(root[0][0].attrib['width']),
               int(root[0][0].attrib['height']), int(root[0].attrib['firstgid']),
               int(root[0].attrib['tilewidth']), int(root[0].attrib['tileheight'])
               )
tilesetList.append(Test)



#creating a list of all the textures in the game. The index of the texture corresponds to its GID.
tile_atlas = []
tile_atlas.append('0') #a placeholder for the 0th gid, a blank space
for tileset in tilesetList:
    ts = Image(tileset.imagePath, allow_stretch=True).texture
    cols = tileset.imageWidth//tileset.tilesetTileWidth
    rows = tileset.imageHeight//tileset.tilesetTileHeight
    for i in range(tileset.tilesetLastGid):                 #adding in all the tiles in a tileset
        x = (i % cols) * tileset.tilesetTileWidth
        y = (rows - (i // cols) - 1) * tileset.tilesetTileHeight
        tile = ts.get_region(x, y, tileset.tilesetTileWidth, tileset.tilesetTileHeight)
        tile_atlas.append(tile)


#reading in the character sprite: h = 64, w = 36, spacing = 32. They are 57px apart horizontally, 
spr = Image('sprite.png', allow_stretch=True).texture
spr_down = []
spr_up = []
spr_right = []
spr_left = []
for i in range(5):
    frame = spr.get_region((26 + i*57 + i*33), 10, 36, 64)
    spr_down.append(frame)
for i in range(5):
    frame = spr.get_region((26 + i*57 + i*33), 102, 36, 64)
    spr_up.append(frame)
for i in range(4, -1, -1): #the frames are placed in opposite order.
    frame = spr.get_region((26 + i*57 + i*33), 194, 36, 64)
    spr_right.append(frame)
for i in range(5):
    frame = spr.get_region((26 + i*57 + i*33), 286, 36, 64)
    spr_left.append(frame)





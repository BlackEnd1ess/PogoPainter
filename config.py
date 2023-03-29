from ursina import *
from item import *

## Player 1-4: Model, Texture, Color
player1_model = 'cube'
player1_texture = None
player1_paint_color = color.yellow

player2_model = 'cube'
player2_texture = None
player2_paint_color = color.red

player3_model = 'cube'
player3_texture = None
player3_paint_color = color.green

player4_model = 'cube'
player4_texture = None
player4_paint_color = color.blue

## Items: Model, Texture
# default object for earning points.
item_crate = 'cube'
item_crate_tex = None

# this object will stun the player
item_nitro_crate = 'cube'
item_nitro_crate_tex = None

# this object will incrase the move speed for 5 seconds.
item_boost_shoe = 'sphere'
item_boost_shoe_tex = None

# this object will color a row of blocks in the direction it's facing
item_arrow = 'assets/item/Arrow/Arrow.obj'
item_arrow_tex = None

# this object will color double side in the direction it's facing
item_double_arrow = 'assets/item/Arrow/DoubleArrow.obj'
item_double_arrow_tex = None

# this object will color 4 ways rows of Blocks.
item_arrow4 = 'assets/item/Arrow/4way.obj'
item_arrow4_tex = None

# this object will subtract the points by 5, who collide with them.
item_mushroom = 'sphere'
item_mushroom_tex = None

# this object will allow, to shoot 1 missile. The player who are hitten by this, will stun for a short time.
item_rocket = 'sphere'
item_rocket_tex = None

## Item Dict: all items are listed here.
## Item Choose: Control the items which spawns in the Arena.
item_choose = (['Crate','SpeedShoes','Arrow','Missile'])
item_dict = {
	'Crate': Crate,
	'SpeedShoes': SpeedShoes,
	'NitroCrate': NitroCrate,
	'Mushroom': Mushroom,
	'Missile': Missile,
	'Arrow': Arrow,
	'DoubleArrow': DoubleArrow,
	'FourWayArrow': FourWayArrow}

## Global Settings! these Values will interact with the Game Logic.
## This Values dont need manual Changes.
item_count = 0
paint_blocks = []
items = []
map_scene = 1
challange_mode = 0
game_stop = True
reset_state = False
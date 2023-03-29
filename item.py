from ursina import *
import random
import config

class Crate(Entity): ## Item Crate: earning points on hit.
	def __init__(self, position=[]):
		super().__init__(model=config.item_crate,texture=config.item_crate_tex,scale=0.5,position=position)
		self.y=-1
		self.color = color.violet
		self.animate_position((self.x,0,self.z), duration=0.5)
	def destroy(self):
		items = config.items
		config.item_count -= 1
		#Audio('',pitch=1.2,volume=2)
		self.disable()
		self.parent = None
		items.remove(self)

class SpeedShoes(Entity): ## incrase temporary players move speed.
	def __init__(self, position=[]):
		super().__init__(model=config.item_boost_shoe,texture=config.item_boost_shoe_tex,color=color.red,scale=0.01,position=position)
		self.y=7
		self.color = color.orange
		self.animate_position((self.x,0,self.z), duration=1.3)
	def destroy(self):
		items = config.items
		config.item_count -= 1
		items.remove(self)
		#Audio('assets/sfx/shoe.wav',pitch=1.15)
		self.disable()
		self.parent = None
	def update(self):
		self.rotation_y += 100 * time.dt

class Arrow(Entity): ## color a whole row of Blocks, which the arrow is facing.
	def __init__(self, position=[]):
		super().__init__(model=config.item_arrow, texture=config.item_arrow_tex, position=position, color=color.violet, rotation_x=90)
		self.change_way = 0
		self.y = 7
		self.animate_position((self.x,0,self.z), duration=1.3)
	def destroy(self):
		items = config.items
		config.item_count -= 1
		items.remove(self)
		self.disable()
		self.parent = None
	def update(self): # change arrows face way
		self.change_way += time.dt
		if self.change_way >= 3:
			self.change_way = 0
			self.rotation_y += 90
			self.rotation_y %= 360

class DoubleArrow(Entity): ## paint double side of rows, which way is facing.
	def __init__(self, position=[]):
		super().__init__(model=config.item_double_arrow, texture=config.item_double_arrow_tex, position=position, color=color.violet,rotation_x=90,scale=0.8)
		self.change_way = 0
		self.y = 7
		self.animate_position((self.x,0,self.z), duration=1.3)
		self.rotation_y = 0
	def destroy(self):
		items = config.items
		config.item_count -= 1
		items.remove(self)
		self.disable()
		self.parent = None
	def update(self):
		self.change_way += time.dt
		if self.change_way >= 3:
			if self.rotation_y == 0:
				self.rotation_y += 90
			elif self.rotation_y == 90:
				self.rotation_y -= 90
			self.change_way = 0

class FourWayArrow(Entity): ## paint whole 4 Rows of blocks.
	def __init__(self, position=[]):
		super().__init__(model=config.item_arrow4,texture=config.item_arrow4_tex,position=position,color=color.violet)
		self.y=7
		self.animate_position((self.x,0,self.z), duration=1.3)
	def destroy(self):
		items = config.items
		config.item_count -= 1
		items.remove(self)
		#Audio('',volume=0.6)
		self.disable()
		self.parent = None

class NitroCrate(Entity): ## Stun victim for a few seconds.
	def __init__(self, position=[]):
		super().__init__(model=config.item_nitro_crate,texture=config.item_nitro_crate_tex,scale=0.5,position=position)
		self.y=-1
		self.animate_position((self.x,0,self.z), duration=0.5)
		self.lifetime = 0
		self.color = color.black
	def destroy(self):
		items = config.items
		config.item_count -= 1
		items.remove(self)
		#Audio('',volume=3)
		self.disable()
		self.parent = None
	def purge(self):
		items = config.items
		config.item_count -= 1
		items.remove(self)
		self.disable()
		self.parent = None
	def update(self):
		self.lifetime += 1 * time.dt
		if self.lifetime > 10:
			self.purge()

class Mushroom(Entity): ## in this case this item will reset all blocks of victim and stun.
	def __init__(self, position=[]):
		super().__init__(model=config.item_mushroom,texture=config.item_mushroom_tex,position=position,scale=0.5)
		self.y=-1
		self.animate_position((self.x,0,self.z), duration=0.5)
		self.lifetime = 0 
	def destroy(self):
		items = config.items
		config.item_count -= 1
		items.remove(self)
		self.disable()
		self.parent = None
	def purge(self):
		items = config.items
		config.item_count -= 1
		items.remove(self)
		self.disable()
		self.parent = None
	def update(self):
		self.lifetime += 1 * time.dt
		if self.lifetime > 10:
			self.purge()

class Missile(Entity): ## stun victim, by shoot this Missile.
	def __init__(self, position=[]):
		super().__init__(model=config.item_rocket,texture=config.item_rocket_tex,scale=0.7,position=position)
		self.y=7
		self.scale_z=1
		self.color = color.cyan
		self.animate_position((self.x,0,self.z), duration=1.3)
	def destroy(self):
		items = config.items
		config.item_count -= 1
		#Audio('',volume=1)
		self.disable()
		self.parent = None
		items.remove(self)
	def update(self):
		self.rotation_y += 100 * time.dt
from ursina import *
from item import Mushroom, NitroCrate, Arrow, Crate, SpeedShoes, Missile, FourWayArrow
from math import sqrt
import config

class P1(Entity): ## Player1 (Player)
	def __init__(self):
		super().__init__(position=(0,0,0))
		self.missile = 0 # Missile counter
		self.points = 0 # current points
		self.speed_time = 0 # speed boost time
		self.move_timer = 0.5 # wait duration for move
		self.colored_blocks = 0 # counter for colored blocks.
		self.victory = 0 # how many times you winned.
		self.default_rot = 0 # faceway 
		self.default_pos = (0,0,0) # start position
		self.color = config.player1_paint_color # model color
		self.paint_color = config.player1_paint_color #color of blocks, which painted by player
	def input(self, key): ## Controls
		if held_keys['w'] and not self.z == 7:
			self.move(360, 0, 1) ## rotation, way
		elif held_keys['s'] and not self.z == 0:
			self.move(180, 0, -1)
		elif held_keys['a'] and not self.x == 0:
			self.move(270, -1, 0)
		elif held_keys['d'] and not self.x == 7:
			self.move(90, 1, 0)
		elif key == 'q':
			self.shoot_rocket()
		elif key == 'space': ## test function for calculating colored blocks.
			print(self.colored_blocks)
	def mvsp_boost(self): ## incrase you move speed by collecting shoes.
		self.speed_time = 7.0
	def stun(self): ## stops the player
		self.move_timer = 3
	def move(self, rotation_y, dx, dz): ## move the player
		if self.move_timer <= 0 and config.game_stop == False:
			self.rotation_y = rotation_y
			new_x = self.x + dx
			new_z = self.z + dz
			if (new_x, new_z) != self.enemy_pos(): ## cannot access victims position.
				self.x = new_x
				self.z = new_z
				if self.speed_time > 0:
					self.move_timer = 0.25
				else:
					self.move_timer = 0.5
	def enemy_pos(self): ## check victoms positions.
		for posit in [player2,player3,player4]:
			return posit.x, posit.z
	def shoot_rocket(self): ## shoot the Missile
		if self.missile >= 1:
			face_way = self.rotation_y
			rocket = Rocket(position=self.position, rotation_y=face_way, shooter=self)
			self.missile = 0
			rocket.rotation_y = face_way if face_way in [0, 90, 180, 270] else 0
	def get_points(self): ## earning points by hit Crates
		self.points += self.colored_blocks
		pt = Text(text=f'{self.colored_blocks}',x=self.x/10,y=0.05,scale=random.randint(2,3))
		pt.color = self.paint_color
		pt.animate_y(1, duration=2)
		self.colored_blocks = 1
	def sub_points(self): ## sub points by hitting Mushrooms
		pt_sub = Text(x=self.x/10,y=0.05,scale=random.randint(2,3))
		if self.points > 20:
			self.points -= 20
			pt_sub.text = '-20'
		else:
			pt_sub.text = f'-{self.points}'
			self.points -= self.points
		pt_sub.animate_y(1, duration=2)
		pt_sub.color = self.paint_color
	def update(self):
		self.move_timer -= time.dt
		if self.speed_time > 0:
			self.speed_time -= 1 * time.dt

class P2(Entity): ## Player2 (Bot)
	def __init__(self):
		super().__init__(position=(0,0,7))
		self.missile = 0
		self.points = 0
		self.speed_time = 0
		self.move_timer = 0.5
		self.colored_blocks = 0
		self.rotation_y = 180
		self.victory = 0
		self.default_rot = 180
		self.default_pos = (0,0,7)
		self.color = config.player2_paint_color
		self.paint_color = config.player2_paint_color
	def mvsp_boost(self):
		self.speed_time = 7.0
	def stun(self):
		self.move_timer = 3
	def enemy_pos(self):
		for posit in [player,player3,player4]:
			return posit.x, posit.z
	def move(self): ## Automatic move position of Bot (need bug fixxes for each Bots.)
		if self.move_timer <= 0 and config.game_stop == False:
			nearest_item = self.find_nearest_item()
			if nearest_item:
				dx, dz = nearest_item.x - self.x, nearest_item.z - self.z
				if abs(dx) > abs(dz):
					new_x = self.x + 1 if dx > 0 else self.x - 1
					new_z = self.z
					self.rotation_y = 90 if dx > 0 else 270
				else:
					new_x = self.x
					new_z = self.z + 1 if dz > 0 else self.z - 1
					self.rotation_y = 0 if dz > 0 else 180
			else:
				if self.x == 0:
					moves = {'d': (1, 90), 'w': (1, 0), 's': (-1, 180)}
				elif self.x == 7:
					moves = {'a': (-1, 270), 'w': (1, 0), 's': (-1, 180)}
				else:
					moves = {'a': (-1, 270), 'd': (1, 90), 'w': (1, 0), 's': (-1, 180)}
				if self.z == 0:
					moves.pop('s', None)
				elif self.z == 7:
					moves.pop('w', None)
				choose_way = random.choice(list(moves.keys()))
				new_x = self.x + moves[choose_way][0]
				new_z = self.z
				self.rotation_y = moves[choose_way][1]
			new_x = max(min(new_x, 7), 0)
			new_z = max(min(new_z, 7), 0)
			if (new_x, new_z) != self.enemy_pos():
				self.x = new_x
				self.z = new_z
				self.move_timer = 0.25 if self.speed_time > 0 else 0.5
	def distance(self, x1, z1, x2, z2):
		return sqrt((x1 - x2)**2 + (z1 - z2)**2)
	def find_nearest_item(self):
		nearest_item = None
		nearest_dist = float('inf')
		for item in config.items:
			if isinstance(item, Crate) or isinstance(item, SpeedShoes) or isinstance(item, Arrow) or isinstance(item, FourWayArrow) or isinstance(item, Missile):
				dist = self.distance(self.x, self.z, item.x, item.z)
				if dist < nearest_dist:
					nearest_dist = dist
					nearest_item = item
		return nearest_item
	def shoot_rocket(self):
		if self.missile >= 1 and random.randint(0, 100) == 99:
			face_way = self.rotation_y
			rocket = Rocket(position=self.position, rotation_y=face_way, shooter=self)
			self.missile = 0
			rocket.rotation_y = face_way if face_way in [0, 90, 180, 270] else 0
	def get_points(self):
		self.points += self.colored_blocks
		pt = Text(text=f'{self.colored_blocks}',x=self.x/10,y=0.05,scale=random.randint(2,3))
		pt.color = self.paint_color
		pt.animate_y(1, duration=2)
		self.colored_blocks = 1
	def sub_points(self):
		pt_sub = Text(x=self.x/10,y=0.05,scale=random.randint(2,3))
		if self.points > 20:
			self.points -= 20
			pt_sub.text = '-20'
		else:
			pt_sub.text = f'-{self.points}'
			self.points -= self.points
		pt_sub.animate_y(1, duration=2)
		pt_sub.color = self.paint_color
	def update(self):
		self.move()
		self.shoot_rocket()
		self.move_timer -= time.dt
		if self.speed_time > 0:
			self.speed_time -= 1 * time.dt

class P3(Entity): ## Player3 (Bot)
	def __init__(self):
		super().__init__(position=(7,0,7))
		self.missile = 0
		self.points = 0
		self.speed_time = 0
		self.move_timer = 0.5
		self.colored_blocks = 0
		self.rotation_y = 180
		self.victory = 0
		self.default_rot = 180
		self.default_pos = (7,0,7)
		self.color = config.player3_paint_color
		self.paint_color = config.player3_paint_color
	def mvsp_boost(self):
		self.speed_time = 7.0
	def stun(self):
		self.move_timer = 3
	def enemy_pos(self):
		for posit in [player,player2,player4]:
			return posit.x, posit.z
	def move(self):
		if self.move_timer <= 0 and config.game_stop == False:
			nearest_item = self.find_nearest_item()
			if nearest_item:
				dx, dz = nearest_item.x - self.x, nearest_item.z - self.z
				if abs(dx) > abs(dz):
					new_x = self.x + 1 if dx > 0 else self.x - 1
					new_z = self.z
					self.rotation_y = 90 if dx > 0 else 270
				else:
					new_x = self.x
					new_z = self.z + 1 if dz > 0 else self.z - 1
					self.rotation_y = 0 if dz > 0 else 180
			else:
				if self.x == 0:
					moves = {'d': (1, 90), 'w': (1, 0), 's': (-1, 180)}
				elif self.x == 7:
					moves = {'a': (-1, 270), 'w': (1, 0), 's': (-1, 180)}
				else:
					moves = {'a': (-1, 270), 'd': (1, 90), 'w': (1, 0), 's': (-1, 180)}
				if self.z == 0:
					moves.pop('s', None)
				elif self.z == 7:
					moves.pop('w', None)
				choose_way = random.choice(list(moves.keys()))
				new_x = self.x + moves[choose_way][0]
				new_z = self.z
				self.rotation_y = moves[choose_way][1]
			new_x = max(min(new_x, 7), 0)
			new_z = max(min(new_z, 7), 0)
			if (new_x, new_z) != self.enemy_pos():
				self.x = new_x
				self.z = new_z
				self.move_timer = 0.25 if self.speed_time > 0 else 0.5
	def distance(self, x1, z1, x2, z2):
		return sqrt((x1 - x2)**2 + (z1 - z2)**2)
	def find_nearest_item(self):
		nearest_item = None
		nearest_dist = float('inf')
		for item in config.items:
			if isinstance(item, Crate) or isinstance(item, SpeedShoes) or isinstance(item, Arrow) or isinstance(item, FourWayArrow) or isinstance(item, Missile):
				dist = self.distance(self.x, self.z, item.x, item.z)
				if dist < nearest_dist:
					nearest_dist = dist
					nearest_item = item
		return nearest_item
	def shoot_rocket(self):
		if self.missile >= 1 and random.randint(0, 100) == 99:
			face_way = self.rotation_y
			rocket = Rocket(position=self.position, rotation_y=face_way, shooter=self)
			self.missile = 0
			rocket.rotation_y = face_way if face_way in [0, 90, 180, 270] else 0
	def get_points(self):
		self.points += self.colored_blocks
		pt = Text(text=f'{self.colored_blocks}',x=self.x/10,y=0.05,scale=random.randint(2,3))
		pt.color = self.paint_color
		pt.animate_y(1, duration=2)
		self.colored_blocks = 1
	def sub_points(self):
		pt_sub = Text(x=self.x/10,y=0.05,scale=random.randint(2,3))
		if self.points > 20:
			self.points -= 20
			pt_sub.text = '-20'
		else:
			pt_sub.text = f'-{self.points}'
			self.points -= self.points
		pt_sub.animate_y(1, duration=2)
		pt_sub.color = self.paint_color
	def update(self):
		self.move()
		self.shoot_rocket()
		self.move_timer -= time.dt
		if self.speed_time > 0:
			self.speed_time -= 1 * time.dt

class P4(Entity): ## Player4 (Bot)
	def __init__(self):
		super().__init__(position=(7,0,0))
		self.missile = 0
		self.points = 0
		self.speed_time = 0
		self.move_timer = 0.5
		self.colored_blocks = 0
		self.victory = 0
		self.default_rot = 0
		self.default_pos = (7,0,0)
		self.color = config.player4_paint_color
		self.paint_color = config.player4_paint_color
	def mvsp_boost(self):
		self.speed_time = 7.0
	def stun(self):
		self.move_timer = 3
	def enemy_pos(self):
		for posit in [player,player2,player3]:
			return posit.x, posit.z
	def move(self):
		if self.move_timer <= 0 and config.game_stop == False:
			nearest_item = self.find_nearest_item()
			if nearest_item:
				dx, dz = nearest_item.x - self.x, nearest_item.z - self.z
				if abs(dx) > abs(dz):
					new_x = self.x + 1 if dx > 0 else self.x - 1
					new_z = self.z
					self.rotation_y = 90 if dx > 0 else 270
				else:
					new_x = self.x
					new_z = self.z + 1 if dz > 0 else self.z - 1
					self.rotation_y = 0 if dz > 0 else 180
			else:
				if self.x == 0:
					moves = {'d': (1, 90), 'w': (1, 0), 's': (-1, 180)}
				elif self.x == 7:
					moves = {'a': (-1, 270), 'w': (1, 0), 's': (-1, 180)}
				else:
					moves = {'a': (-1, 270), 'd': (1, 90), 'w': (1, 0), 's': (-1, 180)}
				if self.z == 0:
					moves.pop('s', None)
				elif self.z == 7:
					moves.pop('w', None)
				choose_way = random.choice(list(moves.keys()))
				new_x = self.x + moves[choose_way][0]
				new_z = self.z
				self.rotation_y = moves[choose_way][1]
			new_x = max(min(new_x, 7), 0)
			new_z = max(min(new_z, 7), 0)
			if (new_x, new_z) != self.enemy_pos():
				self.x = new_x
				self.z = new_z
				self.move_timer = 0.25 if self.speed_time > 0 else 0.5
	def distance(self, x1, z1, x2, z2):
		return sqrt((x1 - x2)**2 + (z1 - z2)**2)
	def find_nearest_item(self):
		nearest_item = None
		nearest_dist = float('inf')
		for item in config.items:
			if isinstance(item, Crate) or isinstance(item, SpeedShoes) or isinstance(item, Arrow) or isinstance(item, FourWayArrow) or isinstance(item, Missile):
				dist = self.distance(self.x, self.z, item.x, item.z)
				if dist < nearest_dist:
					nearest_dist = dist
					nearest_item = item
		return nearest_item
	def shoot_rocket(self):
		if self.missile >= 1 and random.randint(0, 100) == 99:
			face_way = self.rotation_y
			rocket = Rocket(position=self.position, rotation_y=face_way, shooter=self)
			self.missile = 0
			rocket.rotation_y = face_way if face_way in [0, 90, 180, 270] else 0
	def get_points(self):
		self.points += self.colored_blocks
		pt = Text(text=f'{self.colored_blocks}',x=self.x/10,y=0.05,scale=random.randint(2,3))
		pt.color = self.paint_color
		pt.animate_y(1, duration=2)
		self.colored_blocks = 1
	def sub_points(self):
		pt_sub = Text(x=self.x/10,y=0.05,scale=random.randint(2,3))
		if self.points > 20:
			self.points -= 20
			pt_sub.text = '-20'
		else:
			pt_sub.text = f'-{self.points}'
			self.points -= self.points
		pt_sub.animate_y(1, duration=2)
		pt_sub.color = self.paint_color
	def update(self):
		self.move()
		self.shoot_rocket()
		self.move_timer -= time.dt
		if self.speed_time > 0:
			self.speed_time -= 1 * time.dt

class Rocket(Entity): ## Missile, which will hit a Player (not the Item)
	def __init__(self, position, rotation_y, shooter):
		super().__init__(model=config.item_rocket,texture=config.item_rocket_tex,scale=0.7,position=position)
		self.color=color.red
		self.rotation_y=rotation_y
		self.lifetime = 0
		self.shooter = shooter
	def update(self):
		self.lifetime += 1 * time.dt
		if self.rotation_y == 360:
			self.z += 6 * time.dt
		elif self.rotation_y == 180:
			self.z -= 6 * time.dt
		elif self.rotation_y == 90:
			self.x += 6 * time.dt
		elif self.rotation_y == 270:
			self.x -= 6 * time.dt
		if self.lifetime > 2.5 or self.x < -1 or self.x > 8 or self.z < -1 or self.z > 9:
			self.disable()
			self.hide()
			self.parent = None
		for item in config.items:
			item_pos = (round(item.x), round(item.y), round(item.z))
			rocket_pos = (round(self.x), round(self.y), round(self.z))
			if rocket_pos == item_pos:
				if isinstance(item, Mushroom) or isinstance(item, NitroCrate):
					item.purge()
					self.disable()
					self.hide()
					self.parent = None
				else:
					pass
		for any_player in [player,player2,player3,player4]:
				rocket_pos = (round(self.x), round(self.y), round(self.z))
				p_pos = (round(any_player.x), round(any_player.y), round(any_player.z))
				if p_pos == rocket_pos and any_player != self.shooter:
					any_player.stun()
					self.disable()
					self.hide()
					self.parent = None

player = P1()
player2 = P2()
player3 = P3()
player4 = P4()
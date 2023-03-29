from ursina import *
from player import *
from item import *
import time
import config
import spawn
import ui

class Map(Entity): ## Load Arena
	def __init__(self):
		global timer, start_time
		Sky(color=color.random_color()) # background in the Arena
		camera.position=(3.5,6.5,-9.5)
		camera.rotation_x=21
		timer=90 # time duration for Game
		start_time=3.9 # wait time before start the Match.
		camera.fov=55
		ui.show()
		self.scene()
	def scene(self): ## create the Arena Field with 8x8 Blocks.
		self.border()
		for z in range(8):
			for x in range(8):
				ground = Entity(parent=scene, position=(x,0,z), model='cube', origin_y=.5, texture='white_cube', scale_y=0.25)
				ground.owner = None
				config.paint_blocks.append(ground)
	def border(self): ## create the Arena Wall
		left_border = Entity(model='cube',position=(-0.75,-0.1,3.5),scale=(0.5,0.5,8),color=color.gray)
		right_border = Entity(model='cube',position=(7.75,-0.1,3.5),scale=(0.5,0.5,8),color=color.gray)
		bottom_border = Entity(model='cube',position=(3.5,-0.1,-0.75),scale=(9,0.5,0.5),color=color.gray)
		top_border = Entity(model='cube',position=(3.5,-0.1,7.75),scale=(9,0.5,0.5),color=color.gray)
		if config.map_scene == 0:
			scene_wall = Entity(model='quad',position=(0,6,100),scale=(200,100,1),color=color.rgb(0,0,90))
			tree = Entity(model='assets/item/tree/Tree_Apple.obj',texture='assets/item/tree/Tex_0003_0.png',position=(8.8,-1,3),scale=(5,3,5),rotation_y=90)
			Entity(model=Terrain('heightmap_1', skip=4),scale=(100,5,20),position=(2,-0.8,7), texture='grass')

def paint_single(owner): ## Paint a Block on Players position
	for pos in [owner]:
		for block in config.paint_blocks:
			if pos.x == block.x and pos.z == block.z and block.color != pos.paint_color:
				block.color = pos.paint_color
				pos.colored_blocks += 1
				if block.owner == player:
					if not player.colored_blocks <= 0:
						player.colored_blocks -= 1
				elif block.owner == player2:
					if not player2.colored_blocks <= 0:
						player2.colored_blocks -= 1
				elif block.owner == player3:
					if not player3.colored_blocks <= 0:
						player3.colored_blocks -= 1
				elif block.owner == player4:
					if not player4.colored_blocks <= 0:
						player4.colored_blocks -= 1
				block.owner = pos

def reset_blocks(collider): ## delete all Blocks from player, which trigger this func.
	for pos in [collider]:
		for blocks in config.paint_blocks:
			if pos.paint_color == blocks.color:
				blocks.color = color.white
				blocks.owner = None
		pos.colored_blocks -= pos.colored_blocks

def paint_row(face_way, x, z, color, collider): ## the paint_row func
	for block in config.paint_blocks:
		if (face_way == 90 and block.position.z == z and block.position.x < x
			or face_way == 270 and block.position.z == z and x < block.position.x
			or face_way == 180 and block.position.x == x and z < block.position.z
			or face_way == 0 and block.position.x == x and block.position.z < z):
			if block.owner in (player, player2, player3, player4):
				block.owner.colored_blocks -= 1
			if block.color != collider.paint_color:
				block.color = collider.paint_color
				collider.colored_blocks += 1

def fourway_paint(collider): ##four_way func for painting 4 rows of blocks
	for blocks in config.paint_blocks:
		if blocks.position.x == collider.position.x or blocks.position.z == collider.position.z and blocks.color != collider.paint_color:
			blocks.color = collider.paint_color
			collider.colored_blocks += 1
			if blocks.owner == player:
				player.colored_blocks -= 1
			elif blocks.owner == player2:
				player2.colored_blocks -= 1
			elif blocks.owner == player3:
				player3.colored_blocks -= 1
			elif blocks.owner == player4:
				player4.colored_blocks -= 1

def double_paint(rotation_y, collider): ## double side Paint func for double arrow.
	for blocks in config.paint_blocks:
		if rotation_y == 0:
			if blocks.position.x == collider.position.x:
				blocks.color = collider.paint_color
				collider.colored_blocks += 1
				if block.owner == player:
					player.colored_blocks -= 1
				elif block.owner == player2:
					player2.colored_blocks -= 1
				elif block.owner == player3:
					player3.colored_blocks -= 1
				elif block.owner == player4:
					player4.colored_blocks -= 1
		else:
			if blocks.position.z == collider.position.z:
				blocks.color = collider.paint_color
				collider.colored_blocks += 1
				if block.owner == player:
					player.colored_blocks -= 1
				elif block.owner == player2:
					player2.colored_blocks -= 1
				elif block.owner == player3:
					player3.colored_blocks -= 1
				elif block.owner == player4:
					player4.colored_blocks -= 1

def check_position(): ### will refresh any logics in the Arena and check, if one of the 4 Players collide with one of the listed Items.
	for painter in [player,player2,player3,player4]:
		paint_single(owner=painter)
	for item in config.items:
			collided_players = [p for p in [player,player2,player3,player4] if p.position == item.position]
			if len(collided_players) > 0:
				if isinstance(item, Crate):
					collided_players[0].get_points()
					reset_blocks(collider=collided_players[0])
				elif isinstance(item, SpeedShoes):
					collided_players[0].mvsp_boost()
				elif isinstance(item, NitroCrate):
					collided_players[0].stun()
				elif isinstance(item, Arrow):
					paint_row(face_way=item.rotation_y, x=item.x, z=item.z, color=collided_players[0].paint_color, collider=collided_players[0])
				elif isinstance(item, Mushroom):
					collided_players[0].sub_points()
				elif isinstance(item, Missile):
					if collided_players[0].missile < 1:
						collided_players[0].missile += 1
				elif isinstance(item, FourWayArrow):
					fourway_paint(collider=collided_players[0])
				elif isinstance(item, DoubleArrow):
					double_paint(rotation_y=item.rotation_y, collider=collided_players[0])
				item.destroy()

def reset_arena(): ## After Win, reset Arena for next Round.
	global timer, start_time
	config.reset_state = False
	for players in [player,player2,player3,player4]:
		players.points = 0
		players.colored_blocks = 0
		players.position = players.default_pos
		players.rotation_y = players.default_rot
		players.show()
	timer = 90
	ui.start_time_text.show()
	start_time = 3.9

def set_victory(): ## Choose the Winner with the most collected points.
	highest_score = max(player.points, player2.points, player3.points, player4.points)
	if player.points == player2.points == player3.points == player4.points == highest_score:
		winner_text = Text(text='Tie!',position=(-0.3, 0.15), scale=6,color=color.green)
	elif player.points == highest_score:
		winner_text = Text(text='Player1 wins!',position=(-0.3, 0.15), scale=6,color=player.paint_color)
		player.rotation_y = 180
		player.victory += 1
		player2.hide()
		player3.hide()
		player4.hide()
	elif player2.points == highest_score:
		winner_text = Text(text='Player2 wins!',position=(-0.3, 0.15), scale=6,color=player2.paint_color)
		player2.rotation_y = 180
		player2.victory += 1
		player.hide()
		player3.hide()
		player4.hide()
	elif player3.points == highest_score:
		winner_text = Text(text='Player3 wins!',position=(-0.3, 0.15), scale=6,color=player3.paint_color)
		player3.rotation_y = 180
		player3.victory += 1
		player2.hide()
		player.hide()
		player4.hide()
	elif player4.points == highest_score:
		winner_text = Text(text='Player4 wins!',position=(-0.3, 0.15), scale=6,color=player4.paint_color)
		player4.rotation_y = 180
		player4.victory += 1
		player2.hide()
		player3.hide()
		player.hide()
	invoke(reset_arena, delay=5)
	invoke(winner_text.hide, delay=5)

def arena_dynamics(): ## refresh function.
	global timer, start_time
	spawn.rand()
	ui.refresh()
	check_position()
	if config.game_stop == True:
		for items in config.items:
			items.destroy()
	if config.reset_state == True:
		for blocks in config.paint_blocks:
			blocks.color = color.white
			blocks.owner = None
	if start_time > 0:
		start_time -= time.dt/1.25
		if start_time <= 0:
			config.game_stop = False
			ui.start_time_text.hide()
	if timer > 0 and config.game_stop == False:
		timer -= time.dt
		if timer <= 0:
			config.game_stop = True
			config.reset_state = True
			set_victory()
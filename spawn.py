from ursina import *
from player import *
import config
import random

def p_pos():
	for ppos in [player,player2,player3]:
		return ppos.position

def i_pos():
	for ipos in config.items:
		return ipos.position

def rand():
	if random.randint(0,100) == 100 and config.item_count < 20 and config.game_stop == False:
		spw_pos = (random.randint(0,7),0,random.randint(0,7))
		if spw_pos != i_pos() or spw_pos != p_pos():
			item_type = random.choice(config.item_choose)
			item_dict = config.item_dict
			config.item_count += 1
			item = item_dict[item_type](position=spw_pos)
			items = config.items
			items.append(item)
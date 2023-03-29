from ursina import *
from config import *
from player import *
import arena

# Info: in config.py you can customize the Models by linking it to a .obj and Texture Files.

def instance(): ## load the Game
	app = Ursina()
	arena.Map()
	player.model=player1_model
	#player.texture=player1_texture
	player2.model=player2_model
	#player2.texture=player2_texture
	player3.model=player3_model
	#player3.texture=player3_texture
	player4.model=player4_model
	#player4.texture=player4_texture
	app.run()
def update(): ## will update the Game Interfaces and Logics.
	arena.arena_dynamics()
instance()
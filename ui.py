from ursina import *
from player import *
import arena

def show():
	global point_text, point_text_a, point_text_b, point_text_c
	global timer_text, start_time_text, points
	timer_text = Text(text=arena.timer,position=(-0.05, 0.45), scale=3.5,color=color.orange)
	start_time_text = Text(text=arena.start_time,position=(-0.05, 0.15), scale=6,color=color.green)
	point_text = Text(text=player.points,position=(-0.75, 0.45), scale=2, color=config.player1_paint_color)
	point_text_a = Text(text=player2.points,position=(-0.55, 0.45), scale=2,color=config.player2_paint_color)
	point_text_b = Text(text=player2.points,position=(0.55, 0.45), scale=2,color=config.player3_paint_color)
	point_text_c = Text(text=player2.points,position=(0.75, 0.45), scale=2,color=config.player4_paint_color)

def refresh():
	minutes, seconds = divmod(int(arena.timer), 60)
	timer_text.text = f"{minutes:02d}:{seconds:02d}"
	start_time_text.text = int(arena.start_time)
	point_text.text = player.points
	point_text_a.text = player2.points
	point_text_b.text = player3.points
	point_text_c.text = player4.points
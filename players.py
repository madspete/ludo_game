from shutil import ExecError
import numpy as np

class Player:
	def __init__(self):
		pass

	def choose_move(self, player_pieces, enemy_pieces, dice, move_pieces):
		raise Exception("Should be implemented")
	
	def do_learn(self, player_pieces, enemy_pieces):
		raise Exception("Should be implemented")

class RandomPlayer(Player):
	def __init__(self):
		pass

	def choose_move(self, player_pieces, enemy_pieces, dice, move_pieces):
		if len(move_pieces):
			piece_to_move = move_pieces[np.random.randint(0, len(move_pieces))]
		else:
			piece_to_move = -1
		
		return piece_to_move

	def do_learn(self, player_pieces, enemy_pieces):
		pass
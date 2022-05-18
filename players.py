import numpy as np
from stateAndActions import StateAndActions
from ludopy.player import get_enemy_at_pos

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


# This player is taken from https://github.com/RasmusDonbaek/Ludo-help-for-tools-of-AI/blob/master/Players/player_fast.h
class PlayerFast(Player):
	def __init__(self):
		self.logic  = StateAndActions()

	def choose_move(self, player_pieces, enemy_pieces, dice, move_pieces):
		if len(move_pieces) == 1:
			piece_to_move = move_pieces[0]
			return piece_to_move
		elif len(move_pieces):
			for i in range(len(move_pieces)):
				pos = player_pieces[move_pieces[i]]
				if self.logic.can_reach_goal(pos, dice, enemy_pieces):
					piece_to_move = move_pieces[i]
					return piece_to_move
			
			for i in range(len(move_pieces)):
				pos = player_pieces[move_pieces[i]]
				if self.logic.home(pos) and self.logic.can_get_out_of_home(dice):
					pass 
					

		else:
			piece_to_move = -1
			return piece_to_move


	def do_learn(self, player_pieces, enemy_pieces):
		pass
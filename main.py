import ludopy
import numpy as np
import random
from qplayer import Qplayer
from players import RandomPlayer

if __name__ == '__main__':
	g = ludopy.Game()
	rand_player1 = RandomPlayer()
	rand_player2 = RandomPlayer()
	rand_player3 = RandomPlayer()
	q_player = Qplayer()
	q_player.save_q_table() # reset table
	players = [rand_player1, rand_player2, rand_player3, q_player]
	# Play some games
	for _ in range(100):
		there_is_a_winner = False
		g.reset()
		print(players)
		players = random.sample(players, len(players))
		print(players)
		while there_is_a_winner == False:
			(dice, move_pieces, player_pieces, enemy_pieces, player_is_a_winner, there_is_a_winner), player_i = g.get_observation()
			piece_to_move = players[player_i].choose_move(player_pieces, enemy_pieces, dice, move_pieces)
			_, _, new_pos, new_enemy_pos, _, there_is_a_winner = g.answer_observation(piece_to_move)
			players[player_i].do_learn(new_pos, new_enemy_pos)
		
		q_player.save_q_table()

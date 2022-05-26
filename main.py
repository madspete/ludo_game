import ludopy
import numpy as np
import random

from qplayer import Qplayer
from players import RandomPlayer, PlayerFast

LEARNING_FLAG = False
TEST_LEARNING_RATE = False
TEST_DISCOUNT_FACTOR = False
RANDOM_PLAYERS = False
SS_PLAYERS = False
SELF_PLAY = True
mean_rewards = []
win_percentage_learning_rates = []
win_percentage_discount_factor = []
win_percentage_against_random = []
win_percentage_against_ss = []
winner_count_against_random = []
winner_count_against_ss = []
q_value_changes = []
learning_rates = [0.001, 0.01, 0.05, 0.1, 0.2, 0.3]
discount_factors = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7,0.8,0.9]
if __name__ == '__main__':
	if LEARNING_FLAG:
		if TEST_LEARNING_RATE:
			g = ludopy.Game()

			# Play some games
			for learning_rate in learning_rates:
				win_percentage = []
				rand_player1 = RandomPlayer()
				rand_player2 = RandomPlayer()
				rand_player3 = RandomPlayer()
				q_player = Qplayer(learning_rate=learning_rate, epsilon=1.0, decay_rate=0.9995)
				q_player.save_q_table() # reset table
				players = [rand_player1, rand_player2, rand_player3, q_player]
				win_count = 0
				game_count = 0
				for i in range(5000):
					there_is_a_winner = False
					g.reset()
					players = random.sample(players, len(players))
					rewards = []
					while there_is_a_winner == False:
						(dice, move_pieces, player_pieces, enemy_pieces, player_is_a_winner, there_is_a_winner), player_i = g.get_observation()
						piece_to_move = players[player_i].choose_move(player_pieces, enemy_pieces, dice, move_pieces)
						_, _, player_pieces, enemy_pieces, _, there_is_a_winner = g.answer_observation(piece_to_move)
						players[player_i].do_learn(player_pieces, enemy_pieces)

					q_player.save_q_table()
					q_value_changes.append(q_player.get_q_value_changes())
					q_player.decrease_exploration_rate()
					q_player.average_q_values()
					q_player.reset()

				q_player.stop_learning()
				q_player.load_q_table()

				for i in range(1000):
					there_is_a_winner = False
					g.reset()
					players = random.sample(players, len(players))
					while there_is_a_winner == False:
						(dice, move_pieces, player_pieces, enemy_pieces, player_is_a_winner, there_is_a_winner), player_i = g.get_observation()
						piece_to_move = players[player_i].choose_move(player_pieces, enemy_pieces, dice, move_pieces)
						_, _, player_pieces, enemy_pieces, _, there_is_a_winner = g.answer_observation(piece_to_move)
					game_count = game_count + 1
					if players[g.get_winner_of_game()] == q_player:
						win_count = win_count + 1
					win_percentage.append((win_count/game_count)*100)

				win_percentage_learning_rates.append(win_percentage)
				win_percentage = []

		if TEST_DISCOUNT_FACTOR:
			g = ludopy.Game()

			# Play some games
			for discount_factor in discount_factors:
				win_percentage = []
				rand_player1 = RandomPlayer()
				rand_player2 = RandomPlayer()
				rand_player3 = RandomPlayer()
				q_player = Qplayer(learning_rate=0.05, epsilon=1.0, decay_rate=0.9995, discount_factor=discount_factor)
				q_player.save_q_table() # reset table
				players = [rand_player1, rand_player2, rand_player3, q_player]
				win_count = 0
				game_count = 0
				for i in range(5000):
					there_is_a_winner = False
					g.reset()
					players = random.sample(players, len(players))
					rewards = []
					while there_is_a_winner == False:
						(dice, move_pieces, player_pieces, enemy_pieces, player_is_a_winner, there_is_a_winner), player_i = g.get_observation()
						piece_to_move = players[player_i].choose_move(player_pieces, enemy_pieces, dice, move_pieces)
						_, _, player_pieces, enemy_pieces, _, there_is_a_winner = g.answer_observation(piece_to_move)
						players[player_i].do_learn(player_pieces, enemy_pieces)

					q_player.save_q_table()
					rewards.append(q_player.get_mean_rewards())
					q_value_changes.append(q_player.get_q_value_changes())
					q_player.decrease_exploration_rate()
					q_player.average_q_values()
					q_player.reset()

				q_player.stop_learning()
				q_player.load_q_table()

				for i in range(1000):
					there_is_a_winner = False
					g.reset()
					players = random.sample(players, len(players))
					while there_is_a_winner == False:
						(dice, move_pieces, player_pieces, enemy_pieces, player_is_a_winner, there_is_a_winner), player_i = g.get_observation()
						piece_to_move = players[player_i].choose_move(player_pieces, enemy_pieces, dice, move_pieces)
						_, _, player_pieces, enemy_pieces, _, there_is_a_winner = g.answer_observation(piece_to_move)
					game_count = game_count + 1
					if players[g.get_winner_of_game()] == q_player:
						win_count = win_count + 1
					win_percentage.append((win_count/game_count)*100)

				win_percentage_discount_factor.append(win_percentage)
				win_percentage = []
				
		if RANDOM_PLAYERS:
			g = ludopy.Game()
			rand_player1 = RandomPlayer()
			rand_player2 = RandomPlayer()
			rand_player3 = RandomPlayer()
			q_player = Qplayer(learning_rate=0.01, epsilon=1.0, decay_rate=0.9995, discount_factor=0.7)
			q_player.save_q_table(filename="qtables/random_players_qtable.txt") # reset table
			players = [rand_player1, rand_player2, rand_player3, q_player]
			# Play some games
			rewards = []
			for i in range(5000):
				there_is_a_winner = False
				g.reset()
				players = random.sample(players, len(players))
				while there_is_a_winner == False:
					(dice, move_pieces, player_pieces, enemy_pieces, player_is_a_winner, there_is_a_winner), player_i = g.get_observation()
					piece_to_move = players[player_i].choose_move(player_pieces, enemy_pieces, dice, move_pieces)
					_, _, player_pieces, enemy_pieces, _, there_is_a_winner = g.answer_observation(piece_to_move)
					players[player_i].do_learn(player_pieces, enemy_pieces)

				q_player.decrease_exploration_rate()
				q_player.average_q_values()
				q_player.reset()
				q_player.save_q_table(filename="qtables/random_players_qtable.txt")

		if SS_PLAYERS:
			g = ludopy.Game()
			ss_player1 = PlayerFast()
			ss_player2 = PlayerFast()
			ss_player3 = PlayerFast()
			q_player = Qplayer(learning_rate=0.01, epsilon=1.0, decay_rate=0.9995, discount_factor=0.7)
			q_player.save_q_table(filename="qtables/ss_players_qtable.txt") # reset table
			players = [ss_player1, ss_player2, ss_player3, q_player]
			# Play some games
			rewards = []
			for i in range(5000):
				there_is_a_winner = False
				g.reset()
				players = random.sample(players, len(players))
				while there_is_a_winner == False:
					(dice, move_pieces, player_pieces, enemy_pieces, player_is_a_winner, there_is_a_winner), player_i = g.get_observation()
					piece_to_move = players[player_i].choose_move(player_pieces, enemy_pieces, dice, move_pieces)
					_, _, player_pieces, enemy_pieces, _, there_is_a_winner = g.answer_observation(piece_to_move)
					players[player_i].do_learn(player_pieces, enemy_pieces)

				q_player.decrease_exploration_rate()
				q_player.average_q_values()
				q_player.reset()
				q_player.save_q_table(filename="qtables/ss_players_qtable.txt")

		if SELF_PLAY:
			g = ludopy.Game()
			q_player1 = Qplayer(learn=False)
			q_player2 = Qplayer(learn=False)
			q_player3 = Qplayer(learn=False)
			q_player = Qplayer(learning_rate=0.01, epsilon=1.0, decay_rate=0.9995, discount_factor=0.7)
			q_player.save_q_table(filename="qtables/q_players_qtable.txt") # reset table
			players = [q_player1, q_player2, q_player3, q_player]
			# Play some games
			rewards = []
			for i in range(5000):
				q_player1.load_q_table(filename="qtables/q_players_qtable.txt")
				q_player2.load_q_table(filename="qtables/q_players_qtable.txt")
				q_player3.load_q_table(filename="qtables/q_players_qtable.txt")
				there_is_a_winner = False
				g.reset()
				players = random.sample(players, len(players))
				while there_is_a_winner == False:
					(dice, move_pieces, player_pieces, enemy_pieces, player_is_a_winner, there_is_a_winner), player_i = g.get_observation()
					piece_to_move = players[player_i].choose_move(player_pieces, enemy_pieces, dice, move_pieces)
					_, _, player_pieces, enemy_pieces, _, there_is_a_winner = g.answer_observation(piece_to_move)
					players[player_i].do_learn(player_pieces, enemy_pieces)

				q_player.decrease_exploration_rate()
				q_player.average_q_values()
				q_player.reset()
				q_player.save_q_table(filename="qtables/q_players_qtable.txt")

	else:
		g = ludopy.Game()
		rand_player1 = RandomPlayer()
		rand_player2 = RandomPlayer()
		rand_player3 = RandomPlayer()
		q_player = Qplayer(learn=False)
		if RANDOM_PLAYERS:
			q_player.load_q_table(filename="qtables/random_players_qtable.txt") # load table
		elif SS_PLAYERS:
			q_player.load_q_table(filename="qtables/ss_players_qtable.txt") # load table
		elif SELF_PLAY:
			q_player.load_q_table(filename="qtables/q_players_qtable.txt") # load table
		players = [rand_player1, rand_player2, rand_player3, q_player]
		for j in range(10):
			game_count = 0
			winner_count = 0
			win_percentage = []
			for i in range(2000):
				there_is_a_winner = False
				g.reset()
				players = random.sample(players, len(players))
				while there_is_a_winner == False:
					(dice, move_pieces, player_pieces, enemy_pieces, player_is_a_winner, there_is_a_winner), player_i = g.get_observation()
					piece_to_move = players[player_i].choose_move(player_pieces, enemy_pieces, dice, move_pieces)
					_, _, new_pos, new_enemy_pos, _, there_is_a_winner = g.answer_observation(piece_to_move)
				game_count = game_count + 1
				if players[g.get_winner_of_game()] == q_player:
					winner_count = winner_count + 1
				win_percentage.append((winner_count/game_count)*100)
			win_percentage_against_random.append(win_percentage)
			winner_count_against_random.append(winner_count)
		
		ss_player1 = PlayerFast()
		ss_player2 = PlayerFast()
		ss_player3 = PlayerFast()		
		players = [q_player, ss_player1, ss_player2, ss_player3]
		for j in range(10):
			game_count = 0
			winner_count = 0
			win_percentage = []
			for i in range(2000):
				there_is_a_winner = False
				g.reset()
				players = random.sample(players, len(players))
				while there_is_a_winner == False:
					(dice, move_pieces, player_pieces, enemy_pieces, player_is_a_winner, there_is_a_winner), player_i = g.get_observation()
					piece_to_move = players[player_i].choose_move(player_pieces, enemy_pieces, dice, move_pieces)
					_, _, new_pos, new_enemy_pos, _, there_is_a_winner = g.answer_observation(piece_to_move)
				game_count = game_count + 1
				if players[g.get_winner_of_game()] == q_player:
					winner_count = winner_count + 1
				win_percentage.append((winner_count/game_count)*100)
			win_percentage_against_ss.append(win_percentage)
			winner_count_against_ss.append(winner_count)

if LEARNING_FLAG:
	if TEST_LEARNING_RATE:
		file1 = open("data/win_percentage_learning_rates.txt", "w")
		for i in range(len(win_percentage_learning_rates[0])):
			for j in range(len(win_percentage_learning_rates)):
				file1.write(str(win_percentage_learning_rates[j][i]))
				file1.write(",")	
			file1.write("\n")
		file1.close()
	
	if TEST_DISCOUNT_FACTOR:
		file1 = open("data/win_percentage_discount_factor.txt", "w")
		for i in range(len(win_percentage_discount_factor[0])):
			for j in range(len(win_percentage_discount_factor)):
				file1.write(str(win_percentage_discount_factor[j][i]))
				file1.write(",")	
			file1.write("\n")
		file1.close()		

	file1 = open("data/q_value_changes.txt", "w")
	for i in range(len(q_value_changes)):
		file1.write(str(q_value_changes[i]))
		file1.write("\n")
	file1.close()
else:
	if RANDOM_PLAYERS:
		file1 = open("data/win_percentage_random_against_random.txt", "w")
		for i in range(len(win_percentage_against_random[0])):
			for j in range(len(win_percentage_against_random)):
				file1.write(str(win_percentage_against_random[j][i]))
				file1.write(",")	
			file1.write("\n")
		file1.close()

		file1 = open("data/win_count_random_against_random.txt", "w")
		for j in range(len(winner_count_against_random)):
			file1.write(str(winner_count_against_random[j]))
			file1.write("\n")
		file1.close()

		file1 = open("data/win_percentage_random_against_ss.txt", "w")
		for i in range(len(win_percentage_against_ss[0])):
			for j in range(len(win_percentage_against_ss)):
				file1.write(str(win_percentage_against_ss[j][i]))
				file1.write(",")	
			file1.write("\n")
		file1.close()

		file1 = open("data/win_count_random_against_ss.txt", "w")
		for j in range(len(winner_count_against_ss)):
			file1.write(str(winner_count_against_ss[j]))
			file1.write("\n")
		file1.close()		

	if SS_PLAYERS:
		file1 = open("data/win_percentage_ss_against_random.txt", "w")
		for i in range(len(win_percentage_against_random[0])):
			for j in range(len(win_percentage_against_random)):
				file1.write(str(win_percentage_against_random[j][i]))
				file1.write(",")	
			file1.write("\n")
		file1.close()

		file1 = open("data/win_count_ss_against_random.txt", "w")
		for j in range(len(winner_count_against_random)):
			file1.write(str(winner_count_against_random[j]))
			file1.write("\n")
		file1.close()

		file1 = open("data/win_percentage_ss_against_ss.txt", "w")
		for i in range(len(win_percentage_against_ss[0])):
			for j in range(len(win_percentage_against_ss)):
				file1.write(str(win_percentage_against_ss[j][i]))
				file1.write(",")	
			file1.write("\n")
		file1.close()

		file1 = open("data/win_count_ss_against_ss.txt", "w")
		for j in range(len(winner_count_against_ss)):
			file1.write(str(winner_count_against_ss[j]))
			file1.write("\n")
		file1.close()		

	if SELF_PLAY:
		file1 = open("data/win_percentage_self_against_random.txt", "w")
		for i in range(len(win_percentage_against_random[0])):
			for j in range(len(win_percentage_against_random)):
				file1.write(str(win_percentage_against_random[j][i]))
				file1.write(",")	
			file1.write("\n")
		file1.close()

		file1 = open("data/win_count_self_against_random.txt", "w")
		for j in range(len(winner_count_against_random)):
			file1.write(str(winner_count_against_random[j]))
			file1.write("\n")
		file1.close()

		file1 = open("data/win_percentage_self_against_ss.txt", "w")
		for i in range(len(win_percentage_against_ss[0])):
			for j in range(len(win_percentage_against_ss)):
				file1.write(str(win_percentage_against_ss[j][i]))
				file1.write(",")	
			file1.write("\n")
		file1.close()

		file1 = open("data/win_count_self_against_ss.txt", "w")
		for j in range(len(winner_count_against_ss)):
			file1.write(str(winner_count_against_ss[j]))
			file1.write("\n")
		file1.close()		
import sys
import os
from qplayer import Qplayer
import ludopy
import random
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../TOAI_LUDO_Project.AI/')))
from TOAI_LUDO_Project.AI import AI

win_percentage_against_jens = []
winner_count_against_jens = []
JENS = True

if __name__ == '__main__':
	g = ludopy.Game()
	if not JENS:
		jensAi1 = AI("/home/mads/git/TOAI_LUDO_Project/Qtable.npy")
		jensAi2 = AI("/home/mads/git/TOAI_LUDO_Project/Qtable.npy")
		jensAi3 = AI("/home/mads/git/TOAI_LUDO_Project/Qtable.npy")
		q_player = Qplayer(learn=False)
		q_player.load_q_table("qtables/ss_players_qtable.txt")
		players = [jensAi1, jensAi2, jensAi3, q_player]
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
					if players[player_i] == q_player:
						piece_to_move = players[player_i].choose_move(player_pieces, enemy_pieces, dice, move_pieces)
					else:
						piece_to_move =  players[player_i].onePass(dice, player_pieces, enemy_pieces)
					_, _, new_pos, new_enemy_pos, _, there_is_a_winner = g.answer_observation(piece_to_move)
				game_count = game_count + 1
				if players[g.get_winner_of_game()] == q_player:
					winner_count = winner_count + 1
				print(f"there is a winner {game_count}")
				win_percentage.append((winner_count/game_count)*100)
			win_percentage_against_jens.append(win_percentage)
			winner_count_against_jens.append(winner_count)
		

		file1 = open("data/win_percentage_against_jens.txt", "w")
		for i in range(len(win_percentage_against_jens[0])):
			for j in range(len(win_percentage_against_jens)):
				file1.write(str(win_percentage_against_jens[j][i]))
				file1.write(",")	
			file1.write("\n")
		file1.close()

		file1 = open("data/win_count_against_jens.txt", "w")
		for j in range(len(winner_count_against_jens)):
			file1.write(str(winner_count_against_jens[j]))
			file1.write("\n")
		file1.close()		
	else:
		jensAi = AI("/home/mads/git/TOAI_LUDO_Project/QTable1Player.npy")
		q_player1 = Qplayer(learn=False)
		q_player2 = Qplayer(learn=False)
		q_player3 = Qplayer(learn=False)
		q_player1.load_q_table("qtables/ss_players_qtable.txt")
		q_player2.load_q_table("qtables/ss_players_qtable.txt")
		q_player3.load_q_table("qtables/ss_players_qtable.txt")
		players = [q_player1, q_player2, q_player3, jensAi]
		for j in range(10):
			game_count = 0
			winner_count = 0
			win_percentage = []
			for i in range(1000):
				there_is_a_winner = False
				g.reset()
				players = random.sample(players, len(players))
				while there_is_a_winner == False:
					(dice, move_pieces, player_pieces, enemy_pieces, player_is_a_winner, there_is_a_winner), player_i = g.get_observation()
					if players[player_i] == jensAi:
						piece_to_move =  players[player_i].onePass(dice, player_pieces, enemy_pieces)
					else:
						piece_to_move = players[player_i].choose_move(player_pieces, enemy_pieces, dice, move_pieces)
					_, _, new_pos, new_enemy_pos, _, there_is_a_winner = g.answer_observation(piece_to_move)
				game_count = game_count + 1
				if players[g.get_winner_of_game()] == jensAi:
					winner_count = winner_count + 1
				print(f"there is a winner {game_count}")
				win_percentage.append((winner_count/game_count)*100)
			win_percentage_against_jens.append(win_percentage)
			winner_count_against_jens.append(winner_count)
		

		file1 = open("data/win_percentage_for_jens.txt", "w")
		for i in range(len(win_percentage_against_jens[0])):
			for j in range(len(win_percentage_against_jens)):
				file1.write(str(win_percentage_against_jens[j][i]))
				file1.write(",")	
			file1.write("\n")
		file1.close()

		file1 = open("data/win_count_for_jens.txt", "w")
		for j in range(len(winner_count_against_jens)):
			file1.write(str(winner_count_against_jens[j]))
			file1.write("\n")
		file1.close()		
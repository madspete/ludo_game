import matplotlib.pyplot as plt
import csv
import numpy as np

RANDOM_PLAY = False
SS_PLAY = False
SELF_PLAY = False
AGAINST_JENS = True

path = ""
path1 = ""

if RANDOM_PLAY:
	path = "data/win_percentage_random_against_random.txt"
	path1 = "data/win_percentage_random_against_ss.txt"
if SS_PLAY:
	path = "data/win_percentage_ss_against_random.txt"
	path1 = "data/win_percentage_ss_against_ss.txt"	
if SELF_PLAY:
	path = "data/win_percentage_self_against_random.txt"
	path1 = "data/win_percentage_self_against_ss.txt"	
if AGAINST_JENS:
	path = "data/win_percentage_against_jens.txt"
	path1 = "data/win_percentage_against_jens.txt"

average_win_percentages_random = []
average_win_percentages_ss = []
game_count = []
final_win_percentage_random = []
final_win_percentage_ss = []

with open(path) as csv_file:
	csv_reader = csv.reader(csv_file, delimiter=',')
	counter = 0
	for row in csv_reader:
		final_win_percentage_random = []
		win_percentage = float(row[0]) + float(row[1]) + float(row[2]) + float(row[3]) + float(row[4]) + \
						 float(row[5]) + float(row[6]) + float(row[7]) + float(row[8]) + float(row[9])
		game_count.append(counter)
		final_win_percentage_random.append(float(row[0]))
		final_win_percentage_random.append(float(row[1]))
		final_win_percentage_random.append(float(row[2]))
		final_win_percentage_random.append(float(row[3]))
		final_win_percentage_random.append(float(row[4]))
		final_win_percentage_random.append(float(row[5]))
		final_win_percentage_random.append(float(row[6]))
		final_win_percentage_random.append(float(row[7]))
		final_win_percentage_random.append(float(row[8]))
		final_win_percentage_random.append(float(row[9]))
		counter += 1
		average_win_percentages_random.append(win_percentage / 10)

with open(path1) as csv_file:
	csv_reader = csv.reader(csv_file, delimiter=',')
	for row in csv_reader:
		final_win_percentage_ss = []
		win_percentage = float(row[0]) + float(row[1]) + float(row[2]) + float(row[3]) + float(row[4]) + \
						 float(row[5]) + float(row[6]) + float(row[7]) + float(row[8]) + float(row[9])
		average_win_percentages_ss.append(win_percentage / 10)
		final_win_percentage_ss.append(float(row[0]))
		final_win_percentage_ss.append(float(row[1]))
		final_win_percentage_ss.append(float(row[2]))
		final_win_percentage_ss.append(float(row[3]))
		final_win_percentage_ss.append(float(row[4]))
		final_win_percentage_ss.append(float(row[5]))
		final_win_percentage_ss.append(float(row[6]))
		final_win_percentage_ss.append(float(row[7]))
		final_win_percentage_ss.append(float(row[8]))
		final_win_percentage_ss.append(float(row[9]))

plt.figure(1)
plt.plot(game_count, average_win_percentages_random)
plt.xlabel("Number of games")
plt.ylabel("Win percentage [%]")
plt.title("Average winning percentage against 3 random players")

plt.figure(2)
plt.plot(game_count, average_win_percentages_ss)
plt.xlabel("Number of games")
plt.ylabel("Win percentage [%]")
plt.title("Average winning percentage against 3 of Jens's Q-player")

# Statitics 
print(f"Mean winning percentage after 2000 games against ss players {np.mean(final_win_percentage_ss)}")
print(f"std dev winning percentage after 2000 games against ss players {np.std(final_win_percentage_ss)}")
print(f"Mean winning percentage after 2000 games against random players {np.mean(final_win_percentage_random)}")
print(f"std dev winning percentage after 2000 games against random players {np.std(final_win_percentage_random)}")

print(final_win_percentage_random)
print(final_win_percentage_ss)

plt.show()
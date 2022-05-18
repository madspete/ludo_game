import matplotlib.pyplot as plt
import csv

path = "data/win_percentage_learning_rates.txt"
path1 = "data/win_percentage_discount_factor.txt"

win_percentage = []
win_percentage1 = []
win_percentage2 = []
win_percentage3 = []
win_percentage4 = []
win_percentage5 = []
win_percentage6 = []
win_percentage7 = []
win_percentage8 = []
episode = []

with open(path1) as csv_file:
	csv_reader = csv.reader(csv_file, delimiter=',')
	counter = 0
	for row in csv_reader:
		win_percentage.append(float(row[0]))
		win_percentage1.append(float(row[1]))
		win_percentage2.append(float(row[2]))
		win_percentage3.append(float(row[3]))
		win_percentage4.append(float(row[4]))
		win_percentage5.append(float(row[5]))
		win_percentage6.append(float(row[6]))
		win_percentage7.append(float(row[7]))
		win_percentage8.append(float(row[8]))
		episode.append(counter)
		counter += 1

plt.figure(1)
plt.plot(episode, win_percentage)
plt.plot(episode, win_percentage1)
plt.plot(episode, win_percentage2)
plt.plot(episode, win_percentage3)
plt.plot(episode, win_percentage4)
plt.plot(episode, win_percentage5)
plt.plot(episode, win_percentage6)
plt.plot(episode, win_percentage7)
plt.plot(episode, win_percentage8)
plt.xlabel("Number of games")
plt.ylabel("Win percentage [%]")
plt.title("Winning rate against 3 random players with different discount factors")
plt.legend(["0.1, WP:72.4", "0.2 WP:72.5", "0.3 WP:71.5", "0.4 WP:70.3", "0.5 WP:69.9", "0.6 WP:71.3", "0.7 WP:73.6","0.8 WP:70.6","0.9 WP:53.4"], loc ="lower right")

win_percentage = []
win_percentage1 = []
win_percentage2 = []
win_percentage3 = []
win_percentage4 = []
win_percentage5 = []
win_percentage6 = []
win_percentage7 = []
win_percentage8 = []
episode = []

with open(path) as csv_file:
	csv_reader = csv.reader(csv_file, delimiter=',')
	counter = 0
	for row in csv_reader:
		win_percentage.append(float(row[0]))
		win_percentage1.append(float(row[1]))
		win_percentage2.append(float(row[2]))
		win_percentage3.append(float(row[3]))
		win_percentage4.append(float(row[4]))
		win_percentage5.append(float(row[4]))
		episode.append(counter)
		counter += 1

plt.figure(2)
plt.plot(episode, win_percentage)
plt.plot(episode, win_percentage1)
plt.plot(episode, win_percentage2)
plt.plot(episode, win_percentage3)
plt.plot(episode, win_percentage4)
plt.plot(episode, win_percentage5)
plt.xlabel("Number of games")
plt.ylabel("Win percentage [%]")
plt.title("Winning rate against 3 random players with different learning rates")
plt.legend(["0.001 WP: 66.5", "0.01 WP: 71.7", "0.05 WP: 74.5", "0.1 WP: 72.0", "0.2 WP: 72.1", "0.3 WP: 73.0"], loc ="lower right")

plt.show()
import numpy
import itertools

STATES = ["goal", "home", "safe", "unsafe", "danger", "goal zone"]
ACTIONS = ["move_out", "goal_zone", "star", "globe", "protect", "kill", "goal", "move closets piece", "die", "miss goal", "nothing", "move out of danger"]
		
class Qtable:
	def __init__(self):
		self.__states = list(itertools.combinations_with_replacement(STATES, 4))
		self.__q_table = numpy.zeros((len(self.__states),len(ACTIONS)))

	def get_index(self, in_goal, home, safe, unsafe, danger, goal_zone):
		comb = []
		for i in range(in_goal):
			comb.append("goal")
		for i in range(home):
			comb.append("home")
		for _ in range(safe):
			comb.append("safe")
		for _ in range(unsafe):
			comb.append("unsafe")
		for _ in range(danger):
			comb.append("danger")
		for _ in range(goal_zone):
			comb.append("goal zone")
		
		if len(comb) != 4:
			raise Exception("invalid combination size")
		comb = tuple(comb)

		return self.__get_index(comb)
	
	def get_values(self, index):
		"""Returns all the values at the specific state."""
		return self.__q_table[index]

	def set_value(self, index, values):
		"""Set all the values at a specific index"""
		self.__q_table[index] = values

	def save_values(self, file_name):
		file = open(file_name, "w")
		if file.writable():
			for i in range(len(self.__q_table)):
				for j in range(len(self.__q_table[i])):
					if j != 0:
						file.write(",")
					file.write(str(self.__q_table[i][j]))
				file.write("\n")
		else:
			raise Exception("Failed to write to a file")

	def load_values(self, file_name):
		file = open(file_name, "r")
		if file.readable():
			lines = file.readlines()
			index = 0
			for line in lines:
				data = line.split(",")
				for i in range(len(data)):
					self.__q_table[index][i] = float(data[i]) 
				index = index + 1
		else:
			raise Exception("Failed to read from the file")		

	def __get_index(self, comb):
		index = None
		for i in range(len(self.__states)):
			res = all(x == y for x, y in zip(comb, self.__states[i]))
			if res:
				index = i
				break
		if index == None:
			raise Exception("Unable to find combination")

		return index

# Used for testing the class
if __name__ == '__main__':
	q_table = Qtable()
	states = list(itertools.combinations_with_replacement(STATES, 4))
	for i in range(len(states)):
		goal_count = 0
		home_count = 0 
		safe_count = 0
		unsafe_count = 0
		danger_count = 0
		goal_zone_count = 0
		for j in range(len(states[i])):
			if states[i][j] == "goal":
				goal_count = goal_count + 1
			elif states[i][j] == "home":
				home_count = home_count + 1
			elif states[i][j] == "safe":
				safe_count = safe_count + 1
			elif states[i][j] == "unsafe":
				unsafe_count = unsafe_count + 1
			elif states[i][j] == "danger":
				danger_count = danger_count + 1
			elif states[i][j] == "goal zone":
				goal_zone_count = goal_zone_count + 1

		q_table.get_index(goal_count, home_count, safe_count, unsafe_count, danger_count, goal_zone_count)
	q_table.set_value(12, [2,2,2,2,2,2,2,2,2,2,2,2])
	q_table.save_values("q_table.txt")
	q_table.load_values("q_table.txt")
	print(q_table.get_values(12))
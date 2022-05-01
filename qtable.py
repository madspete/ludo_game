import numpy
import itertools
from stateAndActions import States, Actions
		
class Qtable:
	def __init__(self):
		states = []
		for data in States:
			states.append(data.name)
		self.__states = list(itertools.combinations_with_replacement(states, 4))
		self.__q_table = numpy.zeros((len(self.__states),len(Actions)))

	def get_index(self, states):
		comb = []
		# We need to make sure the list has the correct order
		for data in States:
			cur_count = states.count(data)
			for _ in range(cur_count):
				comb.append(data.name)

		if len(comb) != 4:
			raise Exception("invalid combination size")
		comb = tuple(comb)

		return self.__get_index(comb)
	
	def get_values(self, index):
		"""Returns all the values at the specific state."""
		return self.__q_table[index]

	def set_value(self, index, action, value):
		"""Set the value at a specific index"""
		self.__q_table[index][action.value] = value

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
				print(self.__states[i])
				index = i
				break
		if index == None:
			raise Exception("Unable to find combination")

		return index

# Used for testing the class
if __name__ == '__main__':
	q_table = Qtable()
	states = []
	for data in States:
		states.append(data.name)
	states = list(itertools.combinations_with_replacement(states, 4))
	for i in range(len(states)):
		goal_count = 0
		home_count = 0 
		safe_count = 0
		unsafe_count = 0
		danger_count = 0
		goal_zone_count = 0
		cur_state = []
		for j in range(len(states[i])):
			if states[i][j] == States.GOAL.name:
				cur_state.append(States.GOAL)
			elif states[i][j] == States.HOME.name:
				cur_state.append(States.HOME)
			elif states[i][j] == States.SAFE.name:
				cur_state.append(States.SAFE)
			elif states[i][j] == States.DANGER.name:
				cur_state.append(States.DANGER)
			elif states[i][j] == States.GOAL_ZONE.name:
				cur_state.append(States.GOAL_ZONE)

		index = q_table.get_index(cur_state)
	q_table.set_value(12, [2,2,2,2,2,2,2,2,2,2,2,2,2])
	q_table.save_values("q_table.txt")
	q_table.load_values("q_table.txt")
	print(q_table.get_values(12))

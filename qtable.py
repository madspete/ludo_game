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
				index = i
				break
		if index == None:
			raise Exception("Unable to find combination")

		return index
	
	def write_states_to_file(self):
		file1 = open("q_table_name.txt", "w")
		for i in range(len(self.__states)):
			file1.write(str(self.__states[i]))
			file1.write("\n")
		file1.close()

# Used for testing the class
if __name__ == '__main__':
	q_table = Qtable()
	q_table.write_states_to_file()	
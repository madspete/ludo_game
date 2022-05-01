from tkinter import N
import numpy
from stateAndActions import StateAndActions, Actions, REWARDS
from qtable import Qtable
from players import Player

class Qplayer(Player):
	def __init__(self, learn=True, discount_factor = 0.8, learning_rate=0.1, epsilon=0.1):
		self.learn = learn

		if (discount_factor < 0.0 or discount_factor > 1.0):
			raise Exception("discountt factor should be between 0 and 1")
		self.discount_factor = discount_factor
		if (learning_rate < 0.0 or learning_rate > 1.0):
			raise Exception("Learning rate should be between 0 and 1")
		self.learning_rate = learning_rate
		if (epsilon < 0.0 or epsilon > 1.0):
			raise Exception("Epsilon shold be betwen 0 and 1")
		self.epsilon = epsilon
		self.state_and_action = StateAndActions()
		self.q_table = Qtable()
		self.q_index = -1
		self.reward = -1
		self.action = None

	def set_learning_rate(self, learning_rate):
		if (learning_rate < 0.0 or learning_rate > 1.0):
			raise Exception("Learning rate should be between 0 and 1")
		self.learning_rate = learning_rate
	
	def set_discout_factor(self, discount_factor):
		if (discount_factor < 0.0 or discount_factor > 1.0):
			raise Exception("discountt factor should be between 0 and 1")
		self.discount_factor = discount_factor
	
	def set_epsilon(self, epsilon):
		if (epsilon < 0.0 or epsilon > 1.0):
			raise Exception("Epsilon shold be betwen 0 and 1")
		self.epsilon = epsilon
	
	def choose_move(self, player_pieces, enemy_pieces, dice, move_pieces):
		"""Choose which piece to move."""
		piece_to_move = -1
		# Get state

		state_vector = self.get_state(player_pieces, enemy_pieces)
		self.q_index = self.q_table.get_index(state_vector)
		q_values = self.q_table.get_values(self.q_index)

		# Get possible actions
		action_vector = []
		for i in range(len(player_pieces)):
			other_pieces = []
			for j in range(len(player_pieces)):
				if j == i:
					continue
				other_pieces.append(player_pieces[j])	
			action_vector.append(self.state_and_action.get_action(state_vector[i], player_pieces[i], dice, other_pieces, enemy_pieces))
		
		# Extract the possible actions to a list
		possible_actions = []
		available_q_values = []
		piece = []
		for i in range(len(action_vector)):
			for j in range(len(action_vector[i])):
				if action_vector[i][j] != Actions.NOTHING:
					possible_actions.append(action_vector[i][j])
					available_q_values.append(q_values[action_vector[i][j].value])
					piece.append(i)

		# No moves available	
		if len(available_q_values) == 0:
			self.action = None
			return piece_to_move

		# Exploration
		if self.learn and numpy.random.random() < self.epsilon:
			# Choose random among possible actions
			possible_actions = numpy.array(possible_actions)
			index = numpy.random.choice(numpy.arange(possible_actions.size))
			piece_to_move = piece[index]
			self.q_value = q_values[index]
			self.reward = REWARDS[int(possible_actions[index].value)]
			self.action = possible_actions[index]
		# Exploitation
		else:
			# Chose maximum q value, if there are multiple chose randomely among them
			indices = [index for index, item in enumerate(available_q_values) if item == max(available_q_values)]
			if len(indices) > 1:
				index = numpy.random.choice(indices)
				piece_to_move = piece[index]
				self.q_value = q_values[index]
				self.reward = REWARDS[int(possible_actions[index].value)]
				self.action = possible_actions[index]
			else:
				piece_to_move = piece[indices[0]]
				self.q_value = q_values[indices[0]]
				self.reward = REWARDS[int(possible_actions[indices[0]].value)]
				self.action = possible_actions[indices[0]]			

		return piece_to_move

	def do_learn(self, player_pieces, enemy_pieces):
		if self.action == None or self.do_learn == False:
			return
		state_vector = self.get_state(player_pieces, enemy_pieces)
		new_q_index = self.q_table.get_index(state_vector)
		updated_q_value = self.learning_rate * (self.reward + self.discount_factor*max(self.q_table.get_values(new_q_index)) - self.q_value)
		self.q_table.set_value(self.q_index, self.action, updated_q_value)
			
	def get_state(self, player_pieces, enemy_pieces):
		state_vector = []
		for i in range(len(player_pieces)):
			other_pieces = []
			for j in range(len(player_pieces)):
				if j == i:
					continue
				other_pieces.append(player_pieces[j])

			state_vector.append(self.state_and_action.get_state(player_pieces[i],other_pieces, enemy_pieces))
		
		return state_vector
	
	def save_q_table(self):
		self.q_table.save_values("q_table.txt")

	def load_q_table(self):
		self.q_table.load_values("q_table.txt")


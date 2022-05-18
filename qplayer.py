import numpy
from stateAndActions import StateAndActions, Actions, REWARDS, States, STATE_REWARDS
from players import Player

class Qplayer(Player):
	def __init__(self, learn=True, discount_factor = 0.6, learning_rate=0.1, epsilon=1.0, decay_rate=0.9995):
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
		self.q_index = -1
		self.reward = -1
		self.action = None
		self.reward_list = []
		self.exploration_rate_decay = decay_rate
		self.min_epsilon = 0.1
		self.Q = numpy.zeros([len(States)*4, len(Actions)])
		print(self.Q.shape)
		self.piece_to_move = -1
		self.q_value_changes = 0

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
		self.piece_to_move = -1
		# Get state
		state_vector, action_vector, q_values, indices = self.get_state_and_actions(player_pieces, dice, enemy_pieces)

		# Just figure out how to choose an action and that stuff
		# No moves available
		if not len(move_pieces):
			self.action = None
			return self.piece_to_move

		# Exploration
		if self.learn and numpy.random.random() <= self.epsilon:
			# Choose random among possible actions
			index = numpy.random.choice(numpy.arange(len(action_vector)))
			self.piece_to_move = indices[index]
			self.q_value = q_values[index]
			self.reward = REWARDS[int(action_vector[index].value)] + STATE_REWARDS[state_vector[self.piece_to_move].value]
			self.action = action_vector[index]
			self.state = state_vector[indices[index]]
		# Exploitation
		else:
			# Chose maximum q value, if there are multiple chose randomely among them
			max_value_index = [index for index, item in enumerate(q_values) if item == max(q_values)]
			if len(max_value_index) > 1:
				index = numpy.random.choice(max_value_index)
				self.piece_to_move = indices[index]
				self.q_value = q_values[index]
				self.reward = REWARDS[int(action_vector[index].value)] + STATE_REWARDS[state_vector[self.piece_to_move].value]
				self.action = action_vector[index]
				self.state = state_vector[indices[index]]
			else:
				self.piece_to_move = indices[max_value_index[0]]
				self.q_value = q_values[max_value_index[0]]
				self.reward = REWARDS[int(action_vector[max_value_index[0]].value)] + STATE_REWARDS[state_vector[self.piece_to_move].value]
				self.action = action_vector[max_value_index[0]]
				self.state = state_vector[indices[max_value_index[0]]]	

		return self.piece_to_move

	def do_learn(self, player_pieces, enemy_pieces):
		if self.learn == False:
			return

		# If action is nothing, then no update is nescerray
		if self.action == None:
			return

		new_state = self.get_state(player_pieces, enemy_pieces, self.piece_to_move)
		max_new_q_value = max(self.get_q_values(new_state, self.piece_to_move))

		updated_q_value = self.learning_rate * (self.reward + self.discount_factor*max_new_q_value - self.q_value)
		self.q_value_changes += updated_q_value
		updated_q_value = self.q_value + updated_q_value
		self.set_q_value(self.state, self.piece_to_move, self.action, updated_q_value)
		self.reward_list.append(self.reward)
			
	def get_state_and_actions(self, player_pieces, dice, enemy_pieces):
		state_vector = []
		action_vector = []
		q_values = []
		indicies = []
		for i in range(len(player_pieces)):
			other_pieces = []
			for j in range(len(player_pieces)):
				if j == i:
					continue
				other_pieces.append(player_pieces[j])

			state_vector.append(self.state_and_action.get_state(player_pieces[i],other_pieces, enemy_pieces))
			cur_actions = self.state_and_action.get_action(state_vector[i], player_pieces[i], dice, other_pieces, enemy_pieces)
			if len(cur_actions) > 1 or cur_actions[0] != Actions.NOTHING:
				indicies += [i]*len(cur_actions)
				action_vector += cur_actions
				q_values += self.get_available_q_values(state_vector[i], i, cur_actions)
		
		return state_vector, action_vector, q_values, indicies
	
	def get_state(self, player_pieces, enemy_pieces, index):
		other_pieces = []
		for j in range(len(player_pieces)):
			if j == index:
				continue
			other_pieces.append(player_pieces[j])
		
		state = self.state_and_action.get_state(player_pieces[index], other_pieces, enemy_pieces)
		return state

	def save_q_table(self):
		numpy.savetxt("q_table.txt", self.Q)

	def load_q_table(self):
		self.Q = numpy.loadtxt("q_table.txt")
		print(self.Q*10)

	def reset(self):
		self.q_index = -1
		self.reward = -1
		self.action = None
		self.reward_list = []
		self.piece_to_move = -1
		self.q_value_changes = 0

	def get_mean_rewards(self):
		if not len(self.reward_list):
			return 0.0
		return sum(self.reward_list) / len(self.reward_list)
	
	def decrease_exploration_rate(self):
		if self.exploration_rate_decay == 0.0:
			return
		self.epsilon = self.epsilon * self.exploration_rate_decay
		self.epsilon = max(self.epsilon, self.min_epsilon)
		print(self.epsilon)
	
	def get_available_q_values(self, state, index, actions):
		q_values = []
		q_index = state.value + len(States)*index
		for i in range(len(actions)):
			q_values.append(self.Q[q_index][actions[i].value])
		
		return q_values
	
	def get_q_values(self, state, index):
		return self.Q[state.value + len(States)*index]
	
	def set_q_value(self, state, index, action, value):
		self.Q[state.value + len(States)*index][action.value] = value
	
	def average_q_values(self):
		for i in range(len(Actions) - 1):
			for j in range(len(States)):
				temp = 0
				for k in range(4):
					temp += self.Q[j+len(States)*k][i]
				
				self.Q[j][i] = temp/4
				self.Q[j+len(States)][i] = temp/4
				self.Q[j+len(States)*2][i] = temp/4
				self.Q[j+len(States)*3][i] = temp/4
	
	def get_q_value_changes(self):
		return self.q_value_changes
	
	def stop_learning(self):
		self.learn = False
from ludopy.player import get_enemy_at_pos
from enum import Enum

from numpy import empty

# Implement the actions aswell, almost done but need to handle what to do if we are at home position, since the dice will not move it 6 pieces.
# Served a bit of inspiration https://github.com/NDurocher/YARAL/blob/main/src/Qlearn.py
# This also served as a bit of information https://www.researchgate.net/publication/261279306_TDl_and_Q-learning_based_Ludo_players
# If just one of the tokens has normal move, then move_piece_closets should be available.

REWARDS = [0.5, 0.8, -0.01, 0.45, -0.8, 0.35, 0.4, 0.4, 0.3, 0.01, 0.38, -0.01, 0.0]

class States(Enum):
	HOME = 0,
	GOAL = 1,
	GOAL_ZONE = 2,
	SAFE = 3,
	DANGER = 4

class Actions(Enum):
	MOVE_OUT = 0
	GOAL = 1
	MISS_GOAL = 2
	GOAL_ZONE = 3
	DIE = 4
	STAR = 5
	GLOBE = 6
	PROTECT = 7
	KILL = 8
	NORMAL_MOVE = 9
	MOVE_OUT_OF_DANGER = 10
	MOVE_DANGER = 11
	NOTHING = 12

class StateAndActions:
	def __init__(self):
		self.star_positions = [5, 12, 18, 25, 31, 38, 44, 51]
		self.globus_positions = [9, 22, 35, 48]
		self.enemy_globus = [14, 27, 40]
	
	def get_state(self, pos, other_pieces, enemy_pieces):
		state = None
		if self.home(pos):
			state = States.HOME
		elif self.goal(pos):
			state = States.GOAL
		elif self.goal_zone(pos):
			state = States.GOAL_ZONE
		elif self.safe(pos, other_pieces):
			state = States.SAFE
		elif self.in_danger(pos, enemy_pieces):
			state = States.DANGER
		# If we are not in danger then we are safe
		else:
			state = States.SAFE
		
		return state

	def get_action(self, state, pos, dice, other_pieces, enemy_pieces):
		"""Implemt this"""
		action = []
		# Home state, either we can move out or then we cannot do anything
		if state == States.HOME:
			if self.can_get_out_of_home(dice):
				action.append(Actions.MOVE_OUT)
			else:
				action.append(Actions.NOTHING)

		# No action available, when we are in the goal state
		elif state == States.GOAL:
			action.append(Actions.NOTHING)

		# We can either miss goal or reach goal
		elif state == States.GOAL_ZONE:
			if self.can_reach_goal(pos, dice, enemy_pieces):
				action.append(Actions.GOAL)
			else:
				action.append(Actions.MISS_GOAL)

		elif state == States.SAFE:
			# Goal can be reached from a star
			if self.can_reach_goal(pos, dice, enemy_pieces):
				action.append(Actions.GOAL)
			# No other actions are available if we reach goal zone
			if self.can_reach_goal_zone(pos, dice):
				action.append(Actions.GOAL_ZONE)
				return action
			# No other actions are available if we die
			if self.can_die(pos, dice, enemy_pieces):
				action.append(Actions.DIE)
				return action
			if self.can_reach_star(pos, dice):
				action.append(Actions.STAR)
			if self.can_get_on_globe(pos, dice):
				action.append(Actions.GLOBE)
			if self.can_protect(pos, dice, other_pieces):
				action.append(Actions.PROTECT)
			if self.can_kill(pos, dice, enemy_pieces):
				action.append(Actions.KILL)
			if self.danger_move(pos, dice, enemy_pieces):
				action.append(Actions.MOVE_DANGER)
			if not action:
				action.append(Actions.NORMAL_MOVE)
		
		elif state == States.DANGER:
			# Goal can be reached from a star
			if self.can_reach_goal(pos, dice, enemy_pieces):
				action.append(Actions.GOAL)
			# No other actions are available if we reach goal zone
			if self.can_reach_goal_zone(pos, dice):
				action.append(Actions.GOAL_ZONE)
				return action
			# No other actions are available if we die
			if self.can_die(pos, dice, enemy_pieces):
				action.append(Actions.DIE)
				return action
			if self.can_reach_star(pos, dice):
				action.append(Actions.STAR)
			if self.can_get_on_globe(pos, dice):
				action.append(Actions.GLOBE)
			if self.can_protect(pos, dice, other_pieces):
				action.append(Actions.PROTECT)
			if self.can_kill(pos, dice, enemy_pieces):
				action.append(Actions.KILL)
			if self.can_move_out_of_danger(pos, dice, enemy_pieces):
				action.append(Actions.MOVE_OUT_OF_DANGER)
			if not action:
				action.append(Actions.MOVE_DANGER)				

		return action
	
	def get_reward(self, action):
		reward = REWARDS[action.value]
		return reward	


	def home(self, pos):
		"""Will return if the piece is home."""
		if pos == 0:
			return True

		return False

	def goal(self, pos):
		"""Will return the number if the piece is in the goal."""
		if pos == 59:
			return True

		return False

	def goal_zone(self, pos):
		"""Will return the number of pieces in the goal zone"""
		if self.__on_goal_stripe(pos):
			return True

		return False

	def safe(self, pos, other_piece):
		"""Will return if the position is safe."""
		if self.__on_a_globus(pos) or pos == 1:
			return True
		
		for i in range(len(other_piece)):
			if self.__same_position(pos, other_piece[i]) and not self.__on_enemy_globus(pos):
				return True

		return False

	def in_danger(self, pos, enemy_pieces):
		"""Will return the danger count."""
		return self.__token_is_in_danger(pos, enemy_pieces)

	def unsafe(self):
		"""Dummy function if the token is not in any other state, then it must be unsafe."""
		return True

	def can_get_out_of_home(self, dice_roll):
		if dice_roll == 6:
			return True

		return False

	def can_reach_goal(self, pos, dice_roll, enemy_pieces):
		if (pos + dice_roll == 59):
			return True
		
		# if we hit the last star, we will also reach the goal
		if (pos+ dice_roll == self.star_positions[-1]):
			_, enemies_at_pos = get_enemy_at_pos(self.star_positions[-1], enemy_pieces)
			if len(enemies_at_pos) >= 2:
				return False
			return True

		return False

	def can_reach_goal_zone(self, pos, dice_roll):
		if self.__on_goal_stripe(pos + dice_roll):
			return True
		
		return False
	
	def can_reach_star(self, pos, dice_roll):
		if self.__on_a_star(pos + dice_roll):
			return True

		return False

	def can_move_pieces(self,pieces, dice_roll):
		moveable_pieces = [True, True, True, True]
		for i in range(len(pieces)):
			if (pieces[i] == 0 and dice_roll != 6 or pieces[i] == 59):
				moveable_pieces[i] = False
		
		return moveable_pieces

	def can_get_on_globe(self, pos, dice_roll):
		if self.__on_a_globus(pos + dice_roll):
			return True

		return False

	def can_protect(self, pos, dice_roll, other_pieces):
		star_idx = None
		if self.__on_a_star(pos+dice_roll):
	
			# Cannot protect if we hit the last star position
			if self.star_positions[-1] == pos + dice_roll:
				return False
			for j in range(len(self.star_positions)):
				if self.star_positions[j] == pos + dice_roll:
					star_idx = j
					break

		for i in range(len(other_pieces)):
			if star_idx is not None:
				# Test if a piece is located at the next star position
				if self.__same_position(self.star_positions[star_idx+1], other_pieces[i]):
					return True
			else:
				if self.__same_position(pos+dice_roll, other_pieces[i]) and not self.__on_enemy_globus(other_pieces[i]):
					return True

		return False

	def can_die(self, pose, dice_roll, enemy_pieces):
		# Check if there is 2 enemies at the end of the star jump or at the first star
		if self.__on_a_star(pose + dice_roll):
			star_idx = None
			for j in range(len(self.star_positions)):
				if self.star_positions[j] == pose + dice_roll:
					star_idx = j
					break
			
			# Check for enemies at the first star
			_, enemies_at_pos = get_enemy_at_pos(self.star_positions[star_idx], enemy_pieces)
			if len(enemies_at_pos) >= 2:
				return True

			# Last star, there will be no new star
			if star_idx == len(self.star_positions) - 1:
				return False
			
			# Check for enemies at the next star
			_, enemies_at_pos = get_enemy_at_pos(self.star_positions[star_idx+1], enemy_pieces)
			if len(enemies_at_pos) >= 2:
				return True

		# Reaching globus position, check if an enemy is already there 
		elif (pose + dice_roll) in self.globus_positions:
			for j in range(len(self.globus_positions)):
				if self.globus_positions[j] == pose + dice_roll:
					enemy_at_pos, _ = get_enemy_at_pos(self.globus_positions[j], enemy_pieces)
					if enemy_at_pos != -1:
						return True
					
		
		# Check if there enemies at the enemy globe
		elif self.__on_enemy_globus(pose + dice_roll):
			for j in range(len(self.enemy_globus)):
				if self.enemy_globus[j] == pose + dice_roll:
					enemy_at_pos, enemies_at_pos = get_enemy_at_pos(self.enemy_globus[j], enemy_pieces)
					if enemy_at_pos == j:
						return True
					elif len(enemies_at_pos) >= 2:
						return True
					break

		# Check if there is two enemies at the new position
		else:
			_, enemies_at_pos = get_enemy_at_pos(pose + dice_roll, enemy_pieces)
			if len(enemies_at_pos) >= 2:
				return True
		
		return False
	
	def can_kill(self, pos, dice_roll, enemy_pieces):
		# No need to check for the number of enemies at the position, since we have already checked if the token can die
		# Star kill
		if self.__on_a_star(pos + dice_roll):
			star_idx = None
			# Only hit one star at the last position
			if self.star_positions[-1] == pos + dice_roll:
				enemy_at_pos, _ = get_enemy_at_pos(self.star_positions[-1], enemy_pieces)
				if enemy_at_pos != -1:
					return True
			else:
				for j in range(len(self.star_positions)):
					if self.star_positions[j] == pos + dice_roll:
						star_idx = j
						break

				enemy_at_pos, _ = get_enemy_at_pos(self.star_positions[star_idx+1], enemy_pieces)
				if enemy_at_pos != -1:
					return True
				enemy_at_pos, _ = get_enemy_at_pos(self.star_positions[star_idx], enemy_pieces)
				if enemy_at_pos != -1:
					return True	
		# Normal kill
		else:
			enemy_at_pos, _ = get_enemy_at_pos(pos+ dice_roll, enemy_pieces)
			if enemy_at_pos != -1:
				return True
		
		return False

	def can_move_out_of_danger(self, pose, dice_roll, enemy_pieces):
		if self.__token_is_in_danger(pose + dice_roll, enemy_pieces) == False:
			return True

		return False

	def danger_move(self, pose, dice_roll, enemy_pieces):
		if self.__on_a_star(pose+dice_roll):
			star_idx = None
			for i in range(len(self.star_positions)):
				if self.star_positions[i] == pose+dice_roll:
					star_idx = i
					break
			# Last star we will hit goal
			if star_idx == len(self.star_positions) - 1:
				return False

			if self.__token_is_in_danger(self.star_positions[star_idx+1], enemy_pieces) == True:
				return True
		else:
			if self.__token_is_in_danger(pose + dice_roll, enemy_pieces) == True:
				return True

		return False

	def __same_position(self, position1, position2):
		return position1 == position2

	def __on_a_globus(self, position):
		if position in self.globus_positions:
			return True
		
		return False
		
	def __on_enemy_globus(self, position):
		
		if (position in self.enemy_globus):
			return True

		return False

	def __on_a_star(self, position):
		if (position in self.star_positions):
			return True

		return False

	def __on_goal_stripe(self, position):
		goal_positions = (53,54,55,56,57,58)
		if (position in goal_positions):
			return True

		return False

	def __token_is_in_danger(self, position, enemy_pieces):
		
		if self.__on_a_star(position):
			star_idx = None
			for i in range(len(self.star_positions)):
				if self.star_positions[i] == position:
					star_idx = i
					break
			if star_idx == 0:
				for i in (1,2,3,4,5,6):
					enemy_at_pos, _ = get_enemy_at_pos(self.star_positions[-1]-i, enemy_pieces)
					if enemy_at_pos != -1:
						return True		
					enemy_at_pos, _ = get_enemy_at_pos(self.star_positions[star_idx]-i, enemy_pieces)
					if enemy_at_pos != -1:
						return True									
			else:
				for i in (1,2,3,4,5,6):
					enemy_at_pos, _ = get_enemy_at_pos(self.star_positions[star_idx-1]-i, enemy_pieces)
					if enemy_at_pos != -1:
						return True
					enemy_at_pos, _ = get_enemy_at_pos(self.star_positions[star_idx]-i, enemy_pieces)
					if enemy_at_pos != -1:
						return True					

		elif self.__on_enemy_globus(position):
			return True
		
		elif self.__on_a_globus(position):
			return False

		else:
			if position >= 7:
				for i in (1,2,3,4,5,6):
					enemy_at_pos, _ = get_enemy_at_pos(position-i, enemy_pieces)
					if enemy_at_pos != -1:
						return True
			else:
				for i in (1,2,3,4,5,6):
					enemy_at_pos = -1
					if position - i < 1:
						enemy_at_pos, _ = get_enemy_at_pos(52 + position - i, enemy_pieces)
					else:
						enemy_at_pos, _ = get_enemy_at_pos(position-i, enemy_pieces)
					if enemy_at_pos != -1:
						return True

		return False

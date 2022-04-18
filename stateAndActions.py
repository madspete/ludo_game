from tkinter.messagebox import NO
from anyio import move_on_after
from ludopy.player import get_enemy_at_pos

# Implement the actions aswell, almost done but need to handle what to do if we are at home position, since the dice will not move it 6 pieces.
class StateAndActions:
	def __init__(self):
		self.star_positions = [5, 12, 18, 25, 31, 38, 44, 51]
		self.globus_positions = [9, 22, 35, 48]
		self.enemy_globus = [14, 27, 40]

	def in_danger(self, pieces, enemy_pieces):
		"""Will return the danger count."""
		# All pieces are safe
		safe_count = 0
		safe_pieces = self.safe(pieces)
		goal_zone_pieces = self.goal_zone(pieces)
		goal_pieces = self.goal(pieces)
		home_pieces = self.home(pieces)
		danger_pieces = [False, False, False, False]
		
		for i in range(len(safe_pieces)):
			if safe_pieces[i] == True or goal_pieces[i] == True or goal_zone_pieces[i] == True or home_pieces[i] == True:
				safe_count = safe_count + 1

		if safe_count == 4:
			return danger_pieces

		for i in range(len(pieces)):
			if self.__on_enemy_globus(pieces[i]):
				danger_pieces[i] = True
		
		for i in range(len(pieces)):
			if safe_pieces[i] == True or goal_pieces[i] == True or goal_zone_pieces[i] == True or home_pieces[i] == True:
				continue
			danger_pieces[i] = self.__token_is_in_danger(pieces[i], enemy_pieces)
		
		return danger_pieces

	def safe(self, pieces):
		"""Will return if the position is safe."""
		goal_pieces = self.goal(pieces)
		goal_zone_pieces = self.goal_zone(pieces)
		home_pieces = self.home(pieces)
		safe_pieces = [False, False, False, False]
		for i in range(len(pieces)):
			if self.__on_a_globus(pieces[i]):
				safe_pieces[i] = True
		
		for i in range(len(pieces)-1):
			j = i + 1
			if goal_zone_pieces[i] == True or goal_pieces[i] == True or home_pieces[i] == True:
				continue
			while j < len(pieces):
				if self.__same_position(pieces[i], pieces[j]) and not self.__on_enemy_globus(pieces[j]):
					safe_pieces[i] = True
					safe_pieces[j] = True
				j = j + 1

		return safe_pieces

	def unsafe(self, pieces, enemy_pieces):
		"""Will return the number of unsafe pieces."""
		safe_pieces = self.safe(pieces)
		goal_pieces = self.goal(pieces)
		goal_zone_pieces = self.goal_zone(pieces)
		danger_pieces = self.in_danger(pieces, enemy_pieces)
		home_pieces = self.home(pieces)
		unsafe_pieces = [False, False, False, False]
		for i in range(len(pieces)):
			if safe_pieces[i] == True or goal_pieces[i] == True or goal_zone_pieces[i] == True or danger_pieces[i] == True or home_pieces[i] == True:
				continue
			unsafe_pieces[i] = True

		return unsafe_pieces	
	
	def goal(self, pieces):
		"""Will return the number of pieces in the goal."""
		goal_pieces = [False, False, False, False]
		for i in range(len(pieces)):
			if pieces[i] == 59:
				goal_pieces[i] = True

		return goal_pieces 

	def home(self, pieces):
		"""Will return the number of pieces at home."""
		home_pieces = [False, False, False, False]
		for i in range(len(pieces)):
			if pieces[i] == 0:
				home_pieces[i] = True

		return home_pieces

	def goal_zone(self, pieces):
		"""Will return the number of pieces in the goal zone"""
		goal_zone_pieces = [False, False, False, False]
		for i in range(len(pieces)):
			if self.__on_goal_stripe(pieces[i]):
				goal_zone_pieces[i] = True

		return goal_zone_pieces

	def can_get_out_of_home(self, pieces, dice_roll):
		can_get_out_of_home_pieces = [False, False, False, False]
		home_pieces = self.home(pieces)
		if dice_roll == 6:
			can_get_out_of_home_pieces = home_pieces

		return can_get_out_of_home_pieces

	def can_reach_goal(self, pieces, dice_roll):
		can_reach_goal_pieces = [False, False, False, False]
		for i in range(len(pieces)):
			if (pieces[i] + dice_roll == 59):
				can_reach_goal_pieces[i] = True
		
			# if we hit the last star, we will also reach the goal
			if (pieces[i]+ dice_roll == self.star_positions[-1]):
				can_reach_goal_pieces[i] = True

		return can_reach_goal_pieces

	def can_reach_goal_zone(self, pieces, dice_roll):
		can_reach_goal_zone = [False, False, False, False]
		for i in range(len(pieces)):
			if self.__on_goal_stripe(pieces[i] + dice_roll):
				can_reach_goal_zone = True
		
		return can_reach_goal_zone
	
	def can_reach_star(self, pieces, dice_roll, can_die_pieces):
		can_reach_star = [False, False, False, False]
		for i in range(len(pieces)):
			if self.__on_a_star(pieces[i] + dice_roll) and can_die_pieces[i] == False:
				can_reach_star[i] = True

		return can_reach_star

	def can_move_pieces(self,pieces, dice_roll):
		moveable_pieces = [True, True, True, True]
		for i in range(len(pieces)):
			if (pieces[i] == 0 and dice_roll != 6 or pieces[i] == 59):
				moveable_pieces[i] = False
		
		return moveable_pieces

	def can_get_on_globe(self, pieces, dice_roll, can_die_pieces):
		globe_pieces = [False, False, False, False]
		for i in range(len(pieces)):
			if self.__on_a_globus(pieces[i] + dice_roll) and can_die_pieces[i] == False:
				globe_pieces[i] = True

		return globe_pieces

	def can_protect(self, pieces, dice_roll):
		goal_pieces = self.goal(pieces)
		goal_zone_pieces = self.goal_zone(pieces)
		home_pieces = self.home(pieces)
		protect_pieces = [False, False, False, False]
		for i in range(len(pieces)):
			for j in range(len(pieces)):
				if goal_zone_pieces[i] == True or goal_pieces[i] == True or home_pieces[i] == True:
					continue
				if self.__same_position(pieces[i]+dice_roll, pieces[j]) and not self.__on_enemy_globus(pieces[j]):
					protect_pieces[i] = True

		return protect_pieces

	def can_die(self, pieces, dice_roll, enemy_pieces):
		can_die_pieces = [False, False, False, False]
		for i in range(len(pieces)):
			# Check if there is 2 enemies at the end of the star jump
			if self.__on_a_star(pieces[i] + dice_roll):
				star_idx = None
				# Cannot die if we hit the last star position
				if self.star_positions[-1] == pieces[i] + dice_roll:
					continue
				for j in range(len(self.star_positions)):
					if self.star_positions[j] == pieces[i] + dice_roll:
						star_idx = j
						break
				
				_, enemies_at_pos = get_enemy_at_pos(self.star_positions[star_idx+1], enemy_pieces)
				if len(enemies_at_pos) >= 2:
					can_die_pieces[i] = True

			# Reaching globus position, check if an enemy is already there 
			elif (pieces[i] + dice_roll) in self.globus_positions:
				for j in range(len(self.globus_positions)):
					if self.globus_positions[j] == pieces[i] + dice_roll:
						enemy_at_pos, _ = get_enemy_at_pos(self.globus_positions[j], enemy_pieces)
						if enemy_at_pos != -1:
							can_die_pieces[i] = True
						break
			
			# Check if there enemies at the enemy globe
			elif self.__on_enemy_globus(pieces[i] + dice_roll):
				for j in range(len(self.enemy_globus)):
					if self.enemy_globus[j] == pieces[i] + dice_roll:
						enemy_at_pos, enemies_at_pos = get_enemy_at_pos(self.enemy_globus[j], enemy_pieces)
						if enemy_at_pos == j:
							can_die_pieces[i] = True
						elif len(enemies_at_pos) >= 2:
							can_die_pieces[i] = True
						break

			# Check if there is two enemies at the new position
			else:
				_, enemies_at_pos = get_enemy_at_pos(pieces[i] + dice_roll, enemy_pieces)
				if len(enemies_at_pos) >= 2:
					can_die_pieces[i] = True
		
		return can_die_pieces
	
	def can_kill(self, pieces, dice_roll, enemy_pieces, can_die_pieces):
		can_kill_pieces = [False, False, False, False]
		for i in range(len(pieces)):
			if can_die_pieces[i] == True:
				continue
			# Star kill
			if self.__on_a_star(pieces[i] + dice_roll):
				star_idx = None
				# Cannot kill if we hit the last star position
				if self.star_positions[-1] == pieces[i] + dice_roll:
					continue
				for j in range(len(self.star_positions)):
					if self.star_positions[j] == pieces[i] + dice_roll:
						star_idx = j
						break
				
				enemy_at_pos, _ = get_enemy_at_pos(self.star_positions[star_idx+1], enemy_pieces)
				if enemy_at_pos != -1:
					can_kill_pieces[i] = True		
			# Normal kill
			else:
				enemy_at_pos, _ = get_enemy_at_pos(pieces[i] + dice_roll, enemy_pieces)
				if enemy_at_pos != -1:
					can_kill_pieces[i] = True
		
		return can_kill_pieces
	
	def move_closets_piece(self, pieces, dice_roll, can_die_pieces):
		"""Move the piece closets to goal, that cannot get killed."""
		closets_piece = [False, False, False, False]
		movable_pieces = self.can_move_pieces(pieces, dice_roll)
		closets_piece_idx = None
		max_pos = -1
		for i in range(len(pieces)):
			if movable_pieces[i] == True and can_die_pieces[i] == False and max_pos < pieces[i]:
				max_pos = pieces[i]
				closets_piece_idx = i

		if closets_piece_idx is not None:
			closets_piece[closets_piece_idx] = True

		return closets_piece
	
	def move_out_of_danger(self, pieces, dice_roll, danger_pieces):
		move_out_of_danger_pieces = [False, False, False, False]
		for i in range(len(pieces)):
			if danger_pieces[i] == True and self.__token_is_in_danger(pieces[i] + dice_roll) == False:
				move_out_of_danger_pieces[i] = True

		return move_out_of_danger_pieces
	
	def miss_goal(self, pieces, dice_roll, goal_zone_pieces):
		miss_goal_pieces = [False, False, False, False]
		for i in range(len(pieces)):
			if goal_zone_pieces[i] == True and (pieces[i] + dice_roll) != 59:
				miss_goal_pieces[i] = True

		return miss_goal_pieces		

	def __same_position(self, position1, position2):
		return position1 == position2

	def __on_a_globus(self, position):
		print(position)
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
			
			for i in (1,2,3,4,5,6):
				enemy_at_pos, _ = get_enemy_at_pos(self.star_positions[star_idx-1]-i, enemy_pieces)
				if enemy_at_pos != -1:
					return True
		else:		
			for i in (1,2,3,4,5,6):
				enemy_at_pos, _ = get_enemy_at_pos(position-i, enemy_pieces)
				if enemy_at_pos != -1:
					return True
			
		return False



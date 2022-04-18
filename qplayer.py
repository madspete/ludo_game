import numpy

STATES = ["goal", "home", "safe", "unsafe", "danger", "goal zone"]
ACTIONS = ["move_out", "goal_zone", "star", "globe", "protect", "kill", "goal", "move closets piece", "die", "miss goal", "move out of danger", "nothing"]
REWARDS = [0.7, 0.8, 0.6, 0.5, 0.5, 0.4, 0.9, 0.1, -0.25, -0.1, 0.2]

class Qplayer:
	def __init__(self, learn=True):
		self.learn = learn
		
		

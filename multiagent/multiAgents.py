# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent
CONST_MAX = 99999999999999999999999999999999999

class ReflexAgent(Agent):
	"""
	  A reflex agent chooses an action at each choice point by examining
	  its alternatives via a state evaluation function.

	  The code below is provided as a guide.  You are welcome to change
	  it in any way you see fit, so long as you don't touch our method
	  headers.
	"""


	def getAction(self, gameState):
		"""
		You do not need to change this method, but you're welcome to.

		getAction chooses among the best options according to the evaluation function.

		Just like in the previous project, getAction takes a GameState and returns
		some Directions.X for some X in the set {North, South, West, East, Stop}
		"""
		# Collect legal moves and successor states
		legalMoves = gameState.getLegalActions()

		# Choose one of the best actions
		scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
		bestScore = max(scores)
		bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
		chosenIndex = random.choice(bestIndices) # Pick randomly among the best

		"Add more of your code here if you want to"

		return legalMoves[chosenIndex]

	def evaluationFunction(self, currentGameState, action):
		"""
		Design a better evaluation function here.

		The evaluation function takes in the current and proposed successor
		GameStates (pacman.py) and returns a number, where higher numbers are better.

		The code below extracts some useful information from the state, like the
		remaining food (newFood) and Pacman position after moving (newPos).
		newScaredTimes holds the number of moves that each ghost will remain
		scared because of Pacman having eaten a power pellet.

		Print out these variables to see what you're getting, then combine them
		to create a masterful evaluation function.
		"""
		# Useful information you can extract from a GameState (pacman.py)
		successor_game_state = currentGameState.generatePacmanSuccessor(action)
		next_pacman_pos = successor_game_state.getPacmanPosition()
		next_food_list = successor_game_state.getFood().asList()
		next_ghost_states = successor_game_state.getGhostStates()
		next_scared_times = [ghostState.scaredTimer for ghostState in next_ghost_states]

		"*** YOUR CODE HERE ***"
		res = successor_game_state.getScore()
		min_ghost_dist = min([manhattanDistance(ghost_state.getPosition(), next_pacman_pos) for ghost_state in next_ghost_states])
		max_ghost_dist = max([manhattanDistance(ghost_state.getPosition(), next_pacman_pos) for ghost_state in next_ghost_states])
		if min(next_scared_times) > 2:
			if min_ghost_dist <= 1:
				return CONST_MAX
			if len(next_food_list) == 0:
				return res
			bonus = max([manhattanDistance(food, next_pacman_pos) / max_ghost_dist for food in next_food_list])
			res = res + bonus
		else:
			if min_ghost_dist <= 1:
				return -CONST_MAX
			if len(next_food_list) == 0:
				return res
			bonus = max([min_ghost_dist / manhattanDistance(food, next_pacman_pos) for food in next_food_list])
			res = res + bonus
		return res
		# return successorGameState.getScore()

def scoreEvaluationFunction(currentGameState):
	"""
	  This default evaluation function just returns the score of the state.
	  The score is the same one displayed in the Pacman GUI.

	  This evaluation function is meant for use with adversarial search agents
	  (not reflex agents).
	"""
	return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
	"""
	  This class provides some common elements to all of your
	  multi-agent searchers.  Any methods defined here will be available
	  to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

	  You *do not* need to make any changes here, but you can if you want to
	  add functionality to all your adversarial search agents.  Please do not
	  remove anything, however.

	  Note: this is an abstract class: one that should not be instantiated.  It's
	  only partially specified, and designed to be extended.  Agent (game.py)
	  is another abstract class.
	"""

	def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
		self.index = 0 # Pacman is always agent index 0
		self.evaluationFunction = util.lookup(evalFn, globals())
		self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
	"""
	  Your minimax agent (question 2)
	"""

	def getAction(self, gameState):
		"""
		  Returns the minimax action from the current gameState using self.depth
		  and self.evaluationFunction.

		  Here are some method calls that might be useful when implementing minimax.

		  gameState.getLegalActions(agentIndex):
			Returns a list of legal actions for an agent
			agentIndex=0 means Pacman, ghosts are >= 1

		  gameState.generateSuccessor(agentIndex, action):
			Returns the successor game state after an agent takes an action

		  gameState.getNumAgents():
			Returns the total number of agents in the game
		"""
		"*** YOUR CODE HERE ***"
		return self.minimax_value(gameState, 1, 0)
		util.raiseNotDefined()

	def minimax_value(self, game_state, cur_depth, cur_agent):
		if cur_depth > self.depth or game_state.isWin() or game_state.isLose():
			return self.evaluationFunction(game_state)

		legal_moves = [action for action in game_state.getLegalActions(cur_agent) if action != 'Stop']
		next_agent = (cur_agent + 1) % game_state.getNumAgents()
		next_depth = cur_depth + ((next_agent == 0) & 1)
		successor_game_state = [game_state.generateSuccessor(cur_agent, action) for action in legal_moves]
		next_scores = [self.minimax_value(next_game_state, next_depth, next_agent) for next_game_state in successor_game_state]

		if cur_agent == 0:
			best_score = max(next_scores)
			if (cur_depth == 1):
				bestIndices = [index for index in range(len(next_scores)) if next_scores[index] == best_score]
				chosen_index = random.choice(bestIndices)
				return legal_moves[chosen_index]
			return best_score
		else:
			best_score = min(next_scores)
			return best_score
			
class AlphaBetaAgent(MultiAgentSearchAgent):
	"""
	  Your minimax agent with alpha-beta pruning (question 3)
	"""

	def getAction(self, gameState):
		"""
		  Returns the minimax action using self.depth and self.evaluationFunction
		"""
		"*** YOUR CODE HERE ***"
		return self.minimax_value(gameState, 1, 0, -CONST_MAX, CONST_MAX)
		util.raiseNotDefined()
	
	def minimax_value(self, game_state, cur_depth, cur_agent, alpha, beta):
		if cur_depth > self.depth or game_state.isWin() or game_state.isLose():
			return self.evaluationFunction(game_state)

		legal_moves = [action for action in game_state.getLegalActions(cur_agent) if action != 'Stop']
		next_agent = (cur_agent + 1) % game_state.getNumAgents()
		next_depth = cur_depth + ((next_agent == 0) & 1)

		if cur_agent == 0:
			best_score = -CONST_MAX
			best_action = None
			
			for action in legal_moves:
				next_game_state = game_state.generateSuccessor(cur_agent, action)
				next_score = self.minimax_value(next_game_state, next_depth, next_agent, alpha, beta)
				if best_score < next_score:
					best_score = next_score
					best_action = action
				if best_score > beta:
					return best_score if cur_depth != 1 else action
				alpha = max(alpha, best_score)
			return best_score if cur_depth != 1 else best_action
		else:
			best_score = CONST_MAX
			for action in legal_moves:
				next_game_state = game_state.generateSuccessor(cur_agent, action)
				best_score = min(best_score, self.minimax_value(next_game_state, next_depth, next_agent, alpha, beta))
				if best_score < alpha:
					return best_score
				beta = min(beta, best_score)
			return best_score

class ExpectimaxAgent(MultiAgentSearchAgent):
	"""
	  Your expectimax agent (question 4)
	"""

	def getAction(self, gameState):
		"""
		  Returns the expectimax action using self.depth and self.evaluationFunction

		  All ghosts should be modeled as choosing uniformly at random from their
		  legal moves.
		"""
		"*** YOUR CODE HERE ***"
		return self.expectimax_value(gameState, 1, 0)
		util.raiseNotDefined()

	def expectimax_value(self, game_state, cur_depth, cur_agent):
		if cur_depth > self.depth or game_state.isWin() or game_state.isLose():
			return self.evaluationFunction(game_state)

		legal_moves = [action for action in game_state.getLegalActions(cur_agent) if action != 'Stop']
		next_agent = (cur_agent + 1) % game_state.getNumAgents()
		next_depth = cur_depth + ((next_agent == 0) & 1)
		successor_game_state = [game_state.generateSuccessor(cur_agent, action) for action in legal_moves]
		next_scores = [self.expectimax_value(next_game_state, next_depth, next_agent) for next_game_state in successor_game_state]

		if cur_agent == 0:
			best_score = max(next_scores)
			if (cur_depth == 1):
				bestIndices = [index for index in range(len(next_scores)) if next_scores[index] == best_score]
				chosen_index = random.choice(bestIndices)
				return legal_moves[chosen_index]
			return best_score
		else:
			return sum(next_scores) / len(next_scores)

def betterEvaluationFunction(currentGameState):
	"""
	  Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
	  evaluation function (question 5).

	  DESCRIPTION: <write something here so we know what you did>
	"""
	"*** YOUR CODE HERE ***"
	res = currentGameState.getScore()
	cur_food_list = currentGameState.getFood().asList()
	cur_pacman_pos = currentGameState.getPacmanPosition()
	cur_ghost_states = currentGameState.getGhostStates()
	cur_scared_times = [ghostState.scaredTimer for ghostState in cur_ghost_states]
	cur_capsules_pos = currentGameState.getCapsules()

	min_ghost_dist = min([manhattanDistance(ghost_state.getPosition(), cur_pacman_pos) for ghost_state in cur_ghost_states])
	max_ghost_dist = max([manhattanDistance(ghost_state.getPosition(), cur_pacman_pos) for ghost_state in cur_ghost_states])
	if min(cur_scared_times) > 2:
		if min_ghost_dist <= 1:
			return CONST_MAX
		if len(cur_food_list) == 0:
			return res
		bonus = max([manhattanDistance(food, cur_pacman_pos) / max_ghost_dist for food in cur_food_list])
		res = res + bonus
	else:
		if min_ghost_dist <= 1:
			return -CONST_MAX
		if len(cur_food_list) == 0:
			return res
		bonus = max([min_ghost_dist / manhattanDistance(food, cur_pacman_pos) for food in cur_food_list])
		# if len(cur_capsules_pos) > 0:
		# 	bonus = max(bonus, max([min_ghost_dist / manhattanDistance(capsule, cur_pacman_pos) for capsule in cur_capsules_pos]))
		res = res + bonus
	return res
	util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction


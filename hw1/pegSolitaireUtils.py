import readGame
import config

#######################################################
# These are some Helper functions which you have to use 
# and edit.
# Must try to find out usage of them, they can reduce
# your work by great deal.
#
# Functions to change:
# 1. is_wall(self, pos):
# 2. is_validMove(self, oldPos, direction):
# 3. getNextPosition(self, oldPos, direction):
# 4. getNextState(self, oldPos, direction):
#######################################################
class game:
	def __init__(self, filePath):
        	self.gameState = readGame.readGameState(filePath)
                self.nodesExpanded = 0
		self.trace = []	

	def is_corner(self, pos):
		########################################
		# You have to make changes from here
		# check for if the new positon is a corner or not
		# return true if the position is a corner
                if self.gameState[pos[0]][pos[1]] == -1:
                    return True
                return False
	
	def getNextPosition(self, oldPos, direction):
		#########################################
		# YOU HAVE TO MAKE CHANGES HERE
		# See DIRECTION dictionary in config.py and add
		# this to oldPos to get new position of the peg if moved
		# in given direction , you can remove next line
                """
                    The new position is two moves in the specified direction,
                    since the peg jumps over another peg on the baord. Note
                    that the new position returned may not be a valid one.
                """
                return (oldPos[0] + 2 * config.DIRECTION[direction][0],
                        oldPos[1] + 2 * config.DIRECTION[direction][1])
	
	def is_validMove(self, oldPos, direction):
		#########################################
		# DONT change Things in here
		# In this we have got the next peg position and
		# below lines check for if the new move is a corner
		newPos = self.getNextPosition(oldPos, direction)
		if self.is_corner(newPos):
			return False	
		#########################################
		
		########################################
		# YOU HAVE TO MAKE CHANGES BELOW THIS
		# check for cases like:
		# if new move is already occupied
		# or new move is outside peg Board
		# Remove next line according to your convenience

                """ Invalid if there is no peg at the old position """
                if self.gameState[oldPos[0]][oldPos[1]] != 1:
                    return False

                """ Invalid if there is already a peg in the new position """
                if self.gameState[newPos[0]][newPos[1]] == 1:
                    return False

                """ Invalid if there is no peg to jump over """
                midPos = (oldPos[0] + config.DIRECTION[direction][0],
                          oldPos[1] + config.DIRECTION[direction][1])
                if self.gameState[midPos[0]][midPos[1]] != 1:
                    return False

                nrows = len(self.gameState)
                ncols = len(self.gameState[0])

                """ Invalid if the old position is off the board """
                if oldPos[0] >= nrows or oldPos[1] >= ncols \
                   or oldPos[0] < 0 or oldPos[1] < 0:
                    return False

                """ Invalid if the new position is off the board """
                if newPos[0] >= nrows or newPos[1] >= ncols \
                   or newPos[0] < 0 or newPos[1] < 0:
                    return False

		return True
	
        """ NOTE: Modifies self.gameState, self.nodesExpanded """
	def getNextState(self, oldPos, direction):
		###############################################
		# DONT Change Things in here
		self.nodesExpanded += 1
		if not self.is_validMove(oldPos, direction):
			print "Error, You are not checking for valid move"
			exit(0)
		###############################################
		
		###############################################
		# YOU HAVE TO MAKE CHANGES BELOW THIS
		# Update the gameState after moving peg
		# eg: remove crossed over pegs by replacing it's
		# position in gameState by 0
		# and updating new peg position as 1

                newPos = self.getNextPosition(oldPos, direction)
                midPos = (oldPos[0] + config.DIRECTION[direction][0],
                          oldPos[1] + config.DIRECTION[direction][1])

                self.gameState[oldPos[0]][oldPos[1]] = 0 # move old peg
                self.gameState[newPos[0]][newPos[1]] = 1 # to new pos, and
                self.gameState[midPos[0]][midPos[1]] = 0 # delete mid pig

		return self.gameState

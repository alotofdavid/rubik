import re
SOLUTION_REGEX = re.compile("^[RLUDFBMES' 2xyz]*$")
MOVE_REGEX = re.compile("^[RLUDFMBESxyz]['2]?$")

class Algorithm(object):
	def __init__(self,move_string):
		self.moves = []
		for move in move_string:
			self.moves.append(Move(move))

	def __repr__(self):
		return " ".join([str(m) for m in self.moves])

class Move(object):
	def __init__(self,move):
		if (len(move)==1):
			self.face = move
			self.num = 1
		if (len(move)==2):
			self.face = move[:1]
			rest = move[1:]
			if rest == "'":
				self.num = 3
			if rest =="2":
				self.num = 2

	def __repr__(self):
		return self.face + str(self.num)



class Cube(object):
	def __init__(self): 
		self.cube = [[[i for _ in xrange(3)] for _ in xrange(3)] for i in xrange(6)]

	def __repr__(self):
		return str(self.cube)

	def twist(self, move):
		return None


def parse_alg(alg):
	moves = alg.split()
	if valid_moves(moves):
		return Algorithm(moves)
	else:
		return False

def valid_moves(moves):
	for move in moves:
		if not MOVE_REGEX.match(move):
			print("{move} does not match regex".format(move=move))
			return False
	return True
import re
SOLUTION_REGEX = re.compile("^[RLUDFBMES' 2xyz]*$")
MOVE_REGEX = re.compile("^[RLUDFMBESxyz]['2]?$")

move_dict = {"U":0,"L":1,"F":2,"R":3,"B":4,"D":5}

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

	def do_move(self, move):
		self.twist(move_dict[move.face], move.num)

	def twist(self, face, amount):
		for _ in range(amount):
			self.rotate(face)

	def rotate(self, face):
		#U
		if face==0:
			#top row of l,f,r,b cycle
			t = self.cube[1][0]
			self.cube[1][0] = self.cube[2][0]
			self.cube[2][0] = self.cube[3][0]
			self.cube[3][0] = self.cube[4][0]
			self.cube[4][0] = t
			#rotate U face

		#L
		elif face==1:
			return
		#F
		elif face==2:				
			return
		#R
		elif face==3:
			return
		#B
		elif face==4:
			return
		#D
		elif face==5:
			return

	def cycle_stickers(self, *args):
		t = self.cube[args[len(args)-1][0]][args[len(args)-1][1]][args[len(args)-1][2]]
		loop = range(len(args))
		loop.reverse()
		for i in loop:
			if i > 0:
				self.cube[args[i][0]][args[i][1]][args[i][2]] = self.cube[args[i-1][0]][args[i-1][1]][args[i-1][2]]
		self.cube[args[0][0]][args[0][1]][args[0][2]] = t

	def cycle_rows(self, *args):
		t = self.cube[args[len(args)-1][0]][args[len(args)-1][1]]		
		loop = range(len(args))
		loop.reverse()
		for i in range(len(args)):
			if i > 0:
				self.cube[args[i][0]][args[i][1]] = self.cube[args[i-1][0]][args[i-1][1]]
		self.cube[args[0][0]][args[0][1]] = t

def parse_alg_string(alg):
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
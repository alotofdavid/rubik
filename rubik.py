import re
from random import randint as r
MOVE_REGEX = re.compile("^(R|L|U|D|F|B|M|E|S|x|y|z|r|l|u|d|f|b|Rw|Lw|Dw|Uw|Fw|Bw)['2]?$")

FACE_MOVES = ["U","D","F","B","L","R"]
SLICE_MOVES = ["M","E","S"]
WEDGE_MOVES = ["u", "d", "f", "b", "l", "r", "Uw", "Dw", "Fw", "Bw", "Lw", "Rw"]
ROTATIONS = ["x","y","z"]
move_dict = {"U":0,"L":1,"F":2,"R":3,"B":4,"D":5, "E":0, "M":1, "S": 2, "x":0, "y":1, "z":2, "u":0, "d":1, "f":2, "b":3, "l":4, "r":5}


class Algorithm(object):
	def __init__(self,alg):
		assert(valid_alg(alg))
		moves = alg.split()
		self.move_count = 0
		self.moves = []
		for move in moves:
			m = Move(move)
			if m.letter in FACE_MOVES or m.letter in WEDGE_MOVES:
				self.move_count += 1
			elif m.letter in SLICE_MOVES:
				self.move_count += 2
			self.moves.append(m)


	def __repr__(self):
		return " ".join([str(m) for m in self.moves])
	
	def num_moves(self):
		return self.move_count

	def solution(self, sol):
		c = Cube()
		c.apply_alg(self)
		c.apply_alg(sol)
		return c.solved()

	def invert(self):
		inverse_moves = []
		for m in self.moves[::-1]: 
			inverse_moves.append(m.invert())
		return Algorithm(" ".join(inverse_moves))

class Move(object):
	def __init__(self,move):
		if (len(move)==1):
			self.num = 1
			self.letter = move
		elif (len(move)==2):
			self.letter = move[:1]
			rest = move[1:]
			if rest == "w":
				self.letter = self.letter.lower()
				self.num = 1
			if rest == "'":
				self.num = 3
			if rest =="2":
				self.num = 2
		elif (len(move)==3):
			self.letter = move[:1].lower()
			rest = move[2:]
			if rest == "'":
				self.num = 3
			if rest =="2":
				self.num = 2

	def __repr__(self):
		if self.num == 1:
			return self.letter
		if self.num == 2:
			return self.letter + "2"
		if self.num == 3:
			return self.letter + "'"

	def invert(self):
		inverse = ""
		inverse += self.letter
		if self.num == 1:
			inverse += "'"
		elif self.num == 2:
			inverse += "2"
		return inverse




class Cube(object):
	def __init__(self): 
		self.cube = [[[i for _ in xrange(3)] for _ in xrange(3)] for i in xrange(6)]

	def __repr__(self):
		return str(self.cube)

	def solved(self):
		for face in range(6):
			if len(set(self.cube[face][0]).union(set(self.cube[face][1])).union(set(self.cube[face][2]))) > 1:
				return False
		return True

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
		for i in loop:
			if i > 0:
				self.cube[args[i][0]][args[i][1]] = self.cube[args[i-1][0]][args[i-1][1]]
		self.cube[args[0][0]][args[0][1]] = t

	def rotate_face(self, face):
		#rotate the stickers on the face
		self.cycle_stickers([face,0,0],[face,0,2],[face,2,2],[face,2,0])
		self.cycle_stickers([face,0,1],[face,1,2],[face,2,1],[face,1,0])

		#U
		if face==0:
			self.cycle_rows([4,0],[3,0],[2,0],[1,0])
		#L
		elif face==1:
			self.cycle_stickers([0,0,0],[2,0,0],[5,0,0],[4,2,2])
			self.cycle_stickers([0,1,0],[2,1,0],[5,1,0],[4,1,2])
			self.cycle_stickers([0,2,0],[2,2,0],[5,2,0],[4,0,2])
		#F
		elif face==2:				
			self.cycle_stickers([0,2,0],[3,0,0],[5,0,2],[1,2,2])
			self.cycle_stickers([0,2,1],[3,1,0],[5,0,1],[1,1,2])
			self.cycle_stickers([0,2,2],[3,2,0],[5,0,0],[1,0,2])
		#R
		elif face==3:
			self.cycle_stickers([0,2,2],[4,0,0],[5,2,2],[2,2,2])
			self.cycle_stickers([0,1,2],[4,1,0],[5,1,2],[2,1,2])
			self.cycle_stickers([0,0,2],[4,2,0],[5,0,2],[2,0,2])
		#B
		elif face==4:
			self.cycle_stickers([0,0,0],[1,2,0],[5,2,2],[3,0,2])
			self.cycle_stickers([0,0,1],[1,1,0],[5,2,1],[3,1,2])
			self.cycle_stickers([0,0,2],[1,0,0],[5,2,0],[3,2,2])
		#D
		elif face==5:
			self.cycle_rows([1,2],[2,2],[3,2],[4,2])

	def slice(self, axis):
		#E
		if axis==0:
			self.cycle_rows([1,1],[2,1],[3,1],[4,1])

		#M
		elif axis==1:
			self.cycle_stickers([0,0,1],[2,0,1],[5,0,1],[4,2,1])
			self.cycle_stickers([0,1,1],[2,1,1],[5,1,1],[4,1,1])
			self.cycle_stickers([0,2,1],[2,2,1],[5,2,1],[4,0,1])

		#S	
		elif axis==2:
			self.cycle_stickers([0,1,0],[1,2,1],[5,1,2],[3,0,1])
			self.cycle_stickers([0,1,1],[1,1,1],[5,1,1],[3,1,1])
			self.cycle_stickers([0,1,2],[1,0,1],[5,1,0],[3,2,1])

	def rotate(self, axis):
		#x
		if axis == 0: 
			self.apply_move(Move("R"))
			self.apply_move(Move("L'"))
			self.apply_move(Move("M'"))
		#y
		elif axis == 1:
			self.apply_move(Move("U"))
			self.apply_move(Move("E'"))
			self.apply_move(Move("D'"))
		#z
		elif axis == 2:
			self.apply_move(Move("B'"))
			self.apply_move(Move("F"))
			self.apply_move(Move("S'"))

	def rotate_wedge(self, face): 
		#u / Uw
		if face == 0: 
			self.apply_move(Move("U"))
			self.apply_move(Move("E'"))
		#d / Dw
		elif face == 1: 
			self.apply_move(Move("D"))
			self.apply_move(Move("E"))
		#f / Fw
		elif face == 2:
			self.apply_move(Move("F"))
			self.apply_move(Move("S'"))
		#b / Bw
		elif face == 3:
			self.apply_move(Move("B"))
			self.apply_move(Move("S"))
		#l / Lw
		elif face == 4:
			self.apply_move(Move("L"))
			self.apply_move(Move("M"))
		#r / Rw
		elif face == 5:
			self.apply_move(Move("R"))
			self.apply_move(Move("M'"))

	def apply_alg(self, alg):
		for move in alg.moves:
			self.apply_move(move)

	def apply_move(self, move):
		if move.letter in FACE_MOVES:
			for _ in range(move.num):
				self.rotate_face(move_dict[move.letter])
		elif move.letter in WEDGE_MOVES:
			for _ in range(move.num):
				self.rotate_wedge(move_dict[move.letter])
		elif move.letter in SLICE_MOVES:
			for _ in range(move.num):
				self.slice(move_dict[move.letter])
		elif move.letter in ROTATIONS:
			for _ in range(move.num):
				self.rotate(move_dict[move.letter])

def valid_alg(alg_str):
	moves = alg_str.split()
	for move in moves:
		if not MOVE_REGEX.match(move):
			print("{move} does not match regex".format(move=move))
			return False
	return True

# Based on function from http://www.speedsolving.com/forum/showthread.php?25460-My-python-one-liner-scramble-generator/page21
def gen_scramble(l):
	scramble = ""
	m=b=9
	for u in range(l):
		c=b;b=m
		while c+b-4 and m==c or m==b:
			m=r(0,5)
		scramble += "URFBLD"[m]+" '2"[r(0,2)]+" "
	return scramble.replace("  "," ")[:-1]

if __name__ == "__main__":
	c = Cube()
	a = Algorithm("R U R'")


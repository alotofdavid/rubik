from rubik import *

def test_valid_moves():
	assert(valid_moves("R U R' F x2 D2".split()))
	assert(not valid_moves("2R R R'".split()))

def test_cube():
	c = Cube()
	assert(c.cube==[[[i for _ in xrange(3)] for _ in xrange(3)] for i in xrange(6)])
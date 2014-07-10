from rubik import *

def test_valid_alg():
	assert(valid_alg("R U R' F x2 D2"))
	assert(not valid_alg("2R R R'"))
	assert(not valid_alg("R'' U"))

def test_valid_alg_wedge():
	assert(valid_alg("Rw u' d2"))
	assert(not valid_alg("Rww2"))
	assert(not valid_alg("uw2"))

def test_valid_alg_slice():
	assert(valid_alg("M E' S2"))
from rubik import *

def test_rotations():
	cube = Cube()
	alg = Algorithm("R z2 L' U x2 D'")
	cube.apply_alg(alg)
	assert(cube.solved())

def test_algorithms():
	cube = Cube()
	alg = Algorithm("R' B F' L' B' R2 F' B2 L2 F2 U L' R F' B' L2 R D' L B2")
	sol = Algorithm("L B2 L D' F2 U L' U' R' U L U2 F D' B2 D F2 R F R2 B R B' R2 B R' B' L2")
	cube.apply_alg(alg)
	cube.apply_alg(sol)
	assert(cube.solved())


test_rotations()
test_algorithms()
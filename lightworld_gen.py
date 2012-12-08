#from lightroom import Lightroom
#from lightroom_gen import make_rand_room
import lightroom_gen
from lightroom_gen import LightroomGen
import random
import numpy
from numpy.random import random_integers as rand

class Lightworld():
	num_rooms = 2
	
	def __init__(self):
		num_rooms = 2
	
	def gen_world(self):
		self.num_rooms = random.randint(2, 5)
		print("num_rooms: " + str(self.num_rooms))
		lg = LightroomGen()
		list_of_rooms = []
		for i in range(0, self.num_rooms):
			next_room = lg.make_rand_room()
			list_of_rooms.append(next_room)
		for i in range(0, self.num_rooms):
			print("Room " + str(i) + ": ")
			print(list_of_rooms[i])
		return list_of_rooms
		
lw = Lightworld()
lw.gen_world()
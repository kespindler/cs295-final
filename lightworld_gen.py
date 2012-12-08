#from lightroom import Lightroom
#from lightroom_gen import make_rand_room
from lightroom_struct import LightroomStruct
import random
import numpy
from numpy.random import random_integers as rand

#class Lightworld:
#    #num_rooms = 2
#    
#    def __init__(self):
#        #num_rooms = 2
#        pass
    
def gen_world():
    num_rooms = random.randint(2, 5)
    print("num_rooms: " + str(num_rooms))
    #lg = LightroomGen()
    list_of_rooms = []
    for i in range(0, num_rooms):
        lr = LightroomStruct()
        next_room = lr.return_tuple()
        list_of_rooms.append(next_room)
    for i in range(0, num_rooms):
        (key, room) = list_of_rooms[i]
        if(key == 0):
            print("Room " + str(i) + " does not contain a key:")
        else:
            print("Room " + str(i) + " contains a key:")
        print(room)
    return list_of_rooms
   
#gen_world()

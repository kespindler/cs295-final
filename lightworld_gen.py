#!/usr/bin/env python
#from lightroom import Lightroom
#from lightroom_gen import make_rand_room
from lightroom_struct import LightroomStruct as LS
import random
import numpy
from numpy.random import random_integers as rand
from numpy import array_equal

    
def gen_world():
    num_rooms = random.randint(2, 5)
    print("num_rooms: " + str(num_rooms))
    list_of_rooms = []
    for i in range(0, num_rooms):
        lr = LS()
        next_room = lr.return_tuple()
        list_of_rooms.append(next_room)
    for i in range(0, num_rooms):
        (key, room) = list_of_rooms[i]
#        if(key == 0):
#            print("Room " + str(i) + " does not contain a key:")
#        else:
#            print("Room " + str(i) + " contains a key:")
#        print(room)
    return list_of_rooms

def lightroom_equal((lr1_key, lr1_room), (lr2_key, lr2_room)):    
    if((lr1_key == lr2_key) and (array_equal(lr1_room, lr2_room))):
        return True
    return False

def lightworld_equal(lw1, lw2):
    if(len(lw1) == len(lw2)):
        for i in range(0, len(lw1)):
            if(not lightroom_equal(lw1[i], lw2[i])):
                return False
    else:
        return False
    return True   

def gen_100():
    list_of_worlds = []
    for i in range(0, 100):
        is_unique = 1
        world = gen_world()
        j = 0
        while(j < i):
            if(lightworld_equal(list_of_worlds[j], world)):
                world = gen_world
                j = 0
            else:
                j += 1
        list_of_worlds.append(world)
    return list_of_worlds
            
            
#gen_100()    
#   
##gen_world()
#
#room_arr1 = numpy.zeros((3, 3), dtype=int)
#room_arr2 = numpy.zeros((3, 3), dtype=int)
#room_arr3 = numpy.zeros((3, 3), dtype=int)
#room_arr3[0, :] = 1
#room_arr3[1, :] = 2
##print("room_arr1:")
##print(room_arr1)
##print("room_arr2:")
##print(room_arr2)
##print("room_arr3:")
##print(room_arr3)
#lr11 = LS(1, room_arr1).return_tuple()
#lr12 = LS(1, room_arr2).return_tuple()
#lr13 = LS(1, room_arr3).return_tuple()
#lr01 = LS(0, room_arr1).return_tuple()
#
#lw1 = [lr11, lr13]
#lw2 = [lr12, lr13]
#lw3 = [lr01, lr13]
#lw4 = [lr11, lr13, lr12]
#
#assert (lightroom_equal(lr11, lr12))
#assert (lightroom_equal(lr13, lr13))
#assert (not lightroom_equal(lr11, lr13))
#assert (not lightroom_equal(lr11, lr01))
#assert (not lightroom_equal(lr13, lr01))
#
#assert (lightworld_equal(lw1, lw2))
#assert (not lightworld_equal(lw1, lw3))
#assert (not lightworld_equal(lw1, lw4))

if __name__ == '__main__':
    worlds = gen_100()
    import os
    folder = 'lightworlds'
    try:
        os.mkdir(folder)
    except OSError:
        pass
    for i, world in enumerate(worlds):
        world = [w for k, w in world]
        roomstrings = ['\n'.join(''.join(str(i) for i in row) for row in room) for room in world]
        with open(os.path.join(folder, '{0:03}.txt'.format(i)), 'w') as f:
            f.write('\n\n'.join(roomstrings))

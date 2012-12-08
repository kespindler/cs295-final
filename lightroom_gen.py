import random
import numpy
from numpy.random import random_integers as rand

class LightroomGen():
    has_key = 0
    
    def __init__(self):
        has_key = 0

		 
    # generates a random room with dimensions between 4 and 50    
    def make_rand_room(self):
        self.has_key = random.randint(0, 1)
        
        #TODO Generalize to give random padding
        h = random.randint(6, 20)
        w = random.randint(6, 20)
        #print("h: " + str(h))
        #print("w: " + str(w))
        shape = (h, w)
        # initialize room array
        room = numpy.zeros(shape, dtype=int)
        # build edge walls
        room[0, :] = room[-1, :] = 1
        room[:, 0] = room[:, -1] = 1
        room[1, :] = room[-2, :] = 1
        room[:, 1] = room[:, -2] = 1
             
        # Generate the agent's start position
        start_x = random.randint(2, w-3)
        start_y = random.randint(2, h-3)
        #print("start_x: " + str(start_x))
        #print("start_y: " + str(start_y))
        
        # Generate the key's position
        key_x = random.randint(2, w-3)
        key_y = random.randint(2, h-3)
        
        # Generate the lock's position
        # The lock will always appear on a wall
        on_side_wall = random.randint(0, 1)
        which_wall = random.randint(0, 1)
        lock_x = 0
        lock_y = 0
        if(on_side_wall):
            if(which_wall):
                lock_x = w-2
            else:
                lock_x = 1
            lock_y = random.randint(2, h-3)
        else:
            if(which_wall):
                lock_y = h-2
            else:
                lock_y = 1
            lock_x = random.randint(2, w-3)
        
        # Generate the door's position
        # The lock will always appear on a wall
        on_side_wall = random.randint(0, 1)
        which_wall = random.randint(0, 1)
        door_x = 0
        door_y = 0
        if(on_side_wall):
            if(which_wall):
                door_x = w-2
            else:
                door_x = 1
            door_y = random.randint(2, h-3)
        else:
            if(which_wall):
                door_y = h-2
            else:
                door_y = 1
            door_x = random.randint(2, w-3)
        
        room[start_y, start_x] = 2
        if(self.has_key):
            #while((key_y == start_y) and (key_x == start_x)):
		    #    key_x = random.randint(2, w-3)
		    #    key_y = random.randint(2, h-3)
            room[key_y, key_x] = 3
        room[lock_y, lock_x] = 4
        room[door_y, door_x] = 5
        #for i in xrange(h):
        #    print(room[i])
        room_arr = numpy.matrix(room)
        return (self.has_key, room_arr) 
	            
    def make_spec_room_w_key(self, h, w, start_x, start_y, key_x, key_y, lock_x, lock_y, door_x, door_y):
        print("h: " + str(h))
        print("w: " + str(w))
        shape = (h, w)
        # initialize room array
        room = numpy.zeros(shape, dtype=int)
        # build edge walls
        room[0, :] = room[-1, :] = 1
        room[:, 0] = room[:, -1] = 1
        room[1, :] = room[-2, :] = 1
        room[:, 1] = room[:, -2] = 1
        
        room[start_y, start_x] = 2
        room[key_y, key_x] = 3
        room[lock_y, lock_x] = 4
        room[door_y, door_x] = 5
        
        #for i in xrange(h):
        #    print(room[i])
        return room
    
    def make_spec_room_wo_key(self, h, w, start_x, start_y, lock_x, lock_y, door_x, door_y):
        print("h: " + str(h))
        print("w: " + str(w))
        shape = (h, w)
        # initialize room array
        room = numpy.zeros(shape, dtype=int)
        # build edge walls
        room[0, :] = room[-1, :] = 1
        room[:, 0] = room[:, -1] = 1
        room[1, :] = room[-2, :] = 1
        room[:, 1] = room[:, -2] = 1
        
        room[start_y, start_x] = 2
        room[lock_y, lock_x] = 6
        room[door_y, door_x] = 5
        
        for i in xrange(h):
            print(room[i])
        return room
    
    def maze_gen(self, complexity=.75, density=.5):
        h = random.randint(5, 10)
        w = random.randint(5, 10)
        #print("h: " + str(h))
        #print("w: " + str(w))
        
        # Only odd shapes
        shape = ((h // 2) * 2 + 1, (w // 2) * 2 + 1)
        # Adjust complexity and density relative to maze size
        complexity = int(complexity * (5 * (shape[0] + shape[1])))
        density    = int(density * (shape[0] // 2 * shape[1] // 2))
        # Build actual maze
        Z = numpy.zeros(shape, dtype=int)
        # Fill borders
        Z[0, :] = Z[-1, :] = 1
        Z[:, 0] = Z[:, -1] = 1
        # Make isles
        for i in range(density):
            x, y = rand(0, shape[1] // 2) * 2, rand(0, shape[0] // 2) * 2
            Z[y, x] = 1
            for j in range(complexity):
                neighbours = []
                if x > 1:             neighbours.append((y, x - 2))
                if x < shape[1] - 2:  neighbours.append((y, x + 2))
                if y > 1:             neighbours.append((y - 2, x))
                if y < shape[0] - 2:  neighbours.append((y + 2, x))
                if len(neighbours):
                    y_,x_ = neighbours[rand(0, len(neighbours) - 1)]
                    if Z[y_, x_] == 0:
                        Z[y_, x_] = 1
                        Z[y_ + (y - y_) // 2, x_ + (x - x_) // 2] = 1
                        x, y = x_, y_
        print(Z)
        return Z
    
lg = LightroomGen()
#
lg.make_rand_room()
#
#lg.make_spec_room_w_key(5, 5, 3, 2, 2, 1, 0, 3, 3, 0)
#
#lg.make_spec_room_wo_key(5, 5, 3, 2, 0, 3, 3, 0)
#
#lg.maze_gen(.75, .75)

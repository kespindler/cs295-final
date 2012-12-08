from lightroom_gen import LightroomGen

class LightroomStruct():
    has_key = 0
    room = []
    
    def __init__(self):
        lg = LightroomGen()
        (key, room_arr) = lg.make_rand_room()
        self.has_key = key
        self.room = room_arr
        
    def return_tuple(self):
        return (self.has_key, self.room)
    
    
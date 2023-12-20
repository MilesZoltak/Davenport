import numpy as np
import asyncio
import websockets
import json

class MidiInterpreter:
    def __init__(self, prompter):
        self.piano = np.zeros(61)
        self.binary_piano = np.zeros(61)
        self.prompter = prompter

    # return a tuple of pitch, velocity, time
    def decode_event(self, e):
        #      pitch    velocity  time
        return e.data1, e.data2, e.data3
    
    def interpret(self, e):
        pitch, velocity, time = self.decode_event(e)
    
        if (36 <= pitch <= 96): 
            idx = pitch - 36
            self.piano[idx] = velocity
            self.binary_piano[idx] = velocity != 0

        self.prompter.check(self.binary_piano, velocity == 0)
        


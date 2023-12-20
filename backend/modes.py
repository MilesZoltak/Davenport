import numpy as np
import asyncio
import websockets
import json

NOTES = {'C2': 36, 'C#2': 37, 'D♭2': 37, 'D2': 38, 'D#2': 39, 'E♭2': 39, 'E2': 40, 'F2': 41, 'F#2': 42, 'G♭2': 42, 'G2': 43, 'G#2': 44, 'A♭2': 44, 'A2': 45, 'A#2': 46, 'B♭2': 46, 'B2': 47, 'C3': 48, 'C#3': 49, 'D♭3': 49, 'D3': 50, 'D#3': 51, 'E♭3': 51, 'E3': 52, 'F3': 53, 'F#3': 54, 'G♭3': 54, 'G3': 55, 'G#3': 56, 'A♭3': 56, 'A3': 57, 'A#3': 58, 'B♭3': 58, 'B3': 59, 'C4': 60, 'C#4': 61, 'D♭4': 61, 'D4': 62, 'D#4': 63, 'E♭4': 63, 'E4': 64, 'F4': 65, 'F#4': 66, 'G♭4': 66, 'G4': 67, 'G#4': 68, 'A♭4': 68, 'A4': 69, 'A#4': 70, 'B♭4': 70, 'B4': 71, 'C5': 72, 'C#5': 73, 'D♭5': 73, 'D5': 74, 'D#5': 75, 'E♭5': 75, 'E5': 76, 'F5': 77, 'F#5': 78, 'G♭5': 78, 'G5': 79, 'G#5': 80, 'A♭5': 80, 'A5': 81, 'A#5': 82, 'B♭5': 82, 'B5': 83, 'C6': 84, 'C#6': 85, 'D♭6': 85, 'D6': 86, 'D#6': 87, 'E♭6': 87, 'E6': 88, 'F6': 89, 'F#6': 90, 'G♭6': 90, 'G6': 91, 'G#6': 92, 'A♭6': 92, 'A6': 93, 'A#6': 94, 'B♭6': 94, 'B6': 95, 'C7': 96}
MAJORS = {'C2': [36, 40, 43], 'C#2': [37, 41, 44], 'D♭2': [37, 41, 44], 'D2': [38, 42, 45], 'D#2': [39, 43, 46], 'E♭2': [39, 43, 46], 'E2': [40, 44, 47], 'F2': [41, 45, 48], 'F#2': [42, 46, 49], 'G♭2': [42, 46, 49], 'G2': [43, 47, 50], 'G#2': [44, 48, 51], 'A♭2': [44, 48, 51], 'A2': [45, 49, 52], 'A#2': [46, 50, 53], 'B♭2': [46, 50, 53], 'B2': [47, 51, 54], 'C3': [48, 52, 55], 'C#3': [49, 53, 56], 'D♭3': [49, 53, 56], 'D3': [50, 54, 57], 'D#3': [51, 55, 58], 'E♭3': [51, 55, 58], 'E3': [52, 56, 59], 'F3': [53, 57, 60], 'F#3': [54, 58, 61], 'G♭3': [54, 58, 61], 'G3': [55, 59, 62], 'G#3': [56, 60, 63], 'A♭3': [56, 60, 63], 'A3': [57, 61, 64], 'A#3': [58, 62, 65], 'B♭3': [58, 62, 65], 'B3': [59, 63, 66], 'C4': [60, 64, 67], 'C#4': [61, 65, 68], 'D♭4': [61, 65, 68], 'D4': [62, 66, 69], 'D#4': [63, 67, 70], 'E♭4': [63, 67, 70], 'E4': [64, 68, 71], 'F4': [65, 69, 72], 'F#4': [66, 70, 73], 'G♭4': [66, 70, 73], 'G4': [67, 71, 74], 'G#4': [68, 72, 75], 'A♭4': [68, 72, 75], 'A4': [69, 73, 76], 'A#4': [70, 74, 77], 'B♭4': [70, 74, 77], 'B4': [71, 75, 78], 'C5': [72, 76, 79], 'C#5': [73, 77, 80], 'D♭5': [73, 77, 80], 'D5': [74, 78, 81], 'D#5': [75, 79, 82], 'E♭5': [75, 79, 82], 'E5': [76, 80, 83], 'F5': [77, 81, 84], 'F#5': [78, 82, 85], 'G♭5': [78, 82, 85], 'G5': [79, 83, 86], 'G#5': [80, 84, 87], 'A♭5': [80, 84, 87], 'A5': [81, 85, 88], 'A#5': [82, 86, 89], 'B♭5': [82, 86, 89], 'B5': [83, 87, 90], 'C6': [84, 88, 91], 'C#6': [85, 89, 92], 'D♭6': [85, 89, 92], 'D6': [86, 90, 93], 'D#6': [87, 91, 94], 'E♭6': [87, 91, 94], 'E6': [88, 92, 95], 'F6': [89, 93, 96]}
MINORS = {'Cm2': [36, 39, 43], 'C#m2': [37, 40, 44], 'D♭m2': [37, 40, 44], 'Dm2': [38, 41, 45], 'D#m2': [39, 42, 46], 'E♭m2': [39, 42, 46], 'Em2': [40, 43, 47], 'Fm2': [41, 44, 48], 'F#m2': [42, 45, 49], 'G♭m2': [42, 45, 49], 'Gm2': [43, 46, 50], 'G#m2': [44, 47, 51], 'A♭m2': [44, 47, 51], 'Am2': [45, 48, 52], 'A#m2': [46, 49, 53], 'B♭m2': [46, 49, 53], 'Bm2': [47, 50, 54], 'Cm3': [48, 51, 55], 'C#m3': [49, 52, 56], 'D♭m3': [49, 52, 56], 'Dm3': [50, 53, 57], 'D#m3': [51, 54, 58], 'E♭m3': [51, 54, 58], 'Em3': [52, 55, 59], 'Fm3': [53, 56, 60], 'F#m3': [54, 57, 61], 'G♭m3': [54, 57, 61], 'Gm3': [55, 58, 62], 'G#m3': [56, 59, 63], 'A♭m3': [56, 59, 63], 'Am3': [57, 60, 64], 'A#m3': [58, 61, 65], 'B♭m3': [58, 61, 65], 'Bm3': [59, 62, 66], 'Cm4': [60, 63, 67], 'C#m4': [61, 64, 68], 'D♭m4': [61, 64, 68], 'Dm4': [62, 65, 69], 'D#m4': [63, 66, 70], 'E♭m4': [63, 66, 70], 'Em4': [64, 67, 71], 'Fm4': [65, 68, 72], 'F#m4': [66, 69, 73], 'G♭m4': [66, 69, 73], 'Gm4': [67, 70, 74], 'G#m4': [68, 71, 75], 'A♭m4': [68, 71, 75], 'Am4': [69, 72, 76], 'A#m4': [70, 73, 77], 'B♭m4': [70, 73, 77], 'Bm4': [71, 74, 78], 'Cm5': [72, 75, 79], 'C#m5': [73, 76, 80], 'D♭m5': [73, 76, 80], 'Dm5': [74, 77, 81], 'D#m5': [75, 78, 82], 'E♭m5': [75, 78, 82], 'Em5': [76, 79, 83], 'Fm5': [77, 80, 84], 'F#m5': [78, 81, 85], 'G♭m5': [78, 81, 85], 'Gm5': [79, 82, 86], 'G#m5': [80, 83, 87], 'A♭m5': [80, 83, 87], 'Am5': [81, 84, 88], 'A#m5': [82, 85, 89], 'B♭m5': [82, 85, 89], 'Bm5': [83, 86, 90], 'Cm6': [84, 87, 91], 'C#m6': [85, 88, 92], 'D♭m6': [85, 88, 92], 'Dm6': [86, 89, 93], 'D#m6': [87, 90, 94], 'E♭m6': [87, 90, 94], 'Em6': [88, 91, 95], 'Fm6': [89, 92, 96]}


class NotePrompter():
    def __init__(self, sequence_length, sequence=None):
        self.NOTES = NOTES
        # the length of the sequence of notes
        self.sequence_length = sequence_length
        
        # the sequence of notes to play (supports custom sequences)
        if sequence != None:
            self.sequence = sequence
        else:
            self.sequence = [(list(NOTES.keys())[i], NOTES[list(NOTES.keys())[i]]) for i in np.random.choice(len(NOTES), sequence_length)]
        
        self.progress = 0

        self.prompt = self.sequence[0][0]
        self.message = ""

        self.build_prompt(False, np.zeros(61))

    async def send_receive_message(self, msg):
        uri = "ws://localhost:8765"
        async with websockets.connect(uri) as websocket:
            await websocket.send(msg)

    def check(self, binary_piano, release):
        # don't check if we have made our way through the sequence already
        if self.progress >= self.sequence_length: return False

        if release:
            self.build_prompt(False, binary_piano)
            return

        goal_note = self.sequence[self.progress][1]
        pressed = np.where(binary_piano == 1)[0]
        success = False

        # only check if a single note is being pressed, and check if it is correct
        # if note is correct then we advance progress
        # otherwise we update the message
        if len(pressed) == 1 and pressed[0] + 36 == goal_note:
            self.progress += 1
            self.message = ""
            success = True
        else:
            self.message = "Wrong note! Try again."

        # update prompt if we won't be reading off the end
        if (self.progress < self.sequence_length):
            self.prompt = self.sequence[self.progress][0]
        else:
            self.prompt = ""
            self.message = "Game Complete!"
            
        self.build_prompt(success, binary_piano)
        
        if self.progress >= self.sequence_length: exit()        
    
    async def send_prompt(self, data):
        uri = "ws://localhost:8765"
        async with websockets.connect(uri) as websocket:
            await websocket.send(data)
    
    def build_prompt(self, success, binary_piano):
        key_data = {}
        for i, x in enumerate(binary_piano):
            if x != 0:
                key_data[i + 36] = "green" if success else "red"
        
        data = json.dumps(
            {"key_data": key_data,
             "prompt": self.prompt,
             "message": self.message}
        )
        asyncio.get_event_loop().run_until_complete(self.send_prompt(data))

    # async def send_prompt(self, data):
    #     uri = "ws://localhost:8765"
    #     async with websockets.connect(uri) as websocket:
    #         await websocket.send(data)
    
    # def build_prompt(self):
    #     key_data = {key_data[i + 36]: "red" if i + 36 != NOTES[self.prompt] else "green" for i, x in enumerate(self.binary_piano) if x != 0}
        
    #     data = json.dumps(
    #         {"key_data": key_data,
    #          "prompt": self.prompt,
    #          "message": self.message}
    #     )
    #     asyncio.get_event_loop().run_until_complete(self.send_prompt(data))

    # def refresh_gui(self):
    #     asyncio.get_event_loop().run_until_complete(self.send_prompt("{}"))


        

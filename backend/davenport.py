import argparse
import threading
from midi_reader import MidiReader
from midi_interpreter import MidiInterpreter
import modes

def main():
    # read the arguments
    args = parse_args()

    mode = modes.NotePrompter(2)
    
    # create the Midi Interpreter so we can have a running represenation of the piano
    interp = MidiInterpreter(mode)
    piano = interp.piano
    binary = interp.binary_piano

    reader = MidiReader(1)

    while True:
        reader.read_inputs(interp, mode)
    
    # yeah, this is messed up but i think i still want it here...
    reader.close()


def parse_args():
    parser = argparse.ArgumentParser(description="My Command Line Program", epilog="Additional information about the program")
    parser.add_argument("--mode", "-m", help="Davenport Modes: [debug, quiz]")
    args = parser.parse_args()

    return {
        "mode": args.mode
    }

if __name__ == "__main__":
    main()

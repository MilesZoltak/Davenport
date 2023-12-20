import pygame as pg
import pygame.midi
import time

class MidiReader():
    def __init__(self, device_id):
        # init pygame and prepare to read events
        pg.init()
        pg.fastevent.init()

        self._print_device_info(quiet=True)

        self.event_get = pg.fastevent.get
        self.event_post = pg.fastevent.post
        self.start = time.time()

        # initialize pygame's midi module
        pygame.midi.init()

        # select a device_id if one was not passed
        if device_id is None:
            input_id = pygame.midi.get_default_input_id()
            output_id = pygame.midi.get_default_output_id()
        else:
            input_id = device_id
            output_id = device_id + 2


        self.input_id = input_id
        
        self.i = pygame.midi.Input(input_id)
        self.o = pygame.midi.Output(output_id)

        # set the display mode to be really basically invisible
        pg.display.set_mode((1, 1))

    def _print_device_info(self, quiet=False):
        pygame.midi.init()

        if not quiet:
            for i in range(pygame.midi.get_count()):
                r = pygame.midi.get_device_info(i)
                (interf, name, input, output, opened) = r

                in_out = ""
                if input:
                    in_out = "(input)"
                if output:
                    in_out = "(output)"

                print(
                    "%2i: interface :%s:, name :%s:, opened :%s:  %s"
                    % (i, interf, name, opened, in_out)
                )
        pygame.midi.quit()

    def output(self, note, velocity):
        self.o.note_on(note, velocity)

    def read_inputs(self, interpreter, prompter):
        # this is where we actually read the events
        going = True
        while going:
            events = self.event_get()
            for e in events:
                if e.type in [pg.QUIT]:
                    going = False
                if e.type in [pg.KEYDOWN]:
                    going = False
                if e.type in [pygame.midi.MIDIIN]:
                    interpreter.interpret(e)

            if self.i.poll():
                midi_events = self.i.read(10)
                
                # convert midi events to pygame events
                midi_evs = pygame.midi.midis2events(midi_events, self.i.device_id)

                for m_e in midi_evs:
                    self.event_post(m_e)
            
        # once we break out of the loop we just quit everything
    def close(self):
        del self.i
        pygame.midi.quit()

def input_main(self, interpreter, prompter, device_id=None):
    pg.init()
    pg.fastevent.init()
    event_get = pg.fastevent.get
    event_post = pg.fastevent.post

    pygame.midi.init()

    if device_id is None:
        input_id = pygame.midi.get_default_input_id()
    else:
        input_id = device_id

    print("using input_id :%s:" % input_id)
    i = pygame.midi.Input(input_id)

    pg.display.set_mode((1, 1))

    going = True
    while going:
        events = event_get()
        for e in events:
            if e.type in [pg.QUIT]:
                going = False
            if e.type in [pg.KEYDOWN]:
                going = False
            if e.type in [pygame.midi.MIDIIN]:
                print(e)

        if i.poll():
            midi_events = i.read(10)
            # convert them into pygame events.
            midi_evs = pygame.midi.midis2events(midi_events, i.device_id)

            for m_e in midi_evs:
                event_post(m_e)

def close(self):
    del i
    pygame.midi.quit()
        


# davenport

Digital Piano Teacher Web UI

This is a 3 part set of programs that I use as my personal piano teacher!

First is the set of Python programs I use to read input from my MIDI keyboard:
- backend/davenport.py             -- the brains of the whole program, connnects the other three .py files together
- backend/midi_reader.py           -- reads input coming from the piano and send it to midi_interpreter.py
- backend/midi_interpreter.py      -- deciphers the midi encoded messages from midi_reader.py and sends them to modes.py
- backend/modes.py                 -- the teaching part of the program! prompts user for specific keys (chords and scales coming soon) and sends them to the server

Then there is a Javascript server that spins up a websocket to communicate with the UI:
- backend/server.js                -- maintains a websocket that listens for activity from modes.py and sends information to Flutter app via localhost:8765

Finally, we have the Flutter app which serves as the UI for the user behind the piano:
- lib/home.dart                    -- displays virtual piano, prompt for user, and messages about performance, etc.  

I'm pretty happy with it so far.  Can't decide if I'm in love with the websocket implemenatation.  It works well enough, but there are a couple factors that make me question if it is overly complicated.  It's been pretty easy to set up and use so I suppose not, but this is all just a work in progress of course.

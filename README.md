# gtr-effects-midi
Capture SYSEX and convert to virtual midi input

### Why
Some effecs boards may have some midi capabilities such as take input or interanl controll but lack a way to send as an output into a DAW.
This program listens for certain SYSEX messages and reacts by creating a secondary midi message down a specific virtaul midi channel.

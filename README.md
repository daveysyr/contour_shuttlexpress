# contour_shuttlexpress
This is to make the Contour Shuttle Express Multimedia Controller work with Shotcut on Linux (Ubuntu 25.04)

I bought a Contour ShuttleXpress (mini item) and was annoyed to find that it did not work on my Linux PC.  As with all Linux problems, you either wait for someone else to fix it, fix it yourself, or have you to just put with it.

This code basically just takes the movements from the controller and outputs keystrokes in the active window.

Took me ages to get the jog and shuttle controls working acceptably, but they do work as they're supposed to now.

To use this, basically:

Download the python code into whatever directory you like.
cd to that directory and run the code by using 'python3 shuttlexpress-listener.py'
you may need to install some dependent libraries, but once you do, it should just find the device and start listening.  Once you change to the Shotcut, the jog, shuttle and keys should function as in the code.

Curent mappings:

1) space
2) enter
3) esc
4) z
5) s

Shuttle is mapped to j, k, and l (reverse, pause, forward)
Jog is mapped to left and right keys.

If you want to add more keys, you need to add them in the KEY_MAP and also within EV_KEY.



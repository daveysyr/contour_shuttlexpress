The purpose of this code is to get the Contour ShuttleXpress working on Linux 25.04.

I bought the Contour ShuttleXpress on the understanding that it works on Linux.  It did not.  I found this annoying.  There are a few implementations for the larger "Pro" version, but nothing for the one I bought.

The device should be plugged in, the python code left running in a terminal window.  Once you switch to another window, any movements will just be output as text into that window like you were hitting the keyboard - so just be careful!

You could make it work for other applications, e.g. OBS, Teams,browser, etc just by using the correct key mappings.

Current mappings are:

1) Space
2) Enter
3) Esc
4) z
5) s


The only buttons I use at the moment are the 's' for 'split' and 'Enter' for pause/play, so these key mappings will change over time for certain.

Feel free to modify this as you need.


You can find out the input devices on your linux by using the following:

ls /dev/input/

and you'll get a list of the available devices.


If you then do the commnand:

evtest /dev/input/event19

for each input, you can then see each input.


I hope all this helps.  Regards, Dave.

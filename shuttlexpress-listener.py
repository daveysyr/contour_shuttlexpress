# This works on Ubuntu Ver 25.04 and Python 3.13.3
# The key mappings are for Shotcut video editor
# This is shared by Dave Sawyer under the GPL licence - feel free to modify it as you need!



import os
from evdev import InputDevice, ecodes, UInput

# Find the ShuttleXpress device by name
device_name = "Contour Design ShuttleXpress"
device = None

# Check the /dev/input directory for devices
for dev_file in os.listdir('/dev/input'):
    dev_path = os.path.join('/dev/input', dev_file)
    try:
        dev = InputDevice(dev_path)
        # Compare device name found to the name that we're looking for
        if dev.name == device_name:
            device = dev
            break
    except OSError:
        # If it's not a valid input device, skip it
        continue

# Handling the device not being found, because it's not plugged in or something
if not device:
    raise RuntimeError(f"Device with name '{device_name}' not found.")


print(f"Listening on {device}...\n")

#device = InputDevice('/dev/input/event22')
#print(f"Listening on {device.name}...\n")


BTN_MAP = {
    260: "Button 1",
    261: "Button 2",
    262: "Button 3",
    263: "Button 4",
    264: "Button 5",  # Button 's'
}


KEY_MAP = {
    260: ecodes.KEY_SPACE,    # Button 1
    261: ecodes.KEY_ENTER,    # Button 2
    262: ecodes.KEY_ESC,      # Button 3
    263: ecodes.KEY_Z,        # Button 4
    264: ecodes.KEY_S,        # Button 5 → 's'
}


# This section creates the virtual keyboard

uinput = UInput({
    ecodes.EV_KEY: [
        ecodes.KEY_LEFTCTRL,
        ecodes.KEY_LEFT,
        ecodes.KEY_RIGHT,
        ecodes.KEY_UP,
        ecodes.KEY_DOWN,
        ecodes.KEY_SPACE,
        ecodes.KEY_ENTER,
        ecodes.KEY_ESC,
        ecodes.KEY_Z,
        ecodes.KEY_X,
        ecodes.KEY_S,
        ecodes.KEY_J,
        ecodes.KEY_L,
        ecodes.KEY_K,
    ]
}, name="shuttle-uinput")



last_dial_value = None
shuttle_old = 'initial'

for event in device.read_loop():
    if event.type == ecodes.EV_REL:
        # This is the part for the inner, clicky 'jog' control
        if event.code == ecodes.REL_DIAL:
            # Check for wraparound condition
            if last_dial_value is not None:
                print (last_dial_value)
                # Handle the wraparound from 255 to 1 or 1 to 255
                if event.value == 1 and last_dial_value == 255:
                    delta = 1  # Treat this as a left movement
                elif event.value == 255 and last_dial_value == 1:
                    delta = -1  # Treat this as a right movement
                else:
                    delta = event.value - last_dial_value



                if delta > 0:
                    print("Jog Right → KEY_RIGHT")
                    uinput.write(ecodes.EV_KEY, ecodes.KEY_RIGHT, 1)
                    uinput.write(ecodes.EV_KEY, ecodes.KEY_RIGHT, 0)
                    uinput.syn()
                elif delta < 0:
                    print("Jog Left → KEY_LEFT")
                    uinput.write(ecodes.EV_KEY, ecodes.KEY_LEFT, 1)
                    uinput.write(ecodes.EV_KEY, ecodes.KEY_LEFT, 0)
                    uinput.syn()
            last_dial_value = event.value

        # This is the part for the outer, sprung 'Shuttle' control
        elif event.code == ecodes.REL_WHEEL:
            print (event.value)
            
            if -2 <= event.value <= 2:
                print (event.value)
                print ('Wheel centred - ish')
                shuttle_new = 'centred'
                if shuttle_new != shuttle_old:
                    print ('shuttle changed!')
                    uinput.write(ecodes.EV_KEY, ecodes.KEY_K, 1)
                    uinput.write(ecodes.EV_KEY, ecodes.KEY_K, 0)
                    uinput.syn()
                    print ('shuttle_old', shuttle_old)
                    shuttle_old = shuttle_new
                    print ('shuttle_new', shuttle_old)
            elif -7 <= event.value <= -3:
                print (event.value)
                print ('Wheel left')
                shuttle_new = 'left'
                if shuttle_new != shuttle_old:
                    print ('shuttle changed!')
                    uinput.write(ecodes.EV_KEY, ecodes.KEY_J, 1)
                    uinput.write(ecodes.EV_KEY, ecodes.KEY_J, 0)
                    uinput.syn()
                    print ('shuttle_old', shuttle_old)
                    shuttle_old = shuttle_new
                    print ('shuttle_new', shuttle_old)
            elif 3 <= event.value <= 7:
                print (event.value)
                print ('Wheel right')
                shuttle_new = 'right'
                if shuttle_new != shuttle_old:
                    print ('shuttle changed!')
                    uinput.write(ecodes.EV_KEY, ecodes.KEY_L, 1)
                    uinput.write(ecodes.EV_KEY, ecodes.KEY_L, 0)
                    uinput.syn()
                    print ('shuttle_old', shuttle_old)
                    shuttle_old = shuttle_new
                    print ('shuttle_new', shuttle_old)
            
            #Store the latest shuttle value
            #print ('shuttle_old', shuttle_old)
            #shuttle_old=shuttle_new
            #print ('shuttle_new', shuttle_old)
            

    elif event.type == ecodes.EV_KEY:
        keycode = KEY_MAP.get(event.code)
        if keycode and event.value == 1:  # Only handle "Pressed"
            print(f"{BTN_MAP[event.code]}: Pressed → {ecodes.KEY[keycode]}")

            if keycode == ecodes.KEY_X:
                # Ctrl+X combo
                uinput.write(ecodes.EV_KEY, ecodes.KEY_LEFTCTRL, 1)
                uinput.write(ecodes.EV_KEY, ecodes.KEY_X, 1)
                uinput.write(ecodes.EV_KEY, ecodes.KEY_X, 0)
                uinput.write(ecodes.EV_KEY, ecodes.KEY_LEFTCTRL, 0)
            else:
                uinput.write(ecodes.EV_KEY, keycode, 1)
                uinput.write(ecodes.EV_KEY, keycode, 0)

            uinput.syn()







import board
import keypad
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from time import monotonic as check
from layout import layout_matrix

pins = [getattr(board, f'D{i}') for i in range(11)] #list of pins D[i]
key_matrix = keypad.KeyMatrix(
    row_pins = pins[0:5],
    column_pins = pins[5:11],
    interval=0.05, #debounce time
    columns_to_anodes=False
)

hid_kbd = Keyboard(usb_hid.devices)
hid_layout = KeyboardLayoutUS(hid_kbd)
event = keypad.Event()
layer = 0
layer_set = 0
num = 0

def tick(delay):
    return check() + delay

while True:
    if key_matrix.events.get_into(event):
        row, col = key_matrix.key_number_to_row_column(event.key_number)
        key = layout_matrix[row][col]
        obj = key[layer::-1][0]
        
        if event.pressed:
            try:
                if 'mod' in obj:
                    mark = tick(0.05)
                    layer_set += int(obj[3])
                elif obj.isdigit():
                    num += int(obj)
                    print(num)
                else:
                    hid_layout.write(obj)
                    print(obj+' sent')
            except TypeError:
                hid_kbd.press(obj)
                print(f'{obj} pressed')
        else:
                if isinstance(obj, int):
                    hid_kbd.release(obj)
                    print(f'{obj} released')
                elif obj.isdigit():
                    if num > 0:
                        hid_layout.write(str(num))
                        num = 0
                        print(num)
                elif 'mod' in obj:
                    layer_set -= min(layer_set, int(obj[3]))
                    hid_kbd.release_all()
                    print('all released')
        
        print(f'key {event.key_number} {event.pressed} layer {layer} obj {obj}')
    elif layer_set != layer:
        if check() > mark:
            layer = layer_set
            print(f'layer {layer}')

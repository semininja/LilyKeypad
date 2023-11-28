import board
import keypad
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode as KC
from time import monotonic as check

pins = [getattr(board, f'D{i}') for i in range(11)] #list of pins D[i]
key_matrix = keypad.KeyMatrix(
    row_pins = pins[0:5],
    column_pins = pins[5:11],
    interval=0.005, #debounce time
    columns_to_anodes=False
)

layout_matrix = [ #grouped by row, column, layer
    [['a', '*'], ['b'], ['c'], ['d'], ['is', '\\trill'], ["'"]],
    [['r', 'R', 's'], ['e'], ['f', '\\relative f'], ['g'], ['es', '\\turn'], [',']],
    [['1', '1', '6',], ['2', '2', '7', '\\tuplet 3/2'], ['4', '3', '8', '\partial'], ['8', '4', '9'], ['16', '5', '0'], ['.', ' ~', '\\fermata']],
    [['->', '-^', '--'], ['-.', '-+', '\\open'], ['\\p', '\\pp', '\\mp'],
        ['\\f', '\\mf', '\\ff'], ['\\!', '\\>', '\\<', '\\n'],
        [' |\n', '\\bar "||"', '\\bar "|."']],
    [[' ', '\\', '/'], ['(', '<', '['], ['mod1', 'mod1', KC.LEFT_ARROW, 'mod1'], ['mod2', KC.RIGHT_ARROW, 'mod2', 'mod2'],
        [')', ']', '>'], [KC.ENTER, KC.BACKSPACE, KC.TAB]]]

hid_kbd = Keyboard(usb_hid.devices)
hid_layout = KeyboardLayoutUS(hid_kbd)
event = keypad.Event()
layer = 0
layer_set = 0

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
                else:
                    hid_layout.write(obj)
                    print(obj+' sent')
            except TypeError:
                hid_kbd.press(obj)
                print(f'{obj} pressed')
        else:
            try:
                hid_kbd.release(obj)
                print(f'{obj} released')
            except TypeError:
                if 'mod' in obj:
                    layer_set -= min(layer_set, int(obj[3]))
                    hid_kbd.release_all()
                    print('all released')
        
        print(f'key {event.key_number} {event.pressed} layer {layer}')
    elif layer_set != layer:
        if check() > mark:
            layer = layer_set
            print(f'layer {layer}')

from adafruit_hid.keycode import Keycode as KC

layout_matrix = [ #grouped by row, column, layer
    [['a'], ['b'], ['c'], ['d'], ['is', '\\trill'], ["'"]],
    [['r', 'R', 's'], ['e'], ['f'], ['g'], ['es', '\\turn'], [',']],
    [['1', "*"], ['2','\\relative f'], ['4', '\\tuplet'], ['8'], ['16'], ['.', ' ~', '\\fermata']],
    [['->', '-^', '--'], ['-.', '-+', '\\open'], ['\\p', '\\pp', '\\mp'],
        ['\\f', '\\mf', '\\ff'], ['\\!', '\\>', '\\<', '\\n'],
        [' |\n', '\\bar "||"', '\\bar "|."']],
    [[' ', '\\', '/'], ['(', '<', '['], ['mod1', 'mod1', KC.LEFT_ARROW, 'mod1'], ['mod2', KC.RIGHT_ARROW, 'mod2', 'mod2'],
        [')', ']', '>'], [KC.ENTER, KC.BACKSPACE, KC.TAB]]]

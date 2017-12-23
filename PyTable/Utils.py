import os, itertools, math

# thanks google: http://christophe-simonis-at-tiny.blogspot.be/2008/08/python-reverse-enumerate.html
def reverse_enumerate(it): 
    return itertools.izip(reversed(xrange(len(it))), reversed(it))


def halign(string, width, align = "left", pad_char = " "):
    def line_halign_left(string, width):
        return string + pad_char * max(width-len(string), 0)

    def line_halign_center(string, width):
        total_added_space = max(width-len(string), 0)
        left_space = int(math.floor(total_added_space/2.0))
        right_space = int(math.ceil(total_added_space/2.0))
        return pad_char * left_space + string + pad_char * right_space

    def line_halign_right(string, width):
        return pad_char * max(width-len(string), 0) + string
    
    
    if align == "left":
        _align = line_halign_left
    elif align == "center":
        _align = line_halign_center
    elif align == "right":
        _align = line_halign_right
    else:
        raise ValueError("Invalid alignment type \"{}\". Valid types are \"left\", \"center\" and \"right\".")

    lines = string.split(os.linesep)
    string = ""
    for line_index, line in enumerate(lines):
        string += _align(line, width)
        if line_index < len(lines) - 1:
            string += os.linesep

    return string


def valign(string, height, align = "top"):
    def lines_valign_top(lines, height):
        for i in range(max(height-len(lines), 0)):
            lines.append("")

    def lines_valign_center(lines, height):
        total_added_lines = max(height-len(lines), 0)
        top_space = int(math.floor(total_added_lines/2.0))
        bottom_space = int(math.ceil(total_added_lines/2.0))
        for i in range(top_space):
            lines.insert(0, "")
        for i in range(bottom_space):
            lines.append("")

    def lines_valign_bottom(lines, height):
        for i in range(max(height-len(lines), 0)):
            lines.insert(0, "")


    if align == "top":
        _align = lines_valign_top
    elif align == "center":
        _align = lines_valign_center
    elif align == "bottom":
        _align = lines_valign_bottom
    else:
        raise ValueError("Invalid alignment type \"{}\". Valid types are \"top\", \"center\" and \"bottom\".")

    lines = string.split(os.linesep)
    _align(lines, height)
    return os.linesep.join(lines)


def string_dimensions(string, htrim=False, vtrim=True, vtrim_whitespace = True):
    #todo: trim left to minimum position for htrim
    lines = string.split(os.linesep)

    def trim_line(line, trim):
        return line.expandtabs().rstrip() if trim else line.expandtabs()

    def empty_line(line):
        return len(trim_line(line, vtrim_whitespace)) == 0

    w = 0
    for line in lines:
        w = max(w, len(trim_line(line, htrim)))
    
    h = 0

    begin_line_index = 0
    end_line_index = len(lines)
    if vtrim:
        for line_index, line in enumerate(lines):
            if not empty_line(line):
                begin_line_index = line_index
                break

        for line_index, line in reverse_enumerate(lines):
            if not empty_line(line):
                end_line_index = line_index
                break

        h = max(end_line_index - begin_line_index + 1, 0)
    
    else:
        h = len(lines)

    return (w, h, os.linesep.join([trim_line(line, htrim) for line in lines[begin_line_index : end_line_index+1]]))


def string_squarify(string, pad_char = " "):
    w, h, l = string_dimensions(string, htrim=False, vtrim=False, vtrim_whitespace = False)
    return halign(valign(string, h), w, pad_char = pad_char)


def string_padding(string, hpad = 1, vpad = 0, pad_char = " "):
    w, h, l = string_dimensions(string, htrim=False, vtrim=False, vtrim_whitespace = False)
    return halign(valign(string, h + 2*vpad, align="center"), w + 2*hpad, align="center")


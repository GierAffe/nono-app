import tkinter as tk
from tkinter import font
import nanogramm1 as ng

root = tk.Tk()

# Assemble UI
myHeader = tk.Label(root, text="TKinter Version " + str(tk.TkVersion))
myPuzzle = tk.Canvas(root, height=800, width=800, background='black')

# Positioning widgets
myHeader.grid(row=0, column=0)
myPuzzle.grid(row=1, column=0)

# Puzzle settings
ng_cols = ng.cols       # columns and rows of the nonogramm
ng_rows = ng.rows
square_size = 16
font_size = -14  # negative number means pixels is used as unit
spacer_width = 2  # space between two numbers in a row
line_width = 1
line_width_bold = 2
rec_empty_color = '#ffffff'         # standard = white
rec_fill_color = '#404040'          # standard = dark grey
rec_dot_color = '#404040'           # standard = dark grey
sel_color_fill = '#404040'          # colors used for selection, when a selection is made on the grid
sel_color_dot = '#eeeeee'           # light gray
sel_color_clear = '#eeeeee'         # light gray
# sel_bd_width = 3                    # selection highlight width
# sel_dash = (3, 1)                   # selection dash sequence

# will get set during gridDraw function
title_row_width = 0
title_col_width = 0

# playing field
grid = None                 # two dimensional list of chars. E = empty, F = filled, D = dotted
num_cols = 0                # number of columns
num_rows = 0                # number of rows

# Variables for grid selection and highlighting functionality, like when the user selects multiple squares at once
# sel_coordinates = False     # grid square coordinates as tuple (x0, y0, x1, y1)
sel_origin = 0              # column and row of the clicked grid square as tuple of strings
sel_button = 0              # which button has been used for the selection, 0 if no selection is active

# Populate canvas widget
myPuzzleFont = font.Font(family='Arial', size=font_size, weight='bold')
myPuzzleFontNarrow = font.Font(family='Arial Narrow', size=font_size, weight='bold')

# measure font height and width
number_width = myPuzzleFontNarrow.measure('00')
number_height = myPuzzleFont.metrics('linespace')


def calcTitleRowWith(rows):
    """ Returns the length (in pixel) of the longest title row.
        At the moment, puzzles are fixed on two digit numbers """
    # TODO make puzzle adjust dynamically to one or more digit puzzles

    biggest_tuple, biggest_tuple_id = 0, 0
    for row_id in range(len(rows)):  # iterate through all the row tuples, find the row with the most numbers
        if len(rows[row_id]) > biggest_tuple: biggest_tuple, biggest_tuple_id = len(rows[row_id]), row_id

    # calculate and return width of one the biggest tuple found
    return len(rows[biggest_tuple_id]) * number_width + (len(rows[biggest_tuple_id]) - 1) * spacer_width


def calcTitleColWith(cols):
    """ returns the length (in pixel) of the longest title column"""
    max_numbers = 1
    for col in cols:
        if len(col) > max_numbers: max_numbers = len(col)

    return myPuzzleFont.metrics('linespace') * max_numbers


def calcSquarePosition(col_or_row):
    """ Calculates the relative position of a square to the offset point
        col_or_row = number of column or row for which the coordinates should be calculated
        Returns a float variable: x_rel_pos or y_rel_pos """
    return (col_or_row - 1) * (square_size + line_width) + int((col_or_row - 1) / 5) * (line_width_bold - line_width)


def drawGrid():
    """ Draws a nanogramm grid on the canvas """

    # count columns and rows
    global num_cols, num_rows
    num_cols, num_rows = len(ng_cols), len(ng_rows)

    # create 'virtual' playing field
    global grid
    grid = [['E' for x in range(num_rows)] for y in range(num_cols)]    # first dimension = cols, second = rows

    # measure title row and column width
    global title_col_width, title_row_width
    title_row_width = calcTitleRowWith(ng_rows)
    title_col_width = calcTitleColWith(ng_cols)

    # Create upper left box
    myPuzzle.create_rectangle(0, 0, title_row_width, title_col_width, fill='white')

    # calculate offset for the squares grid
    x_offset, y_offset = title_row_width + line_width_bold, title_col_width + line_width_bold

    # Draw title rows and columns
    # create rectangles as background, then put the numbers on top of them
    for col in range(num_cols):
        # rectangles
        x_coord = calcSquarePosition(col + 1)
        myPuzzle.create_rectangle(x_offset + x_coord, 0, x_offset + x_coord + square_size, title_col_width,
                                  fill='white', width=0)
        # column number
        inv_col = ng_cols[col][::-1]  # inverse tuple
        for number in range(len(ng_cols[col])):
            # calculate y axis offset for ever single number
            y_offset_number = title_col_width - number * number_height

            if inv_col[number] < 10:             # account for narrow font & offset
                my_font, num_off = myPuzzleFont, 0
            else:
                my_font, num_off = myPuzzleFontNarrow, 1

            # create text items for column numbers
            myPuzzle.create_text(x_offset + x_coord + square_size / 2 - num_off, y_offset_number, text=inv_col[number],
                                 font=my_font, anchor=tk.S,
                                 tags=('colNumber', 'COL.' + str(col) + '.' + str(len(inv_col) - number -1)))

    # bind event handler to left click events of all numbers in the title columns
    myPuzzle.tag_bind('colNumber', '<Button-1>', handleColNumberClick)

    # same goes for the rows
    for row in range(num_rows):
        # rectangles
        y_coord = calcSquarePosition(row + 1)
        myPuzzle.create_rectangle(0, y_offset + y_coord, title_row_width, y_offset + y_coord + square_size,
                                  fill='white', width=0)
        # row numbers
        inv_row = ng_rows[row][::-1]  # inverse tuple, has to be done... weired...
        for number in range(len(ng_rows[row])):  # iterate through the numbers of tuple 'row'
            # calculate x axis offset for every single number
            x_offset_number = title_row_width - number * (number_width + spacer_width) - number_width / 2

            if inv_row[number] < 10:              # account for narrow font & offset
                my_font, num_off = myPuzzleFont, 0
            else:
                my_font, num_off = myPuzzleFontNarrow, 1

            # create text items for row numbers
            myPuzzle.create_text(x_offset_number - num_off, y_offset + y_coord - num_off, text=inv_row[number],
                                 font=my_font, anchor=tk.N,
                                 tags=('rowNumber', 'ROW.' + str(row) + '.' + str(len(inv_row) - number -1)))

    # bind event handler to left click events of all numbers in the title rows
    myPuzzle.tag_bind('rowNumber', '<Button-1>', handRowNumberClick)

    # Create the squares
    for col in range(num_cols):  # Iterate through all rows, then columns
        # calculate the relative position for this column
        x_coord = calcSquarePosition(col + 1)
        for row in range(num_rows):
            # calculate the relative square position
            y_coord = calcSquarePosition(row + 1)
            # draw a square at that position, including offsets
            myPuzzle.create_rectangle(x_coord + x_offset, y_coord + y_offset,
                                      x_coord + square_size + x_offset, y_coord + square_size + y_offset,
                                      fill=rec_empty_color, width=0,
                                      tags=('gridSquare', 'GRID.' + str(col) + '.' + str(row)))     # 'GRID.x.y'

    # bind event handler to all 'button down' and 'button up' events of all grid squares
    myPuzzle.tag_bind('gridSquare', '<Button>', handleRecButtonDown)
    myPuzzle.tag_bind('gridSquare', '<ButtonRelease>', handleRecButtonUp)

    # Resize Canvas to final size
    canvas_x_pos = calcSquarePosition(len(ng_cols)) + x_offset + square_size
    canvas_y_pos = calcSquarePosition(len(ng_rows)) + y_offset + square_size
    myPuzzle.configure(height=canvas_y_pos, width=canvas_x_pos)


def getTagCoordinates(tags_string, key):
    """ Returns the Coordinate-Tag (key.x.y.z...)  as a whole [0] and split by '.' [1-x] as list.
        key needs to be in the format 'KEY.' """
    tags = tags_string.split(' ')
    for tag in tags:
        if tag[0:len(key)] == key:
            return [tag] + tag.split('.')


def handleColNumberClick(event):
    """ handle right click on column number, cross out that number """

    # collect information about the clicked text item
    text_item_id = event.widget.find_withtag('current')[0]
    coords_tag = getTagCoordinates(myPuzzle.itemcget(text_item_id, 'tags'), 'COL.')     # get the 'COL.x.y' tag

    # check if there was already a strike out line. this can happen, if the user slightly misses the strike out line
    # and clicks on the number again. The strike out line has the same coordinate tag as the number, but adds '.SOL'
    # to the end. If found, delete the strike out line and return function
    if myPuzzle.find_withtag(coords_tag[0] + '.SOL'):
        myPuzzle.delete(coords_tag[0] + '.SOL')
        return

    # create line item to cross out number
    x_offset = title_row_width + line_width_bold + calcSquarePosition(int(coords_tag[2]) + 1)
    y_offset = title_col_width - (len(ng_cols[int(coords_tag[2])]) - int(coords_tag[3])) * number_height
    strike_out_line = myPuzzle.create_line(x_offset, y_offset, x_offset + square_size, y_offset + square_size,
                                           width=2, capstyle=tk.ROUND,
                                           tags=('StrikeOutLine', coords_tag[0] + '.SOL'))    # SOL = strike out line

    # bind event handler to right click event on strike out line
    myPuzzle.tag_bind(strike_out_line, '<Button-1>', handleStrikeOutLineClick)


def handRowNumberClick(event):
    """ handle right click on row number, cross out that number """

    # collect information about the clicked text item
    text_item_id = event.widget.find_withtag('current')[0]
    coords_tag = getTagCoordinates(myPuzzle.itemcget(text_item_id, 'tags'), 'ROW.')     # get the 'ROW.' tag

    # check if there was already a strike out line. this can happen, if the user slightly misses the strike out line
    # and clicks on the number again. The strike out line has the same coordinate tag as the number, but adds '.SOL'
    # to the end. If found, delete the strike out line and exit
    if myPuzzle.find_withtag(coords_tag[0] + '.SOL'):
        myPuzzle.delete(coords_tag[0] + '.SOL')
        return

    # create line item to cross out number
    x_offset = title_row_width - (len(ng_rows[int(coords_tag[2])]) - int(coords_tag[3])) * (number_width + spacer_width)
    y_offset = title_col_width + line_width_bold + calcSquarePosition(int(coords_tag[2]) + 1)
    strike_out_line = myPuzzle.create_line(x_offset, y_offset, x_offset + square_size, y_offset + square_size,
                                           width=2, capstyle=tk.ROUND,
                                           tags=('StrikeOutLine', coords_tag[0] + '.SOL'))  # SOL = strike out line

    # bind event handler to right click event on strike out line
    myPuzzle.tag_bind(strike_out_line, '<Button-1>', handleStrikeOutLineClick)


def handleStrikeOutLineClick(event):
    """ Handle right click on strike out line, delete that line item """
    # get the item id of the line item that got clicked, then delete that strike out line
    myPuzzle.delete(event.widget.find_withtag('current')[0])


def handleRecButtonDown(event):
    """ Handle 'button down' events on rectangle items on the grid.
        Check for already active selections, since the user could click and hold more then one button at once.
        If not, start a new selection by remembering which square was clicked by which button for
        later processing. A new rectangle item is created for highlighting the selection """

    # buttons 1 (left = fill), 2 (middle = clear) or 3 (right = dot), else abort
    if event.num not in (1, 2, 3):
        return

    global sel_origin, sel_button

    # no active user selection going on, register a new one
    if not sel_button:
        item_id = event.widget.find_withtag('current')[0]        # get item id of clicked square
        sel_button = event.num                                   # save what button was used & active selection going on

        # get and save column and row number
        coords_tag = getTagCoordinates(myPuzzle.itemcget(item_id, 'tags'), 'GRID.')
        sel_origin = (coords_tag[2], coords_tag[3])

        # # use different colors for mouse button 1 (fill) and 3 (dot)
        # if event.num == 1: highlight_color = sel_color_fill
        # elif event.num == 2: highlight_color = sel_color_clear
        # elif event.num == 3: highlight_color = sel_color_dot

        # create rectangle item for highlighting the users selection
        # myPuzzle.create_rectangle(sel_coordinates[0], sel_coordinates[1],
        #                           sel_coordinates[2], sel_coordinates[3],
        #                           width=sel_bd_width, outline=highlight_color, dash=sel_dash)

        # TODO graphical representation of the user selection


def gridOperation(col0, row0, col1, row1, action):
    """ Handles user inputs in the playing field.
        Fills, clears or dots all fields in the selection and saves the information into the virtual playing field
        Fill: action = 1
        Clear: action = 2
        Dot: action = 3 """
    global grid

    # switch col- and row-parameters if it was a 'upwards' selection, so we can use range()
    if col0 > col1:
        col0, col1 = col1, col0
    if row0 > row1:
        row0, row1 = row1, row0

    for x in range(col0, col1 + 1):             # + 1 to make the selection include all squares
        for y in range(row0, row1 + 1):

            # fill or empty actions can be processed the same way
            if action == 1 or action == 2:
                global rec_fill_color, rec_empty_color

                color = rec_fill_color if action == 1 else rec_empty_color          # choose color
                # TODO check if field had a dot before -> delete item
                myPuzzle.itemconfigure('GRID.{0}.{1}'.format(x, y), fill=color)     # fill grid square
                grid[x - 1][y - 1] = 'F' if action == 1 else 'E'

            # dotting action, fill grid square like it was empty and create a dot on top of it
            else:
                pass


def handleRecButtonUp(event):
    """ Handle 'button up' events on rectangle items on the grid. """
    global sel_origin, sel_button

    # only handle message, if a selection has been started before and the correct button has been released
    if event.num != sel_button:
        return

    # get column and row number for the square, over which the button was released
    item_id = event.widget.find_closest(event.x, event.y)[0]
    coords_tag = getTagCoordinates(myPuzzle.itemcget(item_id, 'tags'), 'GRID.')

    # perform selected changes: color grid square, create dot, update virtual playing field
    gridOperation(int(sel_origin[0]), int(sel_origin[1]), int(coords_tag[2]), int(coords_tag[3]), event.num)

    # reset selection
    sel_origin, sel_button = False, 0


drawGrid()


# TODO dragging the mouse to mark blocks
# TODO print puzzle as postscript
# TODO reset functionality

root.mainloop()

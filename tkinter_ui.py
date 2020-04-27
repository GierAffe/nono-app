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
square_size = 16
font_size = -14  # negative number means pixels is used as unit
spacer_width = 2  # space between two numbers in a row
line_width, line_width_bold = 1, 2

# Populate canvas widget
myPuzzleFont = font.Font(family='Arial', size=font_size, weight='bold')
myPuzzleFontNarrow = font.Font(family='Arial Narrow', size=font_size, weight='bold')
number_width = myPuzzleFontNarrow.measure('00')
number_height = myPuzzleFont.metrics('linespace')


def getTextItemCords(item_id):
    """ returns a list with x0, y0, x1, y1 coordinates for a canvas text item """
    x0, y0 = myPuzzle.coords(item_id)
    x1 = x0 + myPuzzleFont.measure(myPuzzle.itemcget(item_id, 'text'))  # x1 depends on the with of the given text
    y1 = y0 + myPuzzleFont.metrics('linespace')  # linespace gives the height for any given font
    return [x0, y0, x1, y1]


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
    """ Calculates the relative position of a square
        col_or_row = number of column or row for which the coordinates should be calculated
        Returns a float variable: x_rel_pos or y_rel_pos """
    return (col_or_row - 1) * (square_size + line_width) + int((col_or_row - 1) / 5) * (line_width_bold - line_width)


def drawGrid(ng_cols, ng_rows):
    """ Draws a nanogramm grid on the canvas """

    # count columns and rows
    num_cols, num_rows = len(ng_cols), len(ng_rows)

    # Create upper left box
    title_row_width = calcTitleRowWith(ng_rows)
    title_col_width = calcTitleColWith(ng_cols)
    myPuzzle.create_rectangle(0, 0, title_row_width, title_col_width, fill='white')

    # calculate offset for the squares grid
    x_offset, y_offset = title_row_width + line_width_bold, title_col_width + line_width_bold

    # TODO optimize grid calculations. Calculate then once, save and reuse em..

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



    # bind event handler to left click events of all
    myPuzzle.tag_bind('colNumber', '<Button-1>', handleRowNumberClick)

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
                                 font=my_font, anchor=tk.N)

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
                                      fill='white', width=0)

    # Resize Canvas to final size
    canvas_x_pos = calcSquarePosition(len(ng_cols)) + x_offset + square_size
    canvas_y_pos = calcSquarePosition(len(ng_rows)) + y_offset + square_size
    myPuzzle.configure(height=canvas_y_pos, width=canvas_x_pos)


def handleRowNumberClick(event):
    text_item_id = event.widget.find_withtag('current')[0]
    print(myPuzzle.itemcget(text_item_id, 'tags'))


drawGrid(ng.cols, ng.rows)

# TODO cross out numbers
# TODO mouse click handling on squares
# TODO dragging the mouse to mark blocks
# TODO print puzzle as postscript

root.mainloop()

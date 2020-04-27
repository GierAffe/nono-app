import nanogramm1 as ng


def get_grid_row(param):
    """ Returns list of grid row <param> """
    if 0 < param <= ng.num_rows:  # check for valid param value
        return ng.grid[param - 1]
    else:
        raise ValueError('Called get_grid_row(param) with invalid param = ' + str(param) + '! '
                          'Expected integer between 1 and ' + str(ng.num_rows))


def get_grid_col(param):
    """ returns list of grid column <param> """
    if 0 < param <= ng.num_rows:  # check for valid param value

        for x in range(ng.num_rows):
            for y in range(ng.num_cols):
                # TODO: copy values in new list and return new list
                pass

    else:
        raise ValueError('Called get_grid_row(param) with invalid param = ' + str(param) + '! '
                         'Expected integer between 1 and ' + str(ng.num_rows))


def get_grid_row_copy():
    pass


def get_grid_col_copy():
    pass


print("Erste Zeile: " + str(get_grid_row('a')))

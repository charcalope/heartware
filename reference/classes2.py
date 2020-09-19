def fetch_conductance(row, col):
    return 0

# check if all zeroes
def basically_zero(change_matrix):
    return False

class Board:
    def __init__(self):
        self.matrix = []
        # not sure if tuples are a thing in C++, this may need to be handled entirely differently
        self.placements = []  # list of (product, change_matrix) placements
        self.mode = "shopping"

        for i in range(15):
            row = []
            for j in range(15):
                row.append(fetch_conductance(i, j))
            self.matrix.append(row)

    # updates the board state representation with latest data
    # returns the change in board state as a 2d array
    # if there is any change, else returns None
    def changed(self):
        change_matrix = []
        for i in range(15):
            row = []
            for j in range(15):
                before = self.matrix[i][j]
                after = fetch_conductance(i, j)
                change = after - before  # get change
                row.append(change)  # update representation of change
                self.matrix[i][j] = after  # update board state
            change_matrix.append(row)

        # C++ deallocate
        if basically_zero(change_matrix):
            return None
        else:
            return change_matrix

    # high level refresh of board state and processing
    # processing should change depending on mode
    def refresh(self):
        # ALL MODES:
        # handle removals, including simultaneous removals

        # SHOPPING MODE:
        # handle place backs:
        #   trigger request for active user
        #   ask active user which product they put back
        #   display user's cart in chronological order
        if self.mode == "shopping":
            ...
        # STOCKING MODE:
        # handle placements:
        #   trigger popup on user interface
        #   get product ID
        else:
            ...



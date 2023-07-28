from collections import OrderedDict 

board = [[0,0,0,1,1,0,0],
         [0,0,1,1,1,0,0],
         [1,1,1,1,0,0,1],
         [0,1,0,0,0,1,1],
         [0,0,1,1,1,1,1],
         [0,1,1,1,0,0,0],
         [1,1,1,1,0,0,0]]


"""This piece of code finds the positions for a 0 valued-group and its non 0 neighbours, aka a sweep or clear"""

def sweep(initial_position, board):          
    def get_cardinals(position):
        row, column = position
        cardinals =  (
                (row - 1 , column - 1), (row - 1 , column),(row - 1 , column + 1),   # TL  U  TR
                (row     , column - 1),                    (row     , column + 1),   # L   P   R
                (row + 1 , column - 1), (row + 1 , column),(row + 1 , column + 1))   # BL  B  BR
        n = len(board)

        #Filtering out out-of-bounds indexes
        filter = []
        for row, column in cardinals:
            if (0 <= row < n) and (0 <= column < n):
                filter.append((row,column))
        return filter

    #The initial position (the clicked tile)

    group = OrderedDict()
    group[initial_position] = None
    i = 0

    #Find 0's within that given group
    while i < len(group):
        for row, column in get_cardinals(list(group)[i]):
            if board[row][column] == 0:
                group[(row, column)] = None
        i += 1


    #Find all neigbours of 0
    neighbours = {}
    for zero_position in group.keys():
        for row, column in get_cardinals(zero_position):
            if board[row][column] != 0:
                neighbours[(row, column)] = None

    # the 0-group has been identified and its non 0 closest neighbours.
    sweep = (group | neighbours).keys()

    return sweep



if __name__ == "__main__":
    board = [
        [0,0,0,1,1,0,0],
        [0,0,1,1,1,0,0],
        [1,1,1,1,0,0,1],
        [0,1,0,0,0,1,1],
        [0,0,1,1,1,1,1],
        [0,1,1,1,0,0,0],
        [1,1,1,1,0,0,0]]
    row, column = initial = (5,5)

    if board[row][column] == 0:
        positions = sweep(initial, board)

    #once the positions have been found we want to make the tiles as visible
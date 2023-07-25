from collections import OrderedDict 

board = [[0,0,0,1,1,0,0],
         [0,0,1,1,1,0,0],
         [1,1,1,1,0,0,1],
         [0,1,0,0,0,1,1],
         [0,0,1,1,1,1,1],
         [0,1,1,1,0,0,0],
         [1,1,1,1,0,0,0]]


            
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

initial = (5,5)
group = OrderedDict()
group[initial] = None
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

sweep = (group | neighbours).keys()

#following this a sweep or cascade has been performed.
#I.e. the 0-group has been identified and its non 0 closest neighbours.
print("done")


from collections import OrderedDict 
from .tile import Tile

import random
import game

class Board():
    
    def __init__(self, interface, rows, columns, mines):
        self.interface  = interface
        self.difficulty = interface.difficulty
        self.screen     = interface.screen
        self.rows = rows
        self.columns = columns
        self.mines = mines
    
        self.board = [[None for _ in range(columns)] for _ in range(rows)]

        cell_width = (game.SCREEN_WIDTH * 0.75) // self.columns
        cell_height =  (game.SCREEN_HEIGHT * 0.75) // self.rows

        cell_increase = 0
        if self.difficulty == "Hard":
            cell_increase = 5

        self.cell_width = self.cell_height = min(cell_width, cell_height) + cell_increase
        self.cell_size = (self.cell_width, self.cell_height)


        self.generate_tiles()
        self.generate_bombs()
        self.set_bomb_number_for_each_tile()
        
        
    def __setitem__(self, position, value):
        if len(position) != 2:
            raise ValueError("Key must be a tuple (row, col)")

        row, column = position
        if  not (0 <= row < self.rows) or not (0 <= column < self.columns):
            print(row, column)
            raise IndexError("Index out of range")

        self.board[row][column] = value

    def __getitem__(self, position):
 
        if len(position) != 2:
            raise ValueError("Key must be a tuple (row, col)")

        row, column = position
        if  not (0 <= row < self.rows) or not (0 <= column < self.columns):
            raise IndexError("Index out of range")

        return self.board[row][column]

    def generate_tiles(self):
        
        for row in range(self.rows):
            for column in range(self.columns):
                x =  (column * self.cell_width) 
                x += (game.SCREEN_WIDTH - (self.cell_height * self.columns)) / 2
                
                y =  (row * self.cell_height)  
                y += (game.SCREEN_HEIGHT - (self.cell_height * self.rows)) / 2
                
                tile = Tile(self, self.screen, row, column, x, y, self.cell_size)      
                self[row, column] = tile 

    def generate_bombs(self):

        for _ in range(self.mines):
            position = (random.randint(0, self.rows - 1), random.randint(0, self.columns - 1))
            self[position].is_bomb = True


    
    def draw(self):
        for row in self.board:
            for tile in row:
                tile.draw()

    def handle_event(self, event):
        for row in self.board:
            for tile in row:
                tile.handle_event(event)

    def set_bomb_number_for_each_tile(self):
        for row in range(self.rows):
            for column in range(self.columns):
                
                if not self[row, column].is_bomb:
                    neighbours = self.get_neighbours((row, column))

                    count = 0
                    for position in neighbours:
                        if self[position].is_bomb: 
                            count += 1
                    self[row, column].bombs_nearby = count


    
    def get_neighbours(self, position):
        
        row, column = position
        cardinals =  (
                (row - 1 , column - 1), (row - 1 , column),(row - 1 , column + 1),   # TL  U  TR
                (row     , column - 1),                    (row     , column + 1),   # L   P   R
                (row + 1 , column - 1), (row + 1 , column),(row + 1 , column + 1))   # BL  B  BR

        #Filtering out out-of-bounds indexes
        filter = []
        for row, column in cardinals:
            if (0 <= row < self.rows) and (0 <= column < self.columns):
                filter.append((row, column))
        return filter

    def get_zero_group_neighbours(self, initial_position):

        #The initial position (the clicked tile)

        group = OrderedDict()
        group[initial_position] = None
        i = 0


        #Given an initial 0-value position we find every other occurence of a zero until there is no more
        while i < len(group):
            for position in self.get_neighbours(list(group)[i]):
                if self[position].bombs_nearby == 0:
                    group[(position)] = None
            i += 1
  

        #Find all neigbours of the 0 group found above
        neighbours = {}
        for zero_position in group.keys():
            for position in self.get_neighbours(zero_position):
                if self[position].bombs_nearby != 0:
                    neighbours[(position)] = None


        # the 0-group has been identified and its non 0 closest neighbours.
        sweep_group = (group | neighbours).keys()

        return sweep_group

    def sweep(self, position):
        self[position].value = Tile.CLICKED_TILE
                       
        group = self.get_zero_group_neighbours(position)
        for position in group:
            tile = self[position]
            tile.visible = True
            tile.value = Tile.CLICKED_TILE

    def show_bombs(self):
        for row in self.board:
            for tile in row:
                if tile.is_bomb and tile.value == Tile.FLAGGED_TILE:
                    tile.value = Tile.CORRECTLY_MARKED_BOMB
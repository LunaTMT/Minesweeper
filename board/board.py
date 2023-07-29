import pygame
import random
import game
import time

import assets.colours as colours

from collections import OrderedDict 
from .tile import Tile
from buttons.reset_button import ResetButton


class Board():
    

    def __init__(self, interface, rows, columns, bombs):
        self.interface  = interface
        self.difficulty = interface.difficulty
        self.screen     = interface.screen
        self.rows = rows
        self.columns = columns
        self.default_bombs = self.bombs = bombs

        #Initialising empty 2d list, size row X column
        self.board = [[None for _ in range(columns)] for _ in range(rows)]

        cell_width = (game.SCREEN_WIDTH * 0.75) // self.columns
        cell_height =  (game.SCREEN_HEIGHT * 0.75) // self.rows

        #Subtle adjustments based on difficulty to make the board look a little nicer and clearer
        cell_increase = 0
        if self.difficulty == "Hard":
            cell_increase = 5
        elif self.difficulty == "Medium":
            cell_increase = 2

        self.cell_width = self.cell_height = min(cell_width, cell_height) + cell_increase #set both the same so cell is perfect square
        self.cell_size = (self.cell_width, self.cell_height) 

        #board center positions on screen
        self.x_center_offset = (game.SCREEN_WIDTH - (self.cell_height * self.columns)) / 2
        self.y_center_offset = ((game.SCREEN_HEIGHT - (self.cell_height * self.rows)) / 2) + 30

        #The top of the board
        #------------------------------------
        self.reset_button = ResetButton(self, self.screen, y = self.y_center_offset - 55 , width=50, height=50)
        self.reset_button.center_x()

        bomb_count_x = self.x_center_offset 
        bomb_count_y = self.y_center_offset - 55
        self.bomb_count_rect = pygame.Rect(bomb_count_x, bomb_count_y, 110, 50)   
        
        timer_x = int(game.SCREEN_WIDTH - self.x_center_offset - 110)
        timer_y = self.y_center_offset - 55
        self.timer_rect = pygame.Rect(timer_x, timer_y, 110, 50)       
        self.timer_value = 0
        #------------------------------------

        #initialising board with necesarry game components
        self.generate()

        #Once components have been generated we then want to determine bomb proximity for each tile
        self.set_bomb_number_for_each_tile()


    def __setitem__(self, position, value):
        """
        This dunder allows the user to access the board attribute directly using the board object
        The function:
            - checks the given position is a tuple (row and column)
            - within the bounds of the board
        And lastly  sets the position on the board to the given 'value'
        """
        if len(position) != 2:
            raise ValueError("Key must be a tuple (row, col)")

        row, column = position
        if  not (0 <= row < self.rows) or not (0 <= column < self.columns):
            raise IndexError("Index out of range")

        self.board[row][column] = value

    def __getitem__(self, position):
        """
        This dunder allows the user to access the board attribute directly using the board object
        The function:
            - checks the given position is a tuple (row and column)
            - within the bounds of the board
        And lastly gets the value located on the board for the 'given position'
        """
        if len(position) != 2:
            raise ValueError("Key must be a tuple (row, col)")

        row, column = position
        if  not (0 <= row < self.rows) or not (0 <= column < self.columns):
            raise IndexError("Index out of range")

        return self.board[row][column]

    def generate_tiles(self):
        """
        This function generates the tiles in the correct positions on board
        """
        for row in range(self.rows):
            for column in range(self.columns):
                x =  (column * self.cell_width) 
                x += self.x_center_offset
                
                y =  (row * self.cell_height)  
                y += self.y_center_offset
                
                tile = Tile(self, self.screen, row, column, x, y, self.cell_size)      
                self[row, column] = tile 

    def generate_bombs(self):
        """
        This function will generate x random bombs in completely random locations
        x depends upon the difficulty 

        """
        self.bomb_locations = []
        for _ in range(self.bombs):
            position = (random.randint(0, self.rows - 1), random.randint(0, self.columns - 1))
            self.bomb_locations += [position]
            self[position].is_bomb = True
        
    def generate(self):
            """
            This function generates the essential parts of the board - the tiles and the bombs

            """
            self.generate_tiles()
            self.generate_bombs()

    def set_bomb_number_for_each_tile(self):
        """
        Given each tile (except bombs) on the board this function will determine how many bombs are in its proximity
        The range of proximity is the cardinal points
        Each tile has an attribute denoting the bomb proximity value
        """
        for row in self.board:
            for tile in row:
                if not tile.is_bomb:
                    count = 0
                    for position in self.get_neighbours((tile.row, tile.column)):
                        if self[position].is_bomb: count += 1
                    tile.bombs_nearby = count

    
    def draw(self):
        """
        This function draws the entire board, it consists of:
            - drawing each tile
            - drawing the reset button at the top center
            - drawing the remaining bombs left
            - drawing the timer the game has been played for,
        respectively.
        """
        for row in self.board:
            for tile in row:
                tile.draw()

        self.reset_button.draw()
        self._draw_remaining_bomb_count()    
        self._draw_timer()

    def _draw_remaining_bomb_count(self):
        """
        This function draws the remaining bomb count in the top left corner of the board
        """
        pygame.draw.rect(self.screen, colours.BLACK, self.bomb_count_rect, border_radius=10) 

        font = pygame.font.Font("assets/fonts/digital.ttf", 50)
        bomb_count_text = font.render(str(self.bombs), True, colours.RED)
        text_x = self.bomb_count_rect.centerx - bomb_count_text.get_width()  // 2
        text_y = self.bomb_count_rect.centery - bomb_count_text.get_height() // 2
        self.screen.blit(bomb_count_text, (text_x, text_y))

    def _draw_timer(self):
        """
        his function draws the current time elapsed since the initialisation of the game
        When the game is finished the timer stops
        The timer never exceds 999
        """
        elapsed_time = time.time() - game.start_time
        if not game.is_finished:
            self.timer_value = int(elapsed_time)
        
        if elapsed_time > 999:
            self.timer_value = 999

        pygame.draw.rect(self.screen, colours.BLACK, self.timer_rect, border_radius=10) 
        font = pygame.font.Font("assets/fonts/digital.ttf", 50)
        timer_text = font.render(f"  {self.timer_value}  ", True, colours.RED)
        text_x = self.timer_rect.centerx - timer_text.get_width()  // 2
        text_y = self.timer_rect.centery - timer_text.get_height() // 2
        self.screen.blit(timer_text, (text_x, text_y))




    def handle_event(self, event):
        """
        This function simply handles the events for the board and the reset button, i.e the only interactable components.
        """
        for row in self.board:
            for tile in row:
                tile.handle_event(event)
        self.reset_button.handle_event(event)


    def get_neighbours(self, position):
        """
        Given any position this function will return the cardinal values, i.e the closest neighbours for that given value
        The 2nd part of the code filters out all out of bound positions.
        """
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
        """
        This function will find all 'zero-valued' tiles on the board that are connected, i.e. in the same group, with the initial position
        A zero-valued tile is a tile that has 0 bombs within its proximity
        """

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
        """
        This function in conjunction with the get_zero_group_neighbours performs what is known as a 'sweep' or 'clear.'
        When a selected tile has 0 bombs in its proximity, by the rules of minesweeper, a sweep must occur.
        This means all other 0 valued tiles and its neighbours must be made visible to the player
        """
        self[position].value = Tile.CLICKED_TILE
                       
        group = self.get_zero_group_neighbours(position)
        for position in group:
            tile = self[position]
            if tile.value == Tile.FLAGGED_TILE:
                self.bombs += 1
            tile.visible = True
            tile.value = Tile.CLICKED_TILE


    def show_bombs(self):
        """
        This function sets the correct bomb values when either the player has:
            - correctly marked it or,
            - not marked it at all
            
        The funciton is used at the end of the game when the gamestate game.is_finished is true.
        It essentially reveals all bombs.
        """
        for row in self.board:
            for tile in row:
                if tile.is_bomb and tile.value == Tile.FLAGGED_TILE:   tile.value = Tile.CORRECTLY_MARKED_BOMB
                elif tile.is_bomb and tile.value != Tile.CLICKED_BOMB: tile.value = Tile.BOMB

    def check_win(self):
        """
        This function simply checks all tiles that are bombs and sees if the value of the tile is flagged or not.
        If all bombs are flagged correctly the user wins.
        """
        correct = 0
        for position in self.bomb_locations:
            if self[position].value == Tile.FLAGGED_TILE:
                correct += 1

        if correct == self.default_bombs:
            self.show_bombs()
            game.won = True
            game.is_finished = True



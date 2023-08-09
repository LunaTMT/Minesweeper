import pygame
import assets.colours as colours
import game

from pygame.locals import *

class Tile:

    """
    It was necessary to instantiate all the following assets as class variables 
    otherwise each tile would have to initialise the following. W
    When set as class variables the initialisation of the board is much more efficient and without delay    
    """
    pygame.mixer.init()
    CLICKED_TILE = pygame.image.load("assets/images/tiles/clicked_tile.png")
    DEFAULT_TILE = pygame.image.load("assets/images/tiles/default_tile.png")
    FLAGGED_TILE = pygame.image.load("assets/images/tiles/flagged_tile.png")
    BOMB = pygame.image.load("assets/images/tiles/bomb.png")
    CORRECTLY_MARKED_BOMB = pygame.image.load("assets/images/tiles/correctly_marked_bomb.png")
    CLICKED_BOMB = pygame.image.load("assets/images/tiles/clicked_bomb.png")
    
    """
    When initialising the first tile image we want to set the sizes of the tiles to the cell size.
    There is no point resizing for every instantiation of Tile. 
    It is impossible to resize here for the cell size is dynamic and can only be passed from board.
    Thus, the size transformation must occur in first tile __init__.
    """
    IMAGES_INIT = False 

    CLICK_SOUND = pygame.mixer.Sound("assets/sounds/tile_click.wav")
    PLACE_FLAG_SOUND = pygame.mixer.Sound("assets/sounds/plant_flag_2.wav")
    REMOVE_FLAG_SOUND = pygame.mixer.Sound("assets/sounds/remove_flag.wav")
    BOMB_SOUND = pygame.mixer.Sound("assets/sounds/bomb.wav")
    SWEEP_SOUND = pygame.mixer.Sound("assets/sounds/sweep.wav")

    NUMBER_COLOUR = {1: colours.BLUE,
                    2: colours.GREEN,
                    3: colours.RED,
                    4: colours.PURPLE,
                    5: colours.BLACK,
                    6: colours.GREY,
                    7: colours.MAROON,
                    8: colours.TURQOUISE}
    
    clicking = False

    def __init__(self, board, screen, row, column,  x, y, cell_size):
        self.board = board
        self.reset_button = board.reset_button
        self.screen = screen
        self.row = row
        self.column = column
        self.position = (self.row, self.column)
        self.x = x
        self.y = y
        self.width, self.height = self.cell_size = cell_size

        self.neighbours = []
        self.bombs_nearby = 0
        self.is_bomb = False
        self.visible = False
        self.hover = False
        self.scroll_wheel_down = False
                
        if not Tile.IMAGES_INIT: #Image init
            Tile.CLICKED_TILE = pygame.transform.scale(Tile.CLICKED_TILE, (self.width, self.height))
            Tile.DEFAULT_TILE = pygame.transform.scale(Tile.DEFAULT_TILE, (self.width, self.height))
            Tile.FLAGGED_TILE = pygame.transform.scale(Tile.FLAGGED_TILE, (self.width, self.height))
            Tile.BOMB = pygame.transform.scale(Tile.BOMB, (self.width, self.height))
            Tile.CORRECTLY_MARKED_BOMB = pygame.transform.scale(Tile.CORRECTLY_MARKED_BOMB, (self.width, self.height))
            Tile.CLICKED_BOMB = pygame.transform.scale(Tile.CLICKED_BOMB, (self.width, self.height))

        self.previous_value = self.value = Tile.DEFAULT_TILE
        self.image = pygame.Surface([self.width, self.height])
        self.rect = self.image.get_rect()
        self.rect.x = x 
        self.rect.y = y


    def draw(self):
        """
        This function simply draws the tile to the screen with its associated image value
        If the tile is visible we will blit the number of bombs within its proximity on top of the tile.
        """

        self.screen.blit(self.value, (self.x, self.y))
        
        if self.visible:
            self._draw_bomb_number()
            


    def handle_event(self, event):
        """
        This funciton handles the events for a tile.
        Given this function is quite large and dense I will write cdescriptions above each main conditional
        """

        #So long as the game has not finished we can interact with a tile
        if event.type == MOUSEBUTTONDOWN and not game.is_finished: 
            
            if self.rect.collidepoint(event.pos):

                #If the user clicks the tile, it is not yet visible or been flagged
                if event.button == 1 and self.value != Tile.FLAGGED_TILE and not self.visible: 
                    self.visible = True
                    Tile.clicking = True
                    self.reset_button.value = self.reset_button.shocked_smiley_image

                    #If the tile is a bomb the game is over and we want to show all bombs and end the current game
                    if self.is_bomb:
                        self.board.show_bombs()
                        self.value = Tile.CLICKED_BOMB
                        Tile.BOMB_SOUND.play()
                        game.lost = True
                        game.is_finished = True

                    #If the current tile has no bombs nearby we want to perform a sweep/clear
                    elif self.bombs_nearby == 0:
                        self.board.sweep(self.position)
                        Tile.SWEEP_SOUND.play()

                    #Otherwise the tile is perfectly fine to be revealed and its associated value can be represent by a clicked_tile
                    else:
                        self.value = Tile.CLICKED_TILE
                        Tile.CLICK_SOUND.play()

                #If the user right clicks and the tile is not yet visible
                elif event.button == 3 and not self.visible: 
                    
                    #If the tile is already flagged we want to remove the flag and set the tile to its default value
                    if self.value == Tile.FLAGGED_TILE:
                        self.value = Tile.DEFAULT_TILE
                        self.board.bombs += 1
                        Tile.REMOVE_FLAG_SOUND.play()

                    #If the tile is not flagged and we still have flags left to place then place a flag down on this tile.
                    elif self.board.bombs > 0:
                        self.value = Tile.FLAGGED_TILE
                        self.board.bombs -= 1
                        self.board.check_win()
                        Tile.PLACE_FLAG_SOUND.play()
                

                elif event.button == 2 and self.bombs_nearby:  # Scroll click
                    self.scroll_wheel_down = True
                    if not self.neighbours:
                        self.neighbours = self.board.get_neighbours(self.position)
                        self.neighbours.append(self.position)
                        

                    for position in self.neighbours:
                        tile = self.board[position] 
                        tile.previous_value = tile.value
                        if tile.value != Tile.FLAGGED_TILE:
                            tile.value = Tile.CLICKED_TILE   
  

        elif event.type == MOUSEBUTTONUP:
            Tile.clicking = False
            

            if event.button == 2 and self.scroll_wheel_down: # Scroll release
                bomb_count = sum(1 for position in self.neighbours if self.board[position].value == Tile.FLAGGED_TILE)

                if self.visible and self.bombs_nearby != 0 and bomb_count == self.bombs_nearby:

                    reveal_count = 0
                    
                    for position in self.neighbours:
                        tile = self.board[position]
                        
                        if tile.is_bomb and tile.value != Tile.FLAGGED_TILE:
                            tile.value = Tile.CLICKED_BOMB
                            Tile.BOMB_SOUND.play()
                            game.lost = True
                            game.is_finished = True
                        elif tile.value == Tile.FLAGGED_TILE:
                            pass
                        elif not tile.visible:
                            reveal_count += 1
                            tile.visible = True
                           # self.value = Tile.CLICKED_TILE
                    
                    
                    if reveal_count > 0:
                        Tile.CLICK_SOUND.play()
                    
                    if game.lost:
                        self.board.show_bombs() 

                else:
                    for position in self.neighbours:
                        tile = self.board[position]
                        if tile.visible or tile.value == Tile.FLAGGED_TILE:
                            tile.value = tile.previous_value
                        else:
                            tile.value = Tile.DEFAULT_TILE
                    
                        
                self.scroll_wheel_down = False
   



    def _draw_bomb_number(self):
        """
        This function blits ontop of the tile the number of bombs in its proximity
        """
        font = pygame.font.Font("assets/fonts/digital.ttf", int(self.width))
        if self.bombs_nearby == 0:
            text_surface = font.render("", True, (0, 0, 0))
        else:
            text_surface = font.render(str(self.bombs_nearby), True, Tile.NUMBER_COLOUR[self.bombs_nearby])

        text_rect = text_surface.get_rect(center = self.rect.center)
        self.screen.blit(text_surface, text_rect)

    def _set_neighbours(self, image):
        for position in self.neighbours:
            tile = self.board[position]
            tile.value = image   
        self.value = image

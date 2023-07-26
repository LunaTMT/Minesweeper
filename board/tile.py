import pygame
from pygame.locals import *
import assets.colours as colours
import game

class Tile:

    pygame.mixer.init()
    CLICKED_TILE = pygame.image.load("assets/images/tiles/clicked_tile.png")
    DEFAULT_TILE = pygame.image.load("assets/images/tiles/default_tile.png")
    FLAGGED_TILE = pygame.image.load("assets/images/tiles/flagged_tile.png")
    BOMB = pygame.image.load("assets/images/tiles/bomb.png")
    CORRECTLY_MARKED_BOMB = pygame.image.load("assets/images/tiles/correctly_marked_bomb.png")
    CLICKED_BOMB = pygame.image.load("assets/images/tiles/clicked_bomb.png")
    
    IMAGES_INIT = False

    CLICK_SOUND = pygame.mixer.Sound("assets/sounds/tile_click_2.wav")
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

    def __init__(self, board, screen, row, column,  x, y, cell_size):
        self.board = board
        self.screen = screen
        self.row = row
        self.column = column
        self.x = x
        self.y = y
        self.width, self.height = self.cell_size = cell_size

        
        if not Tile.IMAGES_INIT:
            Tile.CLICKED_TILE = pygame.transform.scale(Tile.CLICKED_TILE, (self.width, self.height))
            Tile.DEFAULT_TILE = pygame.transform.scale(Tile.DEFAULT_TILE, (self.width, self.height))
            Tile.FLAGGED_TILE = pygame.transform.scale(Tile.FLAGGED_TILE, (self.width, self.height))
            Tile.BOMB = pygame.transform.scale(Tile.BOMB, (self.width, self.height))
            Tile.CORRECTLY_MARKED_BOMB = pygame.transform.scale(Tile.CORRECTLY_MARKED_BOMB, (self.width, self.height))
            Tile.CLICKED_BOMB = pygame.transform.scale(Tile.CLICKED_BOMB, (self.width, self.height))

        self.bombs_nearby = 0
        self.is_bomb = False
        self.visible = False
        self.hover = False

        self.value = Tile.DEFAULT_TILE
        self.image = pygame.Surface([self.width, self.height])
        self.rect = self.image.get_rect()
        self.rect.x = x 
        self.rect.y = y


    def draw(self):
        #if self.is_bomb:
        #    self.value = Tile.BOMB
        self.screen.blit(self.value, (self.x, self.y))
        
        if self.visible:
            self._draw_bomb_number()
            


    def handle_event(self, event):

        if event.type == pygame.MOUSEBUTTONDOWN and not game.is_finished:
    
            if self.rect.collidepoint(event.pos):
                if event.button == 1 and self.value != Tile.FLAGGED_TILE:  # Check if it's a left-click
                    self.visible = True

                    if self.is_bomb:
                        self.value = Tile.CLICKED_BOMB
                        Tile.BOMB_SOUND.play()
                        game.is_finished = True

                    elif self.bombs_nearby == 0:
                        self.board.sweep((self.row, self.column))
                        Tile.SWEEP_SOUND.play()

                    else:
                        self.value = Tile.CLICKED_TILE
                        Tile.CLICK_SOUND.play()

                elif event.button == 3 and not self.visible:  # Check if it's a right-click
                    if self.value == Tile.FLAGGED_TILE:
                        self.value = Tile.DEFAULT_TILE
                        Tile.REMOVE_FLAG_SOUND.play()
                    else:
                        self.value = Tile.FLAGGED_TILE
                        Tile.PLACE_FLAG_SOUND.play()
   

    def _draw_bomb_number(self):
        font = pygame.font.Font("assets/fonts/digital.ttf", int(self.width))
        if self.bombs_nearby == 0:
            text_surface = font.render("", True, (0, 0, 0))
        else:
            text_surface = font.render(str(self.bombs_nearby), True, Tile.NUMBER_COLOUR[self.bombs_nearby])

        text_rect = text_surface.get_rect(center = self.rect.center)
        self.screen.blit(text_surface, text_rect)


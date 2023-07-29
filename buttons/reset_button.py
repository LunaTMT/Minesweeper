import pygame
import game
import time

from board.tile import Tile
from .button import Button
class ResetButton(Button):

    def __init__(self, board, screen, x=0, y=0, width=0, height=0, text=None, font=None):
        super().__init__(screen, x, y, width, height, text, font)
        self.board = board

        self.clicked_smiley_image = pygame.image.load("assets/images/buttons/clicked_smiley_button.png")
        self.dead_smiley_image = pygame.image.load("assets/images/buttons/dead_smiley_button.png")
        self.shocked_smiley_image = pygame.image.load("assets/images/buttons/shocked_smiley_button.png")
        self.smiley_image = pygame.image.load("assets/images/buttons/smiley_button.png")
        self.cool_smiley_image = pygame.image.load("assets/images/buttons/cool_smiley_button.png")

        self.clicked_smiley_button = pygame.transform.scale(self.clicked_smiley_image, (50, 50))
        self.dead_smiley_image = pygame.transform.scale(self.dead_smiley_image, (50, 50))
        self.shocked_smiley_image = pygame.transform.scale(self.shocked_smiley_image, (50, 50))
        self.smiley_image = pygame.transform.scale(self.smiley_image, (50, 50))
        self.cool_smiley_image = pygame.transform.scale(self.cool_smiley_image, (50, 50))

        self.select_sound = pygame.mixer.Sound("assets/sounds/tile_click.wav")
        self.image = self.smiley_image

    def draw(self) -> None:
        """
        This function draws the reset button object depending upon its state
        If the user lost we want to show a dead face
        If they won, a cool smiley
        """
        if game.lost:
            self.image = self.dead_smiley_image
        elif game.won:
            self.image = self.cool_smiley_image
        
        if Tile.clicking:
            self.image = self.shocked_smiley_image

        self.screen.blit(self.image, self.rect)
    
    def handle_event(self, event) -> None:
        """
        This function handles the events that pertain to the reset button.
        If the user clicks on the button we reset all necessary states and the board for a new game to be played
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                
                self.board.bombs = self.board.default_bombs
                self.board.generate()
                self.board.set_bomb_number_for_each_tile()
                game.start_time = time.time()
                game.won = game.lost = game.is_finished = False
                
                self.image = self.clicked_smiley_button
                self.select_sound.play()
        else:    
            self.image = self.smiley_image #Default image
        
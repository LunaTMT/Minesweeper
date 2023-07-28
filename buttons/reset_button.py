from .button import Button
import pygame
import game
import time

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

        self.select_sound = pygame.mixer.Sound("assets/sounds/tile_click_2.wav")
        self.image = self.smiley_image

    def draw(self) -> None:

        if game.lost:
            self.image = self.dead_smiley_image
        elif game.won:
            self.image = self.cool_smiley_image

        self.screen.blit(self.image, self.rect)
    
    def handle_event(self, event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                
                self.board.reset_mines()
                self.board.generate()
                game.start_time = time.time()
                game.won = game.lost = game.is_finished = False
                

                self.image = self.clicked_smiley_button
                self.select_sound.play()
                return self.text
        else:    
            self.image = self.smiley_image
        
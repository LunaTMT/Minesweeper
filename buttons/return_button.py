import pygame
import game

from buttons.button import Button


class ReturnButton(Button):
    
    def __init__(self, interface, x=0, y=0, width=50, height=50, text=None, font=None):
        super().__init__(interface, x, y, width, height, text, font)
    
        self.interface              = interface
        self.init_menu_buttons      = interface.init_menu_buttons
        self.screen                 = interface.screen

        self.return_image = pygame.image.load("assets/images/buttons/return_button.png")
        self.default_image = self.return_image = pygame.transform.scale(self.return_image, (50, 50))
    
        self.select_sound = pygame.mixer.Sound("assets/sounds/tile_click.wav")

    def draw(self):
        """
        This function simply draws the return button increased in size a tiny bit if the user hovers over the rect
        Or else just draws the default button
        """
        if self.hover:
            self.image = pygame.transform.scale(self.image, (55, 55)) 
    
        else:
            self.image = self.default_image   

        self.screen.blit(self.image, self.rect)

    def handle_event(self, event) -> None:
        """
        This function handles all events that pertain to the return button object
        
        If the user clicks the button, all necessary gamestate changes are made to return back to the menu and stop playing the game
        """
        if event.type == pygame.MOUSEMOTION:
            self.hover = True if self.rect.collidepoint(event.pos) else False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                game.won = game.lost = game.is_finished = False
                self.interface.play_game = False
                self.interface.show_menu = True
                self.interface.handle_menu_buttons = True
                self.init_menu_buttons()
                self.select_sound.play()

                

import pygame
import assets.colours as colours

import game

class Button:

   

    def __init__(self, screen, x=0, y=0, width=0, height=0, text=None, font=None):
        self.screen = screen

        #default rectangle
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.surface = pygame.Surface((width, height), pygame.SRCALPHA)

        #Default appearance
        self.text = text
        self.font = font
        self.rect_colour = colours.WHITE
        self.text_colour = colours.WHITE

        self.hover = False
        self.clicked = False
        
        self.select_sound = pygame.mixer.Sound("assets/sounds/menu_button.wav")

   
    def draw(self) -> None:
        """
        Draws the button rectangle on screen
        """
        pygame.draw.rect(self.surface, self.rect_colour, self.rect, border_radius = 20)
        self.screen.blit(self.surface, (self.rect.x, self.rect.y))

        if text:        
            text = self.font.render(self.text, True, self.text_colour)
            text_rect = text.get_rect(center = self.rect.center)
            self.screen.blit(text, text_rect)

    def handle_event(self, event) -> None:
        """
        handles the events for all button objects
        """
        if event.type == pygame.MOUSEMOTION:
            self.hover = True if self.rect.collidepoint(event.pos) else False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.clicked = True
                self.select_sound.play()
                return self.text
           
                
    def center(self) -> None:
        """
        This function centers the button, updates its coordinates and calls the method update the rectangle but recreating it
        """
        self.rect.x = (game.SCREEN_WIDTH - self.width) // 2 
        self.rect.y = (game.SCREEN_HEIGHT - self.height) // 2
    
    def center_x(self) -> None:
        self.rect.x = (game.SCREEN_WIDTH - self.width) // 2 
    
    def center_y(self) -> None:
        self.rect.y = (game.SCREEN_HEIGHT - self.height) // 2

    def tranpose(self, x_multiplier = None, y_multiplier = None):
        self.rect.x *= x_multiplier
        self.rect.y *= y_multiplier

        

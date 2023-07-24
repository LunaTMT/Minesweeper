import pygame
import assets.colours as colours

import game

class Button:

    def __init__(self, screen, x, y, width, height, text, font):
        self.screen = screen

        #default rectangle
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        #Default appearance
        self.text = text
        self.font = font
        self.rect_colour = colours.WHITE
        self.text_colour = colours.WHITE

        self.hover = False
        #self.function = function
        

   
    def draw(self) -> None:
        """
        Draws the button rectangle on screen
        """
        pygame.draw.rect(self.screen, self.rect_colour, self.rect, border_radius = 20)
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
                return self.text
                #self.function()
           
                
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

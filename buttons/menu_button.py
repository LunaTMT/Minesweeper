import pygame
from .button import Button
import assets.colours as colours

class MenuButton(Button):
    
    def __init__(self, 
                 screen, 
                 x, y, 
                 width, 
                 height, 
                 text, 
                 font_size,
                 text_colour=colours.WHITE, 
                 rect_colour=colours.WHITE):
        
        super().__init__(screen, x, y, width, height, text, font_size)
        self.font = pygame.font.SysFont("assets/fonts/Game_title.otf", 30)
        self.text_colour = text_colour
        self.default_rect_colour = self.rect_colour = rect_colour

    def __str__(self):
        return str(self.hover)

    def draw(self):
        if self.hover:
            self.rect_colour = colours.GREY_60
        else:
            self.rect_colour = self.default_rect_colour

        pygame.draw.rect(self.screen, self.rect_colour, self.rect, border_radius = 20)
        text = self.font.render(self.text, True, self.text_colour)
        text_rect = text.get_rect(center=self.rect.center)
        self.screen.blit(text, text_rect)
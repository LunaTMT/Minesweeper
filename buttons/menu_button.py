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
        self.font = pygame.font.Font("assets/fonts/menu_buttons.ttf", 30)
        self.default_text_colour = self.text_colour = text_colour
        self.default_rect_colour = self.rect_colour = rect_colour

    def __str__(self):
        return str(self.hover)

    def draw(self):
        if self.hover:
            self.rect_colour = colours.GREY_60
            self.text_colour = colours.WHITE
        
        else:
            self.rect_colour = self.default_rect_colour
            self.text_colour = self.default_text_colour

        self._draw_base_rectangle()

        if self.hover:
            self._draw_flag()

        self.screen.blit(self.surface, (self.rect.x , self.rect.y))
        

    def _draw_base_rectangle(self):

        rounded_rect_rect = pygame.Rect(0, 0, self.width, self.height)
        pygame.draw.rect(self.surface, self.rect_colour, rounded_rect_rect, border_radius=20)


        text = self.font.render(self.text, True, self.text_colour)
        text_x = (self.width  - text.get_width()) // 2
        text_y = (self.height - text.get_height()) // 2
        self.surface.blit(text, (text_x, text_y))
        
       

    def _draw_flag(self):
        # Load the image
        flag = pygame.image.load("assets/images/flag.png")
        flag = pygame.transform.scale(flag, (50, 50))

        image_x = ((self.width - flag.get_width()) // 2 ) + 90
        image_y = (self.height - flag.get_height()) // 2 

        self.surface.blit(flag, (image_x, image_y))